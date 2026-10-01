# Robotics Extension — Embodied Profile

## 1. Scope

Embodied Profile добавляет physical sensors, actuators, real-time deadlines, energy/thermal limits and hazards. Он не отменяет отраслевые safety standards и certification.

## 1.1 Единая модель

Robotics extension не вводит отдельной архитектуры: физическое воплощение — тот же контур DOA с дополнительными ограничениями.

```text
Perception -> State -> Decision -> Action -> Feedback
```

| Звено | DOA-механизм | Embodied-ограничение |
|---|---|---|
| Perception | N-01 `Observation`, R-01 sensor fusion, R-02 modality | calibration, covariance/uncertainty, `UNCERTAIN` при расхождении |
| State | N-02 proprioception, R-05 body schema и frame | версионированная map/frame, freshness |
| Decision | N-05 cortex (proposal), N-06 decision service | модель не единственный разрешающий компонент |
| Action | N-07 motor hierarchy, R-03 actuator envelope | bounded envelope, deadline, независимый interlock |
| Feedback | N-01 + H-01 homeostasis | watchdog, latency budget, energy/thermal регуляция |

Дополнительные ограничения: physical safety (R-04), actuator constraints (R-03), latency (real-time budget, REQ-EMB-03), calibration (R-01), embodiment (`genome.spec.embodiment`), environmental uncertainty (UNCERTAIN/LIMITED состояния). Safety states — машина `embodied_safety` (`specifications/state-machines.yaml`, `diagrams/embodied-safety.md`).

## 2. Command path

```text
intent proposal
 -> policy and task authorization
 -> world-state freshness check
 -> motion/action planner
 -> safety envelope validator
 -> independent interlock
 -> actuator command with deadline
 -> feedback + watchdog
```

Generative model output считается proposal, не motor command.

## 3. Sensor contract

Каждое observation содержит device identity, calibration version, timestamp/clock domain, unit/frame, covariance/uncertainty, range, validity and freshness. Sensor disagreement переводит world state в `UNCERTAIN`, а не усредняется без policy.

## 4. Actuator contract

Command содержит actuator, coordinate frame, bounded magnitude/speed/force, start/deadline, preconditions, cancellation and safe-state fallback. Expired command MUST NOT исполняться.

## 5. Safety states

```text
INIT -> CALIBRATING -> READY -> ACTIVE <-> LIMITED
ACTIVE | LIMITED -> SAFE_STOP -> LOCKED_OUT
LOCKED_OUT -> INSPECTED -> RESET_AUTHORIZED -> CALIBRATING
```

Переходы с guards, authority и timeouts — `docs/LIFECYCLE.md`, раздел 10.

Emergency stop и hard limit реализуются независимо от LLM, network control plane and high-level planner.

## 6. Embodied homeostasis

Регулируются battery/energy, temperature, structural load, localization confidence, communication quality, sensor health and actuator wear. При конфликте physical safety имеет приоритет над task completion.

## 7. Spatial organization

Frames, maps, geofences, no-go zones, collision domains and human proximity являются versioned state. Planning MUST указывать использованную map/frame version.

## 8. Required evidence

- hazard analysis and safe-state definition;
- timing budget and worst-case response evidence;
- sensor calibration/fault-injection tests;
- independent watchdog and emergency-stop test;
- stale/replayed command rejection;
- degraded communication and power-loss behavior;
- recovery/reset authority test.
