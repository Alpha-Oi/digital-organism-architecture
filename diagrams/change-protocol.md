# Change Protocol

```mermaid
stateDiagram-v2
  [*] --> OBSERVED
  OBSERVED --> PROPOSED
  PROPOSED --> SIMULATED
  PROPOSED --> EVALUATED
  PROPOSED --> REJECTED
  SIMULATED --> EVALUATED
  SIMULATED --> REJECTED
  EVALUATED --> APPROVED
  EVALUATED --> REJECTED
  APPROVED --> CANARY
  CANARY --> PROMOTED
  CANARY --> ROLLED_BACK
  PROMOTED --> [*]
  ROLLED_BACK --> [*]
  REJECTED --> [*]
```

Learning (class=learning) пропускает `SIMULATED`; evolution (class=evolution) проходит все стадии. Terminal: `PROMOTED`, `ROLLED_BACK`, `REJECTED`.

Источник истины: `specifications/state-machines.yaml` (машина `change`); валидатор проверяет совпадение рёбер.
