# Biology-to-IT Mapping Registry

**Версия:** DOA v1.0 (`DOA-FS-1.0`). Этот документ является канонической матрицей механизмов: каждая строка — нормативная карточка.

## 1. Правило чтения

Цепочка для каждого механизма:

`Biology → Responsibility → Component → Contract → Protocol / State machine → Invariant → Failure mode → Security / safety control → Observability → Evidence`

| Колонка | Смысл |
|---|---|
| `ID` | Стабильный идентификатор; на него ссылаются другие документы, requirements и claims |
| Biological mechanism | Источник функции. Биологическая точность не требуется и не доказывает пригодность IT-реализации |
| Digital responsibility | Какую системную функцию выполняет механизм |
| Digital component | Кто его реализует (роль, не обязательный продукт) |
| Contract | Проверяемый интерфейс или policy object; для многих — schema в `specifications/` |
| Protocol / State machine | Разрешённые состояния и переходы; канонические машины — в `specifications/state-machines.yaml` |
| Invariant | Условие, которое MUST выполняться всегда |
| Failure mode | Как механизм отказывает |
| Security / safety control | Что предотвращает, ограничивает или обнаруживает нарушение |
| Observability | Сигналы (metrics/events/traces), по которым нарушение или состояние обнаруживается |
| Evidence | Артефакт, который реализация предъявляет в conformance claim |
| Profile | Нормативный статус строки (см. ниже) |

## 2. Нормативный статус строки (`Profile`)

| Profile | Значение |
|---|---|
| `Core` | MUST для любой реализации, заявляющей DOA |
| `Distributed` | MUST при заявлении Distributed Profile |
| `Adaptive` | MUST при заявлении Adaptive Profile |
| `Embodied` | MUST при заявлении Embodied Profile |
| `Conditional` | MUST, если реализация допускает соответствующую возможность (reproduction, federation, horizontal transfer); иначе возможность MUST быть явно запрещена в genome (`ecology`) |
| `Pattern` | SHOULD / MAY: паттерн реализации; отсутствие не нарушает соответствие, но реализация MUST NOT заявлять механизм без полного контракта |
| `Anti-pattern` | Описывает недопустимое поведение; реализация MUST иметь механизм обнаружения и ограничения, указанный в строке |

Строка уровня `Core` или выбранного профиля MUST быть либо реализована с evidence, либо исключена с письменным обоснованием в conformance claim (`docs/CONFORMANCE.md`). Строка без любого из полей контракта считается метафорой и MUST NOT использоваться как доказательство соответствия.

Стек в Приложении A приведён как возможный, не обязательный. Конкретные schema IDs, owners, SLO thresholds, action limits и test evidence реализация определяет локально; реестр не заменяет threat/hazard analysis.


## 1. Клетка: молекулярный и внутриклеточный уровень

