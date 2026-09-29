# Biology-to-IT Mapping Registry

## Правило чтения

Каждая строка является минимальной нормативной карточкой механизма. `Contract` означает проверяемый интерфейс или policy object; `Protocol` — допустимые состояния/переходы; `Invariant` — условие, которое MUST быть наблюдаемо. Стек приведён как возможный, не обязательный.

## 1. Молекулярный и клеточный уровень

| Механизм | System responsibility / digital component | Contract | State machine / protocol | Observability invariant | Failure modes | Security implications | Возможный стек |
|---|---|---|---|---|---|---|---|
| Атомы/молекулы | типизированные immutable values и pure transforms | schema + hash + units | parse→validate→transform→emit | одинаковый input/version даёт одинаковый output | type confusion, overflow, nondeterminism | parser abuse, deserialization | Protobuf, JSON Schema, WASM |
| DNA / genome | signed desired state | `GenomeManifest` | draft→validated→signed→active→superseded | active digest известен каждому компоненту | drift, corruption, incompatible version | unauthorized mutation | Git/OCI, Sigstore, in-toto |
| RNA / transcript | request-scoped executable plan | `ExecutionTranscript` | resolve→authorize→bind→execute→expire | transcript связан с genome+intent | stale plan, context loss | injected plan, confused deputy | DAG engine, CEL/OPA |
| Epigenetics | reversible expression overlays | `PolicyOverlay` with scope/TTL | proposed→approved→active→expired/revoked | effective config reconstructable | overlay conflict, sticky flag | privilege amplification | feature flags, OPA, signed config |
| DNA repair | integrity detection and repair | `RepairCase` + trusted source | detect→arrest→compare→repair→verify | no repaired artifact promoted unverified | silent corruption, wrong repair source | malicious rollback | hashes, ECC, object versioning |
| Nucleus | protected authority/configuration domain | `NuclearAPI` | sealed→readable→change-request→commit | writes only via authorized change path | split brain, unavailable authority | crown-jewel compromise | KMS/HSM, policy store, GitOps |
| Nuclear pores | controlled config import/export | capability-scoped request | authenticate→authorize→filter→transfer | every transfer audited | bypass, stale grant | exfiltration, policy injection | API gateway, mTLS, SPIFFE |
| Nucleolus | build/assembly of execution machinery | signed `RuntimeBundle` | source→build→scan→attest→publish | running runtime has provenance | poisoned build, nonreproducible bundle | supply-chain attack | SLSA, CI, OCI registry |
| Ribosome | compile/bind plan into executable work | `TaskBinding` | queued→compiled→loaded→running→done | artifact/model version attached to task | compile error, wrong target | unsafe code generation | vLLM, TensorRT-LLM, ONNX, WASM |
| ER | folding/quality control of artifacts and workflows | `QualityGateResult` | synthesize→fold→inspect→pass/refold/reject | invalid artifact cannot reach Golgi | bad schema, dependency mismatch | malicious payload disguised as artifact | CI, sandbox, type checker |
| Unfolded-protein response | backpressure and degraded synthesis | `ProteostasisSignal` | normal→stress→throttle→recover/escalate | stress has TTL and resolution | retry storm, permanent throttle | denial of service | queues, circuit breaker, rate limits |
| Golgi | package, label, version and route artifacts | `ArtifactEnvelope` | receive→enrich→classify→sign→dispatch | destination/classification preserved | misrouting, wrong label | data leak, artifact substitution | registry, SBOM, metadata service |
| Vesicles | bounded intracellular delivery | signed envelope + destination | create→seal→transport→ack/expire | no unsealed cross-compartment payload | loss, duplicate, reorder | tampering/replay | CloudEvents, NATS/Kafka, mTLS |
| Cytoskeleton | topology, placement and execution scaffolding | `PlacementConstraint` | discover→place→monitor→relocate | placement satisfies declared constraints | hotspot, collapse, drift | co-location side channel | Kubernetes scheduler, service mesh |
| Motor proteins | work/data movement along known routes | `TransferJob` | reserve→move→verify→commit | checksum and destination ack | partial copy, stuck transfer | path traversal, interception | workflow engine, DMA/RDMA controls |
| Mitochondria | compute/energy conversion | `ResourceBudget` | reserve→consume→account→release | all work charged to budget | exhaustion, thermal/power limit | cryptomining/resource theft | GPU scheduler, cgroups, FinOps |
| Peroxisomes | isolate hazardous transforms/detox | `SandboxJob` | ingest→isolate→transform→inspect→release | hazardous work never runs outside sandbox | escape, toxic residue | malware/code execution | gVisor, Firecracker, seccomp |
| Lysosomes | classify and dispose stale/corrupt material | `DisposalRecord` | detect→classify→hold→destroy/archive | forensic evidence not auto-destroyed | premature deletion, leak | secure deletion/audit destruction | TTL, GC, WORM archive |
| Autophagy | recycle internal obsolete components | `MaintenanceCandidate` | inventory→isolate→verify-unused→recycle | protected/live dependency not removed | dependency break, cache thrash | attacker-induced cleanup | dependency graph, GC |
| Membrane | cell trust boundary | `Ingress/EgressDecision` | inspect→allow/deny/throttle/quarantine | no unmediated boundary crossing | bypass, overload | primary enforcement point | Envoy, API gateway, eBPF |
| Receptors | typed signal recognition | versioned receptor schema | bind→validate→normalize→signal | unknown types rejected/quarantined | spoofing, desensitization | input attack | schema registry, authn/authz |
| Endocytosis | safe ingress packaging | `IngressEnvelope` | authn→scan→normalize→seal→route | raw input never becomes trusted memory directly | parser bomb, contamination | prompt/malware injection | WAF, AV, sandbox, DLP |
| Exocytosis | governed egress/action | `EgressRequest` | authorize→redact→sign→deliver→receipt | side effect maps to approved intent | duplicate action, leakage | exfiltration, forged output | DLP, transactional outbox |
| Cell cycle | controlled creation/replication | `CellAdmission` | G0→admitted→provisioned→ready→replicate/stop | replicas never exceed policy/quota | runaway scaling, immature cell | uncontrolled persistence | admission controller, quotas |
| Checkpoints | integrity/readiness gates | `CheckpointEvidence` | evaluate→pass/hold/repair/apoptosis | no phase advance on failed gate | false pass, deadlock | gate bypass | policy engine, attestations |
| Apoptosis | bounded safe termination | `TerminationPlan` | suspect→isolate→revoke→snapshot→terminate | terminated cell has no active grant | zombie, cascade kill | evidence loss, sabotage | leases, IAM revoke, orchestrator |
| Senescence | contain aging component | `SenescencePolicy` | active→aging→restricted→replaced→retired | senescent cell cannot replicate/escalate | stale dependency, SASP-like noise | vulnerable legacy foothold | deprecation policy, SBOM/EOL |

