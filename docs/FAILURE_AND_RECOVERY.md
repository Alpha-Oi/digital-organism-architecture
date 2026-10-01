# Failure, Recovery and Runaway Growth

**Версия:** DOA v1.0 (`DOA-FS-1.0`). Нормативный документ.

Цепочка для любого критического отказа: `Damage → Detection → Isolation → Repair → Validation → Recovery`; для каждого класса ниже MUST существовать `Detection → Containment → Recovery → Verification`. Идентификаторы `C-…`, `H-…`, `I-…` и т. д. ссылаются на `BIOLOGY_TO_IT_MAPPING.md`.

## 1. Таксономия восстановления

Regeneration ≠ restart. Восстановление MUST выбирать наименее разрушительный режим, чьё precondition выполнено, и повышать режим только при провале verification. Режимы объявляются органом в `organ.recovery.modes`.

| Режим | Что делает | Identity | Lineage | Provenance | Требуемое состояние | Security guarantees | Precondition | Verification |
|---|---|---|---|---|---|---|---|---|
| `RESTART` | перезапуск того же артефакта без смены состояния | сохраняется | не меняется | сохраняется | сохраняется (in-memory теряется) | не ослабляются; grants перевыдаются | артефакт и состояние не повреждены | readiness + semantic health |
| `RESTORE` | возврат состояния из checkpoint/backup | сохраняется | не меняется | цепочка состояния продолжается | возвращается к checkpoint | tombstone/epoch проверяются (E-04) | доверенный backup вне failure domain | state-chain check, RPO |
| `REPAIR` | исправление повреждённой части по trusted source | сохраняется | не меняется | repair записан | сохраняется | repair source независим (C-05) | повреждение локализовано, arrest выполнен | attestation + functional check |
| `REPLACE` | новый экземпляр вместо старого, тот же genome/lineage | сохраняется (admission как SELF) | новая клетка, тот же родитель | новый экземпляр атрибутирован | переносится только проверенное | новые credentials, старые отозваны | замена доступна, старая изолирована | attestation, traffic canary |
| `REGENERATE` | воссоздание утраченного компонента из seed | сохраняется | продолжается от seed | seed attested | восстанавливается из verified memory | seed подписан, не использовался в трафике (T-05) | seed доступен, потеря подтверждена | attestation до трафика (I-14) |
| `REBUILD` | пересборка из genome и источников | сохраняется или `rotated` | новая версия в lineage | новая provenance | state restore по политике | build hermetic, SLSA-class (C-08) | сборка воспроизводима | provenance + smoke evaluation |
| `RECONFIGURE` | изменение overlay/параметров без смены кода | сохраняется | не меняется | overlay подписан | сохраняется | overlay не повышает authority (C-04) | допустимо в границах genome | effective-policy diff |
| `ROLLBACK` | возврат к предыдущей проверенной версии artifact/policy/model | сохраняется | помечается откат | версия и причина записаны | совместимость state проверена | откат не снижает security уровень ниже floor | предыдущая версия подписана и не отозвана | регрессионный health + drift check |

Общие правила:

- Восстановление MUST NOT копировать повреждённое observed state или credentials упавшего экземпляра; источник — trusted desired state (genome, signed artifacts, verified backups).
- Каждое восстановление сохраняет identity, lineage и provenance либо явно записывает `new-identity` (см. `BOUNDARY_AND_IDENTITY.md`).
- Критическое восстановление организма (`REPAIRING→PROVISIONING`) требует human authority и увеличения epoch (E-06).
- Бесконечные retry запрещены: исчерпание retry budget повышает режим или переводит компонент в quarantine (C-11).
- Режимы MUST быть протестированы (restore/rollback drill); непроверенный режим не может быть объявлен в `recovery.modes` как доказанный.

Эскалация по умолчанию: `RESTART → RECONFIGURE → REPAIR → REPLACE → REGENERATE → REBUILD`; `RESTORE` и `ROLLBACK` — боковые режимы для повреждения состояния и неудачных изменений соответственно.

## 2. Реестр классов отказа

Машиночитаемая форма реестра — `specifications/failure-classes.yaml`; таблица ниже и этот файл MUST совпадать (проверяет `scripts/validate_repository.py`). Claim может ссылаться на класс по id (`F-01`…) в необязательном поле `failure_classes`.

Каждая реализация MUST отметить применимые классы и показать для них detection, containment, recovery и verification (`REQ-CORE-23`). Столбец Recovery использует режимы из раздела 1.