| ID | Biological mechanism | Digital responsibility | Digital component | Contract | Protocol / State machine | Invariant | Failure mode | Security / safety control | Observability | Evidence | Profile |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-01 | Atoms/molecules | Гарантировать детерминированное представление данных | Typed immutable values, pure transforms | schema + hash + units | parse→validate→transform→emit | Одинаковые input и version дают одинаковый output | Type confusion, overflow, nondeterminism | Strict parser, size/depth limits, schema validation до обработки | parse_reject_total, schema_version по каждому типу | Schema-conformance tests и golden vectors | Pattern |
| C-02 | DNA / genome | Хранить подписанный desired state организма | Genome store и change service | `GenomeManifest` (`genome.schema.json`) | draft→validated→signed→active→superseded | Active digest известен каждому компоненту; active genome immutable | Drift, corruption, несовместимая версия | Подпись, content-addressing, запись только через change service | genome_digest в каждом EventEnvelope и health evidence | Подписанный genome, schema-validation log, digest-match report | Core |
| C-03 | RNA / transcript | Преобразовать genome+intent в request-scoped план исполнения | Expression engine | `ExecutionTranscript` | resolve→authorize→bind→execute→expire | Transcript связан с genome digest, overlay digests и intent | Stale plan, потеря контекста | Plan expiry, policy check при bind, запрет исполнения неподписанного плана | transcript_id в trace; expired_transcript_total | Воспроизведённый transcript из зафиксированных versions | Core |
| C-04 | Epigenetics | Менять expression без изменения genome | Overlay controller | `PolicyOverlay` (`policy-overlay.schema.json`) | proposed→approved→active→expired/revoked | Effective config восстанавливается из genome + активных overlays; каждый overlay имеет TTL | Конфликт overlays, sticky flag | Подпись, обязательные scope/precedence/expiry, запрет повышения authority | active_overlays, overlay_age, overlay_conflict_total | Effective-policy snapshot и overlay digests в `organism` record | Core |
| C-05 | DNA repair | Обнаружить и исправить нарушение целостности artifacts/config | Integrity scanner и repair controller | `RepairCase` с trusted source | detect→arrest→compare→repair→verify | Ни один repaired artifact не промотируется без проверки | Silent corruption, неверный источник repair | Repair source независим от повреждённой реплики; arrest до repair | integrity_mismatch_total, mean_time_to_repair | Test: подмена артефакта → arrest → repair → attestation | Core |
| C-06 | Nucleus | Защитить authority/configuration domain | Policy и genome authority | `NuclearAPI` (change-request интерфейс) | sealed→readable→change-request→commit | Запись только через авторизованный change path | Split brain, недоступность authority | KMS/HSM, раздельные issuer и enforcer, quorum на изменения | authority_write_total по субъекту, authority_availability | Access-policy test: прямая запись из runtime отклонена | Core |
| C-07 | Nuclear pores | Контролировать импорт/экспорт конфигурации | Config gateway | Capability-scoped request | authenticate→authorize→filter→transfer | Каждый transfer попадает в audit | Обход, устаревший grant | mTLS, scoped grants, allowlist полей | config_transfer_total, denied_transfer_total | Audit-трасса transfer + negative test обхода | Core |
| C-08 | Nucleolus | Собирать и подписывать исполняемые bundles | Build/attestation pipeline | Signed `RuntimeBundle` | source→build→scan→attest→publish | Работающий runtime имеет provenance | Poisoned build, невоспроизводимая сборка | SLSA-class provenance, hermetic build, signature verify при admission | bundle_provenance_missing_total | Attestation + verification log при admission | Core |
| C-09 | Ribosome | Привязать plan к исполняемому artifact/модели | Task binder/compiler | `TaskBinding` | queued→compiled→loaded→running→done | Версия artifact/модели прикреплена к задаче | Compile error, неверная цель | Digest pinning, sandbox для сгенерированного кода | task_artifact_version в trace | Trace с artifact digest на каждой задаче | Pattern |
| C-10 | Endoplasmic reticulum | Контролировать качество artifacts и workflows до распространения | Quality gate | `QualityGateResult` | synthesize→fold→inspect→pass/refold/reject | Невалидный artifact не достигает distribution | Плохая schema, несовместимые зависимости | Sandbox, type check, behavior eval, retry budget | quality_gate_pass_ratio, refold_count | Gate-отчёты на каждый promoted artifact | Core |
| C-11 | Unfolded-protein response (proteostasis) | Ограничить синтез при перегрузке quality gate | Backpressure controller | `ProteostasisSignal` | normal→stress→throttle→recover/escalate | Stress имеет TTL и критерий разрешения | Retry storm, постоянный throttle | Retry budget, circuit breaker, quarantine вместо бесконечного refold | proteostasis_state, retry_budget_remaining | Fault-injection: поток плохих artifacts → throttle → recovery | Distributed |
| C-12 | Golgi | Упаковать, пометить версией и маршрутизировать artifacts | Artifact packager/router | `ArtifactEnvelope` | receive→enrich→classify→sign→dispatch | Destination и classification сохраняются | Misrouting, неверная метка | Подпись envelope, classification gate | artifact_dispatch_total по destination | Envelope signature log, SBOM | Pattern |
| C-13 | Vesicles | Доставить payload между compartments | Sealed transport envelope | Signed envelope + destination | create→seal→transport→ack/expire | Нет unsealed payload через границу compartment | Потеря, дубликат, reorder | Подпись, TTL, idempotency key, replay window | vesicle_lag, dup_total, expired_total | Replay/duplicate test | Distributed |
| C-14 | Cytoskeleton | Удерживать topology и placement исполнения | Placement controller | `PlacementConstraint` | discover→place→monitor→relocate | Placement соблюдает declared constraints и failure domains | Hotspot, collapse, drift | Anti-affinity, topology spread, admission validation | placement_violation_total | Placement-report vs genome topology | Distributed |
| C-15 | Motor proteins | Переместить данные/работу по известным маршрутам | Transfer worker | `TransferJob` | reserve→move→verify→commit | Checksum и ack получателя подтверждены | Partial copy, stuck transfer | Path allowlist, checksum, quota | transfer_duration, checksum_mismatch_total | Transfer log с checksum | Pattern |
| C-16 | Mitochondria | Преобразовать ресурсы в вычислительную работу в рамках budget | Resource scheduler | `ResourceBudget` | reserve→consume→account→release | Вся работа списывается на budget | Exhaustion, thermal/power limit | Hard quotas, preemption, cost cap | budget_used_ratio, rejected_reservation_total | Accounting-report: сумма charges = потребление | Core |
| C-17 | Peroxisomes | Изолировать опасные трансформации | Sandbox runner | `SandboxJob` | ingest→isolate→transform→inspect→release | Опасная работа не исполняется вне sandbox | Escape, токсичный остаток | Strong isolation (microVM/gVisor), seccomp, no egress по умолчанию | sandbox_escape_alert_total, sandbox_jobs | Escape-test и profile isolation | Core |
| C-18 | Lysosomes | Классифицировать и утилизировать устаревший/повреждённый материал | Disposal service | `DisposalRecord` | detect→classify→hold→destroy/archive | Forensic evidence не удаляется автоматически | Преждевременное удаление, утечка | Legal/forensic hold приоритетнее GC, WORM archive | disposal_total по классу, hold_active | Disposal records + hold-test | Core |
| C-19 | Autophagy | Переработать собственные устаревшие компоненты | Maintenance collector | `MaintenanceCandidate` | inventory→isolate→verify-unused→recycle | Live/protected зависимость не удаляется | Разрыв зависимостей, cache thrash | Dependency graph check, quarantine перед удалением | recycled_total, rollback_total | Dependency-graph report перед recycle | Pattern |
| C-20 | Membrane | Обеспечить trust boundary клетки | Ingress/egress enforcement point | `IngressDecision`/`EgressDecision` | inspect→allow/deny/throttle/quarantine | Нет неопосредованного пересечения границы | Bypass, перегрузка | Deny-by-default, mTLS, rate limit | boundary_decision_total по verdict | Boundary-inventory + bypass-test | Core |
| C-21 | Receptors | Распознавать типизированные сигналы | Schema-bound adapters | Версионированная receptor schema | bind→validate→normalize→signal | Неизвестные типы отклоняются или карантинятся | Spoofing, desensitization | Schema registry, authn/authz источника | unknown_type_total | Test: неизвестный тип → reject/quarantine | Core |
| C-22 | Endocytosis | Безопасно принять внешний ввод | Ingress packager | `IngressEnvelope` | authn→scan→normalize→seal→route | Raw input не становится trusted memory напрямую | Parser bomb, контаминация | Scan, normalize, sandbox parser, DLP | ingress_reject_total | Test: injected content не меняет policy/memory | Core |
| C-23 | Exocytosis | Управлять egress и действиями наружу | Egress gateway | `EgressRequest` | authorize→redact→sign→deliver→receipt | Side effect соответствует approved intent | Дубли, утечка | DLP, transactional outbox, approval boundary | egress_total, egress_denied_total | Receipt ↔ intent reconciliation | Core |
| C-24 | Compartmentalization | Ограничить радиус отказа и привилегий | Failure-domain declaration и bulkheads | `FailureDomainDeclaration` в genome `boundary`/`topology` | declare→enforce→verify-isolation | Отказ клетки не становится отказом организма без явного пути распространения | Скрытая общая зависимость, shared fate | Раздельные quotas, namespaces, независимые failure domains | blast_radius_estimate, shared_dependency_count | Cell-kill test: соседние клетки сохраняют SLO | Core |
| C-25 | Cell cycle | Контролировать создание и репликацию клеток | Admission controller | `CellAdmission` + `lineage` | G0→admitted→provisioned→ready→replicate/stop | Число реплик и generation не превышают quota и `growth_control` | Runaway scaling, незрелая клетка | Quota, spawn depth/rate limit, независимый issuer grants | cell_count, spawn_rate, generation_depth | Admission-test: превышение quota отклонено | Core |
| C-26 | Checkpoints | Блокировать продвижение по стадиям без доказательства | Gate evaluator | `CheckpointEvidence` | evaluate→pass/hold/repair/apoptosis | Нет перехода стадии при failed gate | Ложный pass, deadlock | Policy engine, attestations, timeout на hold | checkpoint_result_total | Gate evidence на каждый transition | Core |
| C-27 | Apoptosis | Безопасно завершать клетку по ограниченному протоколу | Termination controller | `TerminationPlan`, 8 шагов apoptosis | suspect→isolate→revoke→snapshot→terminate→verify | У завершённой клетки нет активных grants, endpoints и реплик | Zombie, cascade kill | Revocation без кооперации клетки, lease expiry, внешний kill authority | apoptosis_step_duration, live_grants_after_term | Apoptosis-test и terminal record | Core |
| C-28 | Necrosis | Обрабатывать неконтролируемый отказ клетки | Lease/fencing и failure detector | `FailureRecord` (переход в `FAILED`) | ACTIVE→FAILED→fence (lease expiry)→ISOLATED→repair/terminate | Упавшая клетка не удерживает grants и не продолжает side effects; потеря отличима от остановки | Утечка частичного состояния, дубль исполнения, zombie writer | Fencing token, lease expiry, idempotency, revoke без кооперации | failed_cells_total, fencing_latency, orphaned_grants | Crash-injection: kill -9 → fencing → grants revoked | Core |
| C-29 | Cellular stress response | Дать клетке локальный защитный режим до эскалации | Cell supervisor | `StressState` (ACTIVE↔STRESSED) | ACTIVE→STRESSED→ACTIVE/SUSPECT | Режим STRESSED имеет TTL, ограничения нагрузки и критерий выхода | Вечный stress, скрытая деградация | Shed optional work, снижение capability, повышенная telemetry | cell_stress_state, stress_ttl_remaining | Test: перегрузка → STRESSED → выход или SUSPECT | Core |
| C-30 | Senescence | Ограничить стареющий компонент до замены | Lifecycle controller | `SenescencePolicy` | active→aging→restricted→replaced→retired | Senescent cell не реплицируется и не повышает привилегии | Stale dependency, noisy aging component | Reduced privilege, запрет replication, replacement deadline | senescent_cells, time_in_senescence | Policy + replacement record | Core |

## 2. Ткани, развитие и межклеточная коммуникация

