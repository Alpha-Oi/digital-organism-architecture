# DOA Architecture

## 1. Системный контекст

DOA разделяет четыре границы:

1. **Environment boundary** — внешний мир и его недоверенные сигналы.
2. **Organism boundary** — identity, policy, genome и global homeostasis.
3. **Organ boundary** — SLO и failure domain отдельной функции.
4. **Cell boundary** — минимальная runtime-изоляция и capability set.

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
| Repair | reconcile, regenerate, restore | копировать corrupted state |
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
recovery: source of truth, RTO, RPO, validation
owner: accountable authority
```

## 5. Cell contract

Клетка MUST иметь identity, type, tissue, image/artifact digest, genome reference, capabilities, resource envelope, data scope, lifecycle, lease, health evidence и termination policy. Process/container/VM/robot safety domain выбирается по требуемой isolation strength.

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