| ID | Класс | Detection | Containment | Recovery | Verification | Механизмы |
|---|---|---|---|---|---|---|
| F-01 | Component failure (crash клетки) | failure detector, lease expiry, `FAILED` | fencing, revoke grants, discovery removal | `REPLACE` / `REPAIR` | readiness + semantic health, нет orphan grants | C-28, C-24 |
| F-02 | Partial failure (деградировавший орган) | health evidence: correctness/freshness, SLO burn | graceful degradation, failover на реплику | `REPAIR` / `REPLACE` | возврат SLO в target range stable_for | H-05, N-03 |
| F-03 | Network partition / split-brain | epoch mismatch, quorum loss, divergence detector | fencing по epoch, остановка минорити-стороны | reconcile после reconnect, `RESTORE` минорити | единый epoch, отсутствие конфликтующих side effects | H-04, N-21, N-11 |
| F-04 | Stale state / stale memory | freshness, validity interval, supersession age | read-only для устаревшего, пометка `UNKNOWN` | refresh из источника, reconsolidation | recomputed confidence, freshness в норме | N-14, N-17, N-01 |
| F-05 | Corrupted state / memory | digest mismatch, state-chain break | arrest компонента, quarantine записей | `RESTORE` из независимого backup / `REPAIR` | digest match, state-chain проверена | C-05, E-04, M-04 |
| F-06 | Poisoning (data, model, memory, tool output) | provenance gate, anomaly, eval regression | quarantine источника и затронутых записей | purge + `RESTORE`/`ROLLBACK` | повторная проверка на poisoning test set | C-22, N-16, I-02, E-14 |
| F-07 | Model failure (outage, hallucination, degradation) | semantic health, groundedness check, provider status | failover на другую модель, degraded mode | `REPLACE` модели / `ROLLBACK` | eval sample passes | N-05, E-11 |
| F-08 | Model / behavioral drift | drift score vs baseline | заморозка адаптации, canary stop | `ROLLBACK` / retrain через change protocol | drift ниже порога на governed eval set | E-11, N-20 |
| F-09 | Incorrect adaptation | delta vs baseline, human override rate | остановка canary | `ROLLBACK` | baseline restored | N-20, E-09 |
| F-10 | Unsafe evolution (genome change) | invariant/safety check в SIMULATED | запрет promote, отзыв варианта | `ROLLBACK` genome version | lineage и подпись предыдущей версии | E-08, E-02 |
| F-11 | Reward hacking | multi-signal invariant, audit sampling, proxy-vs-outcome divergence | safety gates как hard constraints, остановка promotion | пересмотр fitness, `ROLLBACK` | safety violations = 0 на hard gates | E-09, H-01 |
| F-12 | Tool failure | tool health, error/timeout rate, circuit breaker | circuit breaker, egress seal | alternative tool, `REPLACE`, degrade | tool probe passes | E-12, C-23 |
| F-13 | Dependency failure | dependency status в HealthEvidence, SLO | failover, bounded retry, degrade | `RECONFIGURE` / failover | dependency PASS stable_for | C-24, H-05 |
| F-14 | Cascading failure | correlated failures, retry storm, saturation | bulkheads, load shedding, emergency circulation | поэтапное восстановление по приоритету | рост нагрузки не вызывает вторичных отказов | C-24, M-03, H-02, C-11 |
| F-15 | Resource exhaustion / starvation | saturation, budget burn, queue age | hard quotas, preemption, spawn gate (M-14) | scale/shed, `RECONFIGURE` | watermarks в норме, fair share | C-16, M-09, E-15 |
| F-16 | Deadlock / livelock | no-progress watchdog, wait-for graph | timeout, cancel, lock lease expiry | `RESTART` / `REPLACE` участников | прогресс возобновлён | N-03, C-28 |
| F-17 | Synchronization failure (clock skew, ordering) | skew metric, epoch/ordering anomalies | отклонение событий вне окна, fencing | resync, `RECONFIGURE` | skew в допуске | N-21, N-19 |
| F-18 | Runaway process / runaway growth | spawn rate, generation depth, orphan count, cost burn | freeze spawn, isolate, внешний kill | `TERMINATING` расширившихся, `RESTORE` quotas | cell_count ≤ `max_cells`, нет orphans | I-17, C-25, H-02 |
| F-19 | Security compromise | innate/adaptive detection, attestation failure | quarantine, revoke, seal | incident machine → `REGENERATE`/`REBUILD` | clean attestation, новые credentials | I-04, I-12, C-27 |
| F-20 | Identity spoofing | identity verification failure, attestation mismatch | deny, step-up auth, revoke | rotate credentials, `REPLACE` | negative spoofing test | I-03, E-03 |
| F-21 | Privilege escalation | grant-vs-parent diff, unexpected capability use | revoke, isolate, freeze delegation | `REPLACE` клетки, ревизия grants | grants ⊆ declared, attenuation соблюдена | I-17, N-11, C-04 |
| F-22 | Adversarial manipulation (prompt injection, sensor spoofing) | input anomaly, cross-sensor disagreement | BBB brokering, `UNCERTAIN` state | `RESTORE` memory, recalibration | injection test set passes | I-02, R-01, C-22 |
| F-23 | Loss of provenance | provenance_missing, lineage chain gap | отклонение объектов без provenance | `REBUILD` с attestation / re-ingest | chain полна | E-01, E-02 |
| F-24 | Catastrophic loss (организм) | потеря control plane / trust root / region | остановка внешних side effects | catastrophic recovery (`REPAIRING→PROVISIONING`) | epoch+1, identity continuity decision, drill report | E-06, T-05, E-04 |
| F-25 | Deceptive or silent health | absence of signal, independent telemetry mismatch | трактовать как `UNKNOWN`, независимый sensor | restore observability, `REPLACE` sensor | independent sensor agrees | N-01, I-05 |

