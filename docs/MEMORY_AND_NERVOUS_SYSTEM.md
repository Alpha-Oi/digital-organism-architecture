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

Ни одна LLM не должна одновременно быть единственным proposer, policy authority, executor и verifier для high-impact action.

## 2. Memory types

### Working

Request-scoped, size-bounded, isolated, short TTL. После задачи удаляется либо целенаправленно консолидируется.

### Episodic

Хранит наблюдаемые события, actions, outcomes, time, actors и provenance. Corrections добавляются через supersession, а не скрытое переписывание истории.

### Semantic

Хранит facts/entities/relations с source, confidence, validity interval и contradiction handling. Vector similarity не является truth test.

### Procedural

Хранит signed scripts/workflows/skills с test evidence, permissions, dependencies и retirement policy.

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

Forgetting — управляемая функция: TTL, legal/business retention, consent withdrawal, supersession, compaction и cryptographic erasure where applicable. Audit evidence и user data имеют разные retention policies.

## 5. Neuroplasticity

Изменение model weights, adapters, routing, prompts, retrieval, skill selection или reward policy требует baseline, dataset provenance, offline evaluation, safety constraints, approval rule, canary, drift monitor и rollback artifact.

## 6. Adaptive learning protocol

```text
OBSERVE -> CURATE -> TRAIN/OPTIMIZE -> EVALUATE -> RED-TEAM
        -> APPROVE -> CANARY -> MONITOR -> PROMOTE | ROLLBACK
```

Online learning MAY изменять только declared adaptive parameters. Critical policy, authority и audit semantics не являются learnable runtime parameters.

## 7. Required metrics

- retrieval precision/grounding and source coverage;
- stale/contradictory fact rate;
- memory write/read/forget decisions;
- cross-tenant isolation violations;
- skill success/failure by version;
- adaptation delta versus baseline;
- drift, rollback rate and human override.
