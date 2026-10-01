# Organism Lifecycle

```mermaid
stateDiagram-v2
  [*] --> SPECIFIED
  SPECIFIED --> VALIDATED
  VALIDATED --> PROVISIONING
  PROVISIONING --> DEVELOPING
  DEVELOPING --> READY
  READY --> ACTIVE
  ACTIVE --> STRESSED
  STRESSED --> ACTIVE
  STRESSED --> DEGRADED
  ACTIVE --> DEGRADED
  DEGRADED --> REPAIRING
  REPAIRING --> ACTIVE
  REPAIRING --> DEGRADED
  REPAIRING --> PROVISIONING
  ACTIVE --> QUIESCENT
  QUIESCENT --> ACTIVE
  ACTIVE --> SENESCENT
  DEGRADED --> SENESCENT
  SENESCENT --> REPAIRING
  SENESCENT --> RETIRING
  ACTIVE --> RETIRING
  DEGRADED --> RETIRING
  QUIESCENT --> RETIRING
  RETIRING --> TERMINATED
  TERMINATED --> [*]
```

Birth → Development → Maturity → Aging → Termination. `QUARANTINED` is an orthogonal security state (см. `LIFECYCLE.md`).

Источник истины: `specifications/state-machines.yaml` (машина `organism`); валидатор проверяет совпадение рёбер.
