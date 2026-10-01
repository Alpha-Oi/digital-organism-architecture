# Lifecycle, Aging and Termination

**Версия:** DOA v1.0 (`DOA-FS-1.0`). Нормативный документ.

Канонические state machines определены в `specifications/state-machines.yaml`; схемы (`organism.schema.json`, `cell.schema.json`, `lifecycle-transition.schema.json`) и диаграммы (`diagrams/`) MUST совпадать с ним. Это проверяется `scripts/validate_repository.py`.

## 1. Правила переходов

1. Каждый переход MUST иметь guard, authority и timeout (таблицы ниже) и MUST эмитировать событие `doa.lifecycle.<entity>.transitioned.v1` с payload по `lifecycle-transition.schema.json` (guard evidence, authority, время).
2. Переход, отсутствующий в таблице, запрещён. Терминальные состояния не имеют исходящих переходов.
3. Истечение timeout без выполнения guard MUST приводить к эскалации (событие и действие по `failure_policy`), а не к молчаливому ожиданию.
4. Переход в состояние, расширяющее права или трафик (`READY→ACTIVE`, `REPAIRING→ACTIVE`, `QUIESCENT→ACTIVE`), MUST опираться на свежее health evidence с `correctness`, а не только на liveness.

## 2. Цепочка жизни: Birth → Development → Maturity → Aging → Termination

| Фаза | Состояния организма | Контракт |
|---|---|---|
| Birth | `SPECIFIED`, `VALIDATED`, `PROVISIONING` | подписанный genome, trust root, бюджет, identity |
| Development | `DEVELOPING` | development checkpoints (C-26), topology (T-06), стадийная зрелость (T-10) |
| Maturity | `READY`, `ACTIVE`, `STRESSED`, `QUIESCENT` | homeostasis, health evidence, SLO |
| Aging | `DEGRADED`, `REPAIRING`, `SENESCENT` | `AgingIndex` (I-18), senescence policy (C-30), replacement plan |
| Termination | `RETIRING`, `TERMINATED` | termination plan (E-05), tombstone, sealed audit |

## 3. Организм

| From | To | Guard | Authority | Timeout |
|---|---|---|---|---|
| `SPECIFIED` | `VALIDATED` | genome schema-valid and signature verified | genome owner via change service | 1h |
| `VALIDATED` | `PROVISIONING` | trust root and budget available | provisioning controller | 1h |
| `PROVISIONING` | `DEVELOPING` | substrate and identity issued | development controller | 30m |
| `DEVELOPING` | `READY` | all developmental checkpoints passed | development controller | 1h |
| `READY` | `ACTIVE` | readiness and semantic health evidence present | organism controller | 10m |
| `ACTIVE` | `STRESSED` | homeostatic variable outside target range | homeostasis controller | 1m |
| `STRESSED` | `ACTIVE` | recovery criterion met for stable_for window | homeostasis controller | 1h |
| `STRESSED` | `DEGRADED` | stress exceeds TTL or safety ceiling reached | homeostasis controller | 15m |
| `ACTIVE` | `DEGRADED` | critical organ lost or in degraded mode | homeostasis controller | 5m |
| `DEGRADED` | `REPAIRING` | repair plan authorized from trusted source | repair controller | 15m |
| `REPAIRING` | `ACTIVE` | post-repair validation passed | repair controller | 4h |
| `REPAIRING` | `DEGRADED` | repair attempt failed within retry budget | repair controller | 4h |
| `REPAIRING` | `PROVISIONING` | catastrophic recovery with restored trust root and continuity record | human authority plus repair controller | 24h |
| `ACTIVE` | `QUIESCENT` | maintenance window or operator request | organism controller | 1h |
| `QUIESCENT` | `ACTIVE` | policy and genome revalidated on wake | organism controller | 10m |
| `ACTIVE` | `SENESCENT` | AgingIndex above senescence threshold | lifecycle controller | 24h |
| `DEGRADED` | `SENESCENT` | AgingIndex above threshold and repair not economical | lifecycle controller | 24h |
| `SENESCENT` | `REPAIRING` | replacement plan approved | lifecycle controller | 24h |
| `SENESCENT` | `RETIRING` | retirement decision recorded | human authority | 7d |
| `ACTIVE` | `RETIRING` | retirement decision recorded | human authority | 7d |
| `DEGRADED` | `RETIRING` | retirement decision recorded | human authority | 7d |
| `QUIESCENT` | `RETIRING` | retirement decision recorded | human authority | 7d |
| `RETIRING` | `TERMINATED` | grants revoked and audit sealed and tombstone issued | lifecycle controller | 7d |

