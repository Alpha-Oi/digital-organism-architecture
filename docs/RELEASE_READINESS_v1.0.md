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
