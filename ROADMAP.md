# DOA Roadmap

Версия 1.0 фиксирует терминологию, контракты и conformance model. Roadmap не меняет требования v1.0.

## 1.0.x — Clarifications

- исправления неоднозначностей без изменения semantics (errata);
- дополнительные schema examples;
- внешний peer review биологических соответствий и evidence первых claims.

## 1.1 — Verification Kit

- executable conformance test plan;
- chaos/fault scenarios для cell, organ и circulation failures;
- reference OpenTelemetry semantic conventions `doa.*`;
- threat-model и hazard-analysis templates.

## 1.2 — Implementation Profiles

- modular-monolith profile;
- Kubernetes/event-streaming profile;
- edge/robotics profile;
- air-gapped and high-assurance profile.

## 2.0 — Evidence-driven revision

Крупная версия возможна только после минимум двух независимых implementations, documented gaps и compatibility review. Не планируется превращать DOA в vendor-specific runtime.
