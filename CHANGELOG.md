# Changelog

Все существенные изменения стандарта документируются здесь. Формат версий — SemVer; политика совместимости — `GOVERNANCE.md`.

## [Unreleased]

Пилот направления «механизмы»: карточки биологических механизмов, граф связей между механизмами и принципы. Изменения additive и informative; версия стандарта не менялась.

### Added

- `mechanisms/README.md`: зачем нужен раздел, критерий отбора механизмов, как пользоваться графом, ограничения.
- `mechanisms/interaction-graph.yaml`: граф из 119 механизмов реестра и 163 связи девяти типов; у каждой связи указано основание (требование, класс отказа, документ или статья PubMed), три связи помечены гипотезами. У каждого механизма указана роль в учёте ресурсов (`resource_role`: 100 рабочих, 15 хранилищ, 2 пассивных, 2 антипаттерна) по `REQ-CORE-18`.
- `mechanisms/cards/`: девять карточек со ссылками на статьи PubMed: ATP-синтаза, ДНК-полимераза с корректурой, контроль качества белков, запас АТФ и способ гибели клетки, врождённое распознавание и контекст, иммунная толерантность, каскад свёртывания (усиление и тормоз), заживление и ниша стволовых клеток, старение клетки и рубцевание.
- `mechanisms/principles.yaml`: девятнадцать принципов-кандидатов (P-01…P-19) и идеи проверок.
- `scripts/analyze_interaction_graph.py`: самые связанные механизмы, механизмы без входов, выходов и связей, роли в учёте ресурсов, гипотезы, все циклы длиной до 6, петли усиления.
- Проверки в `scripts/validate_repository.py`: узлы графа равны реестру механизмов, основания связей существуют, PMID цитируется в карточке, петли усиления защищены `H-02`, структура карточек и принципов.

### Changed

- `README.md`, `docs/README.md`, `docs/TERMINOLOGY.md`: ссылки и статус документов раздела.

### Основание и ограничения

- Граф неполный и написан автором без независимой проверки; отсутствие связи не означает отсутствия зависимости. Полный перебор всех 7 021 пар механизмов и подтверждение каждой статьёй невозможны; полнота обеспечивается правилами по всем 119 механизмам (роль в учёте ресурсов, входы и выходы, циклы). Граф показал шесть механизмов без связей и несколько без входов или выходов, а также пробел стандарта: нет требования резервировать бюджет на корректное завершение (принцип P-07, гипотеза).
- Карточки опираются на рефераты статей PubMed, полные тексты не читались; карточка полимеразы опирается на один обзор. Проверка биологом не проводилась.
- Принципы и идеи проверок не являются требованиями.

## [1.3.1] - 2026-10-02

Patch-релиз: clarifications в informative-документах без изменения semantics. Требования, схемы, state machines, идентификаторы и реестры не менялись.

### Clarified

- `profiles/modular-monolith.md`: ткань — группа однотипных воркеров (клеток), а не воркеров или модулей; орган описан с SLO, владельцем и областью отказа (по глоссарию `docs/TERMINOLOGY.md`). В `profiles/modular-monolith.yaml` и таблице `REQ-CORE-20` орган — модуль с SLO и владельцем.
- `profiles/kubernetes-event-streaming.md` и `.yaml`: орган описан с областью отказа; `cordon` — операция над узлом, а не над pod (`REQ-CORE-14`).
- `diagrams/change-protocol.md`: «одобрено отдельным органом» заменено на «лицом или службой (authority)», чтобы не путать с органом DOA.
- `diagrams/cell-lifecycle.md`, `diagrams/apoptosis-flow.md`: некроз описан как аварийный отказ клетки, а fencing — как реакция на него.
- `diagrams/embodied-safety.md`: `proximity` описан без домысла «человек рядом».
- `README.md`: регенерация — воссоздание утраченного компонента из доверенного seed.
- `docs/README.md`: статусы `TERMINOLOGY.md` и `RELEASE_READINESS_v1.0.md` не утверждаются, так как не указаны в таблице статусов.

