# DOA Conformance

**Версия:** DOA v1.0 (`DOA-FS-1.0`). Нормативный документ.

Соответствие DOA определяется **доказательствами**, а не упоминанием «DOA» в документации. Наличие термина, диаграммы или аналогии не является conformance claim.

## 1. Профили

| Профиль | Что добавляет |
|---|---|
| Core | идентичность, boundary, genome/epigenome, lifecycle, homeostasis, immunity, accounting, memory, observability, recovery, aging, termination |
| Distributed | event contract, partial failure, topology, quorum/failover, clocks, drift, catastrophic recovery |
| Adaptive | learning/evolution governance, drift detection, lineage вариантов, measured learned defenses |
| Embodied | physical safety, real-time budget, calibration, actuator envelope, reset authority |
| Conditional | controls для возможностей reproduction, federation, horizontal transfer (либо их явный запрет) |

Каждый claim MUST включать Core. Строки `Core`/профильного уровня в `BIOLOGY_TO_IT_MAPPING.md` реализуются через requirements ниже.

## 2. Реестр требований

Источник истины — `specifications/requirements.yaml`. Таблица ниже отражает его (согласованность проверяется валидатором).

Способы проверки: `schema` — проверяется машинно по схемам `specifications/`; `test` — документированный выполненный тест с воспроизводимым результатом; `inspection` — документированный review артефакта.