| ID | Biological mechanism | Digital responsibility | Digital component | Contract | Protocol / State machine | Invariant | Failure mode | Security / safety control | Observability | Evidence | Profile |
|---|---|---|---|---|---|---|---|---|---|---|---|
| T-01 | Gap junctions | Быстрая связь соседних клеток | Local typed channel | Peer-scoped channel contract | connect→exchange→close | Peer identity и rate наблюдаемы | Связанность, каскад отказов | mTLS, rate limit, allowlist peers | peer_channel_active, peer_rate | Peer inventory | Pattern |
| T-02 | Paracrine signals | Локально ограниченное вещание | Scoped pub/sub | `LocalSignal(scope,ttl)` | publish→fanout→expire | Приём ограничен scope ткани | Spillover, storm | Namespace ACL, TTL, fan-out limit | signal_fanout, expired_total | Scope-leak test | Distributed |
| T-03 | Tissue specialization | Однородная ролевая группа клеток | `TissueProfile` | `TissueProfile` | recruit→differentiate→serve→renew | Все члены удовлетворяют одному SLO/policy | Skew, monoculture failure | Общий admission profile, diversity budget | tissue_slo_compliance | Tissue-inventory + SLO report | Distributed |
| T-04 | Differentiation | Специализировать клетку по least privilege | Expression profile controller | Signed expression profile | stem→candidate→trained→verified→specialized | Рост capability сопровождается admission evidence | Неверная роль, необратимый drift | Admission decision на каждое расширение прав | capability_delta_total | Admission log для каждого capability increase | Core |
| T-05 | Stem-cell niche | Хранить доверенный запас для regeneration | Seed registry | `SeedArtifact` | dormant→activated→instantiate→replenish | Seed чист, подписан и не используется в обычном трафике | Seed corruption, исчерпание | Offline/изолированный registry, ротация seeds | seed_age, seed_verification_total | Seed verification + restore test | Core |
| T-06 | Morphogenesis | Строить topology организма | Topology builder | `TopologyPlan` | blueprint→stage→connect→validate→mature | Фактическая topology соответствует declared graph | Отсутствует орган, неверная связность | Graph validator, GitOps, запрет hidden control path | topology_drift_total | Declared-vs-observed topology report | Core |
| T-07 | Extracellular matrix | Предоставить структурную среду контрактов | Schema/interface registry | Versioned contract registry | propose→review→publish→deprecate | Runtime interfaces разрешаются в совместимые версии | Contract erosion | Signed schemas, version-squatting protection | contract_resolution_failure_total | Registry audit + compatibility matrix | Core |
| T-08 | Cell adhesion | Членство и service discovery | Endpoint lease registry | Identity-bound endpoint lease | join→healthy→discoverable→drain→leave | Discoverable только ready cells | Stale endpoint | Identity binding, lease TTL | discoverable_cells | Test: not-ready cell не обнаруживается | Distributed |
| T-09 | Polarity | Разделить направления ingress и egress | Port/role policy | Direction policy | receive-side→process→send-side | Нарушения направления наблюдаемы | Feedback loop, wrong-way traffic | Network policy, раздельные порты | direction_violation_total | Policy test | Pattern |
| T-10 | Development / ontogeny | Развивать организм по стадиям | Development controller | `DevelopmentStage` (organism machine) | PROVISIONING→DEVELOPING→READY | Стадийные gates пройдены до exposure | Преждевременный exposure | Progressive checkpoints, запрет traffic до READY | stage_duration, gate_result | Organism state-transition log | Core |

## 3. Нервная система: сенсорика, решение, действие, память

| ID | Biological mechanism | Digital responsibility | Digital component | Contract | Protocol / State machine | Invariant | Failure mode | Security / safety control | Observability | Evidence | Profile |
|---|---|---|---|---|---|---|---|---|---|---|---|
| N-01 | Sensory receptor (sensory hierarchy) | Получить калиброванное наблюдение и поднять его по иерархии: raw→feature→percept | Sensor adapters | `Observation(value,unit,time,uncertainty)` | sample→calibrate→validate→publish | Freshness и uncertainty присутствуют; отсутствие сигнала = UNKNOWN | Drift, blindness, ложный sensor | Signed telemetry, независимый второй источник | observation_age, uncertainty, unknown_ratio | Freshness/UNKNOWN test | Core |
| N-02 | Proprioception | Знать собственное состояние | Self-state inventory | `SelfStateSnapshot` | poll→reconcile→publish | Inventory совпадает с runtime | Stale topology, скрытый implant | Runtime attestation, drift alert | self_state_drift_total | Inventory-vs-runtime diff | Core |
| N-03 | Nociception | Быстрый локальный сигнал повреждения | Watchdog/damage detector | `DamageSignal` | detect→reflex→escalate→resolve | Критическое повреждение обходит медленный planner | Alert fatigue, ложная боль | Rate limit сигнала, pain gating | damage_signal_total по severity | Injected-damage test: reflex сработал в бюджете latency | Core |
| N-04 | Thalamus (routing, attention/salience) | Фильтровать, приоритизировать и маршрутизировать входы; ограничить attention budget | Event router | `RouteDecision(priority, salience, budget, reason)` | classify→prioritize→route/drop | Каждый принятый вход имеет причину маршрута и бюджет внимания | Bottleneck, misroute, salience hijack | Salience не может повышать authority; budget на источник | route_decision_total, dropped_by_budget | Route log + salience-abuse test | Core |
| N-05 | Cortex | Семантические гипотезы и планы | Reasoning pool | `PlanProposal` | perceive→hypothesize→plan→verify | Proposal не является authority grant | Hallucination, loop | Plan validator, исполнение только через decision service | plan_reject_total, loop_guard_trips | Test: plan без grant не исполняется | Core |
| N-06 | Basal ganglia | Выбрать действие по policy/risk/resource | Decision service | `ActionDecision` | candidates→policy/risk/resource→select | Выбранное действие имеет decision evidence | Unsafe selection, confused deputy | Policy engine, risk threshold, step-up approval | decision_total по verdict | Decision log + denied-action test | Core |
| N-07 | Motor hierarchy (actuation) | Превратить решение в ограниченное действие | Executor cells и tool gateway | `ActuationCommand(grant, deadline, idempotency_key)` | intent→plan→grant→command→feedback | Команда исполняется только с valid grant и до deadline | Duplicate action, expired command | Grant check на исполнителе, idempotency, deadline | command_total, expired_rejected_total | Test: expired/replayed command отклонена | Core |
| N-08 | Cerebellum | Проверенные процедурные навыки | Skill registry | `SkillArtifact` | observe→compile→test→promote | Версия и результат skill измеряются | Brittle automation, poisoned skill | Подпись, тесты, change protocol | skill_success_rate по версии | Skill test evidence | Adaptive |
| N-09 | Spinal reflex | Детерминированная низколатентная реакция | Reflex engine | `ReflexRule` | trigger→guard→act→report | Ограничены latency и action envelope | Oscillation, stale rule | Bounded action set, TTL правил | reflex_fired_total, reflex_latency | Reflex-latency test | Core |
| N-10 | Autonomic nerves | Фоновое обслуживание | Controllers/operators | Lease/maintenance contract | schedule→execute→verify→renew | Maintenance не падает молча | Resource leak, thundering herd | Jitter, lease, owner | maintenance_missed_total | Maintenance run-log | Pattern |
| N-11 | Peripheral ganglia (central vs peripheral control, distributed cognition) | Ограниченная локальная автономия при потере связи | Edge/peripheral deciders | `DelegationGrant(depth, max_depth, lease)` | delegate→act-locally→report→reconcile/expire | Делегированные права ⊆ прав делегатора; глубина ограничена; lease истекает | Split-brain решения, рекурсивное делегирование | Attenuation, max_depth, lease, reconcile при reconnect | delegation_depth, local_decisions_unreconciled | Test: превышение depth и истёкший lease отклонены | Distributed |
| N-12 | Working memory | Request-local состояние | Scoped scratch store | `MemoryRecord(type=working)` | create→use→expire | Есть TTL и привязка к задаче | Leakage, overflow | Tenant isolation, size bound, encryption | working_memory_size, ttl_expired_total | Isolation test | Core |
| N-13 | Episodic memory | История событий и результатов | Event store | `MemoryRecord(type=episodic)` | append→validate→retain→expire | Хронология неизменна; правка только supersession | Ложный эпизод, audit poisoning | Provenance, append-only, signed writes | episode_write_total, supersession_total | Immutability test | Core |
| N-14 | Semantic memory | Проверенные факты и связи | Knowledge store | `MemoryRecord(type=semantic)` | ingest→verify→index→supersede | Ответ прослеживается до источников | Stale/contradictory fact, poisoning | verified-source write policy, confidence, validity interval | contradiction_rate, stale_fact_rate | Write-policy test с untrusted source | Core |
| N-15 | Procedural memory | Подписанные workflows/skills | Skill/workflow registry | Signed skill manifest | draft→test→approve→active→retire | Исполняется только approved skill | Obsolete procedure | Supply-chain controls, retirement policy | active_skill_versions | Manifest verification log | Core |
| N-16 | Memory consolidation (hippocampus) | Переводить кандидаты в долговременную память по protocol | Memory gateway | Consolidation pipeline contract | classify→redact→verify-provenance→dedupe→approve→store→revalidate | Untrusted content не записывается как instruction/policy/identity fact | Memory poisoning, потеря принятой работы | Policy approval, provenance gate, redaction | consolidation_accept_total, rejected_total | Consolidation log + poisoning test | Core |
| N-17 | Forgetting and memory decay | Управляемо уменьшать и удалять память | Retention controller | `MemoryRecord.retention` + confidence decay | active→decayed→superseded→erased | Retention, consent и decay применяются; erasure проверяема | Преждевременное/невыполненное удаление, stale memory | TTL, consent withdrawal, crypto-erasure, legal hold | expired_records, erasure_verified_total | Erasure-test + retention report | Core |
| N-18 | Sleep / maintenance window | Офлайн-консолидация и обслуживание | Maintenance scheduler | `MaintenanceWindow` | active→quiesce→consolidate→validate→wake | Нет потери принятой работы; wake перепроверяет policy | Missed wake, corrupt checkpoint | Emergency preemption, максимальная длительность | window_duration, missed_window_total | Window run-log | Pattern |
| N-19 | Circadian rhythm | Временные политики нагрузки и обслуживания | Temporal policy engine | `TemporalPolicy` | schedule→prepare→activate→decay | Timezone и missed tick записываются | Clock drift, неверная сезонность | Monotonic timers, emergency override | tick_missed_total, clock_skew | Schedule test с missed tick | Pattern |
| N-20 | Neuroplasticity | Версионируемо менять routing/weights/skills | Adaptation pipeline | `AdaptationProposal` (change machine, class=learning) | OBSERVED→PROPOSED→EVALUATED→APPROVED→CANARY→PROMOTED/ROLLED_BACK | Baseline и delta сопоставимы; изменение только внутри declared adaptive bounds | Catastrophic forgetting, reward poisoning | Evaluation set governance, canary, rollback artifact | adaptation_delta, rollback_total | Change-protocol evidence (state log + eval report) | Adaptive |
| N-21 | Synchronization and ordering | Согласовать время, порядок и членство | Clock/epoch service | `EpochRecord`, event time vs processing time | sync→stamp→order→reconcile | Ordering гарантируется только в объявленном scope; membership epoch во всех решениях | Clock skew, split-brain, stale epoch | Epoch fencing, bounded skew, late-event policy | clock_skew, epoch_mismatch_total | Skew-injection и partition test | Distributed |