## 2. Ткани, развитие и коммуникация

| Механизм | System responsibility / digital component | Contract | State machine / protocol | Observability invariant | Failure modes | Security implications | Возможный стек |
|---|---|---|---|---|---|---|---|
| Gap junctions | low-latency neighbor communication | local typed channel | connect→exchange→close | peer identity and rate visible | coupling/cascade | lateral movement | Unix sockets, shared memory, mTLS |
| Paracrine signals | local scoped broadcast | `LocalSignal(scope,ttl)` | publish→fanout→expire | reception limited to tissue scope | spillover, storm | unauthorized influence | pub/sub topics, namespace ACL |
| Endocrine signals | global mode modulation | `HormoneSignal` | issue→propagate→act→decay/revoke | signed signal always expires | chronic mode, contradictory signals | platform-wide policy abuse | signed config, event bus |
| Quorum sensing | density/load-aware collective action | `QuorumObservation` | sample→threshold→coordinate→release | decision includes membership epoch | split brain, herd effect | Sybil agents | consensus, leases, rate limits |
| Tissue specialization | homogeneous service role | `TissueProfile` | recruit→differentiate→serve→renew | all members satisfy same SLO/policy | skew, monoculture failure | shared exploit | deployments, pools, node groups |
| Differentiation | least-privilege specialization | signed expression profile | stem→candidate→trained→verified→specialized | capability increase has admission evidence | wrong role, irreversible drift | privilege escalation | templates, RBAC, policy overlays |
| Stem-cell niche | trusted capacity for regeneration | `SeedArtifact` | dormant→activated→instantiate→replenish | seed is clean, signed and unused for normal traffic | seed corruption, exhaustion | persistence target | golden images, offline registry |
| Morphogenesis | topology construction | `TopologyPlan` | blueprint→stage→connect→validate→mature | topology matches declared graph | missing organ, wrong wiring | hidden control path | IaC, GitOps, graph validator |
| Extracellular matrix | contracts and structural context | schema/interface registry | propose→review→publish→deprecate | runtime interfaces resolve to compatible versions | contract erosion | malicious schema/version squatting | AsyncAPI, OpenAPI, Protobuf |
| Cell adhesion | membership and service discovery | identity-bound endpoint lease | join→healthy→discoverable→drain→leave | only ready cells discoverable | stale endpoint | impersonation | service discovery, SPIFFE |
| Polarity | directional ingress/egress separation | port/role policy | receive-side→process→send-side | direction violations observable | feedback loop, wrong-way traffic | egress bypass | network policy, CQRS |
| Angiogenesis | capacity/network expansion | `CapacityRequest` | detect demand→risk check→provision→connect→trim | new path respects boundary/policy | cost explosion, shadow network | ungoverned connectivity | autoscaler, SDN, IaC |
| Development/ontogeny | staged maturation | `DevelopmentStage` | embryo→juvenile→mature→aging→retired | stage-specific gates pass | premature exposure | immature controls | progressive delivery, environments |

