# Genome and Evolution

## 1. Genome

Genome — подписанный declarative desired state (`genome.schema.json`). Он описывает identity и trust root, boundary и внешние зависимости, organs, tissues, capabilities, invariants, topology, resources, homeostasis (`ControlLoopSpec`), security, memory policy, adaptation bounds, `growth_control`, `ecology`, `aging`, `recovery` и `termination`; для Embodied Profile — `embodiment`. Genome не содержит secrets.

Условные требования схемы: Distributed требует `topology`; Embodied требует `embodiment`; Adaptive требует `learning_bounds`, `separation_of_duties`, `evaluation_set_ref`, `rollback_ref`. `adaptation.runtime_self_modification` MUST быть `false`.

Properties:

- versioned and content-addressed;
- schema-valid and signed;
- reproducible or accompanied by provenance;
- reviewable and rollback-capable;
- immutable after activation; новая редакция создаёт новую version.

## 2. Epigenome

Epigenome регулирует expression через scoped overlays: environment profile, organization policy, user permissions, feature flags, adapters, risk mode and temporary suppression. Overlay MUST указывать base genome, precedence, scope, issuer, reason, issued/expiry time and signature.

## 3. Expression pipeline

```text
Genome + Epigenome + Environment + Intent + Resource/Security state
 -> capability resolution
 -> policy resolution
 -> topology/runtime binding
 -> execution transcript
 -> admitted cells and organs
```

Expression result MUST быть воспроизводим из входных versions или явно маркироваться non-reproducible.

## 4. DNA repair analogue

Continuous integrity checks сравнивают observed artifacts/config с signed digests. При расхождении component arrest/isolation выполняется раньше repair. Repair source должен быть независим от corrupted replica; после repair обязательны attestation и functional check.

## 5. Controlled mutation

Mutation — proposal, а не прямое изменение production. Эволюционное изменение (genome) проходит машину `change` с class=evolution:

```text
OBSERVED -> PROPOSED -> SIMULATED -> EVALUATED -> APPROVED -> CANARY -> PROMOTED | ROLLED_BACK
```

Обязательны: provenance предложения, safety checks (инварианты и safety constraints не нарушены), `LineageManifest`, rollback artifact, controlled deployment (canary) и distinct proposer/evaluator/approver. Изменение authority, инвариантов или safety constraints требует human approval. Learning (изменение adaptive parameters) — отдельный класс и не меняет genome (`MEMORY_AND_NERVOUS_SYSTEM.md`, раздел 6).

## 6. Selection

Variant оценивается по task quality, safety constraints, reliability, latency, cost, fairness where applicable и reversibility. Fitness score MUST NOT позволять компенсировать critical safety failure высокой полезностью.

## 7. Reproduction and lineage

Создание нового организма требует отдельной identity, trust root, resource budget and lifecycle. Offspring получает `LineageManifest` (`lineage-manifest.schema.json`) с parent genome/version, inherited artifacts and deliberate differences. Credential cloning запрещён (`credential_cloning: false`). Reproduction разрешена только при `ecology.reproduction = plan-gated`; иначе `forbidden`.

Импорт artifacts, skills или моделей из другого lineage (horizontal transfer) допускается только при `ecology.horizontal_transfer = quarantine-gated` и проходит provenance, compatibility и quarantine gates (E-14); иначе запрещён — это reproductive isolation. Расхождение реплик и lineage без отбора (genetic drift, E-10) обнаруживается сверкой digest с signed genome и устраняется reconcile из trusted source.

## 8. Anti-patterns

- runtime writes canonical genome;
- model chooses and approves its own expanded permissions;
- successful reward overwrites audit or safety constraints;
- production traffic одновременно является uncontrolled training set;
- rollback depends on the same corrupted storage/control path;
- undocumented epigenetic overlay becomes permanent architecture.

## 9. Идентичность и lineage

Identity организма не меняется при замене компонентов: непрерывность обеспечивается `LineageManifest.identity_continuity` (`continuous`, `rotated`, `new-identity`) и подписанными continuity records; подробности — `BOUNDARY_AND_IDENTITY.md`. Terminated сущности получают tombstone; восстановление из состояния до tombstone запрещено.
