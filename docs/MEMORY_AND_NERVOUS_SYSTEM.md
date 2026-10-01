# Memory and Nervous System

## 1. Разделение ролей

| Биологический аналог | Цифровая роль |
|---|---|
| Cortex | semantic reasoning and plan proposal |
| Thalamus | input filtering and routing |
| Basal ganglia | policy/risk/resource-aware action selection |
| Hippocampus | episodic consolidation and retrieval |
| Cerebellum | validated procedural skills |
| Spinal cord | deterministic reflexes |
| Brainstem | essential maintenance and watchdogs |
| Peripheral nerves | authenticated agent/tool mesh |
| Peripheral ganglia | ограниченная локальная автономия edge-компонентов по `DelegationGrant` (N-11) |
| Motor cortex / motor units | motor hierarchy: ActionDecision → ActuationCommand → исполнитель (N-07) |

Ни одна LLM не должна одновременно быть единственным proposer, policy authority, executor и verifier для high-impact action.

## 2. Memory types

Контракт записи — `MemoryRecord` (`memory-record.schema.json`): тип, `content_ref`, provenance (источник, время, integrity, trust class), confidence, decay, validity, classification, retention, consent, supersession.

### Working

Request-scoped, size-bounded, isolated, short TTL. После задачи удаляется либо целенаправленно консолидируется.

### Episodic

Хранит наблюдаемые события, actions, outcomes, time, actors и provenance. Corrections добавляются через supersession, а не скрытое переписывание истории.

### Semantic

Хранит facts/entities/relations с source, confidence, validity interval и contradiction handling. Vector similarity не является truth test. Запись из `UNKNOWN` источника запрещена.

### Procedural

Хранит signed scripts/workflows/skills с test evidence, permissions, dependencies и retirement policy; запись требует `approval_ref`.

### Long-term memory

Долговременная память — это не отдельный тип, а состояние записей episodic/semantic/procedural после consolidation: запись долговременна, если прошла consolidation protocol (раздел 3), имеет provenance и retention policy и подлежит decay, перепроверке и forgetting (раздел 4). Working memory не становится долговременной без consolidation.

### Confidence и provenance

Confidence — оценка достоверности записи, затухающая по `decay.half_life` до `floor`; при падении ниже порога запись перепроверяется или переводится в `UNKNOWN`/superseded. Provenance (E-01) обязательна: запись без источника, времени и integrity не допускается в trusted memory и decision path.

## 3. Consolidation protocol

```text
candidate observation
 -> classify
 -> redact/minimize
 -> verify provenance
 -> resolve duplication/contradiction
 -> approve by policy
 -> store/index
 -> later revalidate/expire
```

Untrusted content MUST NOT записываться как instruction, policy или identity fact.

## 4. Forgetting and retention

Forgetting — управляемая функция (N-17): TTL, confidence decay, legal/business retention, consent withdrawal, supersession, compaction и cryptographic erasure where applicable. Audit evidence и user data имеют разные retention policies. Erasure MUST быть проверяемым (`erasure_verified_total`); legal/forensic hold приоритетнее автоматического удаления. Устаревшая (stale) память помечается и перепроверяется, а не используется как факт.

## 5. Neuroplasticity

Изменение model weights, adapters, routing, prompts, retrieval, skill selection или reward policy требует baseline, dataset provenance, offline evaluation, safety constraints, approval rule, canary, drift monitor и rollback artifact. Это **learning**: оно допустимо только внутри `adaptation.learning_bounds`.

## 6. Learning ≠ Evolution

| | Learning | Evolution |
|---|---|---|
| Что меняется | declared adaptive parameters (weights, adapters, prompts, routing, skills, memory policy внутри bounds) | genome: capabilities, organs, topology, invariants, bounds |
| Машина | `change`, class=learning | `change`, class=evolution (+ `SIMULATED`) |
| Может менять authority/инварианты/audit | **нет** | только с human approval и новой подписанной genome version |
| Lineage | версия artifact с provenance | `LineageManifest` с parent, deliberate differences |
| Rollback | rollback artifact, canary | откат genome version, lineage помечается |
| Production traffic как training set | только через curated, provenance-checked выборку | запрещён как неконтролируемый источник |
| Кто решает | proposer ≠ evaluator ≠ approver | то же + governance |

Эволюция не допускает произвольной мутации: любой вариант (E-08) проходит validation, safety checks, provenance, rollback, lineage tracking и controlled deployment (canary). Online learning MAY изменять только declared adaptive parameters. Critical policy, authority и audit semantics не являются learnable runtime parameters.

## 6.1 Adaptive learning protocol

```text
OBSERVED -> PROPOSED (CURATE, TRAIN/OPTIMIZE, RED-TEAM внутри шага)
         -> EVALUATED -> APPROVED -> CANARY (MONITOR) -> PROMOTED | ROLLED_BACK
```

Шаги CURATE, TRAIN/OPTIMIZE и RED-TEAM выполняются внутри `PROPOSED`→`EVALUATED` и фиксируются в evidence; состояния определены машиной `change`.

## 7. Required metrics

- retrieval precision/grounding and source coverage;
- stale/contradictory fact rate;
- memory write/read/forget decisions;
- cross-tenant isolation violations;
- skill success/failure by version;
- confidence calibration and decay (stale records);
- adaptation delta versus baseline;
- drift, rollback rate and human override.
