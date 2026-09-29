# DOA v1.0 Release Readiness

**Assessment date:** 2026-09-29

**Target:** `DOA-FS-1.0` in `main`

**Status:** `УСЛОВНО ГОТОВО`

## Release criteria

| Gate | Status | Evidence |
|---|---|---|
| Canonical standard and supporting documents | PASS | required repository structure present |
| JSON Schema validity | PASS | 6 schemas accepted by `Draft202012Validator.check_schema` |
| Example genome | PASS | YAML parses and validates against `genome.schema.json` |
| Biology-to-IT contract coverage | PASS | mapping table has required fields and coverage floor |
| Local links and Mermaid containers | PASS | `scripts/validate_repository.py` |
| Whitespace integrity | PASS | `git diff --check` |
| License and changelog | PASS | Apache-2.0 and `CHANGELOG.md` present |
| Governance and conformance process | PASS | `GOVERNANCE.md`, `CONTRIBUTING.md`, claim template |
| Remote GitHub Actions run | NOT_RUN | workflow must run after publication |
| `main` branch protection | NOT_CONFIGURED | external repository setting |
| Owner approval for tag/release | PENDING | tag and GitHub Release require explicit decision |

## Blocking before `v1.0.0`

1. Опубликовать validation workflow и получить успешный remote run.
2. Принять решение по защите `main` и required status check.
3. Получить явное разрешение владельца на tag `v1.0.0` и GitHub Release.

## Accepted risks

- Внешняя peer review биологических соответствий ещё не проведена; это не скрывается и не заменяется self-review.
- GitHub Actions используют поддерживаемые major tags `actions/checkout@v4` и `actions/setup-python@v5`, а не immutable commit SHA. Workflow ограничен `contents: read`.
- DOA v1.0 определяет contracts и conformance evidence, но пока не имеет опубликованного claim от независимой реализации.

## Not applicable

- Runtime deployment, production data migration и rollback приложения отсутствуют: репозиторий содержит стандарт и schemas.
- Performance benchmark не является release gate для документационного стандарта.

## Reassessment rule

Статус может стать `ГОТОВО` только после успешного remote workflow и фиксации решения по branch protection. Любое normative изменение после оценки требует повторного полного прогона.
