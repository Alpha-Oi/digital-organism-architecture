# Genome and Evolution

## 1. Genome

Genome — подписанный declarative desired state. Он описывает identity, organs, tissues, capabilities, invariants, topology, resources, lifecycle, homeostasis, security and adaptation bounds. Genome не содержит secrets.

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

Mutation — proposal, а не прямое изменение production:

```text
baseline -> variant -> simulation -> evaluation -> safety review
         -> approval -> canary -> promotion | rollback
```

## 6. Selection

Variant оценивается по task quality, safety constraints, reliability, latency, cost, fairness where applicable и reversibility. Fitness score MUST NOT позволять компенсировать critical safety failure высокой полезностью.

## 7. Reproduction and lineage

Создание нового организма требует отдельной identity, trust root, resource budget and lifecycle. Offspring получает lineage manifest с parent genome/version, inherited artifacts and deliberate differences. Credential cloning запрещён.

## 8. Anti-patterns

- runtime writes canonical genome;
- model chooses and approves its own expanded permissions;
- successful reward overwrites audit or safety constraints;
- production traffic одновременно является uncontrolled training set;
- rollback depends on the same corrupted storage/control path;
- undocumented epigenetic overlay becomes permanent architecture.
