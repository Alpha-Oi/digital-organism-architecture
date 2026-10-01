# DOA Verification Kit

**Версия:** DOA v1.2 (`DOA-FS-1.0`). Informative документ: не вводит требований; при противоречии действуют нормативные документы (`docs/TERMINOLOGY.md`, раздел 3).

Kit помогает владельцу реализации получить воспроизводимое evidence для требований, чей способ проверки — `test`, `schema` или `inspection` (`docs/CONFORMANCE.md`, раздел 2), и показать его так, чтобы ассессор мог повторить проверку. Использование kit необязательно: claim без него остаётся допустимым, а прогон kit без claim соответствия не создаёт.

## 1. Состав

| Артефакт | Назначение |
|---|---|
| `verification/conformance-test-plan.yaml` | тестовые кейсы `TC-…`: по одному и более на каждое требование реестра, с процедурой, критериями прохождения и ожидаемым evidence |
| `verification/fault-scenarios.yaml` | сценарии отказа `FS-…` для клеток, органов, circulation и организма; покрытие классов `F-01`…`F-25` |
| `verification/otel-semantic-conventions.yaml` | атрибуты, события и метрики пространства `doa.*` для OpenTelemetry |
| `specifications/verification-report.schema.json` | формат отчёта о прогоне |
| `scripts/check_verification_report.py` | проверка отчёта по плану и, при желании, по claim |
| `templates/DOA_THREAT_MODEL.md`, `templates/DOA_HAZARD_ANALYSIS.md` | шаблоны threat model и hazard analysis |

## 2. Порядок использования

1. Выберите профили claim. Возьмите кейсы плана для требований этих профилей и `Conditional`.
2. Подготовьте среду: `isolated` (без production-данных и credentials) либо `staging`. Кейсы и сценарии с `isolated_environment: true` и `minimum_environment: isolated` MUST NOT выполняться вне изолированной среды.
3. Выполните кейсы и сценарии, сохраните evidence в неизменяемом хранилище (правило 2 `docs/CONFORMANCE.md`, раздел 3).
4. Составьте отчёт по `verification-report.schema.json`. `run_id` отчёта используйте как значение атрибута `doa.verification.run.id` в телеметрии прогона.
5. Проверьте отчёт: `python scripts/check_verification_report.py report.yaml`; вместе с claim: `python scripts/check_verification_report.py report.yaml --claim claim.yaml`.
6. Сошлитесь на отчёт и его артефакты в `evidence_ref` соответствующих требований claim.

## 3. Тестовый план

Кейс содержит: `id` вида `TC-<профиль>-<номер требования>-<номер кейса>`, `requirement`, `method` (совпадает с `verification` требования), `procedure`, `pass_criteria`, `evidence`, а также необязательные `scenarios` и `isolated_environment`. Кейс с `scenarios` считается пройденным только если пройдены перечисленные сценарии.

План определяет, что проверять и что считать результатом. Он не задаёт инструменты, пороги SLO и допуски: их объявляет реализация в genome и в claim, а кейс требует показать соответствие объявленному.

## 4. Сценарии отказа

Сценарий описывает одну инъекцию (`fault`), наблюдаемое исходное состояние (`steady_state`), ожидаемую цепочку `detection → containment → recovery → verification` (`docs/FAILURE_AND_RECOVERY.md`), условия прерывания (`abort_conditions`) и ограничение области воздействия (`blast_radius`).

Правила:

- сценарий запускается только в `isolated` или `staging` среде; прогон на production-данных и production-credentials недопустим;
- перед инъекцией фиксируется steady state, при выходе за `abort_conditions` инъекция снимается;
- окно инъекции отмечается событиями `doa.verification.scenario.injected.v1` и `doa.verification.scenario.completed.v1`, чтобы ожидаемые отклонения не принимались за реальные инциденты;
- реестр сценариев покрывает каждый класс отказа `F-01`…`F-25`: либо сценарием, либо кейсом плана с объяснением (раздел `coverage`; проверяет `scripts/validate_repository.py`);
- физическая инъекция отказов для Embodied Profile вне kit: она допустима только после утверждённого hazard analysis (`templates/DOA_HAZARD_ANALYSIS.md`).

## 5. Конвенции OpenTelemetry `doa.*`

Реестр определяет атрибуты, события и метрики. Значения перечислений берутся из схем и реестров (`lifecycle-transition.schema.json`, `failure-classes.yaml`, режимы восстановления органа, `health-evidence.schema.json`); валидатор репозитория проверяет, что источники существуют, а типы сущностей и режимы восстановления совпадают с каноническими машинами и таксономией.

- Имена: корневое пространство `doa`, нижний регистр, компоненты через точку, внутри компонента `snake_case`, единицы не входят в имя метрики.
- События названы типами `EventEnvelope`; переход состояния — `doa.lifecycle.<entity_type>.transitioned.v1`, как в `REQ-CORE-11`.
- Атрибуты с неограниченной кардинальностью (`metric_safe: false`: идентификаторы клеток, grants, сущностей, прогонов) допустимы на событиях и spans, но не на метриках.
- Атрибуты и события MUST NOT нести secrets и unrestricted reasoning traces (`REQ-CORE-24`).
- Отсутствие сигнала передаётся как `doa.health.result = UNKNOWN`, а не как отсутствие метрики со здоровым значением по умолчанию (`REQ-CORE-13`).
- Reserved и observed accounting различаются атрибутом `doa.accounting.kind` (`REQ-CORE-18`).

Ограничения: реестр записан в собственном формате DOA, он не проверялся инструментами OpenTelemetry, а правила именования не сверены с актуальной редакцией OpenTelemetry Semantic Conventions. Перед публикацией инструментария сверьте имена с нею; стабильность реестра — `development`, имена могут измениться в следующем minor-релизе.

## 6. Шаблоны

- `templates/DOA_THREAT_MODEL.md` связывает активы, границы доверия и угрозы с классами отказа, требованиями и проверками; содержит обязательные вопросы DOA (cognition и authority, делегирование, symbionts, provenance, identity, audit).
- `templates/DOA_HAZARD_ANALYSIS.md` связывает опасности с safe state, независимыми safety functions, real-time budget, reset authority и полями genome `spec.embodiment`.

Шаблон — не документ. Evidence даёт только заполненный документ, проверенный reviewer'ом, который не является его автором.

## 7. Что kit не делает

- Kit не содержит исполнителя: план и сценарии структурированы и проверяемы машинно, но запуск процедур и сбор evidence выполняет реализация. Машинно проверяются ссылки, структура отчёта и согласованность с claim, а не истинность результата.
- Проверка отчёта не открывает артефакты evidence; это обязанность ассессора.
- Прохождение кейсов — evidence для требований, а не сертификация; DOA не сертифицирует реализации (`GOVERNANCE.md`, раздел 6).
- Kit составлен без независимой реализации: процедуры не были выполнены на сторонней системе, и их применимость может потребовать errata в `1.2.x`.

## 8. Совместимость

Kit — additive: требования, идентификаторы `REQ-*`, схемы и state machines `1.1.0` не менялись. Claim по `1.0.x` и `1.1.x` остаются действительными. Схема `verification-report` необязательна и на claim не влияет.
