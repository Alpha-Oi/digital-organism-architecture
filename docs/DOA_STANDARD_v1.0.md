# Digital Organism Architecture (DOA) v1.0 — Foundational Standard

**Идентификатор:** `DOA-FS-1.0`

**Версия релиза:** v1.2.0

**Дата фиксации:** 2026-10-01

**Статус:** Canonical / Foundational Standard

Нормативный язык (MUST/SHOULD/MAY), статус документов и глоссарий — в [TERMINOLOGY.md](TERMINOLOGY.md).

## 1. Назначение и границы

DOA задаёт переносимый метапаттерн для AI-систем, которые должны сохранять целевую полезность при изменении контекста, нагрузки, ресурсов, внутренних отказах и внешних угрозах. Главный объект проектирования — весь цифровой организм, а не отдельная модель.

DOA применим к LLM-сервисам, multi-agent systems, автономным software agents, AI OS, distributed AI platforms и робототехнике. Стандарт не требует микросервисов, Kubernetes, конкретной LLM или облака.

Не входят в область стандарта:

- утверждение, что цифровая система биологически жива или обладает сознанием;
- буквальное копирование биологии без инженерного обоснования;
- скрытая автономия, саморепликация или самоизменение без policy gate;
- замена domain safety, отраслевого regulation или threat model.

## 2. Нормативная модель мэппинга

Каждый заявленный биологический механизм MUST иметь запись:

```text
Biological mechanism
  -> digital responsibility
  -> digital component
  -> contract
  -> protocol / state machine
  -> invariant
  -> failure mode
  -> security / safety control
  -> observability
  -> evidence
```

Если хотя бы одно обязательное поле отсутствует, термин считается только метафорой и MUST NOT использоваться как доказательство соответствия DOA.

Полный реестр (канонная матрица) приведён в [BIOLOGY_TO_IT_MAPPING.md](BIOLOGY_TO_IT_MAPPING.md). Колонка `Profile` определяет нормативный статус строки: `Core` и профильные строки — MUST; `Pattern` — SHOULD/MAY; `Conditional` — MUST, если возможность допущена; `Anti-pattern` — обязательный контроль обнаружения и ограничения.

## 3. Базовые сущности

| Сущность | Нормативное цифровое значение |
|---|---|
| Environment | внешние пользователи, сервисы, физический мир и ресурсы вне trust boundary |
| Organism | версионируемая система с identity, boundary, genome, lifecycle и homeostasis |
| Organ | подсистема с отдельным SLO, owner, interface и failure domain |
| Tissue | группа однотипных клеток с общей политикой и функцией |
| Cell | минимальная независимо изолируемая runtime-единица |
| Organelle | внутренняя capability клетки, не обязательно отдельный сервис |
| Genome | подписанный декларативный desired state и набор допустимых capabilities |
| Epigenome | временные policy overlays, которые регулируют expression без изменения genome |
| Phenotype | наблюдаемое runtime-поведение конкретного deployment |
| Signal | адресное или широковещательное сообщение с provenance, TTL и schema |
| Memory | управляемое состояние с retention, provenance, confidence и access policy |
| Immune event | наблюдение о нарушении доверия, целостности или policy; вход в incident |
| Incident | жизненный цикл иммунного ответа (`LIFECYCLE.md`) |
| Lease / Epoch / Tombstone | истекающее право существования, номер членства для fencing, подписанная запись о завершённой сущности |
| Symbiont | допущенный guest (plugin, tool, agent) с quota и revocation |

Границы организма, identity и trust boundaries определены в [BOUNDARY_AND_IDENTITY.md](BOUNDARY_AND_IDENTITY.md).

## 4. Конституционные инварианты

Совместимый организм MUST обеспечивать:

1. **Identity:** каждое действие связано с проверяемым субъектом, компонентом и версией.
2. **Boundary:** ingress и egress проходят policy enforcement; внутреннее расположение не создаёт доверия.
3. **Desired/observed separation:** геном описывает желаемое, telemetry — наблюдаемое; reconciliation связывает их.
4. **Least capability:** клетка получает только нужные права, данные, время и ресурсы.
5. **No unilateral self-modification:** runtime не изменяет канонический genome, policies или собственные полномочия напрямую.
6. **Closed-loop homeostasis:** control action зависит от измеримого отклонения, bounded response и recovery criterion.
7. **Compartmentalization:** отказ клетки не должен автоматически становиться отказом организма.
8. **Provenance:** данные, модели, policies, memories и artifacts имеют источник и integrity evidence.
9. **Reversibility:** адаптация, обучение и rollout имеют validation, canary и rollback/containment path.
10. **Observable lifecycle:** создание, активация, деградация, quarantine и termination оставляют audit evidence.
11. **Human authority:** high-impact side effects имеют явно определённую authority model и approval boundary.
12. **Truthful uncertainty:** отсутствие сигнала не трактуется как здоровье; неизвестное состояние обозначается явно.
13. **Bounded growth:** число клеток, глубина spawn и делегирования, скорость репликации и потребление ресурсов ограничены genome и могут быть прекращены authority вне растущего компонента.
14. **Identity continuity:** identity организма сохраняется при замене компонентов подписанной цепочкой continuity; завершённая или отозванная сущность не может быть воскрешена из устаревшего состояния.

