# DOA Roadmap

Версия 1.0 фиксирует терминологию, контракты и conformance model. Roadmap не меняет требования v1.0.

## 1.0.x — Clarifications

- исправления неоднозначностей без изменения semantics (errata);
- дополнительные schema examples;
- внешний peer review биологических соответствий и evidence первых claims.

## 1.1 — Conformance contract refinements (выпущен)

- необязательный статус `DESIGNED` и поле `failure_classes` в claim, реестр `specifications/failure-classes.yaml`;
- различие reserved и observed accounting (`REQ-CORE-18`), область tombstone (`REQ-CORE-22`);
- предупреждения checker'а для подвижных ссылок на evidence.

## 1.2 — Verification Kit (выпущен)

В релиз вошло исправление формулировок `REQ-CORE-18` и `REQ-CORE-22` из 1.1.0 по результатам review.

- executable conformance test plan;
- chaos/fault scenarios для cell, organ и circulation failures;
- reference OpenTelemetry semantic conventions `doa.*`;
- threat-model и hazard-analysis templates.

## 1.3 — Implementation Profiles (в работе)

- modular-monolith profile — готов, см. `profiles/modular-monolith.md`;
- Kubernetes/event-streaming profile;
- edge/robotics profile;
- air-gapped and high-assurance profile.

## 2.0 — Evidence-driven revision

Крупная версия возможна только после минимум двух независимых implementations, documented gaps и compatibility review. Не планируется превращать DOA в vendor-specific runtime.