`QUARANTINED` — ортогональное security state (`organism.security_state`), оно MAY блокировать любые переходы и расширение прав из любого runtime-состояния. Соответствие incident machine: `NORMAL` — нет открытых incidents; `SUSPECT` — `DETECTED`/`IDENTIFIED`; `QUARANTINED` — `CONTAINED`/`QUARANTINED`/`NEUTRALIZED`; `RECOVERING` — `RECOVERED`/`LEARNED`/`DEFENSES_UPDATED`.

## 4. Клетка

| From | To | Guard | Authority | Timeout |
|---|---|---|---|---|
| `DECLARED` | `ADMITTED` | admission passed (quota and signature and lineage budget) | admission controller | 1m |
| `DECLARED` | `TERMINATED` | admission denied | admission controller | 1m |
| `ADMITTED` | `PROVISIONED` | resources reserved and grants issued | scheduler | 5m |
| `PROVISIONED` | `STARTING` | artifact digest matches genome | scheduler | 5m |
| `STARTING` | `READY` | startup and readiness checks passed | cell supervisor | 5m |
| `STARTING` | `FAILED` | startup deadline exceeded or crash | cell supervisor | 5m |
| `READY` | `ACTIVE` | lease valid and discovery endpoint published | cell supervisor | 1m |
| `ACTIVE` | `STRESSED` | local stress response triggered | cell supervisor | 1m |
| `STRESSED` | `ACTIVE` | stress resolved within TTL | cell supervisor | 15m |
| `STRESSED` | `SUSPECT` | stress TTL exceeded or integrity doubt | cell supervisor | 15m |
| `ACTIVE` | `SUSPECT` | semantic or integrity or security anomaly | immune system or watchdog | 1m |
| `SUSPECT` | `ACTIVE` | false positive cleared with evidence | immune system | 30m |
| `SUSPECT` | `ISOLATED` | containment decision | immune system | 1m |
| `ISOLATED` | `REPAIRING` | repair source trusted and independent | repair controller | 15m |
| `REPAIRING` | `READY` | attestation and functional check passed | repair controller | 1h |
| `REPAIRING` | `TERMINATING` | repair failed or retry budget exhausted | repair controller | 1h |
| `ISOLATED` | `TERMINATING` | unsafe or unrepairable | immune system | 1m |
| `ACTIVE` | `QUIESCENT` | drain complete | cell supervisor | 5m |
| `QUIESCENT` | `ACTIVE` | lease renewed and policy revalidated | cell supervisor | 5m |
| `QUIESCENT` | `HIBERNATED` | idle beyond hibernation threshold | scheduler | 1h |
| `HIBERNATED` | `STARTING` | wake request authorized | scheduler | 5m |
| `ACTIVE` | `SENESCENT` | cell age or dependency end-of-life reached | lifecycle controller | 1h |
| `SENESCENT` | `TERMINATING` | replacement cell ready | lifecycle controller | 24h |
| `READY` | `TERMINATING` | scale-in or retirement | scheduler | 5m |
| `ACTIVE` | `TERMINATING` | scale-in or retirement or apoptosis trigger | scheduler or immune system | 5m |
| `ACTIVE` | `FAILED` | uncontrolled crash or lease lost | cell supervisor or lease expiry | 1m |
| `STRESSED` | `FAILED` | uncontrolled crash or lease lost | cell supervisor or lease expiry | 1m |
| `SUSPECT` | `FAILED` | uncontrolled crash or lease lost | cell supervisor or lease expiry | 1m |
| `FAILED` | `ISOLATED` | fenced by lease expiry and grants revoked | immune system or lease expiry | 1m |
| `TERMINATING` | `TERMINATED` | apoptosis steps 1-8 completed and terminal record emitted | lifecycle controller | 1h |

### Apoptosis (контролируемое завершение, состояние `TERMINATING`)