### Changed

- `scripts/validate_repository.py`: профиль отклоняется, если строка «Ткань» упоминает модули либо строка «Орган» не содержит SLO и владельца.
- Метаданные версии (`VERSION`, README, `CITATION.cff`, строка «Версия релиза» стандарта, `RELEASE_READINESS`) приведены к 1.3.1.

### Compatibility

- Claim по `1.0.x`–`1.3.0` остаются действительными: нормативные тексты и схемы не менялись.

### Основание и ограничения

Расхождения найдены сверкой собственных документов автора с глоссарием репозитория; независимой проверки смысла нет.

## [1.3.0] - 2026-10-02

Minor-релиз: два профиля внедрения (additive, informative). Новых требований, изменений идентификаторов `REQ-*`, схем и state machines нет. Идентификатор стандарта остаётся `DOA-FS-1.0`. Профили edge/robotics и air-gapped/high-assurance из плана 1.3 в релиз не вошли (см. `ROADMAP.md`).

### Added

- `profiles/README.md`: что такое профиль внедрения и чем он отличается от профиля соответствия.
- `profiles/modular-monolith.md` и `profiles/modular-monolith.yaml`: профиль внедрения для модульного монолита. Соответствие понятий DOA, риск общей судьбы, что реально можно заявить по каждому профилю соответствия, таблица из 29 требований (Core и Conditional) с подходом, пределом монолита и кейсами проверки, особенности проверки по Verification Kit, порядок внедрения.
- `profiles/kubernetes-event-streaming.md` и `profiles/kubernetes-event-streaming.yaml`: профиль внедрения для Kubernetes и потоков событий. Соответствие понятий DOA, риск общего кластера, что можно заявить по каждому профилю соответствия, таблица из 36 требований (Core, Distributed и Conditional) с подходом, пределом платформы и кейсами проверки, особенности проверки по Verification Kit, порядок внедрения.
- Проверки в `scripts/validate_repository.py`: покрытие требований каждым профилем, ссылки на кейсы плана, совпадение таблиц с реестрами профилей.

### Changed

- `README.md`, `docs/README.md`, `docs/TERMINOLOGY.md`, `ROADMAP.md`: ссылки и статус документов профилей.
- `scripts/validate_repository.py`: заголовок `[Unreleased]` в `CHANGELOG.md` допустим выше текущей версии.

### Compatibility

- Claim по `1.0.x`, `1.1.x` и `1.2.x` остаются действительными. Использование профилей необязательно, на claim они не влияют.

### Основание и ограничения

- Профили написаны без независимой реализации: ни одна система не построена и не проверена по ним, предложенные компенсации пределов платформ могут потребовать errata.
- Утверждения о возможностях Kubernetes и систем потоков записаны в общем виде и не сверялись с документацией конкретных версий.

## [1.2.0] - 2026-10-01

Minor-релиз: Verification Kit (additive, informative) и исправление двух нормативных формулировок из 1.1.0 по результатам review (см. Changed и Fixed). Новых требований, изменений идентификаторов `REQ-*` и state machines нет. Идентификатор стандарта остаётся `DOA-FS-1.0`.

### Added