| ID | Profile | Requirement | Mappings | Evidence | Verification |
|---|---|---|---|---|---|
| REQ-CORE-01 | Core | **Identity of every action.** Every action, event and side effect MUST be attributable to a verifiable subject, component and version. | I-03, E-03 | Identity inventory and sample audit trace linking action to subject, component and artifact digest. | inspection |
| REQ-CORE-02 | Core | **Declared organism boundary.** The genome MUST declare ingress, egress and external dependencies; all boundary crossings MUST pass policy enforcement. | C-20, I-01, I-02, C-07, C-21, C-22, C-23 | Genome `spec.boundary`, boundary inventory, and bypass test results. | schema |
| REQ-CORE-03 | Core | **Desired/observed separation.** A signed genome MUST define desired state; telemetry MUST define observed state; a reconciler MUST link them. | C-02, N-02, C-03, T-07 | Signed genome with digest, reconciliation log showing drift detection. | schema |
| REQ-CORE-04 | Core | **Genome/epigenome separation.** Runtime policy changes MUST be expressed as expiring, signed overlays that cannot increase authority; the effective policy MUST be reconstructable. | C-04 | PolicyOverlay records and effective-policy snapshot (`organism.effective_policy`). | schema |
| REQ-CORE-05 | Core | **Least capability and attenuation.** Capabilities MUST be narrow, expiring, revocable CapabilityGrants; delegated grants MUST be a subset of the parent grant with bounded depth. | N-06, N-11, I-17, T-04 | CapabilityGrant samples, deny tests, delegation-depth test. | test |
| REQ-CORE-06 | Core | **No unilateral self-modification.** Runtime components MUST NOT modify the canonical genome, policies or their own authority directly. | C-06, C-02 | Access-policy test showing runtime write to genome/policy store is rejected. | test |
| REQ-CORE-07 | Core | **Closed-loop homeostasis.** Each regulated domain MUST have a ControlLoopSpec with sensor freshness, target range, controller, limits, escalation, recovery and manual override; positive-feedback paths MUST declare ceiling and TTL. | H-01, H-02, H-03, M-14 | ControlLoopSpec records and alert-to-action traces for resource, memory, latency, agent/tool failure, security, dependency and model-quality domains. | schema |
| REQ-CORE-08 | Core | **Compartmentalization.** Failure domains MUST be declared and enforced so that one cell failure does not automatically become organism failure. | C-24, T-03 | Failure-domain declaration and a cell-kill test with unaffected neighbour SLOs. | test |
| REQ-CORE-09 | Core | **Provenance.** Data, models, policies, memories and artifacts admitted to trusted paths MUST have source, time, integrity and classification. | E-01, C-08, N-16, C-10, M-07 | Provenance-gap test; MemoryRecord and artifact attestations. | test |
| REQ-CORE-10 | Core | **Reversibility.** Every rollout, adaptation and recovery action MUST have a validation step and a rollback or containment path outside the failing control path. | I-13, I-14 | Restore and rollback test results. | test |
| REQ-CORE-11 | Core | **Observable lifecycle.** Organism and cell state transitions MUST follow specifications/state-machines.yaml and emit lifecycle-transition events with guard evidence and authority. | T-10, C-25, C-26 | State-transition logs validating against lifecycle-transition.schema.json and the canonical machines. | schema |
| REQ-CORE-12 | Core | **Human authority.** High-impact side effects MUST have a defined authority model and approval boundary; break-glass actions MUST be time-bounded and audited. | N-06, N-07 | Authority matrix and a denied/approved high-impact action trace. | inspection |
| REQ-CORE-13 | Core | **Truthful uncertainty.** Absence of a signal MUST be treated as UNKNOWN, not healthy; liveness MUST NOT be reported as correctness. | N-01, N-03 | HealthEvidence samples including UNKNOWN and stale-signal test. | test |
| REQ-CORE-14 | Core | **Immune response lifecycle.** Security incidents MUST follow the incident machine (detect, identify, contain, quarantine, neutralize, recover, learn, update defenses) and quarantine MUST work without cooperation of the subject. | I-03, I-04, I-05, I-08, I-10, I-12, M-04, C-17 | Incident record for a controlled exercise and a quarantine test against an uncooperative cell. | test |
| REQ-CORE-15 | Core | **Bounded termination (apoptosis).** Cell and organism termination MUST follow the bounded protocol, leave no live grants, endpoints or replicas, and emit a terminal record. | C-27, E-05 | Apoptosis test and terminal record (`lifecycle-transition.terminal_record`). | test |
| REQ-CORE-16 | Core | **Uncontrolled failure containment (necrosis).** Lost or crashed cells MUST be fenced by lease expiry, their grants revoked, and duplicate side effects prevented by idempotency. | C-28, C-29 | Crash-injection test showing fencing latency and revoked grants. | test |
| REQ-CORE-17 | Core | **Growth control.** Cell count, spawn depth, spawn rate and delegation depth MUST be bounded by genome `growth_control`; grant issuer and enforcer MUST be separate; orphans MUST be detected by lease. | C-25, I-17, N-11 | Runaway-spawn test, admission rejection log, orphan-lease report. | test |
| REQ-CORE-18 | Core | **Resource accounting.** Work performed or authorized by the organism MUST be reserved and charged against a budget (reserved accounting); consumption known only from external telemetry (observed accounting) SHOULD be recorded with its source and uncertainty and MUST NOT be reported as reserved; resource scarcity MUST gate growth. | C-16, M-12, M-14, M-09 | Accounting reconciliation report that separates reserved from observed accounting and, where observed figures exist, states their source and uncertainty (claim field `observed_accounting`), and scarcity-gating test. | test |
| REQ-CORE-19 | Core | **Memory governance.** Memory MUST be typed (working, episodic, semantic, procedural), carry provenance, confidence, retention and consent, and support decay, supersession and verified erasure. | N-12, N-13, N-14, N-15, N-16, N-17, C-18 | MemoryRecord samples, consolidation log, erasure test. | schema |
| REQ-CORE-20 | Core | **Recovery taxonomy.** Each organ MUST declare permitted recovery modes (RESTART, RESTORE, REPAIR, REPLACE, REGENERATE, REBUILD, RECONFIGURE, ROLLBACK); recovery MUST NOT clone corrupted observed state or credentials. | C-05, T-05, I-13, I-14 | Organ `recovery.modes`, restore drill, repair-source independence evidence. | schema |
| REQ-CORE-21 | Core | **Aging and senescence.** The organism MUST compute an AgingIndex, move aged components to a restricted senescent state and replace or retire them. | C-30, I-18 | Genome `aging`, aging report, senescence-to-replacement record. | schema |
| REQ-CORE-22 | Core | **Identity continuity and anti-resurrection.** Identity MUST persist across component replacement via signed continuity records, and terminated or revoked entities MUST NOT be restorable from stale state. Continuity records and tombstones apply to identities the organism issues. Identities and credentials issued by others SHOULD be declared as external dependencies and mapped to the organism's own identity; credentials or sessions of others found in restored state MUST be treated as unverified and MUST NOT be used until their external status is verified. | E-03, E-04, E-02 | Component-replacement test, restore-after-tombstone rejection test and, where identities of others exist, a restore test showing that restored external credentials stay unusable until their external status is verified. | test |
| REQ-CORE-23 | Core | **Failure-class coverage.** Each applicable class in docs/FAILURE_AND_RECOVERY.md MUST have documented detection, containment, recovery and verification, or a justified exclusion. | C-24, H-05, I-12 | Failure-class coverage table for the implementation with test references; a claim MAY reference classes by id in `failure_classes`. | inspection |
| REQ-CORE-24 | Core | **Audit and secret hygiene.** Audit records MUST be tamper-evident, survive loss of the ordinary data plane where feasible, and MUST NOT contain secrets or unrestricted reasoning traces. | I-05, M-08 | Audit-store design, secret-scan result over audit samples. | test |
| REQ-CORE-25 | Core | **Microbiome (guest) governance.** Third-party plugins, tools and agents MUST be admitted as bounded symbionts with identity, quota and revocation, and MUST NOT acquire organ privileges. | E-12, I-03 | Symbiont inventory, quota configuration, revocation test. | test |
| REQ-CORE-26 | Core | **Separation of cognition and authority.** Cognitive output (including any LLM) MUST be a proposal; routing and salience MUST NOT raise the authority of a source; no single model may be sole proposer, policy authority, executor and verifier of a high-impact action. | N-04, N-05, N-06, N-07 | Decision-flow diagram, test that a plan without a grant is not executed, test that high salience does not bypass policy. | test |
| REQ-DIST-01 | Distributed | **Event contract and delivery semantics.** Events MUST use EventEnvelope; delivery semantics, ordering scope, idempotency and TTL MUST be declared; consumers MUST validate schema, identity, freshness and authorization. | M-01, C-13, M-11, T-02 | Delivery-semantics declaration, duplicate/replay test. | test |
| REQ-DIST-02 | Distributed | **Partial failure, backpressure and emergency flow.** Backpressure, load shedding and emergency circulation MUST preserve identity, safety, audit and recovery traffic. | C-11, M-03, M-06 | Overload drill showing vital flow latency. | test |
| REQ-DIST-03 | Distributed | **Topology and failure-domain placement.** Critical organs MUST be placed across independent failure domains; placement drift MUST be detected. | C-14, T-06, T-08 | Declared-vs-observed topology report. | schema |
| REQ-DIST-04 | Distributed | **Quorum, failover and split-brain handling.** Quorum and failover MUST use membership epochs and fencing; split-brain MUST be detected and resolved by a declared rule. | H-04, H-05, N-21 | Partition and failover drills with epoch logs. | test |
| REQ-DIST-05 | Distributed | **Clock and synchronization assumptions.** Clock source, skew tolerance, event-time vs processing-time and late-event policy MUST be declared and tested. | N-21, N-19 | Skew-injection test. | test |
| REQ-DIST-06 | Distributed | **Genetic drift detection.** Replica and lineage divergence from the signed genome MUST be detected and reconciled from a trusted source. | E-10, C-05 | Divergence-injection test. | test |
| REQ-DIST-07 | Distributed | **Catastrophic recovery.** A catastrophic recovery path from a seed outside the failure domain MUST exist, with human authority, epoch increment and identity continuity decision. | E-06, T-05, E-04 | Catastrophic recovery drill report. | test |
| REQ-ADPT-01 | Adaptive | **Learning is not evolution.** Learning MUST be confined to declared adaptive parameters and MUST NOT modify the genome, invariants, authority model or audit semantics; evolution (genome change) MUST use the change machine with class=evolution. | N-20, E-08 | Genome `adaptation.learning_bounds` and a test rejecting out-of-bound learning. | schema |
| REQ-ADPT-02 | Adaptive | **Governed change protocol.** Every adaptation MUST pass the change machine with canary and rollback. | N-20, E-08, E-09, N-08 | Change-protocol state logs for at least one promoted and one rolled-back change. | test |
| REQ-ADPT-03 | Adaptive | **Separation of proposer, evaluator and approver.** Proposer, evaluator and approver of a change MUST be distinct authorities. | E-09, N-06 | Genome `adaptation.separation_of_duties` and approval records. | schema |
| REQ-ADPT-04 | Adaptive | **Evaluation-set governance.** Evaluation sets MUST be versioned, provenance-tracked and protected from the proposer. | E-09, E-01 | Evaluation-set registry and access policy. | inspection |
| REQ-ADPT-05 | Adaptive | **Drift detection and reward-hacking resistance.** Model/behavioral drift MUST be measured against baseline; fitness MUST be multi-criteria with safety constraints as hard gates. | E-11, E-09 | Drift-injection test and scorecard with safety gates. | test |
| REQ-ADPT-06 | Adaptive | **Lineage of variants.** Every promoted variant MUST have a LineageManifest linking parent genome, artifacts and deliberate differences. | E-02, E-08 | LineageManifest records for promoted variants. | schema |
| REQ-ADPT-07 | Adaptive | **Learned defenses are measured.** Learned detection rules and indicators MUST be validated for precision, recall and blast radius, and MUST decay or be retired. | I-06, I-07, I-16 | Rule validation report and indicator-decay test. | test |
| REQ-EMB-01 | Embodied | **Hazard analysis and safe state.** A hazard analysis and a defined physical safe state MUST exist and be referenced in the genome `embodiment`. | R-04 | Hazard analysis document reference and safe-state definition. | schema |
| REQ-EMB-02 | Embodied | **Independent interlock, watchdog and emergency stop.** Emergency stop and hard limits MUST be independent of any LLM, planner and network control plane. | R-04, R-03 | E-stop and watchdog tests. | test |
| REQ-EMB-03 | Embodied | **Real-time budget.** Worst-case response time of safety paths MUST be specified and evidenced. | N-09, R-04 | Timing analysis or measurement report. | test |
| REQ-EMB-04 | Embodied | **Calibrated sensing and uncertainty.** Observations MUST carry calibration version, uncertainty and freshness; sensor disagreement MUST yield UNCERTAIN state. | R-01, N-01, R-02 | Calibration and fault-injection tests. | test |
| REQ-EMB-05 | Embodied | **Actuator envelope and stale command rejection.** Actuator commands MUST be bounded, deadline-limited and preconditioned; expired or replayed commands MUST be rejected. | R-03, N-07 | Stale/replayed command rejection test. | test |
| REQ-EMB-06 | Embodied | **Reset authority.** Leaving LOCKED_OUT MUST require inspection and authorized reset by a qualified human. | R-04, R-05 | Reset-authority test and procedure. | test |
| REQ-COND-01 | Conditional | **Reproduction control.** If reproduction is allowed it MUST be plan-gated with independent identity and lineage; otherwise `ecology.reproduction` MUST be forbidden and enforced. | E-07, E-02 | Genome `ecology` and enforcement test. | test |
| REQ-COND-02 | Conditional | **Federation and treaties.** If federation is allowed it MUST use treaties with identity, quotas, data-use policy, expiry and revocation; otherwise `ecology.federation` MUST be none. | E-13, E-16, E-15 | Treaty records and revocation test. | test |
| REQ-COND-03 | Conditional | **Horizontal transfer isolation.** If imports from other lineages are allowed they MUST pass provenance, compatibility and quarantine gates; otherwise `ecology.horizontal_transfer` MUST be forbidden. | E-14, M-04 | Import-gate test. | test |

