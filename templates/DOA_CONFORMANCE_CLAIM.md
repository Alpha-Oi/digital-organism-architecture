# DOA Conformance Claim

> Шаблон для реализации. Machine-readable форма — YAML по `specifications/conformance-claim.schema.json`; проверка: `python scripts/check_conformance_claim.py claim.yaml`. Правила статусов — `docs/CONFORMANCE.md`.

## Identity

- Implementation:
- Owner:
- Version/commit:
- Assessment date:
- DOA standard: `DOA-FS-1.0`
- Status: `UNVERIFIED | PARTIAL | VERIFIED`
- Assurance: `self-assessed | independently-reviewed`
- Assessor:

## Claimed profiles

- [ ] Core (обязателен)
- [ ] Distributed
- [ ] Adaptive
- [ ] Embodied

## Conditional capabilities

- [ ] reproduction (иначе `ecology.reproduction: forbidden`)
- [ ] federation (иначе `ecology.federation: none`)
- [ ] horizontal transfer (иначе `ecology.horizontal_transfer: forbidden`)

## Scope and exclusions

Опишите system boundary, environments, excluded organs/capabilities и assumptions.

## Requirement mapping

Статусы: `PASS | PARTIAL | FAIL | EXCLUDED | NOT_ASSESSED | DESIGNED`. `PASS` требует `evidence_ref`; `EXCLUDED` требует justification; `DESIGNED` (механизм описан, но не реализован или не имеет воспроизводимого evidence) требует component и gap owner и не допускается в claim `VERIFIED`.

