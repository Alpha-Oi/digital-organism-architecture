# Digital Organism Architecture (DOA)

**Version:** 1.0

**Status:** Foundational Standard

**Date:** 2026-09-29

Digital Organism Architecture (DOA) — метаархитектурный стандарт для проектирования ИИ-систем как управляемых, наблюдаемых и восстанавливаемых цифровых организмов.

DOA не является приложением, agent framework, control plane или готовым runtime. `AI-Engineering-Control-Plane`, Cellular OS, Agent Harness, Autopilot Flywheel, LLM-сервисы и робототехнические комплексы могут быть реализациями или надстройками DOA, но не входят в сам стандарт.

## Что нормативно определяет DOA

- границы организма, идентичность, геном, эпигеном и происхождение состояния;
- клетки, ткани, органы и их специализацию;
- data, control, security, memory, metabolic и observability planes;
- гомеостаз, иммунитет, регенерацию, старение и безопасное завершение;
- обучение и эволюцию только через управляемые контуры с проверкой и откатом;
- обязательный мэппинг каждого биологического механизма в цифровой контракт, протокол, инвариант наблюдаемости, отказ и security control;
- уровни соответствия и минимальный комплект доказательств.

## Начало работы

1. Прочитайте [канонический стандарт](docs/DOA_STANDARD_v1.0.md).
2. Выберите conformance profile в [PRINCIPLES.md](docs/PRINCIPLES.md).
3. Сопоставьте компоненты с [реестром Biology-to-IT](docs/BIOLOGY_TO_IT_MAPPING.md).
4. Опишите организм через схемы из `specifications/`.
5. Проверьте reference architecture и наблюдаемые инварианты.

## Канонические документы

- `docs/DOA_STANDARD_v1.0.md` — нормативное ядро;
- `docs/ARCHITECTURE.md` — слои и planes;
- `docs/BIOLOGY_TO_IT_MAPPING.md` — строгий реестр механизмов;
- `docs/SECURITY_AND_IMMUNITY.md` — доверие, иммунитет, карантин и apoptosis;
- `docs/HOMEOSTASIS.md` — измеримые контрольные циклы;
- `docs/MEMORY_AND_NERVOUS_SYSTEM.md` — cognition, reflexes, memory и learning;
- `docs/METABOLISM.md` — ingestion, compute, cost, detoxification и excretion;
- `docs/GENOME_AND_EVOLUTION.md` — signed desired state, expression и controlled evolution;
- `docs/ROBOTICS_EXTENSION.md` — физическая безопасность и real-time профиль;
- `CHANGES_AND_NEW_FINDINGS.md` — отличия от исходного draft и новые находки.

## Нормативный язык

Ключевые слова **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT** и **MAY** используются в смысле RFC 2119/RFC 8174. Биологическая аналогия сама по себе не создаёт соответствия DOA: нужен исполняемый или проверяемый цифровой механизм.

## Лицензия

Apache License 2.0. См. [LICENSE](LICENSE).