## 3. Статусы claim и правила

Статус claim (`conformance-claim.schema.json`, шаблон `templates/DOA_CONFORMANCE_CLAIM.md`):

| Статус | Условия |
|---|---|
| `UNVERIFIED` | claim заявлен без evidence либо evidence не прошёл проверку |
| `PARTIAL` | часть требований заявленных профилей имеет статус `PASS` с evidence; остальные `PARTIAL`/`FAIL`/`NOT_ASSESSED`/`DESIGNED`/`EXCLUDED`; blocking gaps перечислены |
| `VERIFIED` | **все** требования Core, заявленных профилей и Conditional имеют статус `PASS` с `evidence_ref` либо `EXCLUDED` с письменным `justification`; нет blocking gaps; указаны assessor, дата и срок переоценки |

Статус отдельного требования (поле `status` в `requirements`):

| Статус | Когда ставится | Что требуется |
|---|---|---|
| `PASS` | механизм реализован и подтверждён воспроизводимым evidence | `evidence_ref` |
| `PARTIAL` | реализована и подтверждена часть механизма | — |
| `FAIL` | механизм отсутствует или не работает | — |
| `EXCLUDED` | требование не применимо | письменный `justification` |
| `NOT_ASSESSED` | требование не рассматривалось | — |
| `DESIGNED` | механизм объявлен проектом или инструкциями, но не реализован кодом либо не имеет воспроизводимого evidence | `component` (где он описан) и `gap_owner` |