## 3. Нервная, сенсорная и обучающая системы

| Механизм | System responsibility / digital component | Contract | State machine / protocol | Observability invariant | Failure modes | Security implications | Возможный стек |
|---|---|---|---|---|---|---|---|
| Sensory receptor | acquire calibrated observation | `Observation(value,unit,time,uncertainty)` | sample→calibrate→validate→publish | freshness and uncertainty present | drift, blindness, hallucinated sensor | sensor spoofing | device drivers, OTLP, signed telemetry |
| Vision/audio/tactile | modality-specific perception | typed feature/observation | capture→preprocess→infer→fuse | raw/derived lineage retained | model bias, occlusion | adversarial examples | CV/audio models, sensor fusion |
| Proprioception | self-state inventory | `SelfStateSnapshot` | poll→reconcile→publish | inventory reconciles with runtime | stale topology | hidden implant | asset inventory, runtime attestation |
| Nociception | fast local damage signal | `DamageSignal` | detect→reflex→escalate→resolve | high-severity damage bypasses slow planner | alert fatigue, false pain | induced shutdown | watchdog, kernel/audit events |
| Thalamus | input routing/filtering | `RouteDecision` | classify→prioritize→route/drop | every accepted input has route reason | bottleneck, misroute | censorship/injection | routers, rules engine |
| Cortex | semantic reasoning/planning | `PlanProposal` | perceive→hypothesize→plan→verify | proposal is not authority grant | hallucination, loop | prompt injection | LLM, planner, verifier |
| Basal ganglia | action selection | `ActionDecision` | candidates→policy/risk/resource→select | selected action has decision evidence | unsafe selection | confused deputy | OPA/Cedar, risk engine |
| Cerebellum | proceduralized validated skills | `SkillArtifact` | observe repeats→compile→test→promote | skill version/outcome measured | brittle automation | poisoned skill | workflow engine, signed scripts |
| Spinal reflex | deterministic low-latency response | `ReflexRule` | trigger→guard→act→report | bounded latency and action envelope | oscillation, stale rule | rule abuse | rules engine, RTOS/PLC |
| Autonomic nerves | background maintenance | lease/maintenance contract | schedule→execute→verify→renew | maintenance cannot silently fail | resource leak, thundering herd | maintenance backdoor | controllers, CronJob, operators |
| Working memory | request-local state | scoped scratch record | create→use→expire | TTL and task binding present | leakage, overflow | cross-tenant context | in-memory store, encrypted cache |
| Episodic memory | event/outcome history | provenance-rich episode | append→validate→retain→expire | immutable chronology, correction by supersession | false episode | audit poisoning | event store, object storage |
| Semantic memory | curated facts/relations | fact+source+confidence | ingest→verify→index→supersede | answer traceable to sources | stale/contradictory fact | knowledge poisoning | RDBMS, graph, vector DB |
| Procedural memory | skills/workflows | signed skill manifest | draft→test→approve→active→retire | only approved skill executable | obsolete procedure | supply-chain attack | registry, CI, policy engine |
| Neuroplasticity | change routing/weights/skills | `AdaptationProposal` | observe→train→evaluate→canary→promote/rollback | baseline and delta comparable | catastrophic forgetting, drift | reward poisoning | MLflow, feature/model registry |
| Sleep/consolidation | offline maintenance and memory compaction | `MaintenanceWindow` | active→quiesce→consolidate→validate→wake | no lost accepted work; wake revalidates policy | missed wake, corrupt checkpoint | maintenance exposure | checkpointing, batch workflows |
| Circadian rhythm | temporal policy and capacity cycles | `TemporalPolicy` | schedule→prepare→activate→decay | timezone/missed tick recorded | clock drift, wrong seasonality | timing side channel | scheduler, monotonic timers |

## 4. Circulation, metabolism и excretion