## 5. Иерархия и planes

```text
Environment / ecosystem
        |
Barrier + receptors + identity
        |
Organism control boundary
        +-- Genome / epigenome / expression
        +-- Nervous and endocrine control planes
        +-- Immune and repair planes
        +-- Data circulation and intracellular transport
        +-- Memory and learning
        +-- Metabolism and resource accounting
        +-- Cells -> tissues -> organs
        +-- Observability and audit
```

Planes логически разделяются. Они MAY совместно размещаться физически, но их полномочия, schemas и failure modes MUST быть различимы.

## 6. Общие цифровые контракты

### 6.1 EventEnvelope

```json
{
  "specversion": "1.0",
  "id": "01J...",
  "type": "doa.observation.resource_pressure.v1",
  "source": "doa://organism-a/organ/metabolism",
  "subject": "cell/inference-17",
  "time": "2026-09-29T12:00:00Z",
  "correlation_id": "task-123",
  "causation_id": "event-122",
  "ttl_ms": 30000,
  "classification": "internal",
  "integrity": {"algorithm": "sha256", "digest": "..."},
  "data": {}
}
```

Consumers MUST validate schema, identity, freshness, replay policy, authorization and size before processing.

Схема: `specifications/event.schema.json`. `integrity` с `signature_ref` MUST присутствовать для `confidential` и `restricted`.

### 6.2 CapabilityGrant

```text
subject + capability + resource + constraints + issuer + issued_at + expires_at + nonce + intent + delegation + signature
```

Схема: `capability-grant.schema.json`. Grant MUST be narrow, expiring, revocable and bound to an auditable intent. Делегированный grant MUST быть подмножеством родительского (attenuation), а глубина делегирования MUST NOT превышать `growth_control.max_delegation_depth`.

### 6.3 HormoneSignal (также называемый HomeostaticSignal)

```text
variable + observed + target_range + severity + scope + action_budget + issuer + issued_at + expires_at + reversal + signature
```

Схема: `hormone.schema.json`. Сигнал MUST истекать (`expires_at`) и описывать reversal. Это один и тот же контракт; термин «HomeostaticSignal» использовать как синоним не следует.

### 6.4 MemoryRecord

```text
content_ref + memory_type + provenance + confidence + decay + classification + retention + consent + supersedes
```

Схема: `memory-record.schema.json`. Для `semantic` и `procedural` записей `trust_class` MUST NOT быть `UNKNOWN`; `procedural` требует `approval_ref`.

### 6.5 HealthEvidence

```text
component + startup + readiness + liveness + correctness + freshness + dependencies + observed_at
```

Схема: `health-evidence.schema.json`. `liveness=PASS` MUST NOT imply semantic correctness; `correctness=PASS` MUST NOT быть заявлен при `liveness≠PASS`. Отсутствие данных — `UNKNOWN`.

### 6.6 Остальные контракты

`ControlLoopSpec` (`control-loop.schema.json`), `PolicyOverlay` (`policy-overlay.schema.json`), `LineageManifest` (`lineage-manifest.schema.json`), lifecycle-событие (`lifecycle-transition.schema.json`), `ConformanceClaim` (`conformance-claim.schema.json`), а также `Genome`, `Organ`, `Cell`, `Organism`.

## 7. Жизненный цикл организма

```text
SPECIFIED -> VALIDATED -> PROVISIONING -> DEVELOPING -> READY -> ACTIVE
ACTIVE <-> STRESSED -> DEGRADED -> REPAIRING -> ACTIVE
ACTIVE -> QUIESCENT -> ACTIVE
ACTIVE | DEGRADED -> SENESCENT -> REPAIRING | RETIRING
ACTIVE | DEGRADED | QUIESCENT | SENESCENT -> RETIRING -> TERMINATED
```

Полная машина с guards, authority и timeouts — `specifications/state-machines.yaml` и [LIFECYCLE.md](LIFECYCLE.md). Переходы MUST иметь guard, authority, timeout и emitted event. `QUARANTINED` является orthogonal security state (`organism.security_state`) и может блокировать переходы из любого runtime-состояния.

## 8. Жизненный цикл клетки