Шаги выполняются строго по порядку; каждый шаг фиксируется в audit:

1. Stop admission of new work.
2. Bound or cancel active work.
3. Revoke credentials, tokens and leases.
4. Seal egress.
5. Preserve policy-permitted forensic snapshot.
6. Release resources and remove discovery endpoint.
7. Emit signed terminal record.
8. Verify absence of live grants, endpoints and replicas.

### Necrosis (неконтролируемый отказ, состояние `FAILED`)

Потеря клетки без выполнения apoptosis (crash, OOM, потеря узла, потеря lease). Организм MUST: (1) определить отказ по failure detector или истечению lease; (2) fencing: отозвать grants без кооперации клетки и отклонять её сообщения по fencing token/epoch; (3) пометить возможные частично применённые side effects и сверить по idempotency key; (4) перевести клетку в `ISOLATED`, затем `REPAIRING` либо `TERMINATING`. Клетка в `FAILED` MUST NOT быть discoverable и MUST NOT иметь действующих grants.

## 5. Incident (иммунный ответ)

| From | To | Guard | Authority | Timeout |
|---|---|---|---|---|
| `OBSERVED` | `DETECTED` | innate rule or anomaly threshold fired | immune system | 1m |
| `OBSERVED` | `CLOSED` | observation dismissed with recorded reason | immune system | 1h |
| `DETECTED` | `IDENTIFIED` | evidence normalized and classified | immune system | 15m |
| `DETECTED` | `CLOSED` | false positive recorded against false-positive budget | immune system | 1h |
| `IDENTIFIED` | `CONTAINED` | bounded containment applied with TTL | immune system | 5m |
| `IDENTIFIED` | `CLOSED` | benign or tolerated with ToleranceGrant | immune system plus owner | 1h |
| `CONTAINED` | `QUARANTINED` | subject isolated and evidence preserved | immune system | 15m |
| `QUARANTINED` | `NEUTRALIZED` | threat removed or subject terminated or credentials revoked | immune system | 24h |
| `QUARANTINED` | `CLOSED` | released after review as false positive | owner review | 24h |
| `NEUTRALIZED` | `RECOVERED` | recovery verified from trusted source | repair controller | 24h |
| `RECOVERED` | `LEARNED` | post-incident review recorded | owner | 7d |
| `LEARNED` | `DEFENSES_UPDATED` | new rule validated for precision and blast radius | change protocol | 7d |
| `LEARNED` | `CLOSED` | no defense change warranted | owner | 7d |
| `DEFENSES_UPDATED` | `CLOSED` | rollout verified | owner | 7d |

Один и тот же lifecycle применяется к клетке, данным, artifact и identity. Quarantine MUST прекращать новые high-risk actions, ограничивать network/data access, сохранять разрешённое evidence и поддерживать review ложных срабатываний (false-positive budget, I-16). Подробности по security — `SECURITY_AND_IMMUNITY.md`.

## 6. Change protocol (learning и evolution)

| From | To | Guard | Authority | Timeout |
|---|---|---|---|---|
| `OBSERVED` | `PROPOSED` | proposal within declared adaptive bounds or genome change request | proposer | 7d |
| `PROPOSED` | `SIMULATED` | offline simulation in sandbox | evaluator | 7d |
| `PROPOSED` | `EVALUATED` | learning class only - offline evaluation on governed evaluation set | evaluator | 7d |
| `PROPOSED` | `REJECTED` | outside bounds or provenance missing | evaluator | 7d |
| `SIMULATED` | `EVALUATED` | multi-criteria evaluation with safety constraints dominating | evaluator | 7d |
| `SIMULATED` | `REJECTED` | simulation violated invariant | evaluator | 7d |
| `EVALUATED` | `APPROVED` | approver distinct from proposer and evaluator | approver | 7d |
| `EVALUATED` | `REJECTED` | evaluation below threshold or safety constraint violated | approver | 7d |
| `APPROVED` | `CANARY` | rollback artifact and lineage record exist | release controller | 1d |
| `CANARY` | `PROMOTED` | canary metrics within bounds for observation window | release controller | 7d |
| `CANARY` | `ROLLED_BACK` | canary breach or drift or human override | release controller or any guardian | 1h |

Класс изменения определяет обязательные guards:

