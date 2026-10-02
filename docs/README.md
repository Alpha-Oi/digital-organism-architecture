# Указатель документации DOA

Здесь собраны все документы стандарта с порядком чтения. Главная страница репозитория — [README.md](../README.md). Статус документа (нормативный или информационный) определяет [TERMINOLOGY.md](TERMINOLOGY.md), раздел 2: при противоречии действуют нормативные документы.

## Пути чтения

| Если вам нужно | Читайте по порядку |
|---|---|
| Понять идею за 30 минут | [PRINCIPLES.md](PRINCIPLES.md), [DOA_STANDARD_v1.0.md](DOA_STANDARD_v1.0.md) разделы 1–6, [ARCHITECTURE.md](ARCHITECTURE.md) |
| Применить стандарт к своей системе | [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md), [BOUNDARY_AND_IDENTITY.md](BOUNDARY_AND_IDENTITY.md), [CONFORMANCE.md](CONFORMANCE.md), [шаблон claim](../templates/DOA_CONFORMANCE_CLAIM.md) |
| Проверить реализацию | [VERIFICATION_KIT.md](VERIFICATION_KIT.md), [FAILURE_AND_RECOVERY.md](FAILURE_AND_RECOVERY.md), [CONFORMANCE.md](CONFORMANCE.md) раздел 4 |
| Оценить безопасность | [SECURITY_AND_IMMUNITY.md](SECURITY_AND_IMMUNITY.md), [BOUNDARY_AND_IDENTITY.md](BOUNDARY_AND_IDENTITY.md), [шаблон threat model](../templates/DOA_THREAT_MODEL.md) |
| Работать с физическими системами | [ROBOTICS_EXTENSION.md](ROBOTICS_EXTENSION.md), [LIFECYCLE.md](LIFECYCLE.md) раздел 10, [шаблон hazard analysis](../templates/DOA_HAZARD_ANALYSIS.md) |
| Предложить изменение стандарта | [CONTRIBUTING.md](../CONTRIBUTING.md), [GOVERNANCE.md](../GOVERNANCE.md), [BIOLOGY_TO_IT_MAPPING.md](BIOLOGY_TO_IT_MAPPING.md) |

## Все документы

| Документ | Статус | О чём |
|---|---|---|
| [DOA_STANDARD_v1.0.md](DOA_STANDARD_v1.0.md) | Normative | конституционные инварианты, сущности, профили |
| [TERMINOLOGY.md](TERMINOLOGY.md) | Normative | нормативный язык, статус документов, глоссарий |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Normative | слои, planes, архитектурные цепочки |
| [BOUNDARY_AND_IDENTITY.md](BOUNDARY_AND_IDENTITY.md) | Normative | граница организма, идентичность, доверие |
| [LIFECYCLE.md](LIFECYCLE.md) | Normative | машины состояний, старение, завершение |
| [FAILURE_AND_RECOVERY.md](FAILURE_AND_RECOVERY.md) | Normative | режимы восстановления, 25 классов отказа, ограничение роста |
| [SECURITY_AND_IMMUNITY.md](SECURITY_AND_IMMUNITY.md) | Normative | доверие, иммунитет, карантин |
| [HOMEOSTASIS.md](HOMEOSTASIS.md) | Normative | измеримые контуры регулирования |
| [MEMORY_AND_NERVOUS_SYSTEM.md](MEMORY_AND_NERVOUS_SYSTEM.md) | Normative | познание, рефлексы, память, обучение |
| [METABOLISM.md](METABOLISM.md) | Normative | поступление данных, вычисления, стоимость, учёт |
| [GENOME_AND_EVOLUTION.md](GENOME_AND_EVOLUTION.md) | Normative | геном, экспрессия, управляемая эволюция |
| [BIOLOGY_TO_IT_MAPPING.md](BIOLOGY_TO_IT_MAPPING.md) | Normative по колонке `Profile` | каноническая матрица из 119 механизмов |
| [CONFORMANCE.md](CONFORMANCE.md) | Normative | требования, evidence, статусы claim |
| [ROBOTICS_EXTENSION.md](ROBOTICS_EXTENSION.md) | Normative для Embodied | физическая безопасность и real-time |
| [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) | Informative | руководство по применению |
| [VERIFICATION_KIT.md](VERIFICATION_KIT.md) | Informative | тесты, сценарии отказа, конвенции, шаблоны |
| [PRINCIPLES.md](PRINCIPLES.md) | Informative | обоснование принципов |
| [SOURCES.md](SOURCES.md) | Informative | источники |
| [RELEASE_READINESS_v1.0.md](RELEASE_READINESS_v1.0.md) | Informative | критерии и результат оценки релизов |

Машиночитаемые источники истины лежат в [`specifications/`](../specifications/): схемы контрактов, [`state-machines.yaml`](../specifications/state-machines.yaml), [`requirements.yaml`](../specifications/requirements.yaml), [`failure-classes.yaml`](../specifications/failure-classes.yaml). Диаграммы — в [`diagrams/`](../diagrams/).