```text
DECLARED -> ADMITTED -> PROVISIONED -> STARTING -> READY -> ACTIVE
ACTIVE <-> STRESSED ; ACTIVE | STRESSED -> SUSPECT -> ISOLATED -> REPAIRING -> READY
ACTIVE -> QUIESCENT -> HIBERNATED -> STARTING ; ACTIVE -> SENESCENT -> TERMINATING
ACTIVE | STRESSED | SUSPECT | STARTING -> FAILED (necrosis) -> ISOLATED
ISOLATED | REPAIRING | SENESCENT | READY | ACTIVE -> TERMINATING (apoptosis) -> TERMINATED
```

Apoptosis (`TERMINATING`) MUST быть bounded shutdown protocol из 8 шагов, а не произвольным удалением: stop admission, cancel/finish bounded work, revoke grants, seal egress, preserve permitted forensic evidence, release resources, emit terminal record, verify absence of live grants. Necrosis (`FAILED`) — неконтролируемый отказ: клетка MUST быть fenced (lease expiry, revoke без её кооперации) до любого repair. Подробности — [LIFECYCLE.md](LIFECYCLE.md).

## 9. Развитие, морфогенез и дифференцировка

Организм MUST отличать provisioning от normal operation. Development controller разворачивает genome по стадиям, проверяя prerequisites и invariants. Differentiation создаёт специализированные cell profiles через разрешённые expression overlays; она MUST NOT повышать полномочия без admission decision.

Morphogenesis задаёт topology: placement, connectivity, capacity и failure-domain separation. Пространство в DOA включает region/zone/node/process/robot compartment и data-locality domain.

## 10. Нервная, сенсорная и память-системы

- cortex/reasoning предлагает гипотезы и планы, но не является единственным policy authority;
- thalamus/router фильтрует и маршрутизирует события;
- basal-ganglia/action selection сопоставляет intent с policy, risk и resources;
- spinal/reflex plane выполняет детерминированные low-latency реакции;
- sensory system калибрует, timestamps, validates и оценивает uncertainty;
- memory разделяется на working, episodic, semantic и procedural;
- motor hierarchy превращает решение в ограниченное действие: intent -> plan -> grant -> command -> feedback; исполнитель проверяет grant, deadline и idempotency;
- peripheral (edge) компоненты MAY принимать локальные решения только в пределах `DelegationGrant` с attenuation, ограниченной глубиной и lease; при reconnect решения сверяются;
- salience/attention — часть `RouteDecision` (priority, salience, budget) и MUST NOT повышать authority источника;
- neuroplasticity означает версионируемое изменение routing/weights/skills с offline evaluation, canary и rollback (только learning, см. §14).

## 11. Гомеостаз и временная организация

Каждый control loop MUST определять (`ControlLoopSpec`): variable, sensor с freshness, target range, thresholds, controller, actuator, action limits, hysteresis, escalation, recovery condition и manual override с ограниченной длительностью. Контуры с положительной обратной связью (усиление) MUST иметь ceiling, TTL и внешний terminator. Подробности и обязательные домены — [HOMEOSTASIS.md](HOMEOSTASIS.md). Circadian/temporal policies задают расписание нагрузки, maintenance, consolidation и key rotation, но MUST учитывать timezone, missed tick, clock drift и emergency override.

## 12. Иммунитет, воспаление и толерантность

Innate controls обеспечивают быстрые generic реакции: validation, rate limit, signature, anomaly threshold, sandbox и deny-by-default. Adaptive controls используют подтверждённые indicators и incident learning, но новые правила MUST проходить проверку на false positives.

Inflammation — ограниченное усиление telemetry, isolation и resource mobilization. Оно MUST иметь scope, TTL и resolution criterion, иначе превращается в хроническую деградацию.

Tolerance — явно ограниченная policy для известных self/partner identities. Она не является allowlist без срока и MUST поддерживать revocation. Autoimmune failure — блокирование легитимных функций собственными controls.

Иммунный ответ следует machine `incident`: `OBSERVED -> DETECTED -> IDENTIFIED -> CONTAINED -> QUARANTINED -> NEUTRALIZED -> RECOVERED -> LEARNED -> DEFENSES_UPDATED -> CLOSED` ([LIFECYCLE.md](LIFECYCLE.md), [SECURITY_AND_IMMUNITY.md](SECURITY_AND_IMMUNITY.md)).

## 13. Регенерация, старение и смерть

Repair восстанавливает компонент из trusted desired state, а не клонирует потенциально повреждённое observed state. Regeneration использует clean image, signed genome, verified memory restore и post-repair validation. Режимы восстановления различаются: `RESTART`, `RESTORE`, `REPAIR`, `REPLACE`, `REGENERATE`, `REBUILD`, `RECONFIGURE`, `ROLLBACK` ([FAILURE_AND_RECOVERY.md](FAILURE_AND_RECOVERY.md)); regeneration ≠ restart.

