<div align="center">

# Digital Organism Architecture (DOA)

**Метаархитектурный стандарт для ИИ-систем, которые должны быть управляемыми, наблюдаемыми и восстанавливаемыми.**

[![Validate](https://github.com/Alpha-Oi/digital-organism-architecture/actions/workflows/validate.yml/badge.svg)](https://github.com/Alpha-Oi/digital-organism-architecture/actions/workflows/validate.yml)
[![License: Apache 2.0](https://img.shields.io/github/license/Alpha-Oi/digital-organism-architecture)](LICENSE)
![Standard](https://img.shields.io/badge/standard-DOA--FS--1.0-2ea44f)

[Начать](#с-чего-начать) · [Быстрый старт](#быстрый-старт) · [Как применить](#как-применить-стандарт) · [Состав репозитория](#состав-репозитория) · [Участие](#участие)

</div>

**Version:** 1.5.0

**Standard identifier:** `DOA-FS-1.0`

**Status:** Foundational Standard (released)

**Release notes:** [CHANGELOG.md](CHANGELOG.md) (v1.5.0: в раздел «механизмы» добавлен кластер «кровообращение и регуляция» (4 карточки, принципы P-28…P-36); v1.4.0: раздел «механизмы» — карточки биологических механизмов, граф связей и принципы; v1.3.1: исправлены описания понятий в профилях и диаграммах; v1.3.0: профили внедрения — модульный монолит и Kubernetes с потоками событий)

**Date:** 2026-10-02

> **In short (English).** DOA is a meta-architecture standard that describes an AI system as a *digital organism*: a signed genome (desired state), isolated cells, a lifecycle, homeostasis, an immune response, recovery and bounded termination. It gives you 49 testable requirements, 15 JSON Schemas, 5 canonical state machines, a conformance-claim process and a Verification Kit. It is a specification, not a runtime or a framework. Most documents are written in Russian with English technical terms.

## Что это

Digital Organism Architecture (DOA) — метаархитектурный стандарт. Он описывает ИИ-систему (агентов, инструменты, модели, данные, а при необходимости и физические устройства) как **цифровой организм**: у него есть граница, идентичность, жизненный цикл, механизмы самозащиты и восстановления, ограниченный рост и безопасное завершение.

Биология здесь не украшение, а способ дать каждому механизму ответственность, контракт и способ проверки. Аналогия сама по себе ничего не доказывает: механизм засчитывается, только если у него есть проверяемое цифровое воплощение и evidence (доказательство, которое можно воспроизвести).

| Биологический механизм | Что это в цифровой системе | Где описано |
|---|---|---|
| Геном | подписанное декларативное описание желаемого состояния | [`GENOME_AND_EVOLUTION.md`](docs/GENOME_AND_EVOLUTION.md) |
| Клетка | минимальная изолируемая единица исполнения; агент — клетка | [`LIFECYCLE.md`](docs/LIFECYCLE.md) |
| Гомеостаз | замкнутые контуры регулирования с порогами, эскалацией и ручным отключением | [`HOMEOSTASIS.md`](docs/HOMEOSTASIS.md) |
| Иммунитет | обнаружение, карантин без согласия нарушителя, обновление защит | [`SECURITY_AND_IMMUNITY.md`](docs/SECURITY_AND_IMMUNITY.md) |
| Регенерация | воссоздание утраченного компонента из доверенного seed, а не копирование повреждённого состояния | [`FAILURE_AND_RECOVERY.md`](docs/FAILURE_AND_RECOVERY.md) |
| Апоптоз | ограниченное по времени и шагам завершение без остаточных прав | [`LIFECYCLE.md`](docs/LIFECYCLE.md) |

## Для кого

| Вы | Что вам даёт DOA | С чего начать |
|---|---|---|
| Архитектор ИИ-системы | общий язык и обязательные механизмы: границы, права, восстановление, ограничение роста | [стандарт](docs/DOA_STANDARD_v1.0.md), [архитектура](docs/ARCHITECTURE.md) |
| Владелец реализации | список требований и способ честно показать, что выполнено | [руководство по применению](docs/IMPLEMENTATION_GUIDE.md), [шаблон claim](templates/DOA_CONFORMANCE_CLAIM.md) |
| Инженер по надёжности или QA | кейсы проверки, сценарии отказа, формат отчёта | [Verification Kit](docs/VERIFICATION_KIT.md) |
| Специалист по безопасности | модель доверия, иммунный ответ, шаблон threat model | [безопасность](docs/SECURITY_AND_IMMUNITY.md), [шаблон](templates/DOA_THREAT_MODEL.md) |
| Разработчик робототехники | физическая безопасность, real-time бюджет, hazard analysis | [расширение](docs/ROBOTICS_EXTENSION.md), [шаблон](templates/DOA_HAZARD_ANALYSIS.md) |
| Контрибьютор | правила изменений и модель решений | [CONTRIBUTING.md](CONTRIBUTING.md), [GOVERNANCE.md](GOVERNANCE.md) |

## Чем DOA не является

DOA не приложение, не agent framework, не control plane и не готовый runtime. `AI-Engineering-Control-Plane`, Cellular OS, Agent Harness, Autopilot Flywheel, LLM-сервисы и робототехнические комплексы могут быть реализациями или надстройками DOA, но не входят в сам стандарт. DOA не заменяет отраслевую функциональную безопасность, regulation и вашу методику моделирования угроз, и не сертифицирует реализации.

## Что определяет стандарт

- границы организма, trust boundaries (границы доверия), идентичность и её непрерывность при замене компонентов, геном и эпигеном (временные подписанные настройки, не повышающие права);
- клетки, ткани и органы, их специализацию и failure domains (области, в которых отказ не должен распространяться);
- гомеостаз, иммунитет с полным жизненным циклом ответа, восстановление (`RESTART` ≠ `RESTORE` ≠ `REPAIR` ≠ `REGENERATE`), старение, безопасное завершение и ограничение роста;
- обучение и эволюцию только через управляемые контуры с проверкой и откатом;
- каноническую матрицу из 119 механизмов Biology-to-IT, 25 классов отказа, 5 машин состояний, 15 схем контрактов и 49 проверяемых требований;
- профили соответствия и минимальный комплект доказательств.

## С чего начать

1. Прочитайте [канонический стандарт](docs/DOA_STANDARD_v1.0.md): конституционные инварианты и сущности.
2. Откройте [указатель документации](docs/README.md): там пути чтения для разных ролей.
3. Определите границу организма: [BOUNDARY_AND_IDENTITY.md](docs/BOUNDARY_AND_IDENTITY.md).
4. Выберите профили и изучите требования: [CONFORMANCE.md](docs/CONFORMANCE.md).
5. Опишите организм схемами из [`specifications/`](specifications/) и сверьтесь с [`reference/EXAMPLE_GENOME.yaml`](reference/EXAMPLE_GENOME.yaml).

## Быстрый старт

Нужны Python 3.12 (версия, на которой работает CI) и `pip`. Скрипты проверки только читают файлы репозитория и ничего в нём не изменяют; единственное исключение — `scripts/new_card.py`, он создаёт заготовку карточки в `mechanisms/` (см. [`mechanisms/README.md`](mechanisms/README.md)).

```bash
git clone https://github.com/Alpha-Oi/digital-organism-architecture.git
cd digital-organism-architecture
python -m pip install -r requirements-validation.txt

# проверить сам стандарт: схемы, примеры, машины состояний, реестры, ссылки
python scripts/validate_repository.py

# проверить пример conformance claim
python scripts/check_conformance_claim.py reference/examples/valid/conformance-claim--reference.yaml

# проверить пример отчёта о прогоне Verification Kit
python scripts/check_verification_report.py reference/examples/valid/verification-report--reference.yaml
```

Каждая команда печатает `PASS` или список ошибок. Первая проверяет сам стандарт, две других показывают, как выглядят проверяемые материалы реализации.

## Как применить стандарт

1. **Выберите профили.** `Core` обязателен всегда. Остальные добавляйте по необходимости.
2. **Опишите организм.** Геном (`genome`), органы, клетки, права и ресурсы по схемам из `specifications/`.
3. **Сопоставьте с реестром.** Для каждого требования укажите, где оно реализовано, и приложите evidence.
4. **Проверьте себя.** Используйте кейсы и сценарии [Verification Kit](docs/VERIFICATION_KIT.md) в изолированной или staging-среде, никогда на production.
5. **Оформите claim.** Заполните [шаблон](templates/DOA_CONFORMANCE_CLAIM.md) и проверьте командой `check_conformance_claim.py`. Честные статусы (`PASS`, `PARTIAL`, `DESIGNED`, `FAIL`) ценнее красивого общего ответа.

Профили соответствия:

| Профиль | Что добавляет |
|---|---|
| Core | идентичность, граница, геном, жизненный цикл, гомеостаз, иммунитет, учёт ресурсов, память, наблюдаемость, восстановление, старение, завершение |
| Distributed | контракт событий, частичные отказы, топология, кворум и failover, часы, дрейф, катастрофическое восстановление |
| Adaptive | управляемое обучение и эволюция, обнаружение дрейфа, происхождение вариантов |
| Embodied | физическая безопасность, real-time бюджет, калибровка, ограничения исполнителей, сброс блокировки |
| Conditional | контроль воспроизводства, федерации и обмена между линиями — либо их явный запрет |

Формулировка «реализует DOA Profile X (claim: ссылка)» допустима. Формулировки «DOA-compliant» и «DOA-certified» без ссылки на claim со статусом `VERIFIED` запрещены.

## Состав репозитория

```text
docs/            нормативные и информационные документы стандарта
specifications/  схемы контрактов, машины состояний, реестры требований и классов отказа
reference/       эталонный геном, эталонная архитектура, примеры valid и invalid
verification/    тестовый план, сценарии отказа, конвенции OpenTelemetry doa.*
profiles/        профили внедрения: как выполнить требования в конкретной архитектуре
mechanisms/      карточки биологических механизмов, граф связей между механизмами и принципы (пилот)
templates/       шаблоны claim, threat model и hazard analysis
diagrams/        диаграммы Mermaid, производные от машин состояний
scripts/         проверка стандарта, claim и отчётов; анализ графа механизмов; заготовка карточки
tests/           автотесты валидатора и scripts/new_card.py
.github/         CI, шаблоны issue и pull request, Dependabot
```

Ключевые документы:

- [`docs/DOA_STANDARD_v1.0.md`](docs/DOA_STANDARD_v1.0.md) — нормативное ядро;
- [`docs/CONFORMANCE.md`](docs/CONFORMANCE.md) — требования, evidence, статусы claim;
- [`docs/BIOLOGY_TO_IT_MAPPING.md`](docs/BIOLOGY_TO_IT_MAPPING.md) — каноническая матрица механизмов;
- [`docs/FAILURE_AND_RECOVERY.md`](docs/FAILURE_AND_RECOVERY.md) — таксономия восстановления и классы отказа;
- [`docs/IMPLEMENTATION_GUIDE.md`](docs/IMPLEMENTATION_GUIDE.md) — руководство по применению (informative);
- [`docs/VERIFICATION_KIT.md`](docs/VERIFICATION_KIT.md) — как получать и показывать evidence (informative);
- [`mechanisms/README.md`](mechanisms/README.md) — как устроены биологические механизмы и как они связаны между собой (informative, пилот);
- [`profiles/README.md`](profiles/README.md) — профили внедрения; [модульный монолит](profiles/modular-monolith.md) и [Kubernetes с потоками событий](profiles/kubernetes-event-streaming.md) (informative);
- [`docs/TERMINOLOGY.md`](docs/TERMINOLOGY.md) — нормативный язык, статус документов, глоссарий.

Полный перечень с порядком чтения — в [`docs/README.md`](docs/README.md).

## Версии и дорожная карта

Версионирование — SemVer, правила совместимости — в [GOVERNANCE.md](GOVERNANCE.md). История изменений — [CHANGELOG.md](CHANGELOG.md), планы — [ROADMAP.md](ROADMAP.md). Ближайший пункт — профили внедрения (1.3); крупная версия 2.0 возможна только после двух независимых реализаций.

## Участие

Приветствуются уточнения, найденные пробелы и отчёты о применении стандарта.

- Нашли пробел или неоднозначность: откройте issue по форме [Standard gap](https://github.com/Alpha-Oi/digital-organism-architecture/issues/new/choose).
- Применили DOA: расскажите, что получилось и что нет (форма «Application report»). Такие отчёты нужны для версии 2.0.
- Хотите внести изменение: прочитайте [CONTRIBUTING.md](CONTRIBUTING.md) и [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
- Вопросы: [SUPPORT.md](SUPPORT.md).
- Уязвимости и обход safety controls не публикуйте в issue: [SECURITY.md](SECURITY.md).

## Нормативный язык

Ключевые слова **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT** и **MAY** используются в смысле RFC 2119/RFC 8174. Биологическая аналогия сама по себе не создаёт соответствия DOA: нужен исполняемый или проверяемый цифровой механизм.

## Цитирование

Для ссылки на стандарт используйте [CITATION.cff](CITATION.cff): GitHub покажет кнопку «Cite this repository».

## Лицензия

Apache License 2.0. См. [LICENSE](LICENSE).
