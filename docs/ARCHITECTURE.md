# DOA Architecture

## 1. Системный контекст

DOA разделяет четыре границы:

1. **Environment boundary** — внешний мир и его недоверенные сигналы.
2. **Organism boundary** — identity, policy, genome и global homeostasis.
3. **Organ boundary** — SLO и failure domain отдельной функции.
4. **Cell boundary** — минимальная runtime-изоляция и capability set.

Определение принадлежности к организму, классы внешних зависимостей, trust classes и identity continuity — в [BOUNDARY_AND_IDENTITY.md](BOUNDARY_AND_IDENTITY.md).

## 2. Логические planes

| Plane | Ответственность | Не должен единолично |
|---|---|---|
| Genome/Expression | desired state, capabilities, overlays | менять собственную authority |
| Nervous Control | routing, planning, action selection, reflexes | обходить policy enforcement |
| Endocrine | широковещательные bounded mode changes | отправлять бессрочные сигналы |
| Circulation | commands, events, observations, results | считать доставку равной обработке |
| Immune | detect, contain, quarantine, learn | блокировать без evidence/expiry |
| Memory | retain, retrieve, consolidate, forget | принимать untrusted data как fact |
| Metabolic | compute, storage, network, energy, cost | бесконтрольно расширять budget |
| Repair | reconcile, regenerate, restore (режимы — `FAILURE_AND_RECOVERY.md`) | копировать corrupted state |
| Observability | metrics, traces, logs, audit, profiles | подменять product correctness |

## 3. Reference flow

```text
External stimulus
 -> Barrier/Receptor
 -> Identity + schema + policy validation
 -> Sensory normalization + uncertainty
 -> Thalamic routing
 -> Reflex OR cognitive planning
 -> Action selection (policy/risk/resource)
 -> Capability grant
 -> Cell execution
 -> Egress policy
 -> Observable outcome
 -> Memory consolidation + homeostasis feedback
```

## 4. Organ contract

Каждый орган MUST объявить:

```yaml
identity: stable name and version
responsibility: one cohesive outcome
interfaces: versioned input/output schemas
dependencies: required and optional
slo: availability, correctness, latency, freshness
resources: requests, limits, cost budget
security: identities, capabilities, data classes
health: startup, readiness, liveness, semantic checks
failure_policy: degrade, failover, isolate, terminate
recovery: permitted modes (RESTART|RESTORE|REPAIR|REPLACE|REGENERATE|REBUILD|RECONFIGURE|ROLLBACK), source of truth, RTO, RPO, validation
owner: accountable authority
```

## 5. Cell contract

Клетка MUST иметь identity, type, tissue, image/artifact digest, genome reference, capabilities, resource envelope, data scope, lineage (parent, generation, spawn budget), lifecycle, lease, health evidence и termination policy. Критические органы (`critical: true`) MUST объявлять `redundancy`. Process/container/VM/robot safety domain выбирается по требуемой isolation strength.

## 6. Coordination semantics

- Commands имеют один intended handler и explicit outcome.
- Events являются фактами прошлого и не изменяются задним числом.
- Queries не имеют side effects.
- Retries требуют idempotency key либо explicit at-most-once semantics.
- Delivery semantics (`at-most-once`, `at-least-once`, effectively-once within boundary) MUST быть объявлены.
- Ordering гарантируется только в названном scope.
- Deadlines и cancellation распространяются по causation chain.
- Backpressure является протоколом, а не только метрикой.

## 7. Spatial architecture

Topology model включает region, zone, node, process, accelerator, network segment, data residency и physical compartment. Placement policy учитывает latency, data gravity, hazard, jurisdiction и correlated failure. Critical replicas MUST NOT зависеть от одного failure domain.

## 8. Time architecture

Система MUST различать wall clock и monotonic duration, указывать timezone, допуск clock skew, хранить event time и processing time, определять late-event policy. Scheduled biological analogues (sleep, consolidation, rotation) MUST поддерживать missed-run handling и emergency override.

## 9. Реализация не обязана быть микросервисной

Small Profile MAY быть modular monolith с process isolation и durable queue. Distributed Profile MAY использовать service mesh, event streaming и orchestration. Соответствие определяется контрактами и evidence, а не количеством сервисов.

## 10. Архитектурные цепочки и их контракты

Каждая цепочка ниже имеет контракт на каждом звене: звено без контракта является текстовым описанием и MUST NOT учитываться как соответствие. Идентификаторы — строки `BIOLOGY_TO_IT_MAPPING.md`.

| Цепочка | Звенья (механизм → контракт) | Где проверяется |
|---|---|---|
| Genome → Epigenome → Expression → Cells → Tissues → Organs → Organism | genome C-02 `GenomeManifest` → epigenome C-04 `PolicyOverlay` → expression C-03 `ExecutionTranscript` → cell `cell.schema.json` (C-25) → tissue T-03 `TissueProfile` → organ `organ.schema.json` → organism `organism.schema.json` | REQ-CORE-03, 04, 11; схемы + примеры |
| Sensors → Nervous System → Decision / Coordination → Actuation | receptor N-01 `Observation` → thalamus N-04 `RouteDecision` → cortex N-05 `PlanProposal` → decision N-06 `ActionDecision` → motor N-07 `ActuationCommand` → feedback в N-01 | REQ-CORE-12, 13; REQ-EMB-* для физики |
| Identity → Security → Immunity → Quarantine → Recovery | I-03 `IdentityAssertion` → I-01/C-20 `BoundaryPolicy` → I-04/I-06 rules → M-04 `QuarantineCase` → I-13/I-14 `RecoveryPlan` (машина `incident`) | REQ-CORE-01, 14, 20 |
| Energy → Metabolism → Resource Allocation → Homeostasis | M-14 `ResourceAvailabilitySignal` → C-16 `ResourceBudget` → M-12 `ResourceCharge` → H-01 `ControlLoopSpec` | REQ-CORE-07, 18 |
| Memory → Learning → Adaptation → Evolution | N-12…N-16 `MemoryRecord` → learning N-20 (class=learning) → адаптация внутри `learning_bounds` → evolution E-08 (class=evolution, genome change) | REQ-ADPT-01…06; машина `change` |
| Damage → Detection → Isolation → Repair → Validation → Recovery | N-03 `DamageSignal` → C-28/I-12 fencing и seal → ISOLATED → C-05/I-14 repair → attestation → verified recovery | REQ-CORE-16, 20, 23 |
| Birth → Development → Maturity → Aging → Termination | организм/клетка: машины `organism`, `cell`; T-10, I-18, C-30, E-05 | REQ-CORE-11, 15, 21; `LIFECYCLE.md` |

Звено, имеющее и контракт, и state machine, MUST быть подтверждено evidence в conformance claim.