- `docs/VERIFICATION_KIT.md` (informative): состав kit, порядок использования, правила безопасности прогона, ограничения.
- `verification/conformance-test-plan.yaml`: тестовые кейсы `TC-…` (49, по одному на каждое требование реестра) с процедурой, критериями прохождения, ожидаемым evidence, ссылками на сценарии и признаком изолированной среды.
- `verification/fault-scenarios.yaml`: 22 сценария отказа `FS-…` для клеток, органов, circulation и организма; раздел `coverage` сопоставляет каждый класс отказа `F-01`…`F-25` сценарию либо кейсу плана.
- `verification/otel-semantic-conventions.yaml`: 21 атрибут, 4 события и 14 метрик пространства `doa.*`; значения перечислений привязаны к схемам и реестрам; идентификаторы с неограниченной кардинальностью запрещены на метриках.
- `specifications/verification-report.schema.json` и `scripts/check_verification_report.py`: формат отчёта о прогоне и его проверка по плану и, с `--claim`, по conformance claim (противоречия отмечаются ошибкой, неполное покрытие — предупреждением). В схеме нет окружения production.
- `templates/DOA_THREAT_MODEL.md` и `templates/DOA_HAZARD_ANALYSIS.md`: шаблоны для evidence пакета (`REQ-CORE-14`, `REQ-CORE-23`, `REQ-CORE-24`, `REQ-EMB-01`…`REQ-EMB-06`).
- Примеры отчёта: valid `verification-report--reference.yaml`; invalid `verification-report--pass-without-evidence.yaml`, `verification-report--production-environment.yaml`.
- Необязательное поле claim `observed_accounting` (источник и неопределённость потребления, известного только из внешней телеметрии; `REQ-CORE-18`), шаблонный раздел, valid пример и invalid пример `conformance-claim--observed-accounting-without-uncertainty.yaml`.
- Проверки в `scripts/validate_repository.py`: покрытие требований кейсами, согласованность метода кейса с `verification` требования, ссылки сценариев на классы отказа и требования, полнота и двусторонняя согласованность покрытия классов отказа, правила именования и ссылки реестра `doa.*`, поведение проверки отчёта на искусственных нарушениях.

### Changed (нормативно)

Review формулировок 1.1.0 нашёл ослабление защиты и неточное утверждение о совместимости. Правки требуют review maintainer по `GOVERNANCE.md`, раздел 4.

- `REQ-CORE-22`: чужие credentials и сессии, найденные в восстановленном состоянии, MUST считаться непроверенными и MUST NOT использоваться, пока внешний статус не подтверждён. В 1.1.0 для чужих identities оставалась только необязательная проверка (SHOULD), и старая копия могла вернуть отозванный чужой доступ. Объявление чужих identities внешними зависимостями и их сопоставление со своей identity — SHOULD (в 1.1.0 объявление было MUST). Evidence расширено restore-тестом с чужими credentials. Описание — `docs/LIFECYCLE.md`, раздел 9; `docs/BOUNDARY_AND_IDENTITY.md`, раздел 8.
- `REQ-CORE-18`: запись observed accounting с источником и неопределённостью — SHOULD (в 1.1.0 было MUST). Запрет выдавать observed за reserved (MUST NOT) сохранён. Evidence: источник и неопределённость требуются, если observed-данные есть. Описание — `docs/METABOLISM.md`, раздел 1.
- `docs/TERMINOLOGY.md`, `docs/CONFORMANCE.md`, `README.md`, `ROADMAP.md`: ссылки и статус документов kit.

### Fixed

- Запись `[1.1.0]` утверждала, что ужесточений для существующих реализаций нет. Это было неточно: формулировки 1.1.0 содержали два новых MUST (объявление чужих identities внешними зависимостями в `REQ-CORE-22`, запись observed accounting в `REQ-CORE-18`), что по `GOVERNANCE.md` относится к ужесточению для профиля Core. Запись `[1.1.0]` как исторический документ не изменена; в 1.2.0 оба MUST заменены на SHOULD.
- `docs/METABOLISM.md` ссылался на поле claim для неопределённости observed accounting, которого не было; поле добавлено (`observed_accounting`).

### Compatibility

- Claim по `1.0.x` и `1.1.x` остаются действительными. Использование kit необязательно, схема `verification-report` на claim не влияет.
- Относительно 1.0.x обязательные правила не добавлены: для `REQ-CORE-22` запрет использовать непроверенные чужие credentials следует из запрета восстановления отозванного из устаревшего состояния; для `REQ-CORE-18` добавлен только запрет выдавать observed за reserved. Это суждение reviewer'а, а не независимая проверка.
- Claim с полем `observed_accounting` не проходит схему `1.1.x` и ранее (необязательное поле добавлено, `additionalProperties: false`).

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