| Класс | Что меняется | Обязательно |
|---|---|---|
| `learning` | только declared adaptive parameters (`adaptation.learning_bounds`): weights, adapters, prompts, routing, retrieval, skill selection | evaluation set, canary, rollback artifact, drift monitor; переход `PROPOSED→EVALUATED` разрешён |
| `evolution` | genome: capabilities, organs, topology, invariants, bounds | `SIMULATED` обязательна (переход `PROPOSED→EVALUATED` запрещён), `LineageManifest`, подпись новой genome version, human approval для изменений authority/invariants/safety constraints |

Для обоих классов: proposer, evaluator и approver — разные authorities; рабочая production-нагрузка не является неконтролируемым training set; rollback не зависит от того же повреждённого storage/control path.

## 7. Старение и Senescence

Организм MUST вычислять `AgingIndex` (0..1) по входам, объявленным в `genome.spec.aging.index_inputs` (например: dependency end-of-life, возраст credentials и ключей, error-budget burn, model/behavioral drift, доля неподдерживаемых компонентов). При превышении `senescence_threshold`:

1. компонент переходит в `SENESCENT`: reduced privilege, `spawn_budget = 0`, запрет репликации и новых capabilities;
2. создаётся replacement plan; замена выполняется через admission и attestation как новая клетка той же lineage;
3. после готовности замены старый компонент проходит `TERMINATING`;
4. на уровне организма `SENESCENT` допускает только `REPAIRING` (замена компонентов) или `RETIRING` по решению human authority.

Деградация обнаруживается как `DEGRADED` (потеря функции) или `SENESCENT` (накопленное старение); они различаются: деградацию лечат repair, старение — replacement/retirement.

## 8. Вывод из эксплуатации и безопасное завершение организма

`RETIRING` выполняет: прекращение приёма работы; drain; отзыв всех grants и credentials; закрытие federation/treaties; disposition данных по retention policy и legal hold; sealing audit во внешнем append-only хранилище; выдача tombstone (`termination.tombstone`); верификация отсутствия активных компонентов. Только после этого — `TERMINATED`.

Terminal record (`lifecycle-transition.terminal_record`) MUST фиксировать: grants revoked, endpoints removed, forensic policy, tombstone ref. Audit и provenance сохраняются по retention policy и переживают организм.

## 9. Предотвращение resurrection недействительного состояния

- `TERMINATED` — финальное состояние; из него нет переходов.
- Tombstone содержит `organism_id`/`cell id`, epoch и подпись; хранится вне failure domain организма.
- Restore проверяет tombstone и epoch: backup старше tombstone или с устаревшим epoch отклоняется (E-04).
- Credentials, выданные до tombstone, невалидны; повторное создание — только как `new-identity` по `LineageManifest`.
- Катастрофическое восстановление (`REPAIRING→PROVISIONING`) увеличивает epoch и MUST иметь human authority и continuity record (E-06).

## 10. Embodied safety

| From | To | Guard | Authority | Timeout |
|---|---|---|---|---|
| `INIT` | `CALIBRATING` | hardware self-test passed | safety controller | 1m |
| `CALIBRATING` | `READY` | calibration versions valid and sensors fresh | safety controller | 10m |
| `READY` | `ACTIVE` | task authorized and safety envelope loaded | safety controller | 1m |
| `ACTIVE` | `LIMITED` | uncertainty or degraded sensor or proximity | safety controller | 100ms |
| `LIMITED` | `ACTIVE` | condition cleared for debounce window | safety controller | 1m |
| `ACTIVE` | `SAFE_STOP` | hard limit or watchdog or emergency stop | independent interlock | 50ms |
| `LIMITED` | `SAFE_STOP` | hard limit or watchdog or emergency stop | independent interlock | 50ms |
| `SAFE_STOP` | `LOCKED_OUT` | hazard latched | independent interlock | 1s |
| `LOCKED_OUT` | `INSPECTED` | physical inspection recorded | qualified human | 7d |
| `INSPECTED` | `RESET_AUTHORIZED` | reset authority confirmed | qualified human | 1d |
| `RESET_AUTHORIZED` | `CALIBRATING` | reset executed | safety controller | 1m |

Подробнее — `ROBOTICS_EXTENSION.md`.