`DESIGNED` отличает «описано, но не построено» от `PARTIAL` (часть построена и подтверждена), `FAIL` (механизма нет) и `NOT_ASSESSED` (не смотрели). Он никогда не считается `PASS` и не засчитывается в условие «хотя бы одно `PASS`» для claim `PARTIAL`. Claim с требованием в статусе `DESIGNED` не может быть `VERIFIED`. Ссылка на описание дизайна может быть указана в `evidence_ref`, но по правилу 2 evidence не является.

Необязательное поле `observed_accounting` фиксирует потребление, известное только из внешней телеметрии, с источником и неопределённостью (`REQ-CORE-18`); без обоих полей запись схему не проходит.

Классы отказа из [FAILURE_AND_RECOVERY.md](FAILURE_AND_RECOVERY.md) (реестр: `specifications/failure-classes.yaml`) можно оценивать по отдельности в необязательном поле `failure_classes` с теми же статусами. Если поле указано, оно проверяется на согласованность с реестром, а при `REQ-CORE-23` в статусе `PASS` каждый класс MUST иметь статус `PASS` или `EXCLUDED` с `justification`.

Дополнительные правила:

1. `EXCLUDED` для требования уровня Core допускается в `VERIFIED` claim только при `assurance: independently-reviewed`.
2. `evidence_ref` MUST указывать на неизменяемый или версионированный артефакт (digest, tag, commit, ticket с вложением). Ссылка на «план» или намерение evidence не является. Практические вопросы закрепления ссылок — в [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md), раздел 4.
3. Evidence MUST быть воспроизводимым: тест описывает среду, версию реализации, входы и результат.
4. Требования `Conditional` всегда оцениваются: если возможность запрещена в genome (`ecology`), evidence — тест принудительного запрета; если разрешена — тест соответствующих controls.
5. Claim относится к конкретной версии реализации и версии стандарта и MUST переоцениваться при изменении реализации, major-версии DOA или не реже чем раз в 12 месяцев.
6. `self-assessed` claim MUST НЕ называться «certified»; DOA не определяет сертификационный орган.
7. Формулировка использования: «implements DOA Profile X (claim: <ссылка>)». Запрещены формулировки «DOA-compliant» и «DOA-certified» без ссылки на claim со статусом `VERIFIED`.

