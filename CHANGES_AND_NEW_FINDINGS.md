# Changes and New Findings

## Статус

Этот файл фиксирует переход от `DOA_STANDARD v1.0-draft`, доступного только как частичный conversational draft, к `DOA v1.0 Foundational Standard`.

## Добавлено по прямому запросу

- клеточное ядро и ядрышко;
- цитоскелет и внутриклеточный транспорт;
- эндоплазматический ретикулум, аппарат Гольджи и пероксисомы;
- межклеточная коммуникация, тканевая специализация и extracellular matrix;
- morphogenesis, differentiation, stem-cell pattern и development lifecycle;
- sensor fusion, calibration, proprioception и temporal alignment;
- neuroplasticity, adaptive learning и proceduralization;
- regeneration, inflammation, immune tolerance и wound repair;
- senescence/aging и oncological anti-patterns;
- microbiome/symbiosis и multi-organism interaction;
- barrier systems, DNA repair и epigenetic expression control;
- spatial organization, circadian cycles и sleep/consolidation;
- organ redundancy, emergency circulation и graceful degradation.

## Новые фундаментальные находки, отсутствовавшие в исходном перечне

### 1. Граница организма и среды

Без явной trust/ownership boundary невозможно определить, что является self, partner, symbiont, hostile input или просто infrastructure. Добавлены environment, organism, organ и cell boundaries.

### 2. Происхождение и идентичность состояния

Самовосстановление опасно, если источник восстановления не доказан. Добавлены signed genome, artifact digest, provenance, attestation и trusted restore source.

### 3. Cell-cycle checkpoints

Создание и масштабирование клеток требует admission, quota, integrity и readiness checkpoints. Это отдельный механизм от apoptosis.

### 4. Proteostasis и unfolded-protein response

Ошибочно собранные workflows/models/artifacts требуют quality gate, retry/refold, quarantine и controlled degradation до распространения.

### 5. Extracellular matrix и adhesion

Контракты, schemas, service discovery и topology constraints образуют структурную среду ткани; без неё клетки существуют как несогласованный набор workers.

### 6. Coagulation и wound sealing

После breach/partition необходим быстрый локальный deny/containment, который сохраняет организм до repair. Это не равно долгосрочной иммунной политике.

### 7. Renal, osmotic и acid-base regulation

Одной «печени» недостаточно: нужны quota enforcement, filtration, watermarks, retention, electrolyte-like balance очередей/пулов и удаление отходов.

### 8. Respiratory exchange

Compute availability зависит от capacity intake и waste/heat removal. Добавлен отдельный contract для accelerator capacity, thermal/power envelope и saturation.

### 9. Nociception и pain gating

Нужен быстрый локальный сигнал повреждения, отличный от полного incident diagnosis: он снижает нагрузку и инициирует защитный reflex.

### 10. Quorum sensing

Массовое поведение агентов требует density/load-aware admission, иначе возникает retry storm или неконтролируемая репликация.

### 11. Development over time

Provisioning, maturation, active operation, repair, quiescence и retirement различаются; простая модель «deployed/not deployed» недостаточна.

### 12. Ecology и treaties между организмами

Federation нескольких цифровых организмов требует identity federation, contract negotiation, resource quotas, data-use policy и revocation.

### 13. Observer/actuator integrity

Повреждённый sensor или actuator может разрушить гомеостаз даже при корректном controller. Добавлены calibration, freshness, uncertainty и independent verification.

### 14. Chronic inflammation и autoimmune failure

Security controls сами могут стать источником отказа. Добавлены TTL, scope, false-positive budget, tolerance и resolution criteria.

### 15. Cancer as a family of anti-patterns

Онкологическая аналогия формализована как privilege escalation, uncontrolled replication, resource capture, policy evasion, apoptosis resistance и deceptive health reporting.

## Осознанно не утверждается

- что перечень охватывает буквально все известные биологические детали;
- что один механизм имеет единственный допустимый IT-аналог;
- что применение биологической терминологии улучшает систему без evidence;
- что DOA заменяет safety/security standards или domain regulation.

## Влияние на v1.0

Новые находки включены в нормативный реестр, схемы, reference architecture и conformance evidence. Они не создают зависимость от `AI-Engineering-Control-Plane` и не объявляют конкретный runtime каноническим.

## Финализация v1.0.0 (аудит полноты)

Самостоятельный аудит матрицы на предмет архитектурных пробелов выявил следующие проблемы; все устранены в `v1.0.0`.

### Структурные пробелы матрицы

