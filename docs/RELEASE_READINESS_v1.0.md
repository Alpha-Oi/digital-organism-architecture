# DOA v1.0.0 Release Readiness

**Target:** `DOA-FS-1.0`, release `v1.0.0`

**Status:** `ГОТОВО`

Этот документ фиксирует критерии выпуска и результат локальной оценки на release commit. Результаты, зависящие от внешних систем GitHub (запуск workflow на release commit, tag, GitHub Release, защита `main`), фиксируются в GitHub Release и в истории workflow, а не в замороженном документе.

## Release criteria

| Gate | Статус | Evidence |
|---|---|---|
| Canonical standard и supporting documents | PASS | обязательные файлы проверяются `scripts/validate_repository.py` |
| JSON Schemas (14) | PASS | `Draft202012Validator.check_schema`; `$id` соответствует имени файла |
| Примеры | PASS | `reference/EXAMPLE_GENOME.yaml` и 13 valid примеров проходят; 16 invalid примеров отклоняются схемами |
| State machines | PASS | `state-machines.yaml` согласован со схемами, диаграммами и `docs/LIFECYCLE.md`; достижимость и завершимость состояний проверены |
| Biology-to-IT матрица | PASS | 12 колонок заполнены у каждой из 119 строк; каждая нормативная строка связана с требованием |
| Реестр требований и claim checker | PASS | `specifications/requirements.yaml`, `scripts/check_conformance_claim.py`, самопроверка в валидаторе |
| Ссылки, таблицы, Mermaid, cross-references | PASS | `scripts/validate_repository.py` |
| Единая версия | PASS | `VERSION`, README, стандарт, CHANGELOG, `RELEASE_READINESS` |
| Whitespace | PASS | `git diff --check` |
| License, changelog, governance, security, contributing | PASS | Apache-2.0, `CHANGELOG.md`, `GOVERNANCE.md`, `SECURITY.md`, `CONTRIBUTING.md` |
| Validation workflow | PASS | `.github/workflows/validate.yml`: `contents: read`, запуск на `main`, pull request и tags `v*`, проверка tag = `VERSION` |

## Внешние условия выпуска

Выполняются на стороне GitHub и подтверждаются перед объявлением релиза:

1. успешный запуск workflow `Validate DOA standard` на release commit;
2. tag `v1.0.0` указывает на этот commit;
3. GitHub Release `v1.0.0` создан из этого tag;
4. защита `main` с обязательным status check `validate` (рекомендуемая конфигурация — `GOVERNANCE.md`, раздел 5).

## Accepted risks

- Внешний peer review биологических соответствий не проводился; это не заменяется self-review.
- GitHub Actions используют major tags (`actions/checkout@v5`, `actions/setup-python@v6`), а не immutable commit SHA; workflow ограничен `contents: read`.
- DOA v1.0 определяет contracts и conformance evidence, но не имеет опубликованного claim от независимой реализации.
- Числовые значения в HOMEOSTASIS.md — иллюстративные defaults, а не требования.

## Not applicable

- Runtime deployment, production data migration и rollback приложения отсутствуют: репозиторий содержит стандарт и schemas.
- Performance benchmark не является release gate для документационного стандарта.

## Reassessment rule

Любое normative изменение после этой оценки требует новой версии и повторного полного прогона validation.

## Patch-релиз v1.0.1

`v1.0.1` содержит только clarifications: новый informative документ `docs/IMPLEMENTATION_GUIDE.md` и ссылки на него; нормативные тексты, схемы и скрипты проверки не менялись, кроме добавления файла в список обязательных. Критерии выше проверяются тем же `scripts/validate_repository.py`.

Внешние условия выпуска те же: успешный запуск workflow `Validate DOA standard` на release commit, tag `v1.0.1` на этом commit и GitHub Release из него. Tag создаёт владелец репозитория.

Уточнение к разделу Accepted risks: строка про major tags GitHub Actions относилась к `v1.0.0`; с PR #1 actions закреплены на commit SHA, и валидатор это проверяет.

## Release v1.1.0

`v1.1.0` — minor-релиз с additive изменениями conformance-контракта и двумя нормативными уточнениями (`REQ-CORE-18`, `REQ-CORE-22`); полный список и анализ совместимости — в `CHANGELOG.md`, раздел `[1.1.0]`. Критерии выше проверяются тем же `scripts/validate_repository.py`; для новых артефактов добавлены проверки: реестр `specifications/failure-classes.yaml` против таблицы `FAILURE_AND_RECOVERY.md`, определения статусов требования в `CONFORMANCE.md`, поведение `check_conformance_claim.py` для `DESIGNED`, `failure_classes` и предупреждений, valid/invalid примеры claim.

Для review normative diff (`GOVERNANCE.md`, раздел 5) значимы: `specifications/conformance-claim.schema.json`, `specifications/requirements.yaml` (формулировки `REQ-CORE-18`, `REQ-CORE-22`, evidence `REQ-CORE-23`), `specifications/failure-classes.yaml`, `docs/CONFORMANCE.md`, `docs/FAILURE_AND_RECOVERY.md`, `docs/LIFECYCLE.md`, `docs/METABOLISM.md`.

Внешние условия выпуска: успешный запуск workflow `Validate DOA standard` на release commit, tag `v1.1.0` на этом commit и GitHub Release из него. Tag создаёт владелец репозитория.

## Release v1.2.0

`v1.2.0` — minor-релиз Verification Kit: additive и informative артефакты (`docs/VERIFICATION_KIT.md`, `verification/*`, схема и проверка отчёта, два шаблона); нормативные тексты, реестр требований и существующие схемы не менялись, полный список и анализ совместимости — в `CHANGELOG.md`, раздел `[1.2.0]`. Критерии выше проверяются тем же `scripts/validate_repository.py`; для kit добавлены проверки покрытия требований кейсами, покрытия классов отказа сценариями, реестра `doa.*` и поведения проверки отчёта.

Для review значимы: согласованность `verification/*` с `specifications/requirements.yaml` и `specifications/failure-classes.yaml`, правила безопасности прогона (`docs/VERIFICATION_KIT.md`, разделы 2 и 4), формулировки ограничений. Accepted risks этого релиза: независимая реализация не выполняла kit, а реестр `doa.*` не проверялся инструментами OpenTelemetry.

Внешние условия выпуска: успешный запуск workflow `Validate DOA standard` на release commit, tag `v1.2.0` на этом commit и GitHub Release из него. Tag создаёт владелец репозитория.
