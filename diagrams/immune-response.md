# Immune Response

```mermaid
stateDiagram-v2
  [*] --> OBSERVED
  OBSERVED --> DETECTED
  OBSERVED --> CLOSED
  DETECTED --> IDENTIFIED
  DETECTED --> CLOSED
  IDENTIFIED --> CONTAINED
  IDENTIFIED --> CLOSED
  CONTAINED --> QUARANTINED
  QUARANTINED --> NEUTRALIZED
  QUARANTINED --> CLOSED
  NEUTRALIZED --> RECOVERED
  RECOVERED --> LEARNED
  LEARNED --> DEFENSES_UPDATED
  LEARNED --> CLOSED
  DEFENSES_UPDATED --> CLOSED
  CLOSED --> [*]
```

detect → identify → contain → quarantine → neutralize → recover → learn → update defenses.

Источник истины: `specifications/state-machines.yaml` (машина `incident`); валидатор проверяет совпадение рёбер.