## 4. Циркуляция, метаболизм и выделение

| ID | Biological mechanism | Digital responsibility | Digital component | Contract | Protocol / State machine | Invariant | Failure mode | Security / safety control | Observability | Evidence | Profile |
|---|---|---|---|---|---|---|---|---|---|---|---|
| M-01 | Blood / circulation | Транспорт команд, событий и наблюдений | Event/data bus | `EventEnvelope` (`event.schema.json`) | publish→persist→deliver→ack/dead-letter | Lag, loss, duplicates и pressure наблюдаемы | Congestion, partition | Signed envelope, authz на topic, size/TTL limit | bus_lag, dead_letter_total | Delivery-semantics test | Distributed |
| M-02 | Heart | Планирование потока и backpressure | Flow scheduler | `FlowPolicy` | normal→pressure→shed/prioritize→recover | Критический поток сохраняет минимальную ёмкость | Arrhythmia/oscillation | Priority classes, abuse limits | flow_priority_utilization | Load test | Pattern |
| M-03 | Emergency circulation | Сохранить жизненно важный управляющий трафик | Priority/reserved channels | `EmergencyFlowProfile` | trigger→reserve→shed→stabilize→restore | Identity, safety, audit и recovery пути остаются живыми | Starvation, ложная emergency | Раздельные очереди, TTL режима | emergency_mode_active, vital_flow_latency | Emergency drill | Distributed |
| M-04 | Lymph (quarantine path) | Побочный путь проверки подозрительного материала | Quarantine pipeline | `QuarantineCase` | divert→analyze→release/reject/archive | Подозрительное не возвращается непроверенным | Backlog, leakage | Sandbox, release gate, owner review | quarantine_backlog, release_total | Quarantine release-test | Core |
| M-05 | Angiogenesis / vascularization | Расширять ёмкость и маршруты распределения | Capacity controller | `CapacityRequest` | detect demand→risk check→provision→connect→trim | Новый путь соблюдает boundary и policy | Cost explosion, shadow network | Budget, approval, inventory новых путей | new_path_total, unmanaged_path_total | Inventory diff | Pattern |
| M-06 | Respiratory exchange | Получение вычислительной ёмкости и отвод тепла/нагрузки | Capacity controller | `CapacityEnvelope` | demand→admit→allocate→cool/release | Saturation, power и thermal headroom наблюдаются | Throttling, thermal shutdown | Admission by headroom, power cap | saturation, thermal_headroom | Saturation test | Distributed |
| M-07 | Digestion | Декодировать, разобрать и нормализовать вход | Ingestion pipeline | `IngestionJob` | receive→scan→parse→normalize→emit | Принятые/отклонённые байты учитываются | Parser bomb, semantic loss | Bounded sandbox parser, limits | ingest_bytes_accepted/rejected | Malformed-input test | Core |
| M-08 | Liver (detox) | Классификация, редактирование и очистка | Sanitization service | `SanitizationResult` | inspect→redact→classify→enrich→release | Raw sensitive data не уходит downstream | Over-redaction, missed toxin | DLP, classification labels | redaction_total, leak_alert_total | Redaction test set | Core |
| M-09 | Kidney (filtration) | Фильтровать отходы и регулировать пулы | Retention/filter controller | `FiltrationPolicy` | sample→retain/excrete→balance→report | Watermarks хранилищ и очередей в пределах | Retention breach, потеря данных | Quota, hold rules, purge approval | watermark_state, purged_total | Retention report | Core |
| M-10 | Osmoregulation | Баланс очередей, cache и пулов | Watermark controller | `WatermarkPolicy` | normal→high/low→actuate→hysteresis→normal | Пороги и действия видимы | Oscillation, starvation | Hysteresis, rate limit действий | watermark_crossings_total | Oscillation test | Pattern |
| M-11 | Acid-base / electrolytes | Совместимость протоколов и конфигураций | Compatibility gate | `CompatibilityInvariant` | detect imbalance→buffer→migrate/reject | Версии в допустимых диапазонах | Version poisoning | Schema registry, downgrade protection | incompatible_version_total | Version-matrix test | Distributed |
| M-12 | ATP (resource currency) | Нормализованная валюта ресурсов | Metering service | `ResourceCharge` | reserve→spend→settle/refund | Стоимость задачи атрибутируема | Unbounded spend | Quotas, cost cap | charge_total, unattributed_cost | Accounting reconciliation | Core |
| M-13 | Fat / glycogen (reserve) | Резерв ёмкости для критической работы | Reserve manager | `ReservePolicy` | accumulate→hold→release→replenish | Резерв не расходуется обычной нагрузкой | Stranded capacity | Отдельная policy, replenishment plan | reserve_level | Reserve drill | Pattern |
| M-14 | Nutrient and oxygen sensing | Ощущать доступность ресурсов и ограничивать рост при дефиците | Resource availability sensors | `ResourceAvailabilitySignal` | sense→compare→anabolic/catabolic mode→recover | При дефиците рост/spawn блокируется, неважная работа сворачивается | Growth при дефиците, ложный дефицит | Hard gate на admission по signal, независимый sensor | resource_availability, mode_state | Test: дефицит → spawn отклонён | Core |

