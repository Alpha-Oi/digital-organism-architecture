# Digital Organism Architecture (DOA) v1.0 — Foundational Standard

**Идентификатор:** `DOA-FS-1.0`

**Дата фиксации:** 2026-09-29

**Статус:** Canonical / Foundational Standard

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
  -> system responsibility
  -> digital component
  -> digital contract
  -> state machine or protocol
  -> observability invariant
  -> failure modes
  -> security implications
  -> possible implementation stack
```

Если хотя бы одно обязательное поле отсутствует, термин считается только метафорой и MUST NOT использоваться как доказательство соответствия DOA.

Полный реестр приведён в `BIOLOGY_TO_IT_MAPPING.md`.

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
| Immune event | наблюдение о нарушении доверия, целостности или policy |

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

### 6.2 CapabilityGrant

```text
subject + capability + resource + constraints + issuer + issued_at + expires_at + nonce + signature
```

Grant MUST be narrow, expiring, revocable and bound to an auditable intent.

### 6.3 HomeostaticSignal

```text
variable + observed + target_range + severity + scope + action_budget + ttl + issuer + signature
```

### 6.4 MemoryRecord

```text
content_ref + type + provenance + confidence + classification + retention + consent + supersedes
```

### 6.5 HealthEvidence

```text
component + startup + readiness + liveness + correctness + freshness + dependencies + observed_at
```

`liveness=true` MUST NOT imply semantic correctness.

## 7. Жизненный цикл организма

```text
SPECIFIED
 -> VALIDATED
 -> PROVISIONING
 -> DEVELOPING
 -> READY
 -> ACTIVE
 -> STRESSED
 -> DEGRADED
 -> REPAIRING
 -> QUIESCENT
 -> RETIRING
 -> TERMINATED
```

Переходы MUST иметь guard, authority, timeout и emitted event. `QUARANTINED` является orthogonal security state и может блокировать переходы из любого runtime-состояния.

## 8. Жизненный цикл клетки

```text
DECLARED -> ADMITTED -> PROVISIONED -> STARTING -> READY -> ACTIVE
ACTIVE -> SUSPECT -> ISOLATED -> REPAIRING -> READY
ISOLATED -> SNAPSHOTTED -> CREDENTIALS_REVOKED -> TERMINATED
ACTIVE -> QUIESCENT -> HIBERNATED -> STARTING
```

Apoptosis MUST быть bounded shutdown protocol, а не произвольным удалением: stop admission, cancel/finish bounded work, revoke grants, preserve permitted forensic evidence, release resources, emit terminal record.

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
- neuroplasticity означает версионируемое изменение routing/weights/skills с offline evaluation, canary и rollback.

## 11. Гомеостаз и временная организация

Каждый control loop MUST определять variable, target range, sampling interval, controller, actuator, action limits, hysteresis, recovery condition и manual override. Circadian/temporal policies задают расписание нагрузки, maintenance, consolidation и key rotation, но MUST учитывать timezone, missed tick, clock drift и emergency override.

## 12. Иммунитет, воспаление и толерантность

Innate controls обеспечивают быстрые generic реакции: validation, rate limit, signature, anomaly threshold, sandbox и deny-by-default. Adaptive controls используют подтверждённые indicators и incident learning, но новые правила MUST проходить проверку на false positives.

Inflammation — ограниченное усиление telemetry, isolation и resource mobilization. Оно MUST иметь scope, TTL и resolution criterion, иначе превращается в хроническую деградацию.

Tolerance — явно ограниченная policy для известных self/partner identities. Она не является allowlist без срока и MUST поддерживать revocation. Autoimmune failure — блокирование легитимных функций собственными controls.

## 13. Регенерация, старение и смерть

Repair восстанавливает компонент из trusted desired state, а не клонирует потенциально повреждённое observed state. Regeneration использует clean image, signed genome, verified memory restore и post-repair validation.

Senescence означает перевод устаревшего или ненадёжного компонента в non-replicating, reduced-privilege state до замены. Retirement должен сохранять audit/provenance по retention policy. Неконтролируемое размножение, обход apoptosis и захват ресурсов классифицируются как oncological anti-patterns.

## 14. Обучение и эволюция

Online adaptation MUST быть ограничена параметрами, явно разрешёнными genome/policy. Изменения моделей, prompts, skills, routing или memory policy проходят:

```text
OBSERVE -> PROPOSE -> SIMULATE -> EVALUATE -> APPROVE -> CANARY -> PROMOTE | ROLLBACK
```

Наследование возможно только через signed versioned artifact. Fitness MUST быть многокритериальным: task value, safety, reliability, cost, latency и reversibility; один reward не является достаточным.

## 15. Резервирование и аварийное кровообращение

Critical organs MUST иметь declared redundancy mode: active-active, active-passive, quorum или graceful degradation. Реплики MUST быть разнесены по независимым failure domains. Emergency circulation приоритизирует identity, policy, safety, coordination, audit и recovery traffic; низкоприоритетная нагрузка сбрасывается контролируемо.

## 16. Робототехнический профиль

Физический actuator path MUST включать независимые safety interlocks, bounded command envelope, watchdog, emergency stop и safe-state definition. Generative model MUST NOT быть единственным компонентом, разрешающим опасное действие. Подробности — `ROBOTICS_EXTENSION.md`.

## 17. Conformance

### Core Profile

Обязательны identity, boundary, genome/epigenome separation, cell lifecycle, homeostasis loop, immune/quarantine path, resource accounting, memory governance, observability и bounded termination.

### Distributed Profile

Дополнительно обязательны event contract, partial-failure handling, idempotency, backpressure, topology/failure-domain placement, quorum/failover и clock assumptions.

### Adaptive Profile

Дополнительно обязательны learning provenance, evaluation set governance, canary, rollback, drift detection и separation of proposer/evaluator/approver.

### Embodied Profile

Дополнительно обязательны real-time budget, calibrated sensors, actuator interlocks, physical safe state, independent watchdog и hazard analysis.

Система MUST публиковать conformance claim с profile, exclusions, evidence и date. Claim без evidence считается `UNVERIFIED`.

## 18. Минимальный evidence pack

- подписанный genome и применённый epigenome snapshot;
- inventory клеток/органов и trust boundaries;
- schemas для events, cells, organs и organism;
- state-transition logs;
- SLO, homeostatic targets и alert-to-action traces;
- fault-injection или controlled failure evidence;
- quarantine/apoptosis test;
- restore/rollback test;
- security threat model и access-policy test;
- learning/change provenance для Adaptive Profile;
- hazard evidence для Embodied Profile.

## 19. Ограничение канонической терминологии

DOA — метаархитектурный стандарт. Название DOA MUST NOT использоваться так, будто оно обозначает конкретный product runtime, vendor stack или единственную implementation architecture. Реализации SHOULD формулировать связь как «implements DOA profile X» и прикладывать evidence.

## 20. Источники и инженерная основа

Биологические соответствия опираются на базовые принципы compartmentalization, specialization, signaling, homeostasis, repair и evolution; инженерные механизмы — на проверяемые contracts, zero trust, distributed systems, observability и safety engineering. Ссылки собраны в `SOURCES.md`. Биологический источник объясняет функцию, но не доказывает пригодность конкретной IT-реализации.
