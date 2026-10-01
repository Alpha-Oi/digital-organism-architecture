# Embodied Safety States

```mermaid
stateDiagram-v2
  [*] --> INIT
  INIT --> CALIBRATING
  CALIBRATING --> READY
  READY --> ACTIVE
  ACTIVE --> LIMITED
  LIMITED --> ACTIVE
  ACTIVE --> SAFE_STOP
  LIMITED --> SAFE_STOP
  SAFE_STOP --> LOCKED_OUT
  LOCKED_OUT --> INSPECTED
  INSPECTED --> RESET_AUTHORIZED
  RESET_AUTHORIZED --> CALIBRATING
```

Независимо от LLM и сетевого control plane. Подробности — `docs/ROBOTICS_EXTENSION.md`.

Источник истины: `specifications/state-machines.yaml` (машина `embodied_safety`); валидатор проверяет совпадение рёбер.