Senescence означает перевод устаревшего или ненадёжного компонента в non-replicating, reduced-privilege state до замены. Retirement должен сохранять audit/provenance по retention policy, а завершённая сущность получает tombstone и MUST NOT быть воскрешена из устаревшего состояния. Неконтролируемое размножение, рекурсивное делегирование, обход apoptosis и захват ресурсов классифицируются как oncological anti-patterns и ограничиваются `growth_control` (инвариант 13).

## 14. Обучение и эволюция

Learning ≠ Evolution. **Learning** меняет только declared adaptive parameters (`adaptation.learning_bounds`) и MUST NOT менять genome, инварианты, authority model или audit semantics. **Evolution** меняет genome и является отдельным классом изменения. Оба проходят machine `change`:

```text
OBSERVED -> PROPOSED -> (SIMULATED) -> EVALUATED -> APPROVED -> CANARY -> PROMOTED | ROLLED_BACK
```

`SIMULATED` обязательна для evolution. Proposer, evaluator и approver MUST быть разными authorities. Каждое изменение имеет rollback artifact; evolution дополнительно требует `LineageManifest` и новую подписанную genome version.

Наследование возможно только через signed versioned artifact. Fitness MUST быть многокритериальным: task value, safety, reliability, cost, latency и reversibility; один reward не является достаточным, а safety constraints действуют как hard gates.

## 15. Резервирование и аварийное кровообращение

Critical organs MUST иметь declared redundancy mode: active-active, active-passive, quorum или graceful degradation. Реплики MUST быть разнесены по независимым failure domains. Emergency circulation приоритизирует identity, policy, safety, coordination, audit и recovery traffic; низкоприоритетная нагрузка сбрасывается контролируемо.

## 16. Робототехнический профиль

Физический actuator path MUST включать независимые safety interlocks, bounded command envelope, watchdog, emergency stop и safe-state definition. Generative model MUST NOT быть единственным компонентом, разрешающим опасное действие. Robotics extension не вводит отдельной модели: он реализует ту же цепочку `Perception -> State -> Decision -> Action -> Feedback` с физическими ограничениями. Подробности — [ROBOTICS_EXTENSION.md](ROBOTICS_EXTENSION.md).

## 17. Conformance

### Core Profile

Обязательны identity, boundary, genome/epigenome separation, cell lifecycle (включая apoptosis и necrosis), homeostasis loop, immune/quarantine path, resource accounting, memory governance, recovery taxonomy, aging/senescence, identity continuity, growth control, observability и bounded termination.

### Distributed Profile

Дополнительно обязательны event contract, partial-failure handling, idempotency, backpressure, topology/failure-domain placement, quorum/failover с epoch fencing, clock assumptions, drift detection и catastrophic recovery.

### Adaptive Profile

Дополнительно обязательны learning provenance, evaluation set governance, canary, rollback, drift detection, разделение learning/evolution и separation of proposer/evaluator/approver.

### Embodied Profile

Дополнительно обязательны real-time budget, calibrated sensors, actuator interlocks, physical safe state, independent watchdog и hazard analysis.

### Conditional capabilities

Reproduction, federation и horizontal transfer либо контролируются соответствующими requirements, либо явно запрещены в genome (`ecology`).

Система MUST публиковать conformance claim с profile, exclusions, evidence и date. Реестр требований — `specifications/requirements.yaml`; правила статусов `UNVERIFIED`/`PARTIAL`/`VERIFIED` и evidence — [CONFORMANCE.md](CONFORMANCE.md). Claim без evidence считается `UNVERIFIED`.

## 18. Минимальный evidence pack

- подписанный genome и применённый epigenome snapshot;
- inventory клеток/органов и trust boundaries;
- schemas для events, cells, organs и organism;
- state-transition logs, валидные по `lifecycle-transition.schema.json`;
- SLO, homeostatic targets и alert-to-action traces;
- fault-injection или controlled failure evidence;
- quarantine/apoptosis/necrosis(fencing) tests;
- restore/rollback tests;
- security threat model и access-policy test;
- learning/change provenance для Adaptive Profile;
- hazard evidence для Embodied Profile.

Подробная привязка evidence к требованиям — [CONFORMANCE.md](CONFORMANCE.md).

## 19. Ограничение канонической терминологии

DOA — метаархитектурный стандарт. Название DOA MUST NOT использоваться так, будто оно обозначает конкретный product runtime, vendor stack или единственную implementation architecture. Реализации SHOULD формулировать связь как «implements DOA profile X» и прикладывать evidence.

## 20. Источники и инженерная основа

Биологические соответствия опираются на базовые принципы compartmentalization, specialization, signaling, homeostasis, repair и evolution; инженерные механизмы — на проверяемые contracts, zero trust, distributed systems, observability и safety engineering. Ссылки собраны в [SOURCES.md](SOURCES.md). Биологический источник объясняет функцию, но не доказывает пригодность конкретной IT-реализации.
