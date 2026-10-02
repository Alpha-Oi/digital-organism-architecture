# Terminology and Normative Status

**Версия:** DOA v1.0 (`DOA-FS-1.0`).

## 1. Нормативный язык

Ключевые слова **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, **MAY** (заглавными буквами) используются в смысле RFC 2119 / RFC 8174. Строчные «должен», «может» в нормативных документах трактуются как пояснение, а не требование.

## 2. Нормативный статус документов

| Документ / артефакт | Статус | Примечание |
|---|---|---|
| `docs/DOA_STANDARD_v1.0.md` | Normative | конституционные инварианты, сущности, профили |
| `specifications/*.schema.json`, `state-machines.yaml`, `requirements.yaml`, `failure-classes.yaml` | Normative | точные data contracts, state machines и реестр требований |
| `docs/BIOLOGY_TO_IT_MAPPING.md` | Normative (по колонке `Profile`) | `Core`/профильные строки — MUST; `Pattern` — SHOULD/MAY; `Anti-pattern` — запрещённое поведение с обязательным контролем |
| `docs/ARCHITECTURE.md`, `BOUNDARY_AND_IDENTITY.md`, `LIFECYCLE.md`, `FAILURE_AND_RECOVERY.md`, `SECURITY_AND_IMMUNITY.md`, `HOMEOSTASIS.md`, `MEMORY_AND_NERVOUS_SYSTEM.md`, `METABOLISM.md`, `GENOME_AND_EVOLUTION.md` | Normative | детализация Core/Distributed/Adaptive; ключевые слова определяют уровень |
| `docs/ROBOTICS_EXTENSION.md` | Normative для Embodied Profile; Optional extension для остальных | не обязателен, если Embodied не заявлен |
| `docs/CONFORMANCE.md`, `templates/DOA_CONFORMANCE_CLAIM.md` | Normative (процесс claim) | правила статусов и evidence |
| `docs/PRINCIPLES.md` | Informative | обоснование; требования выражены в нормативных документах |
| `docs/IMPLEMENTATION_GUIDE.md` | Informative | руководство по применению; не вводит требований, при противоречии действует нормативный документ |
| `docs/VERIFICATION_KIT.md`, `verification/*`, `specifications/verification-report.schema.json`, `scripts/check_verification_report.py`, `templates/DOA_THREAT_MODEL.md`, `templates/DOA_HAZARD_ANALYSIS.md` | Informative | Verification Kit: помогает получить evidence, не вводит требований; при противоречии действуют нормативные документы |
| `profiles/*` | Informative | профили внедрения: показывают, как выполнить требования в конкретной архитектуре; не вводят требований и не меняют правила claim |
| `docs/SOURCES.md`, `CHANGES_AND_NEW_FINDINGS.md`, `ROADMAP.md`, `CHANGELOG.md` | Informative | история, источники, планы |
| `reference/*` (architecture, stack, example genome, examples) | Non-normative implementation examples | не обязательны; примеры MUST оставаться валидными по схемам |
| `diagrams/*` | Informative, производные | рёбра state-диаграмм MUST совпадать с `state-machines.yaml` |
| `GOVERNANCE.md`, `CONTRIBUTING.md`, `SECURITY.md` | Normative для процесса репозитория | не накладывают требований на реализации |

## 3. Приоритет при противоречии

Противоречие между документами является дефектом стандарта и исправляется errata. До исправления действует порядок:

1. конституционные инварианты `DOA_STANDARD_v1.0.md` (раздел 4);
2. машиночитаемые спецификации (`specifications/`);
3. тематические нормативные документы;
4. `BIOLOGY_TO_IT_MAPPING.md` (описательные ячейки);
5. informative и non-normative материалы (никогда не переопределяют вышестоящие).

## 4. Глоссарий канонических терминов

Одна сущность имеет одно каноническое имя. Синонимы указаны для распознавания и не должны использоваться как отдельные сущности.

| Канонический термин | Определение | Не использовать как синоним |
|---|---|---|
| Organism | версионируемая система под одним identity root, genome и policy authority | «приложение», «сервис», «агент» |
| Organ | подсистема с SLO, owner, интерфейсом и failure domain | «сервис», «модуль» (без контракта) |
| Tissue | группа однотипных клеток с общей политикой | «пул», «кластер» (как сущность DOA) |
| Cell | минимальная независимо изолируемая runtime-единица; агент — клетка когнитивной ткани | «процесс», «worker» (как нормативный термин) |
| Genome | подписанный декларативный desired state | «конфиг» |
| Epigenome / PolicyOverlay | временные подписанные overlays, не повышающие authority | «feature flag» (как нормативный термин) |
| Phenotype | наблюдаемое runtime-поведение | — |
| Signal | адресное/широковещательное сообщение с provenance, TTL и schema | — |
| HormoneSignal | контракт `hormone.schema.json`; в `DOA_STANDARD` §6.3 именуется HomeostaticSignal — это один и тот же объект | «Hormone», «Homeostatic signal» как два типа |
| ControlLoopSpec | декларация контура гомеостаза (`control-loop.schema.json`) | «alert rule» |
| CapabilityGrant | узкое, истекающее, отзываемое право (`capability-grant.schema.json`) | «permission» без срока |
| MemoryRecord | управляемая запись памяти (`memory-record.schema.json`) | — |
| HealthEvidence | startup/readiness/liveness/correctness/freshness (`health-evidence.schema.json`) | «health check» (если только liveness) |
| Incident | жизненный цикл иммунного ответа (машина `incident`) | «quarantine protocol» (это один из шагов) |
| Immune event | наблюдение о нарушении доверия, целостности или policy; вход в incident | — |
| Quarantine | изоляция субъекта с сохранением evidence; шаг `QUARANTINED` incident machine | — |
| Apoptosis | контролируемое завершение клетки (`TERMINATING`) | «kill», «delete» |
| Necrosis | неконтролируемый отказ клетки (`FAILED`) с обязательным fencing | «crash» без fencing |
| Senescence | ограниченное reduced-privilege состояние старения (`SENESCENT`) | «deprecated» без ограничений |
| Regeneration | воссоздание утраченного компонента из trusted seed | «restart», «restore» |
| Recovery mode | один из `RESTART`, `RESTORE`, `REPAIR`, `REPLACE`, `REGENERATE`, `REBUILD`, `RECONFIGURE`, `ROLLBACK` | — |
| Symbiont | допущенный guest (plugin/tool/agent) с quota и revocation | «integration», «extension» без контракта |
| Treaty | контракт между организмами | «integration agreement» |
| Lease | истекающее право существования клетки/endpoint | — |
| Epoch | монотонный номер членства/восстановления для fencing | «version» |
| Tombstone | подписанная запись о завершённой сущности (anti-resurrection) | — |
| Learning | изменение declared adaptive parameters внутри bounds | «evolution» |
| Evolution | изменение genome (change class=evolution) | «learning» |
| Profile | Core, Distributed, Adaptive, Embodied, Conditional | — |
| Evidence pack | набор артефактов, на которые ссылается claim | — |
| Conformance claim | заявление реализации с evidence (`conformance-claim.schema.json`) | «сертификат» |

## 5. Версионирование идентификаторов

- Стандарт: `DOA v1.0`, идентификатор `DOA-FS-1.0`, релиз `v1.0.0` (файл `VERSION`).
- Схемы: `$id` под `https://doa-standard.org/schemas/`; изменения схем следуют политике совместимости `GOVERNANCE.md`.
- Идентификаторы механизмов (`C-01`, …) и требований (`REQ-…`) стабильны: удаление требует major-версии, добавление — minor.