## 5. Гомеостаз, обратная связь и координация

| ID | Biological mechanism | Digital responsibility | Digital component | Contract | Protocol / State machine | Invariant | Failure mode | Security / safety control | Observability | Evidence | Profile |
|---|---|---|---|---|---|---|---|---|---|---|---|
| H-01 | Homeostasis (negative feedback) | Замкнутое регулирование отклонений | Controllers | `ControlLoopSpec` (`control-loop.schema.json`) | sample→compare→act→settle/escalate | Target, error и action коррелируют; stale signal ≠ здоровье | Oscillation, sensor/actuator fault | Hysteresis, rate limit, safety ceiling, manual override | control_error, action_total, loop_state | Alert-to-action trace + stability test | Core |
| H-02 | Positive feedback (bounded amplification) | Ограничить самоусиливающиеся контуры | Amplification guard | `AmplificationLimit` в `ControlLoopSpec` | trigger→amplify→ceiling/TTL→terminate | Любой усиливающий контур имеет ceiling, TTL и terminator | Runaway amplification, retry storm | Hard ceiling, circuit breaker, внешний terminator | amplification_factor, ceiling_hits_total | Runaway-injection test | Core |
| H-03 | Endocrine signaling (hormones) | Глобальная модуляция режима организма | Signal controller | `HormoneSignal` (`hormone.schema.json`) | issue→propagate→act→decay/revoke | Подписанный сигнал всегда истекает; эффект обратной связи виден | Chronic mode, противоречивые сигналы | Подпись, scope, TTL, separate issuer и enforcer | hormone_active, hormone_conflict_total | Expiry + conflict test | Core |
| H-04 | Quorum sensing | Коллективное действие по плотности/нагрузке | Quorum service | `QuorumObservation` | sample→threshold→coordinate→release | Решение содержит membership epoch | Split brain, herd effect, Sybil | Consensus, leases, rate limits, identity-bound votes | quorum_state, epoch | Partition test | Distributed |
| H-05 | Redundant organs | Доступность при отказе failure domain | Redundancy controller | `RedundancyPolicy` | primary→degraded→failover→reintegrate | Failover протестирован; реплики в независимых domains | Common-mode failure | Quorum, topology spread, standby hardening | failover_readiness | Failover drill | Distributed |

## 6. Иммунитет, барьеры, восстановление и старение

| ID | Biological mechanism | Digital responsibility | Digital component | Contract | Protocol / State machine | Invariant | Failure mode | Security / safety control | Observability | Evidence | Profile |
|---|---|---|---|---|---|---|---|---|---|---|---|
| I-01 | Skin / mucosal barrier | Многослойная внешняя граница | Boundary gateways | `BoundaryPolicy` | inspect→deny/allow→monitor | Все внешние пути инвентаризированы | Unknown ingress | Deny-by-default, WAF, network policy | external_path_inventory | Inventory diff + bypass test | Core |
| I-02 | Blood-brain barrier | Защита high-trust cognition и memory | Privileged ingress broker | `PrivilegedIngress` | request→sanitize→broker→limited context | Raw external content не меняет authority | Context poisoning | Content isolation, brokered context | privileged_ingress_total | Prompt-injection test | Core |
| I-03 | Self / non-self recognition (identity markers) | Различать self, symbiont, partner и unknown | Identity verifier | `IdentityAssertion` с trust class SELF/SYMBIONT/PARTNER/UNKNOWN | present→verify→classify→authorize | Неизвестное по умолчанию не получает доверия; location ≠ identity | Spoofing, ложный self | Workload attestation, mTLS, short-lived credentials | identity_verification_total по class | Spoofing test: подделанная identity отклонена | Core |
| I-04 | Innate immunity | Быстрая универсальная защита | Innate rules | `InnateRule` | detect→contain→signal→expire | Ответ ограничен и залогирован | False positive, evasion | Signature, rate limits, TTL | innate_rule_hit_total | Rule test set | Core |
| I-05 | Antigen presentation | Превращать наблюдения в проверяемые indicators | Finding pipeline | `FindingEvidence` | collect→normalize→correlate→present | Finding ссылается на неизменяемое evidence | Fabricated evidence | Evidence hashing, signed collectors | finding_total, evidence_missing_total | Evidence integrity test | Core |
| I-06 | Adaptive immunity | Обученная проверенная защита | Detection policy registry | `DetectionPolicyVersion` | learn→validate→deploy→monitor→retire | Новое правило измерено на precision/recall и blast radius | Overfit, stale IOC, poisoning | Change protocol, shadow mode, rollback | rule_precision, rule_recall | Rule validation report | Adaptive |
| I-07 | Immune memory | Сохранять проверенные indicators и playbooks для быстрого повторного ответа | Indicator registry | `IndicatorRecord(confidence, expiry, source)` | learn→verify→store→match→decay/retire | Каждый indicator имеет источник, confidence и срок; устаревшие не блокируют | Stale IOC, memory poisoning, autoimmune effect | Provenance, decay, false-positive budget | indicator_hit_rate, indicator_age | Indicator-decay test | Adaptive |
| I-08 | Immune tolerance | Ограниченное доверие к self/partner | Tolerance registry | `ToleranceGrant` | prove identity→grant→monitor→revoke/expire | Exception имеет owner, scope, expiry | Permissive exception | Workload identity, ABAC, no transitive trust | active_tolerances, expired_tolerance_total | Expiry test | Core |
| I-09 | Complement cascade | Усиленная скоординированная локализация | Response orchestrator | `ResponsePlaybook` | trigger→amplify→contain→stop | Cascade имеет rate и stop condition | Runaway response | Circuit breakers, stop condition | playbook_runs | Playbook dry-run | Pattern |
| I-10 | Inflammation | Временное усиление защиты и telemetry | Inflammation controller | `InflammationSignal` | local→amplified→resolution/chronic | TTL и resolution criterion присутствуют | Chronic degradation | TTL, scope | inflammation_active_ttl | TTL test | Core |
| I-11 | Fever | Ограниченный глобальный режим повышенного контроля | Emergency-mode controller | `EmergencyMode` | detect→raise controls→monitor→cool down | Максимальная длительность и ceiling принудительны | Ущерб от долгого режима | Max duration, expiry | emergency_mode_duration | Cool-down test | Pattern |
| I-12 | Coagulation | Быстро запечатать breach/partition | Seal rules | `SealRule` | damage→local deny→isolate→repair→reopen | Запечатанный scope минимален и явен | Thrombosis/deadlock | Minimal scope, auto-reopen TTL | sealed_scopes | Seal/reopen test | Core |
| I-13 | Wound healing | Восстановить сервис после повреждения | Recovery controller | `RecoveryPlan` | hemostasis→cleanup→rebuild→remodel→verify | RTO/RPO и post-repair checks выполнены | Scar/technical debt | Verification gate | recovery_duration | Restore drill | Core |
| I-14 | Regeneration | Восстановить утраченный компонент из доверенного seed, сохранив identity и lineage | Regeneration controller | `RegenerationRequest` | verify loss→instantiate→restore→validate→join | Регенерированный компонент аттестован до трафика; identity и lineage сохранены | Bad seed, state divergence | Trusted seed, attestation, continuity record | regeneration_total, attestation_failed_total | Regeneration drill | Core |
| I-15 | Fibrosis / scarring | Контролировать постоянные обходные решения | Exception-debt register | `ExceptionDebt` | emergency patch→document→limit→remove | Workaround имеет owner и expiry | Permanent brittleness | Debt register, expiry | exception_debt_age | Register review | Pattern |
| I-16 | Autoimmunity | Anti-pattern: защита блокирует валидный self | False-positive budget | `FalsePositiveBudget` | detect→suspend rule→review→repair | Доступность валидных функций отслеживается против controls | Systemic denial | Policy simulation, break-glass | false_positive_ratio | Simulation report | Anti-pattern |
| I-17 | Oncogenesis | Anti-pattern: неконтролируемая репликация, захват привилегий и ресурсов | Growth-control invariants | `GrowthControl` (genome `growth_control`) | detect→freeze→isolate→revoke→eradicate | Репликация и grants в declared limits; потомки учтены по lineage | Hidden clones, apoptosis resistance | Quotas, spawn depth, внешний kill, attestation | spawn_rate, orphan_count, lineage_depth | Runaway-spawn test (см. FAILURE_AND_RECOVERY) | Anti-pattern |
| I-18 | Aging | Измерять накопленный drift и деградацию | Aging index | `AgingIndex` | measure→maintain→senesce→replace | Неподдерживаемые компоненты перечислены | Коррелированное устаревание | SBOM/EOL policy, rotation | aging_index | Aging report | Core |