## 3.1 Проверка claim

```bash
python scripts/check_conformance_claim.py path/to/claim.yaml
```

Скрипт валидирует claim по схеме и проверяет покрытие реестра требований и правила статуса (раздел 3). Он также печатает предупреждения (`warning:`) для `evidence_ref`, который заведомо не удовлетворяет правилу 2: ссылка на подвижную ветку (`main`, `master`, `develop`, `development`, `HEAD`, `latest`) или запись без пути и идентификатора. Предупреждения не меняют код выхода. Он не проверяет сами evidence-артефакты: это задача assessor.

## 4. Минимальный evidence pack

Evidence pack — набор артефактов, на которые ссылаются `evidence_ref` требований:

- подписанный genome и применённый epigenome snapshot (`organism.effective_policy`);
- inventory клеток, органов и trust boundaries (включая `boundary.external_dependencies`);
- state-transition logs, валидные по `lifecycle-transition.schema.json` и `state-machines.yaml`;
- ControlLoopSpec для регулируемых доменов и alert-to-action traces;
- fault-injection/controlled-failure evidence по применимым классам `FAILURE_AND_RECOVERY.md`;
- quarantine, apoptosis и necrosis (fencing) tests;
- restore/rollback и catastrophic-recovery drills;
- security threat model и access-policy tests;
- learning/change provenance и lineage (Adaptive);
- hazard analysis, E-stop/watchdog evidence (Embodied).

