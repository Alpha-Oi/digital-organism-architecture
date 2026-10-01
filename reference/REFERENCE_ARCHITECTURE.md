# Reference Architecture

Эта архитектура является примером соответствия Distributed + Adaptive profiles, а не обязательным deployment topology.

## Components

| DOA role | Reference component | Authority boundary |
|---|---|---|
| Nucleus | signed genome/policy store | write only through reviewed change service |
| Nucleolus | build and attestation pipeline | produces signed runtime bundles |
| Membrane | ingress/egress gateways | authenticates, validates, rate-limits, redacts |
| Receptors | modality adapters | no direct memory/policy writes |
| Thalamus | event router | routes, does not authorize side effects |
| Cortex | planner/reasoning pool | proposes plans only |
| Basal ganglia | policy/risk/resource decision service | issues bounded capability grants |
| Spinal cord | deterministic rule/reflex engine | fixed bounded actions |
| Circulation | event log + RPC mesh | carries typed envelopes |
| Endocrine | mode/config signal controller | signed expiring overlays |
| Hippocampus | memory gateway and stores | enforces provenance/retention |
| Immune system | detection, quarantine and response | independent revoke/isolate authority |
| Metabolism | resource scheduler and accounting | hard quotas and priority budgets |
| Repair | reconciler and restore controller | uses trusted artifacts/backups |
| Sensors | telemetry collectors | independent source and freshness |
| Identity authority | workload identity issuer, continuity and tombstone registry | issues identities; rotation by signed record; rejects restore after tombstone |
| Admission and lease controller | admission controller, lease/fencing service | enforces `growth_control`; fences lost cells without their cooperation |

## End-to-end transaction

1. Gateway authenticates caller and creates `EventEnvelope`.
2. Receptor validates modality, size, schema, classification and freshness.
3. Router selects reflex, workflow or reasoning path.
4. Planner emits `PlanProposal` with assumptions and requested capabilities.
5. Decision service resolves policy, risk and resource availability.
6. Grant service issues short-lived `CapabilityGrant`.
7. Cells execute within quotas and emit correlated observations.
8. Egress gateway enforces side-effect and data-loss policy.
9. Outcome, cost and verifier evidence feed memory and homeostasis.

## Failure-domain rules

- Genome authority and runtime planner are separate.
- Policy decision and policy enforcement are separate components or independently testable modules.
- Audit path survives loss of ordinary data plane where feasible.
- Critical organs have a tested failover or declared graceful-degradation mode.
- Quarantine can revoke a cell without cooperation from that cell.
- Recovery artifacts reside outside the failure domain they restore.

## Minimum deployment for a small system

A modular monolith MAY combine router, planner, decision and memory gateway, provided interfaces remain explicit and the executor is separately isolated. SQLite/object storage MAY replace distributed databases if durability and locking meet the use case. A single-node deployment cannot claim geographic redundancy.