## 3. Runaway growth и онкологические anti-patterns

Онкологическая аналогия — семейство anti-patterns: (1) неконтролируемый spawn агентов и tools; (2) рекурсивное делегирование; (3) privilege amplification; (4) resource exhaustion/capture; (5) self-replication; (6) orphan processes; (7) неконтролируемый рост памяти; (8) обход apoptosis; (9) deceptive health reporting.

| Anti-pattern | Предотвращение | Обнаружение | Ограничение | Genome-поле / schema | Evidence |
|---|---|---|---|---|---|
| Неконтролируемый spawn агентов/tools | admission control, `max_cells`, `spawn_rate_limit_per_minute` | `spawn_rate`, `cell_count` | freeze spawn, предел реплик | `growth_control` | admission-rejection log (REQ-CORE-17) |
| Рекурсивное делегирование | `max_delegation_depth`, `max_spawn_depth` | `delegation_depth`, `generation_depth` | отзыв дочерних grants | `growth_control`, `capability-grant.delegation`, `cell.lineage` | depth-limit test |
| Privilege amplification | attenuation: grant ⊆ parent, issuer ≠ enforcer | grant-vs-parent diff | revoke и isolate | `growth_control.grant_issuer_separate_from_enforcer` | escalation test |
| Resource exhaustion | hard quotas, budgets, fair share, scarcity gate (M-14) | `budget_used_ratio`, saturation | preemption, shed | `resources`, `cell.resources` | exhaustion drill |
| Self-replication | `ecology.reproduction` ∈ {forbidden, plan-gated}, запрет credential cloning | неучтённые экземпляры через inventory | внешний kill, quarantine | `ecology`, `lineage-manifest.credential_cloning=false` | reproduction-forbidden test |
| Orphan processes | lease на каждую клетку, `orphan_lease_ttl` | orphan_count (клетки без родителя/lease) | fencing и termination | `growth_control.orphan_lease_ttl`, `cell.lifecycle.lease_expires_at` | orphan-lease report |
| Unmanaged memory growth | retention quotas, decay, forgetting (N-17) | memory growth rate, stale ratio | purge, quota enforcement | `memory`, `memory-record.retention` | retention report |
| Apoptosis resistance | lease expiry, внешний kill authority | `live_grants_after_term` | revocation без кооперации | `cell.termination` | apoptosis/fencing test |
| Deceptive health reporting | независимая telemetry, attestation | sensor disagreement | `UNKNOWN`-по-умолчанию | `control-loop.sensor.independent_source` | independent-telemetry test |

Обязательные контролы: quotas, admission control, lineage, budget, termination authority вне растущего компонента, containment. Любой компонент, превысивший лимит, MUST быть заморожен (`freeze`) до решения owner; лимиты не подлежат изменению самим компонентом или его потомками.

## 4. Связь с гомеостазом и immunity

- Положительные feedback-пути (spawn, retry, amplification) MUST иметь ceiling, TTL и terminator (H-02).
- Обнаружение отказа запускает incident machine для security-классов (F-06, F-19–F-22) и homeostasis loop для эксплуатационных (F-14–F-17); границы между ними фиксируются в `HOMEOSTASIS.md` и `SECURITY_AND_IMMUNITY.md`.
- После каждого критического отказа выполняется review и, при необходимости, change protocol для обновления защит (`LEARNED → DEFENSES_UPDATED`).
