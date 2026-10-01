# Changelog

Все существенные изменения стандарта документируются здесь. Формат версий — SemVer; политика совместимости — `GOVERNANCE.md`.

## [1.2.0] - 2026-10-01

Minor-релиз: Verification Kit. Все добавления additive и informative; требований, идентификаторов `REQ-*`, state machines и существующих схем нет. Идентификатор стандарта остаётся `DOA-FS-1.0`.

### Added

- `docs/VERIFICATION_KIT.md` (informative): состав kit, порядок использования, правила безопасности прогона, ограничения.
- `verification/conformance-test-plan.yaml`: тестовые кейсы `TC-…` (49, по одному на каждое требование реестра) с процедурой, критериями прохождения, ожидаемым evidence, ссылками на сценарии и признаком изолированной среды.
- `verification/fault-scenarios.yaml`: 22 сценария отказа `FS-…` для клеток, органов, circulation и организма; раздел `coverage` сопоставляет каждый класс отказа `F-01`…`F-25` сценарию либо кейсу плана.
- `verification/otel-semantic-conventions.yaml`: 21 атрибут, 4 события и 14 метрик пространства `doa.*`; значения перечислений привязаны к схемам и реестрам; идентификаторы с неограниченной кардинальностью запрещены на метриках.
- `specifications/verification-report.schema.json` и `scripts/check_verification_report.py`: формат отчёта о прогоне и его проверка по плану и, с `--claim`, по conformance claim (противоречия отмечаются ошибкой, неполное покрытие — предупреждением). В схеме нет окружения production.
- `templates/DOA_THREAT_MODEL.md` и `templates/DOA_HAZARD_ANALYSIS.md`: шаблоны для evidence пакета (`REQ-CORE-14`, `REQ-CORE-23`, `REQ-CORE-24`, `REQ-EMB-01`…`REQ-EMB-06`).
- Примеры отчёта: valid `verification-report--reference.yaml`; invalid `verification-report--pass-without-evidence.yaml`, `verification-report--production-environment.yaml`.
- Проверки в `scripts/validate_repository.py`: покрытие требований кейсами, согласованность метода кейса с `verification` требования, ссылки сценариев на классы отказа и требования, полнота и двусторонняя согласованность покрытия классов отказа, правила именования и ссылки реестра `doa.*`, поведение проверки отчёта на искусственных нарушениях.

### Changed

- `docs/TERMINOLOGY.md`, `docs/CONFORMANCE.md`, `README.md`, `ROADMAP.md`: ссылки и статус документов kit.

### Compatibility

- Claim по `1.0.x` и `1.1.x` остаются действительными. Использование kit необязательно, схема `verification-report` на claim не влияет.

### Основание и ограничения

- Kit составлен без независимой реализации: процедуры не выполнялись на сторонней системе; корректность и применимость кейсов и сценариев не проверены извне и могут потребовать errata `1.2.x`.
- «Executable» означает структурированный и машинно проверяемый план; исполнителя (runner) kit не содержит. Проверка отчёта не открывает артефакты evidence.
- Реестр `doa.*` написан в собственном формате; он не проверялся инструментами OpenTelemetry, а правила именования не сверены с актуальной редакцией OpenTelemetry Semantic Conventions (источник был недоступен при подготовке).
- Шаблоны threat model и hazard analysis не заменяют отраслевые методики и стандарты безопасности.

## [1.1.0] - 2026-10-01

Minor-релиз: additive изменения контракта conformance и два нормативных уточнения. Новых требований, механизмов, схем (кроме расширения схемы claim) и state machines нет. Идентификатор стандарта остаётся `DOA-FS-1.0`.

### Added