## 7. Идентичность, происхождение, эволюция и экология

| ID | Biological mechanism | Digital responsibility | Digital component | Contract | Protocol / State machine | Invariant | Failure mode | Security / safety control | Observability | Evidence | Profile |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-01 | Provenance | Доказать источник и целостность данных, моделей, policies, memory и artifacts | Provenance service | `ProvenanceRecord` (встроен в `MemoryRecord`, `LineageManifest`, artifact digests) | record→sign→verify→chain | Каждый trusted объект имеет источник, время, integrity и classification | Потеря provenance, поддельный источник | Подпись, content-addressing, отклонение объектов без provenance | provenance_missing_total | Provenance-gap test: объект без provenance не допускается | Core |
| E-02 | Heredity / lineage | Передавать проверенный genome и artifacts, хранить родословную | Lineage registry | `LineageManifest` (`lineage-manifest.schema.json`) | select→package→sign→verify→instantiate | Цепочка lineage полна; у каждой клетки и organism есть parent | Унаследованный дефект, разрыв цепочки | Подпись, запрет credential cloning | lineage_chain_gap_total | Lineage-chain verification | Core |
| E-03 | Identity continuity | Сохранять identity организма при замене компонентов | Identity authority и continuity record | `ContinuityRecord` (organism_id, trust_domain, trust root rotation) | replace→rotate→attest→record | organism_id и trust_domain неизменны при замене компонентов; смена trust root — только подписанной ротацией | Identity hijack, обрыв continuity | Подписанная ротация, независимый identity authority, `succeeded_by` при смене identity | identity_rotation_total, continuity_gap_total | Component-replacement test: identity сохранена; ротация подписана | Core |
| E-04 | State continuity and anti-resurrection | Сохранять непрерывную цепочку состояния и не воскрешать недействительное | Checkpoint chain и tombstone registry | `StateChain` + `Tombstone` | checkpoint→chain→restore-verify→tombstone | Terminated/revoked сущность не может быть восстановлена со stale backup и действующими credentials | Stale restore, resurrection of revoked identity | Epoch fencing, tombstone check при restore, hash-chain | restore_rejected_tombstone_total | Test: restore из до-tombstone backup отклонён | Core |
| E-05 | Organism termination (death) | Безопасно завершить организм с сохранением audit | Lifecycle controller | `TerminationPlan` (organism) | ACTIVE→RETIRING→TERMINATED | Grants отозваны, audit запечатан, tombstone выдан, данные утилизированы по policy | Orphaned resources, потеря audit | Revocation, retention policy, внешний audit store | retirement_step_duration, live_grants_after_term | Termination drill + terminal record | Core |
| E-06 | Organism-scale regeneration (catastrophic recovery) | Восстановить организм после катастрофической потери | Recovery controller и offline trust root | `CatastrophicRecoveryPlan` + `ContinuityRecord` | REPAIRING→PROVISIONING (epoch+1)→DEVELOPING→READY | Восстановление из seed вне затронутого failure domain; epoch увеличен; identity продолжена или помечена `succeeded_by` | Compromised seed, split-brain epochs | Offline trust root, human authority, epoch fencing | recovery_epoch, rto_actual | Catastrophic recovery drill | Distributed |
| E-07 | Reproduction | Контролируемо создавать новый организм | Reproduction planner | Signed `ReproductionPlan` | propose→approve→seed→differentiate→independent identity | Потомок получает новую identity и lineage; credential cloning запрещён | Clone storm, распространение компрометации | Genome `ecology.reproduction`, внешний approver | reproduction_total | Test: reproduction=forbidden блокирует создание | Conditional |
| E-08 | Mutation | Предлагать ограниченный вариант | Variant generator | `VariantProposal` (change class=evolution) | mutate→simulate→evaluate→approve/reject | Мутация не редактирует production напрямую | Unsafe phenotype | Sandbox, change protocol, provenance, lineage | variant_proposal_total | Change-protocol evidence | Adaptive |
| E-09 | Natural selection / evolutionary pressure | Отбирать варианты по многокритериальной оценке | Evaluation harness | Multi-objective scorecard | cohort→test→compare→promote/retire | Safety constraints доминируют над reward | Goodhart, monoculture, reward hacking | Safety gates как hard constraints, canary | scorecard_safety_violations | Evaluation report с hard safety gates | Adaptive |
| E-10 | Genetic drift | Обнаруживать расхождение реплик и lineage без отбора | Population drift monitor | `DriftReport` | snapshot→compare→classify→reconcile | Все реплики одного tissue сверяются с signed genome digest | Незаметное расхождение, monoculture | Periodic digest comparison, reconcile из trusted source | replica_digest_divergence | Divergence-injection test | Distributed |
| E-11 | Model / behavioral drift | Обнаруживать деградацию поведения моделей и адаптивных компонентов | Drift monitor | `DriftReport` по behavior eval | baseline→measure→alert→rollback/retrain | Drift относительно baseline измеряется на governed eval set | Silent degradation, incorrect adaptation | Drift threshold, auto-rollback trigger | drift_score | Drift-injection test | Adaptive |
| E-12 | Microbiome (host/guest boundary) | Ограничить вспомогательную экосистему; guest не становится host | Symbiont registry | `SymbiontContract` | discover→vet→grant→monitor→revoke | Каждый symbiont атрибутируем, ограничен quota и не получает права органа | Parasitism, dependency takeover | Plugin sandbox, MCP gateway, revocation | symbiont_inventory, symbiont_quota_usage | Symbiont-revocation test | Core |
| E-13 | Symbiosis / federation | Взаимный обмен услугами и данными между организмами | Federation manager | `FederationAgreement` | negotiate→authorize→exchange→settle→terminate | Data use и obligations аудируемы | Lock-in, asymmetric harm | Treaty, data-use policy, revocation | federation_exchange_total | Agreement audit | Conditional |
| E-14 | Horizontal transfer and reproductive isolation | Не допускать импорт artifacts между несовместимыми lineages без проверки | Import gate | `ImportDecision` + lineage compatibility | receive→verify provenance→check lineage compat→quarantine→admit/reject | Чужой artifact/skill/model не попадает в runtime без provenance и совместимости | Skill poisoning, incompatible semantics | Import quarantine, sandboxed trial, signature | import_rejected_total | Import-gate test | Conditional |
| E-15 | Competition | Справедливое распределение между tissues и organisms | Fair-share scheduler | `FairSharePolicy` | admit→allocate→preempt→account | Никто не превышает declared share | Starvation | Fair queues, quotas | share_utilization | Starvation test | Distributed |
| E-16 | Ecosystem treaty | Границы доверия между организмами | Treaty manager | `Treaty` | negotiate→attest→activate→monitor→revoke | Obligations, identity и expiry видимы | Treaty drift, transitive trust | mTLS, federation policy | treaty_active, treaty_violation_total | Treaty revocation test | Conditional |