| Механизм | System responsibility / digital component | Contract | State machine / protocol | Observability invariant | Failure modes | Security implications | Возможный стек |
|---|---|---|---|---|---|---|---|
| Blood/circulation | shared event/data transport | `EventEnvelope` | publish→persist→deliver→ack/dead-letter | lag, loss, duplicates and pressure visible | congestion, partition | traffic manipulation | Kafka, NATS, RabbitMQ, gRPC |
| Heart | flow scheduling/backpressure | `FlowPolicy` | normal→pressure→shed/prioritize→recover | critical flow retains minimum capacity | arrhythmia/oscillation | priority abuse | queue scheduler, load balancer |
| Emergency circulation | preserve vital control traffic | `EmergencyFlowProfile` | trigger→reserve→shed→stabilize→restore | identity/safety/audit paths remain live | starvation, false emergency | denial via emergency mode | priority classes, separate queues |
| Lymph | quarantine/validation side path | `QuarantineCase` | divert→analyze→release/reject/archive | suspicious data never rejoins unverified | backlog, leakage | sandbox escape | quarantine topics, sandbox |
| Respiratory exchange | acquire compute capacity/remove heat/load | `CapacityEnvelope` | demand→admit→allocate→cool/release | saturation, power, thermal headroom observed | throttling, thermal shutdown | resource hijack | GPU scheduler, power telemetry |
| Digestion | decode/parse/chunk input | `IngestionJob` | receive→scan→parse→normalize→emit | rejected/accepted bytes accounted | parser bomb, semantic loss | malicious documents | ETL, content sandbox |
| Liver | transform/detox/classify | `SanitizationResult` | inspect→redact→classify→enrich→release | raw sensitive data not exposed downstream | over-redaction, missed toxin | PII leak | DLP, policy engine, data catalog |
| Kidney | filter waste and regulate pools | `FiltrationPolicy` | sample→retain/excrete→balance→report | storage/queue watermarks within bounds | retention breach, data loss | attacker-triggered purge | TTL, quotas, compaction |
| Osmoregulation | keep queue/cache/pool balance | `WatermarkPolicy` | normal→high/low→actuate→hysteresis→normal | upper/lower thresholds and action visible | oscillation, starvation | quota evasion | autoscaling, backpressure |
| Acid-base/electrolytes | preserve protocol/config compatibility | `CompatibilityInvariant` | detect imbalance→buffer→migrate/reject | compatible versions/ranges maintained | version poisoning | downgrade attack | schema registry, version gates |
| ATP | normalized resource currency | `ResourceCharge` | reserve→spend→settle/refund | task cost attributable | unbounded spend | billing abuse | quotas, metering, FinOps |
| Fat/glycogen | reserve capacity | `ReservePolicy` | accumulate→hold→release→replenish | reserve not consumed by routine load | stranded capacity | reserve theft | warm pool, reserved capacity |

## 5. Immunity, barriers, repair и aging

| Механизм | System responsibility / digital component | Contract | State machine / protocol | Observability invariant | Failure modes | Security implications | Возможный стек |
|---|---|---|---|---|---|---|---|
| Skin/mucosal barrier | layered external boundary | `BoundaryPolicy` | inspect→deny/allow→monitor | all external paths inventoried | unknown ingress | perimeter bypass | WAF, gateway, network policy |
| Blood-brain barrier | protect high-trust cognition/memory | `PrivilegedIngress` | request→sanitize→broker→limited context | raw external content cannot directly alter authority | context poisoning | prompt injection | broker, content isolation |
| Innate immunity | fast generic defense | `InnateRule` | detect→contain→signal→expire | response bounded and logged | false positive, evasion | signature/rule bypass | WAF, IDS, rate limits |
| Antigen presentation | convert evidence to reviewable indicator | `FindingEvidence` | collect→normalize→correlate→present | finding links to immutable evidence | fabricated evidence | alert poisoning | SIEM, detection pipeline |
| Adaptive immunity | learned verified defense | `DetectionPolicyVersion` | learn→validate→deploy→monitor→retire | new rule measured for precision/recall | overfit, stale IOC | training poisoning | SIEM/SOAR, rule registry |
| Immune tolerance | bounded trust for self/partner | `ToleranceGrant` | prove identity→grant→monitor→revoke/expire | exception has owner, scope, expiry | permissive exception | supply-chain trust abuse | workload identity, ABAC |
| Complement cascade | amplified coordinated containment | `ResponsePlaybook` | trigger→amplify→contain→stop | cascade has rate/stop condition | runaway response | attacker-induced outage | SOAR, circuit breakers |
| Inflammation | temporary defensive resource boost | `InflammationSignal` | local→amplified→resolution/chronic | TTL and resolution criterion present | chronic degradation | resource exhaustion | dynamic logging, autoscaling |
| Fever | bounded global operating-mode shift | `EmergencyMode` | detect→raise controls→monitor→cool down | max duration and safe ceiling enforced | damage from prolonged mode | emergency abuse | feature flags, policy overlay |
| Coagulation | rapid breach/partition sealing | `SealRule` | damage→local deny→isolate→repair→reopen | sealed scope minimal and explicit | thrombosis/deadlock | malicious segmentation | network policy, kill switch |
| Wound healing | restore service after damage | `RecoveryPlan` | hemostasis→cleanup→rebuild→remodel→verify | RTO/RPO and post-repair checks | scar/technical debt | reinfection | backup/restore, GitOps |
| Regeneration | reconstruct lost component from trusted seed | `RegenerationRequest` | verify loss→instantiate→restore→validate→join | regenerated cell attested before traffic | bad seed, state divergence | persistence cloning | golden image, signed backup |
| Fibrosis/scarring | safe but degraded permanent workaround | `ExceptionDebt` | emergency patch→document→limit→remove | workaround has owner/expiry | permanent brittleness | bypass becomes permanent | debt register, policy exception |
| Autoimmunity | anti-pattern: defense attacks valid self | false-positive budget | detect→suspend rule→review→repair | legitimate availability tracked against controls | systemic denial | internal DoS | policy simulation, break-glass |
| Oncogenesis | anti-pattern: replication/privilege/resource capture | growth/capability invariants | detect→freeze→isolate→revoke→eradicate | replication and grants within declared limits | hidden clones, apoptosis resistance | persistence/escalation | quotas, attestation, anomaly detection |
| Aging | accumulated drift/dependency decay | `AgingIndex` | measure→maintain→senesce→replace | unsupported components enumerated | correlated obsolescence | known-vulnerability exposure | SBOM, EOL policy, rotation |