Тестовые кейсы, сценарии отказа, формат отчёта и шаблоны threat model и hazard analysis для получения этого evidence собраны в [VERIFICATION_KIT.md](VERIFICATION_KIT.md) (informative; использование необязательно).

## 5. Совместимость

Claim к `DOA-FS-1.0` остаётся действительным для patch- и minor-релизов 1.x, пока реестр требований профилей не расширен. Если minor-релиз добавляет требование, claim остаётся `VERIFIED` относительно ранее оцененных требований и MUST указывать новые требования как `NOT_ASSESSED` до переоценки. Major-релиз требует нового claim.

Релиз 1.1.0 не добавляет требований: он добавляет необязательный статус `DESIGNED`, необязательное поле `failure_classes`, реестр `specifications/failure-classes.yaml` и уточняет формулировки `REQ-CORE-18` (различие reserved и observed accounting) и `REQ-CORE-22` (область применения tombstone). Идентификатор стандарта остаётся `DOA-FS-1.0`; claim, составленные по 1.0.x, остаются действительными без изменений. Claim, использующий `DESIGNED` или `failure_classes`, не проходит схему 1.0.x.

Релиз 1.2.0 добавляет informative Verification Kit ([VERIFICATION_KIT.md](VERIFICATION_KIT.md)), необязательное поле claim `observed_accounting` и исправляет формулировки `REQ-CORE-18` и `REQ-CORE-22` из 1.1.0: запись observed accounting стала SHOULD (в 1.1.0 было MUST), а непроверенные чужие credentials в восстановленном состоянии MUST NOT использоваться до проверки их внешнего статуса (это следует из запрета восстанавливать отозванное из устаревшего состояния, который действовал в 1.0.x для всех сущностей). Объявление чужих identities внешними зависимостями — SHOULD. Список требований и их идентификаторы не меняются. Claim по 1.0.x и 1.1.x остаются действительными; claim с полем `observed_accounting` не проходит схему 1.1.x и ранее.

Релиз 1.3.0 добавляет informative профили внедрения ([profiles/README.md](../profiles/README.md)) и не меняет реестр требований и правила claim. Claim по 1.0.x, 1.1.x и 1.2.x остаются действительными без переоценки.