- матрица содержала 8 колонок без отдельных Observability и Evidence и без нормативного статуса строки; теперь 12 колонок, стабильные ID и `Profile`;
- отсутствовали строки: self/non-self recognition, immune memory, necrosis, cellular stress response, nutrient/oxygen sensing, compartmentalization, positive feedback, forgetting/decay, motor hierarchy, peripheral ganglia (distributed cognition), synchronization, provenance, identity continuity, state continuity/anti-resurrection, organism termination, organism-scale regeneration, genetic drift, model/behavioral drift, horizontal transfer и reproductive isolation, sensor fusion/calibration, actuator envelope, safe-stop reflex;
- дублирующие строки (`Endocrine signals` и `Endocrine axis`) объединены; механизмы без архитектурной необходимости (polarity, fever, fibrosis, heart и др.) помечены `Pattern`.

### Несогласованности и дефекты контрактов

- cell lifecycle в стандарте (`SNAPSHOTTED`, `CREDENTIALS_REVOKED`), схеме и диаграмме расходились; введены единые state machines, apoptosis как `TERMINATING`, necrosis как `FAILED`, `STRESSED` и `SENESCENT`;
- `CapabilityGrant`, `MemoryRecord`, `HealthEvidence` были нормативными контрактами без схем; добавлены схемы, а также `ControlLoopSpec`, `PolicyOverlay`, `LineageManifest`, lifecycle-событие и `ConformanceClaim`;
- genome schema не проверяла homeostasis loops, termination, memory, boundary; добавлены обязательные разделы и условные требования по профилям;
- `format: date-time`/`uri` не проверялись без дополнительных пакетов; заменены паттернами;
- пример genome не содержал controller, hysteresis, override из §11 стандарта;
- термин HomeostaticSignal/HormoneSignal использовался как два имени одного контракта; зафиксирован канонический термин;
- у иммунного ответа отсутствовали этапы eradicate/recover/learn/update defenses;
- learning и evolution смешивались в двух разных протоколах; введён единый `change` с классами.

### Новые документы

`BOUNDARY_AND_IDENTITY.md` (граница организма и identity), `LIFECYCLE.md` (state machines, старение, завершение), `FAILURE_AND_RECOVERY.md` (таксономия восстановления, 25 классов отказа, runaway growth), `CONFORMANCE.md` (требования и evidence), `TERMINOLOGY.md` (нормативный язык и глоссарий).

## Открытые вопросы для maintainer (по анализу раздела `mechanisms/`)

Источник: `python scripts/analyze_interaction_graph.py` на версии 1.5.0. Это вопросы, а не принятые решения: нормативные тексты они не меняют, а решение по каждому принимается по порядку `GOVERNANCE.md`, раздел 4. Граф связей неполный и составлен автором без независимой проверки, поэтому каждый вопрос стоит проверить по реестрам, а не по графу.

1. **Трассируемость `REQ-CORE-18`.** В `specifications/requirements.yaml` у `REQ-CORE-18` в поле `mappings` перечислены четыре механизма: `C-16`, `M-12`, `M-14`, `M-09`. Граф относит к «рабочим» (то есть тратящим вычисления, время или токены) 100 механизмов, и правило по смыслу охватывает всех. Вопрос: нужно ли расширить `mappings` либо описать в документе, что правило общее и перечень в `mappings` неполный.
2. **Цикл через `M-05` и ограничитель `H-02`.** В графе есть цикл `C-16 → M-12 → M-14 → M-05 → M-06 → C-16` из рёбер `supplies` и `triggers` (основания: `REQ-CORE-18`, `docs/METABOLISM.md`). `REQ-CORE-18` требует, чтобы дефицит ресурса сдерживал рост; `F-18` описывает неограниченный рост; `H-02` (через `REQ-CORE-07`) требует потолка и срока для усиливающих контуров и в графе явно ограничивает `I-09`, `I-10`, `I-12`. Вопрос: считать ли цикл через `M-05` усиливающим и ограничивать ли `M-05` через `H-02` явно. Проверка петель в валидаторе такой цикл не ловит, потому что смотрит только на рёбра типа `amplifies`.
3. **Резерв бюджета на завершение.** `REQ-CORE-15` требует, чтобы завершение шло по ограниченному протоколу и оставляло терминальную запись; `REQ-DIST-02` требует сохранять трафик identity, safety, audit и recovery при перегрузке. В `requirements.yaml` нет формулировки о том, что часть бюджета (`REQ-CORE-18`) закреплена за самим завершением. Биологическая подсказка слабая: карточка `mechanisms/cards/atp-and-cell-death-mode.md` опирается на одну работу на одной линии клеток ([PMID 10987825](https://pubmed.ncbi.nlm.nih.gov/10987825/)), принцип-кандидат `P-07`. Вопрос: нужно ли такое требование и в каком профиле.