## 6. Organ systems, ecology и reproduction

| Механизм | System responsibility / digital component | Contract | State machine / protocol | Observability invariant | Failure modes | Security implications | Возможный стек |
|---|---|---|---|---|---|---|---|
| Endocrine axis | multi-organ mode control | `HormoneSignal` | issue→bind→feedback→decay | feedback shows intended effect | contradictory axes | global config compromise | event bus, policy controller |
| Homeostasis | closed-loop regulation | `ControlLoopSpec` | sample→compare→act→settle/escalate | target, error and action correlated | oscillation, sensor/actuator fault | metric manipulation | Prometheus/OTel, controllers |
| Redundant organs | availability across failure domains | `RedundancyPolicy` | primary→degraded→failover→reintegrate | failover readiness tested | common-mode failure | standby compromise | quorum, replicas, PDB/topology |
| Microbiome | bounded auxiliary ecosystem | `SymbiontContract` | discover→vet→grant→monitor→revoke | each symbiont attributable and quota-bound | dependency takeover | third-party risk | plugin sandbox, MCP gateway |
| Symbiosis | reciprocal service/data exchange | `FederationAgreement` | negotiate→authorize→exchange→settle→terminate | data use and obligations auditable | lock-in, asymmetric harm | federation abuse | OAuth/OIDC, contracts, audit |
| Competition | fair scheduling among tissues/organisms | `FairSharePolicy` | admit→allocate→preempt→account | no tenant exceeds declared share | starvation | priority escalation | fair queues, quotas |
| Reproduction | controlled creation of new organism | signed `ReproductionPlan` | propose→approve→seed→differentiate→independent identity | offspring receives new identity and lineage | clone storm | propagation of compromise | IaC, signed templates, CA |
| Heredity | transmit validated genome/artifacts | `LineageManifest` | select→package→sign→verify→instantiate | lineage chain complete | inherited defect | supply-chain persistence | in-toto, OCI provenance |
| Mutation | proposed bounded variant | `VariantProposal` | mutate→simulate→evaluate→approve/reject | mutation never edits production directly | unsafe phenotype | policy evasion | experiment platform, sandbox |
| Natural selection | governed portfolio evaluation | multi-objective scorecard | cohort→test→compare→promote/retire | safety constraints dominate reward | Goodhart, monoculture | reward hacking | eval harness, canary |
| Ecosystem treaty | cross-organism trust and limits | `Treaty` | negotiate→attest→activate→monitor→revoke | obligations, identity and expiry visible | treaty drift | transitive trust | federation policy, mTLS |

## 7. Обязательная локальная детализация

Implementation MUST расширить каждую используемую строку конкретными schema IDs, owners, SLO thresholds, action limits и test evidence. Этот реестр не разрешает автоматически какой-либо stack и не заменяет threat/hazard analysis.
