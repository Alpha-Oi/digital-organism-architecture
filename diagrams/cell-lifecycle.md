# Cell Lifecycle

```mermaid
stateDiagram-v2
  [*] --> DECLARED
  DECLARED --> ADMITTED
  DECLARED --> TERMINATED
  ADMITTED --> PROVISIONED
  PROVISIONED --> STARTING
  STARTING --> READY
  STARTING --> FAILED
  READY --> ACTIVE
  ACTIVE --> STRESSED
  STRESSED --> ACTIVE
  STRESSED --> SUSPECT
  ACTIVE --> SUSPECT
  SUSPECT --> ACTIVE
  SUSPECT --> ISOLATED
  ISOLATED --> REPAIRING
  REPAIRING --> READY
  REPAIRING --> TERMINATING
  ISOLATED --> TERMINATING
  ACTIVE --> QUIESCENT
  QUIESCENT --> ACTIVE
  QUIESCENT --> HIBERNATED
  HIBERNATED --> STARTING
  ACTIVE --> SENESCENT
  SENESCENT --> TERMINATING
  READY --> TERMINATING
  ACTIVE --> TERMINATING
  ACTIVE --> FAILED
  STRESSED --> FAILED
  SUSPECT --> FAILED
  FAILED --> ISOLATED
  TERMINATING --> TERMINATED
  TERMINATED --> [*]
```

Apoptosis = последовательность в состоянии `TERMINATING`; necrosis = путь через `FAILED` с обязательным fencing.

Источник истины: `specifications/state-machines.yaml` (машина `cell`); валидатор проверяет совпадение рёбер.