## 8. Embodied-расширение (Embodied Profile)

| ID | Biological mechanism | Digital responsibility | Digital component | Contract | Protocol / State machine | Invariant | Failure mode | Security / safety control | Observability | Evidence | Profile |
|---|---|---|---|---|---|---|---|---|---|---|---|
| R-01 | Sensor fusion and calibration | Объединять сенсоры с оценкой неопределённости и калибровкой | Perception/fusion service | `Observation` + `CalibrationRecord` + covariance | sample→calibrate→validate→fuse→publish | Расхождение сенсоров переводит state в UNCERTAIN; calibration version указана | Drift, spoofing, ложное усреднение | Независимые сенсоры, calibration expiry, disagreement policy | calibration_age, sensor_disagreement | Calibration и fault-injection tests | Embodied |
| R-02 | Vision / audio / tactile perception | Модальное восприятие | Modality models | Typed feature/observation | capture→preprocess→infer→fuse | Raw/derived lineage сохранён | Model bias, occlusion, adversarial input | Adversarial-robustness checks, uncertainty | modality_confidence | Perception test set | Embodied |
| R-03 | Motor unit (actuator envelope) | Ограничить команды актуатору физическим envelope | Safety envelope validator | `ActuatorCommand(bounds, deadline, frame, preconditions)` | validate→interlock→execute→feedback | Просроченная или вне envelope команда не исполняется | Over-force, stale command | Независимый interlock, hard limits, watchdog | command_rejected_total | Test: expired/out-of-envelope rejected | Embodied |
| R-04 | Withdrawal reflex (safe stop) | Перевести систему в безопасное состояние независимо от LLM | Independent interlock | `embodied_safety` machine | ACTIVE→SAFE_STOP→LOCKED_OUT→INSPECTED→RESET_AUTHORIZED | E-stop и hard limits реализованы вне LLM и сети | Отказ interlock, ложный stop | Независимый watchdog, latched hazard | safe_stop_total, stop_latency | E-stop и watchdog test | Embodied |
| R-05 | Body schema and spatial frame | Версионированная модель тела, карты и зон | Spatial model | `FrameVersion`, geofence, no-go zones | localize→plan→verify-frame | Planning указывает использованную map/frame version | Stale map, wrong frame | Frame versioning, geofence enforcement | localization_confidence | Frame-staleness test | Embodied |

## Приложение A. Возможные стеки (не нормативно)

