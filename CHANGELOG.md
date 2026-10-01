# Changelog

Все существенные изменения стандарта документируются здесь. Формат версий — SemVer; политика совместимости — `GOVERNANCE.md`.

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