| Requirement | Profile | Implementation component | Evidence | Status | Gap/owner |
|---|---|---|---|---|---|
| REQ-CORE-01 Identity of every action | Core | | | NOT_ASSESSED | |
| REQ-CORE-02 Declared organism boundary | Core | | | NOT_ASSESSED | |
| REQ-CORE-03 Desired/observed separation | Core | | | NOT_ASSESSED | |
| REQ-CORE-04 Genome/epigenome separation | Core | | | NOT_ASSESSED | |
| REQ-CORE-05 Least capability and attenuation | Core | | | NOT_ASSESSED | |
| REQ-CORE-06 No unilateral self-modification | Core | | | NOT_ASSESSED | |
| REQ-CORE-07 Closed-loop homeostasis | Core | | | NOT_ASSESSED | |
| REQ-CORE-08 Compartmentalization | Core | | | NOT_ASSESSED | |
| REQ-CORE-09 Provenance | Core | | | NOT_ASSESSED | |
| REQ-CORE-10 Reversibility | Core | | | NOT_ASSESSED | |
| REQ-CORE-11 Observable lifecycle | Core | | | NOT_ASSESSED | |
| REQ-CORE-12 Human authority | Core | | | NOT_ASSESSED | |
| REQ-CORE-13 Truthful uncertainty | Core | | | NOT_ASSESSED | |
| REQ-CORE-14 Immune response lifecycle | Core | | | NOT_ASSESSED | |
| REQ-CORE-15 Bounded termination (apoptosis) | Core | | | NOT_ASSESSED | |
| REQ-CORE-16 Uncontrolled failure containment (necrosis) | Core | | | NOT_ASSESSED | |
| REQ-CORE-17 Growth control | Core | | | NOT_ASSESSED | |
| REQ-CORE-18 Resource accounting | Core | | | NOT_ASSESSED | |
| REQ-CORE-19 Memory governance | Core | | | NOT_ASSESSED | |
| REQ-CORE-20 Recovery taxonomy | Core | | | NOT_ASSESSED | |
| REQ-CORE-21 Aging and senescence | Core | | | NOT_ASSESSED | |
| REQ-CORE-22 Identity continuity and anti-resurrection | Core | | | NOT_ASSESSED | |
| REQ-CORE-23 Failure-class coverage | Core | | | NOT_ASSESSED | |
| REQ-CORE-24 Audit and secret hygiene | Core | | | NOT_ASSESSED | |
| REQ-CORE-25 Microbiome (guest) governance | Core | | | NOT_ASSESSED | |
| REQ-CORE-26 Separation of cognition and authority | Core | | | NOT_ASSESSED | |
| REQ-DIST-01 Event contract and delivery semantics | Distributed | | | NOT_ASSESSED | |
| REQ-DIST-02 Partial failure, backpressure and emergency flow | Distributed | | | NOT_ASSESSED | |
| REQ-DIST-03 Topology and failure-domain placement | Distributed | | | NOT_ASSESSED | |
| REQ-DIST-04 Quorum, failover and split-brain handling | Distributed | | | NOT_ASSESSED | |
| REQ-DIST-05 Clock and synchronization assumptions | Distributed | | | NOT_ASSESSED | |
| REQ-DIST-06 Genetic drift detection | Distributed | | | NOT_ASSESSED | |
| REQ-DIST-07 Catastrophic recovery | Distributed | | | NOT_ASSESSED | |
| REQ-ADPT-01 Learning is not evolution | Adaptive | | | NOT_ASSESSED | |
| REQ-ADPT-02 Governed change protocol | Adaptive | | | NOT_ASSESSED | |
| REQ-ADPT-03 Separation of proposer, evaluator and approver | Adaptive | | | NOT_ASSESSED | |
| REQ-ADPT-04 Evaluation-set governance | Adaptive | | | NOT_ASSESSED | |
| REQ-ADPT-05 Drift detection and reward-hacking resistance | Adaptive | | | NOT_ASSESSED | |
| REQ-ADPT-06 Lineage of variants | Adaptive | | | NOT_ASSESSED | |
| REQ-ADPT-07 Learned defenses are measured | Adaptive | | | NOT_ASSESSED | |
| REQ-EMB-01 Hazard analysis and safe state | Embodied | | | NOT_ASSESSED | |
| REQ-EMB-02 Independent interlock, watchdog and emergency stop | Embodied | | | NOT_ASSESSED | |
| REQ-EMB-03 Real-time budget | Embodied | | | NOT_ASSESSED | |
| REQ-EMB-04 Calibrated sensing and uncertainty | Embodied | | | NOT_ASSESSED | |
| REQ-EMB-05 Actuator envelope and stale command rejection | Embodied | | | NOT_ASSESSED | |
| REQ-EMB-06 Reset authority | Embodied | | | NOT_ASSESSED | |
| REQ-COND-01 Reproduction control | Conditional | | | NOT_ASSESSED | |
| REQ-COND-02 Federation and treaties | Conditional | | | NOT_ASSESSED | |
| REQ-COND-03 Horizontal transfer isolation | Conditional | | | NOT_ASSESSED | |

## Failure classes (необязательно)

Классы из `specifications/failure-classes.yaml` (`F-01`…`F-25`) можно оценить по отдельности в поле `failure_classes`. Если `REQ-CORE-23` имеет статус `PASS`, каждый класс MUST быть `PASS` или `EXCLUDED` с justification.

| Class | Implementation component | Evidence | Status | Gap/owner |
|---|---|---|---|---|
| F-01 | | | NOT_ASSESSED | |

## Observed accounting (необязательно)

Потребление, известное только из внешней телеметрии (`REQ-CORE-18`), записывается в поле `observed_accounting` с источником и неопределённостью. Его нельзя выдавать за reserved accounting.

| Source | Uncertainty | Evidence |
|---|---|---|
| | | |

## Evidence pack

- Genome and effective overlays:
- Trust-boundary inventory:
- State-transition evidence:
- Fault/restore tests:
- Security tests:
- Adaptive-learning evidence, if applicable:
- Physical hazard evidence, if applicable:

## Decision

- Blocking gaps:
- Accepted risks:
- Reassessment trigger/date:
