# Digital Organism Architecture (DOA)

**Version:** 1.0.1

**Standard identifier:** `DOA-FS-1.0`

**Status:** Foundational Standard (released)

**Date:** 2026-10-01

Digital Organism Architecture (DOA) — метаархитектурный стандарт для проектирования ИИ-систем как управляемых, наблюдаемых и восстанавливаемых цифровых организмов.

DOA не является приложением, agent framework, control plane или готовым runtime. `AI-Engineering-Control-Plane`, Cellular OS, Agent Harness, Autopilot Flywheel, LLM-сервисы и робототехнические комплексы могут быть реализациями или надстройками DOA, но не входят в сам стандарт.

## Что нормативно определяет DOA

- границы организма, trust boundaries, идентичность (включая continuity при замене компонентов), геном, эпигеном и происхождение состояния;
- клетки, ткани, органы и их специализацию;
- data, control, security, memory, metabolic и observability planes;
- гомеостаз (контуры, пороги, эскалация), иммунитет (полный жизненный цикл ответа), восстановление (restart ≠ restore ≠ repair ≠ regenerate), старение, безопасное завершение и ограничение роста;
- обучение и эволюцию только через управляемые контуры с проверкой и откатом;
- обязательный мэппинг каждого биологического механизма: responsibility → component → contract → protocol → invariant → failure mode → security/safety control → observability → evidence;
- машиночитаемые state machines, схемы контрактов и реестр требований соответствия;
- профили соответствия и минимальный комплект доказательств.

## Начало работы

1. Прочитайте [канонический стандарт](docs/DOA_STANDARD_v1.0.md).
2. Выберите профили и изучите требования в [CONFORMANCE.md](docs/CONFORMANCE.md).
3. Сопоставьте компоненты с [реестром Biology-to-IT](docs/BIOLOGY_TO_IT_MAPPING.md).
4. Определите границу организма: [BOUNDARY_AND_IDENTITY.md](docs/BOUNDARY_AND_IDENTITY.md).
5. Опишите организм через схемы из `specifications/` и сверьтесь с `reference/EXAMPLE_GENOME.yaml` и `reference/examples/`.
6. Проверьте reference architecture и наблюдаемые инварианты.

## Канонические документы

- `docs/DOA_STANDARD_v1.0.md` — нормативное ядро;
- `docs/TERMINOLOGY.md` — нормативный язык, статус документов, глоссарий;
- `docs/ARCHITECTURE.md` — слои, planes и архитектурные цепочки;
- `docs/BOUNDARY_AND_IDENTITY.md` — граница организма, identity, trust;
- `docs/LIFECYCLE.md` — state machines, старение, завершение;
- `docs/FAILURE_AND_RECOVERY.md` — таксономия восстановления, классы отказов, runaway growth;
- `docs/CONFORMANCE.md` — требования, evidence, статусы claim;
- `docs/IMPLEMENTATION_GUIDE.md` — как применять стандарт к control plane, навыкам для LLM и системам на стадии проектирования (informative);
- `docs/BIOLOGY_TO_IT_MAPPING.md` — каноническая матрица механизмов;
- `docs/SECURITY_AND_IMMUNITY.md` — доверие, иммунитет, карантин и apoptosis;
- `docs/HOMEOSTASIS.md` — измеримые контрольные циклы;
- `docs/MEMORY_AND_NERVOUS_SYSTEM.md` — cognition, reflexes, memory и learning;
- `docs/METABOLISM.md` — ingestion, compute, cost, detoxification и excretion;
- `docs/GENOME_AND_EVOLUTION.md` — signed desired state, expression и controlled evolution;
- `docs/ROBOTICS_EXTENSION.md` — физическая безопасность и real-time профиль;
- `CHANGES_AND_NEW_FINDINGS.md` — история находок и изменений относительно исходной концепции.

## Проверка и соответствие

Локальная проверка структуры, schemas, примеров (valid и invalid), state machines, матрицы, реестра требований, ссылок и диаграмм:

```bash
python -m pip install -r requirements-validation.txt
python scripts/validate_repository.py
```

Реализация DOA публикует отдельный claim по шаблону `templates/DOA_CONFORMANCE_CLAIM.md` и проверяет его командой `python scripts/check_conformance_claim.py claim.yaml`. Наличие термина DOA в документации без evidence pack не означает соответствие.

Правила изменений определены в `CONTRIBUTING.md`, модель принятия решений — в `GOVERNANCE.md`, порядок сообщения об уязвимостях — в `SECURITY.md`.

## Нормативный язык

Ключевые слова **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT** и **MAY** используются в смысле RFC 2119/RFC 8174. Биологическая аналогия сама по себе не создаёт соответствия DOA: нужен исполняемый или проверяемый цифровой механизм.

## Лицензия

Apache License 2.0. См. [LICENSE](LICENSE).