- Необязательный статус требования `DESIGNED` в `conformance-claim.schema.json`: механизм объявлен проектом или инструкциями, но не реализован кодом либо не имеет воспроизводимого evidence. Требует `component` и `gap_owner`, не считается `PASS`, не допускается в claim `VERIFIED`. Определения статусов требования добавлены в `docs/CONFORMANCE.md`, раздел 3 (issue #5, п. 1).
- `specifications/failure-classes.yaml`: машиночитаемый реестр классов отказа `F-01`…`F-25`, идентичный таблице `docs/FAILURE_AND_RECOVERY.md`, раздел 2; валидатор сверяет id, названия и все колонки (issue #5, п. 5).
- Необязательное поле `failure_classes` в claim: статус по каждому классу. `scripts/check_conformance_claim.py` проверяет id по реестру и дубликаты; при `REQ-CORE-23` в статусе `PASS` (и в `VERIFIED` claim) все классы MUST быть `PASS` или `EXCLUDED`.
- Предупреждения `check_conformance_claim.py` (`warning:`, код выхода не меняется) для `evidence_ref`, ссылающегося на подвижную ветку (`main`, `master`, `develop`, `development`, `HEAD`, `latest`) или не содержащего пути и идентификатора.
- Примеры: valid `conformance-claim--designed-and-failure-classes.yaml`; invalid `conformance-claim--designed-without-owner.yaml` и `conformance-claim--failure-class-bad-id.yaml`; раздел `failure_classes` в шаблоне claim.
- Проверки в `scripts/validate_repository.py`: реестр классов отказа, определения статусов, поведение checker'а для `DESIGNED`, `failure_classes` и предупреждений.

### Changed (нормативно)

- `REQ-CORE-18`: различие reserved accounting (работа, которую организм выполняет или разрешает сам) и observed accounting (потребление, известное только из внешней телеметрии). Observed MUST записываться с источником и неопределённостью и MUST NOT выдаваться за reserved. Описание в `docs/METABOLISM.md`, раздел 1 (issue #5, п. 4).
- `REQ-CORE-22`: область применения. Continuity records и tombstones обязательны для identities, которые организм выдаёт сам; identities других сторон объявляются внешними зависимостями, а сопоставление и проверка их статуса при restore — SHOULD. Описание в `docs/LIFECYCLE.md`, раздел 9 (issue #5, п. 3).
- `REQ-CORE-23`: в тексте evidence упомянуто поле `failure_classes`.

### Compatibility

- Новых обязательных требований для существующих профилей нет. Реализация, соответствовавшая `REQ-CORE-18` и `REQ-CORE-22` по 1.0.x, остаётся соответствующей: ужесточений для неё нет (SHOULD вместо MUST для внешних identities, observed accounting описывает то, что раньше формулировка не покрывала).
- Claim по 1.0.x остаются действительными. Claim, использующий `DESIGNED` или `failure_classes`, не проходит схему 1.0.x (расширены enum и свойства).
- Идентификаторы `REQ-*`, `C-`/`T-`/… и `$id` схем не менялись.

### Основание и ограничения

Изменения выведены из двух применений стандарта (система на стадии проектирования и навык `autopilot-jet`); оба выполнены ассистентом, независимой проверки нет. Нормативные пункты (`REQ-CORE-18`, `REQ-CORE-22`) требуют review maintainer по `GOVERNANCE.md`, раздел 4.

## [1.0.1] - 2026-10-01

Patch-релиз: clarifications без изменения semantics. Требования, схемы, state machines, идентификаторы и поведение скриптов не менялись.

### Added

- `docs/IMPLEMENTATION_GUIDE.md` (informative): как применять стандарт к control plane над внешними агентами (граница организма, когда агент — клетка, что такое genome), к организмам, заданным инструкциями для LLM, и к системам на стадии проектирования; как закреплять evidence, когда claim лежит рядом с кодом; типичные ошибки оценки. Выведено из существующих правил `BOUNDARY_AND_IDENTITY.md` и `CONFORMANCE.md`.

### Clarified

- `docs/CONFORMANCE.md`, `docs/BOUNDARY_AND_IDENTITY.md`: добавлены ссылки на новое руководство.
- `docs/TERMINOLOGY.md`: руководство внесено в таблицу статусов документов как Informative.
- `scripts/validate_repository.py`: новый документ добавлен в список обязательных файлов.
- Метаданные версии (`VERSION`, README, строка «Версия релиза» стандарта, `RELEASE_READINESS`) приведены к 1.0.1; нормативный текст стандарта не менялся.

### Не вошло

Предложения из issue #5, меняющие семантику или схему (статус `DESIGNED`, уточнение области `REQ-CORE-22`, различие reserved и observed в `REQ-CORE-18`, `failure-classes.yaml`), относятся к minor-релизу, а не к patch.

## [1.0.0] - 2026-10-01

Первый канонический релиз `DOA-FS-1.0`.

### Added

- канонический стандарт `DOA-FS-1.0`, Core, Distributed, Adaptive, Embodied и Conditional profiles;
- каноническая матрица Biology-to-IT: 119 механизмов с колонками responsibility, component, contract, protocol, invariant, failure mode, security/safety control, observability, evidence и нормативным статусом (`Profile`); покрытие фундаментальных механизмов (Приложение B);
- новые механизмы, закрывающие архитектурные пробелы: self/non-self recognition, immune memory, necrosis, cellular stress response, nutrient/oxygen sensing, compartmentalization, positive feedback, forgetting, motor hierarchy, peripheral ganglia, synchronization, provenance, identity continuity, state continuity и anti-resurrection, organism termination, organism-scale regeneration, genetic drift, model drift, horizontal transfer/reproductive isolation, sensor fusion/calibration, actuator envelope, safe-stop reflex;
- `BOUNDARY_AND_IDENTITY.md`, `LIFECYCLE.md`, `FAILURE_AND_RECOVERY.md`, `CONFORMANCE.md`, `TERMINOLOGY.md`;
- машиночитаемые `specifications/state-machines.yaml` (organism, cell, incident, change, embodied_safety) и `specifications/requirements.yaml` (49 требований соответствия);
- 14 JSON Schemas (добавлены control-loop, capability-grant, memory-record, health-evidence, policy-overlay, lineage-manifest, lifecycle-transition, conformance-claim), valid и invalid примеры для каждой схемы;
- 5 state-диаграмм, выводимых из state machines;
- `scripts/validate_repository.py` и `scripts/check_conformance_claim.py`;
- governance, contribution и security policies, conformance claim template, CODEOWNERS, pull request и standard-gap templates;
- read-only GitHub Actions validation workflow, проверка соответствия tag и `VERSION`.

### Clarified

- DOA является meta-architecture standard, а не конкретным продуктом;
- биологическая аналогия без цифрового контракта и evidence не является соответствием;
- learning ≠ evolution; self-modification и adaptive learning требуют governance, evidence и rollback;
- restart, restore, repair, replace, regenerate, rebuild, reconfigure и rollback — разные режимы восстановления;
- apoptosis (контролируемое завершение) и necrosis (неконтролируемый отказ с обязательным fencing) различаются.
