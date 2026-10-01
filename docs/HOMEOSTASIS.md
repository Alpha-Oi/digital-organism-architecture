# Homeostasis

Homeostasis в DOA — инженерный механизм замкнутого регулирования (строки H-01, H-02, H-03 реестра), а не метафора. Контракт — `ControlLoopSpec` (`specifications/control-loop.schema.json`); каждый контур в genome `spec.homeostasis` MUST валидироваться по этой схеме.

## 1. ControlLoopSpec

```yaml
id: queue-pressure
variable: queue_depth
sensor:
  source: otel://collector/metrics
  interval: 10s
  freshness_max: 30s
  independent_source: otel://collector-b/metrics
target_range: {lower: 0, upper: 1000}
thresholds: {warning: 800, critical: 1200, safety_ceiling: 5000}
controller: {policy: proportional-with-hysteresis, hysteresis: 100, deadband: 100}
actuators: [scale_workers, shed_low_priority]
limits: {max_step: 2, max_actions_per_minute: 3}
amplification: {ceiling: 4, ttl: 15m, terminator: operator-or-timeout}   # только для усиливающих контуров
escalation:
  - {level: WARNING, condition: "above 800 for 2m", action: scale_workers}
  - {level: CRITICAL, condition: "above 1200 for 2m", action: shed_low_priority}
  - {level: EMERGENCY, condition: "above 5000 or sensor UNKNOWN 5m", action: freeze-and-page-operator}
recovery: {stable_for: 5m, criterion: "queue_depth below 800"}
fallback: freeze-and-escalate
override: {authority: on-call-operator, max_duration: 1h}
```

## 2. Обязательные инварианты

- Sensor имеет unit, timestamp, freshness и confidence.
- Target range версионируется и имеет owner.
- Controller не действует по stale/unknown signal без explicit fallback.
- Actuator подтверждает applied/not-applied и фактический результат.
- Hysteresis и rate limit предотвращают oscillation.
- Safety ceiling имеет приоритет над optimization target.
- Manual override и emergency stop наблюдаемы и ограничены во времени.
- Negative feedback (H-01): действие уменьшает отклонение; контур определяет recovery criterion и критерий стабильности (раздел 8).
- Positive feedback (H-02): любой самоусиливающийся путь (spawn, retry, escalation, inflammation, quorum) MUST иметь `amplification.ceiling`, `ttl` и внешний terminator; запрещено усиление без верхней границы.

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

Hormone — широковещательный modifier, а не команда конкретной клетке. Контракт — `HormoneSignal` (`hormone.schema.json`). Он MUST содержать issuer, scope, severity, issued_at, expires_at, signature и reversal behavior. Issuer и enforcer MUST быть разными компонентами; противоречивые сигналы разрешаются по scope и precedence, а при неразрешимом конфликте — fail-closed и эскалация. Примеры:

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

## 7. Референсные контуры обязательных доменов

Реализация MUST иметь `ControlLoopSpec` для каждого применимого домена. Числа ниже — иллюстративные defaults для расчёта и тестов, а не требования; реальные target ranges, thresholds и owners задаются реализацией и версионируются.

| Домен | Variable (unit) | Target range | WARNING / CRITICAL | Корректирующие действия | Эскалация (EMERGENCY) | Recovery criterion |
|---|---|---|---|---|---|---|
| Resource pressure | saturation CPU/GPU (ratio) | 0.3–0.75 | 0.8 / 0.92 | scale, admission throttle, shed low priority, scarcity gate на spawn (M-14) | sustained > 0.97 → emergency circulation (M-03), freeze spawn | < 0.7 в течение 10m |
| Memory pressure | memory/context fill (ratio), stale/contradiction rate | fill 0.4–0.8; stale < 5% | 0.85 / 0.95; stale 8% / 15% | compact, decay, forget (N-17), quarantine записей | fill > 0.98 → read-only memory, human review | fill < 0.75 и stale < 5% в течение 30m |
| Model degradation | verifier score / groundedness (ratio) vs baseline | ≥ baseline − 2% | −5% / −10% | secondary verification, снижение автономии, failover модели | −20% → отключение модели, `ROLLBACK`, incident | восстановление ≥ baseline − 2% на governed eval set |
| Latency | p95 latency (s) | ≤ SLO | 1.2×SLO / 2×SLO | route to faster path, trim context, shed | > 4×SLO → degraded mode, escalate | ≤ SLO в течение 10m |
| Agent failure | доля failed/looping агентов (ratio) | < 1% | 3% / 10% | restart → replace, loop guard, quarantine агента | > 25% → organ DEGRADED, failover | < 1% в течение 15m |
| Tool failure | error/timeout rate инструмента (ratio) | < 2% | 5% / 20% | circuit breaker, alternative tool, retry budget | недоступен критический tool → fail-closed для зависимых действий | probe PASS ×5 |
| Security incident | число открытых incidents, denied/anomalous actions (rate) | 0 открытых high | любое high-severity / compromise confirmed | contain, step-up auth, revoke, quarantine (incident machine) | подтверждённая компрометация → `QUARANTINED`, human authority | incident `CLOSED`, defenses updated |
| Dependency failure | status внешней зависимости (PASS/FAIL/UNKNOWN) | PASS | UNKNOWN 2m / FAIL | bounded retry, failover, degrade по `failure_policy` | FAIL критической → organ DEGRADED | PASS stable_for 5m |
| Cascading failure | число коррелированно затронутых органов; retry amplification | 0–1 | 2 / ≥3 | bulkheads, load shedding, emergency circulation, снижение retry budget | ≥ 3 органов → `STRESSED→DEGRADED`, human authority | независимые SLO в норме 30m |

## 8. Критерии стабильности и аварийные состояния

Контур считается стабильным, если одновременно:

1. `|error|` не выходит за target range ± deadband в течение `recovery.stable_for`;
2. число смен знака действия (flip-flop) за окно не превышает порога (по умолчанию ≤ 2 за 10 минут);
3. действия не упираются в `limits` более чем N раз подряд (признак integral windup или неисправного actuator);
4. сигнал свеж (`freshness_max`) и подтверждён независимым источником, где он объявлен.

Аварийные состояния (escalation ladder): `NORMAL → WARNING → CRITICAL → EMERGENCY`. Соответствие runtime-состояниям организма: `WARNING`/`CRITICAL` → `STRESSED`; `EMERGENCY` или превышение TTL stress → `DEGRADED`. В `EMERGENCY` MUST быть назначен человек-authority, ограничено время режима (`override.max_duration`, fever/emergency TTL — I-11), а выход выполняется по recovery criterion. Контур с `UNKNOWN` сигналом MUST выполнять `fallback`, а не продолжать действовать по устаревшему значению.

Нарушение стабильности (oscillation, windup, metric gaming) является отказом контура и классифицируется в `FAILURE_AND_RECOVERY.md` (F-11, F-14, F-25). Все действия коррелируются с `control_error` и `action_total` для alert-to-action trace.
