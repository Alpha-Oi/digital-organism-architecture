# Homeostasis

## 1. ControlLoopSpec

```yaml
id: queue-pressure
variable: queue_depth
sensor:
  source: otel://collector/metrics
  interval: 10s
  freshness_max: 30s
target:
  lower: 0
  upper: 1000
controller:
  policy: proportional-with-hysteresis
  deadband: 100
actuators:
  - scale_workers
  - shed_low_priority
limits:
  max_step: 2
  max_actions_per_minute: 3
recovery:
  stable_for: 5m
fallback: freeze-and-escalate
```

## 2. Обязательные инварианты

- Sensor имеет unit, timestamp, freshness и confidence.
- Target range версионируется и имеет owner.
- Controller не действует по stale/unknown signal без explicit fallback.
- Actuator подтверждает applied/not-applied и фактический результат.
- Hysteresis и rate limit предотвращают oscillation.
- Safety ceiling имеет приоритет над optimization target.
- Manual override и emergency stop наблюдаемы и ограничены во времени.

## 3. Основные регулируемые переменные

| Domain | Variables | Типичные действия |
|---|---|---|
| Reliability | error rate, saturation, dependency health | failover, isolate, retry budget |
| Performance | latency, queue depth, throughput | scale, route, shed load |
| Cost/energy | tokens, GPU-ms, joules, currency | model route, context trim, defer |
| Security | anomaly, denied actions, compromised identities | revoke, quarantine, step-up auth |
| Memory | capacity, staleness, contradiction rate | compact, reindex, quarantine |
| Quality | verifier score, groundedness, task success | secondary verify, degrade autonomy |
| Physical | temperature, force, speed, distance | slow, stop, safe pose |

## 4. HormoneSignal

Hormone — широковещательный modifier, а не команда конкретной клетке. Он MUST содержать issuer, scope, severity, issued_at, expires_at, signature и reversal behavior. Примеры:

- `ADRENALINE_HIGH`: блокировать high-risk side effects, повышать verification;
- `CORTISOL_HIGH`: вводить backpressure и load shedding;
- `MELATONIN`: инициировать quiescence/consolidation;
- `GROWTH_SIGNAL`: разрешить bounded capacity expansion.

## 5. Failure analysis

| Failure | Detection | Response |
|---|---|---|
| Sensor drift | disagreement/recalibration failure | mark unknown, switch sensor, stop actuator |
| Actuator stuck | command acknowledged but variable unchanged | isolate actuator, alternative path |
| Oscillation | alternating actions without convergence | widen deadband, freeze, operator review |
| Integral windup | accumulated error after saturation | clamp state, reset controller |
| Metric gaming | proxy improves while outcome worsens | multi-signal invariant, audit sampling |
| Chronic stress | emergency mode exceeds TTL | graceful degradation, incident escalation |

## 6. Circadian and maintenance cycles

Temporal policy SHOULD разделять active, low-load, consolidation и maintenance windows. Все расписания указывают timezone, clock source, jitter, missed-run policy, maximum duration и emergency preemption. Safety and incident response всегда могут прервать sleep cycle.