| ID | Механизм | Возможный стек |
|---|---|---|
| C-01 | Atoms/molecules | Protobuf, JSON Schema, WASM |
| C-02 | DNA / genome | Git/OCI, Sigstore, in-toto |
| C-03 | RNA / transcript | DAG engine, CEL/OPA |
| C-04 | Epigenetics | Feature flags, OPA, signed config |
| C-05 | DNA repair | Хэши, ECC, object versioning |
| C-06 | Nucleus | KMS/HSM, policy store, GitOps |
| C-07 | Nuclear pores | API gateway, mTLS, SPIFFE |
| C-08 | Nucleolus | SLSA, CI, OCI registry |
| C-09 | Ribosome | vLLM, ONNX, WASM |
| C-10 | Endoplasmic reticulum | CI, sandbox, type checker |
| C-11 | Unfolded-protein response (proteostasis) | Queues, circuit breaker, rate limits |
| C-12 | Golgi | Registry, SBOM, metadata service |
| C-13 | Vesicles | CloudEvents, NATS/Kafka, mTLS |
| C-14 | Cytoskeleton | Kubernetes scheduler, service mesh |
| C-15 | Motor proteins | Workflow engine, RDMA controls |
| C-16 | Mitochondria | GPU scheduler, cgroups, FinOps |
| C-17 | Peroxisomes | gVisor, Firecracker, seccomp |
| C-18 | Lysosomes | TTL, GC, WORM archive |
| C-19 | Autophagy | Dependency graph, GC |
| C-20 | Membrane | Envoy, API gateway, eBPF |
| C-21 | Receptors | Schema registry |
| C-22 | Endocytosis | WAF, AV, sandbox, DLP |
| C-23 | Exocytosis | DLP, transactional outbox |
| C-24 | Compartmentalization | Namespaces, cgroups, bulkhead pools |
| C-25 | Cell cycle | Admission controller, quotas |
| C-26 | Checkpoints | Policy engine, attestations |
| C-27 | Apoptosis | Leases, IAM revoke, orchestrator |
| C-28 | Necrosis | Leases, fencing tokens, supervisors |
| C-29 | Cellular stress response | Supervisors, circuit breakers |
| C-30 | Senescence | Deprecation policy, SBOM/EOL |
| T-01 | Gap junctions | Unix sockets, shared memory, mTLS |
| T-02 | Paracrine signals | Pub/sub topics, namespace ACL |
| T-03 | Tissue specialization | Deployments, pools, node groups |
| T-04 | Differentiation | Templates, RBAC, policy overlays |
| T-05 | Stem-cell niche | Golden images, offline registry |
| T-06 | Morphogenesis | IaC, GitOps, graph validator |
| T-07 | Extracellular matrix | AsyncAPI, OpenAPI, Protobuf |
| T-08 | Cell adhesion | Service discovery, SPIFFE |
| T-09 | Polarity | Network policy, CQRS |
| T-10 | Development / ontogeny | Progressive delivery |
| N-01 | Sensory receptor (sensory hierarchy) | OTLP, device drivers |
| N-02 | Proprioception | Asset inventory, attestation |
| N-03 | Nociception | Watchdog, kernel/audit events |
| N-04 | Thalamus (routing, attention/salience) | Routers, rules engine |
| N-05 | Cortex | LLM, planner, verifier |
| N-06 | Basal ganglia | OPA/Cedar, risk engine |
| N-07 | Motor hierarchy (actuation) | Tool gateway, outbox |
| N-08 | Cerebellum | Workflow engine, signed scripts |
| N-09 | Spinal reflex | Rules engine, RTOS/PLC |
| N-10 | Autonomic nerves | Operators, CronJob |
| N-11 | Peripheral ganglia (central vs peripheral control, distributed cognition) | Edge agents, capability tokens |
| N-12 | Working memory | In-memory store |
| N-13 | Episodic memory | Event store, object storage |
| N-14 | Semantic memory | RDBMS, graph, vector DB |
| N-15 | Procedural memory | Registry, CI, policy engine |
| N-16 | Memory consolidation (hippocampus) | Memory gateway, batch workflows |
| N-17 | Forgetting and memory decay | TTL, crypto-erasure, compaction |
| N-18 | Sleep / maintenance window | Checkpointing, batch workflows |
| N-19 | Circadian rhythm | Scheduler, monotonic timers |
| N-20 | Neuroplasticity | MLflow, model registry |
| N-21 | Synchronization and ordering | NTP/PTP, leases, consensus |
| M-01 | Blood / circulation | Kafka, NATS, RabbitMQ, gRPC |
| M-02 | Heart | Queue scheduler, load balancer |
| M-03 | Emergency circulation | Priority classes, separate queues |
| M-04 | Lymph (quarantine path) | Quarantine topics, sandbox |
| M-05 | Angiogenesis / vascularization | Autoscaler, SDN, IaC |
| M-06 | Respiratory exchange | GPU scheduler, power telemetry |
| M-07 | Digestion | ETL, content sandbox |
| M-08 | Liver (detox) | DLP, policy engine, data catalog |
| M-09 | Kidney (filtration) | TTL, quotas, compaction |
| M-10 | Osmoregulation | Autoscaling, backpressure |
| M-11 | Acid-base / electrolytes | Schema registry, version gates |
| M-12 | ATP (resource currency) | Quotas, metering, FinOps |
| M-13 | Fat / glycogen (reserve) | Warm pool, reserved capacity |
| M-14 | Nutrient and oxygen sensing | Quota/usage telemetry, FinOps |
| H-01 | Homeostasis (negative feedback) | Prometheus/OTel, controllers |
| H-02 | Positive feedback (bounded amplification) | Circuit breakers, rate limits |
| H-03 | Endocrine signaling (hormones) | Signed config, event bus |
| H-04 | Quorum sensing | Consensus, leases |
| H-05 | Redundant organs | Quorum, replicas, PDB |
| I-01 | Skin / mucosal barrier | WAF, gateway, network policy |
| I-02 | Blood-brain barrier | Broker, content isolation |
| I-03 | Self / non-self recognition (identity markers) | SPIFFE, OIDC, attestation |
| I-04 | Innate immunity | WAF, IDS, rate limits |
| I-05 | Antigen presentation | SIEM, detection pipeline |
| I-06 | Adaptive immunity | SIEM/SOAR, rule registry |
| I-07 | Immune memory | Threat-intel store, SOAR |
| I-08 | Immune tolerance | Workload identity, ABAC |
| I-09 | Complement cascade | SOAR, circuit breakers |
| I-10 | Inflammation | Dynamic logging, autoscaling |
| I-11 | Fever | Feature flags, policy overlay |
| I-12 | Coagulation | Network policy, kill switch |
| I-13 | Wound healing | Backup/restore, GitOps |
| I-14 | Regeneration | Golden image, signed backup |
| I-15 | Fibrosis / scarring | Debt register, policy exceptions |
| I-16 | Autoimmunity | Policy simulation, break-glass |
| I-17 | Oncogenesis | Quotas, attestation, anomaly detection |
| I-18 | Aging | SBOM, EOL policy, rotation |
| E-01 | Provenance | in-toto, SLSA, Sigstore |
| E-02 | Heredity / lineage | in-toto, OCI provenance |
| E-03 | Identity continuity | Trust root rotation, CA, SPIFFE federation |
| E-04 | State continuity and anti-resurrection | Hash chain, epoch fencing, tombstone registry |
| E-05 | Organism termination (death) | IAM revoke, WORM audit |
| E-06 | Organism-scale regeneration (catastrophic recovery) | Offline backups, IaC, HSM |
| E-07 | Reproduction | IaC, signed templates, CA |
| E-08 | Mutation | Experiment platform, sandbox |
| E-09 | Natural selection / evolutionary pressure | Eval harness, canary |
| E-10 | Genetic drift | GitOps, config drift detection |
| E-11 | Model / behavioral drift | Eval harness, monitoring |
| E-12 | Microbiome (host/guest boundary) | Plugin sandbox, MCP gateway |
| E-13 | Symbiosis / federation | OAuth/OIDC, contracts, audit |
| E-14 | Horizontal transfer and reproductive isolation | Registry policy, quarantine |
| E-15 | Competition | Fair queues, quotas |
| E-16 | Ecosystem treaty | Federation policy, mTLS |
| R-01 | Sensor fusion and calibration | ROS 2, Kalman-class filters |
| R-02 | Vision / audio / tactile perception | CV/audio models |
| R-03 | Motor unit (actuator envelope) | PLC, safety controller |
| R-04 | Withdrawal reflex (safe stop) | Safety PLC, hardware e-stop |
| R-05 | Body schema and spatial frame | ROS 2 TF, maps |

## Приложение B. Покрытие фундаментальных механизмов

Результат аудита полноты: каждый проверенный фундаментальный механизм либо имеет собственную строку, либо явно покрыт строкой, в чьём контракте он выражен. Механизмы, выражаемые как failure classes (poisoning, deadlock, split-brain и др.), приведены в `FAILURE_AND_RECOVERY.md`.

| Проверенный механизм | Строки реестра |
|---|---|
| Endocrine / hormonal signaling | H-03 |
| Immune memory | I-07 |
| Innate vs adaptive immunity | I-04, I-06 |
| Antigen / identity recognition | I-03, I-05 |
| Apoptosis vs necrosis | C-27, C-28 |
| Autophagy | C-19 |
| Lysosomal / waste processing | C-18, M-09 |
| Mitochondrial / energy management | C-16, M-12 |
| Nutrient sensing | M-14 |
| Oxygen / resource sensing | M-14, M-06 |
| Cellular stress response | C-29, C-11 |
| DNA repair | C-05 |
| Replication / reproduction | C-25, E-07 |
| Developmental checkpoints | C-26, T-10 |
| Stem-cell / regenerative pools | T-05, I-14 |
| Transport systems | M-01, C-13, C-15 |
| Vascularization / distribution | M-05, M-01 |
| Barrier systems | I-01, I-02, C-20 |
| Compartmentalization | C-24 |
| Signal propagation | T-02, H-03, M-01 |
| Feedback loops / negative feedback | H-01 |
| Positive feedback | H-02 |
| Redundancy | H-05 |
| Fault isolation | C-24, I-12, C-27 |
| Pathogen detection | I-04, I-05 |
| Mutation control | E-08, C-05 |
| Genetic drift | E-10 |
| Selection / evolutionary pressure | E-09 |
| Reproductive isolation | E-14 |
| Symbiotic dependency | E-12, E-13 |
| Host / guest boundaries | E-12 |
| Ecological resource competition | E-15 |
| Behavioral adaptation | N-20 |
| Learning consolidation | N-16, N-18 |
| Memory decay / forgetting | N-17 |
| Attention / salience | N-04 |
| Reflex arcs | N-09 |
| Central vs peripheral control / distributed cognition | N-11 |
| Sensory hierarchy | N-01 |
| Motor hierarchy | N-07 |
| Coordination / synchronization | H-04, N-21 |
| Developmental stages / maturation | T-10, C-26 |
| Senescence / aging | C-30, I-18 |
| Death / termination | C-27, E-05 |
| Inheritance / lineage / ancestry | E-02 |
| Provenance | E-01 |
| Identity continuity | E-03 |
| State continuity | E-04 |
| Regeneration after catastrophic failure | E-06 |

## Приложение C. Что реестр не утверждает

- что цифровая система биологически жива, обладает сознанием или биологической точностью;
- что у механизма есть единственный допустимый IT-аналог;
- что добавление механизмов улучшает систему без evidence: механизмы без архитектурной необходимости оставлены уровнем `Pattern` или не включены;
- что реестр заменяет domain safety, regulation, threat model или hazard analysis.
