# Security and Immunity

## 1. Trust model

DOA использует zero trust: network location и принадлежность к организму не создают неявного доверия. User, workload, device, model, artifact и data source получают проверяемую identity; доступ принимается по identity, state, resource, context и policy.

## 2. Defense layers

```text
Barrier -> receptor validation -> innate controls -> quarantine
        -> evidence/antigen presentation -> adaptive controls
        -> repair/regeneration -> learning with rollback
```

### Barrier

Inventory всех ingress/egress paths, mutual authentication, schema/size/rate limits, data classification и explicit egress policy.

### Innate immunity

Детерминированные controls: signature verification, deny rules, anomaly thresholds, sandboxing, capability checks. Реакции короткие, локальные и expiring.

### Adaptive immunity

Detection rules, reputations и playbooks, выведенные из подтверждённых incidents. Перед promotion измеряются precision, recall, blast radius и rollback.

### Tolerance

Exceptions для self/partner identities имеют scope, reason, owner, expiry и revocation. Transitive trust запрещён по умолчанию.

## 3. Полный жизненный цикл иммунного ответа

Каждый security incident проходит машину `incident` (`specifications/state-machines.yaml`, `diagrams/immune-response.md`):

```text
OBSERVED -> DETECTED -> IDENTIFIED -> CONTAINED -> QUARANTINED
         -> NEUTRALIZED -> RECOVERED -> LEARNED -> DEFENSES_UPDATED -> CLOSED
```

| Этап | Что происходит | Основные механизмы и контролы | Evidence |
|---|---|---|---|
| detect | срабатывание innate rule, anomaly threshold, attestation failure | I-04, I-05, N-03; audit logs authn/authz | DetectionEvent, FindingEvidence |
| identify | классификация: что, кто, масштаб, trust class | I-03 (self/non-self), provenance E-01, indicators I-07 | классифицированный FindingEvidence |
| contain | ограниченное, истекающее ограничение (TTL, scope): rate limit, seal, deny | I-12 coagulation, capability restrictions, trust boundaries | SealRule с TTL |
| quarantine | изоляция субъекта без его кооперации, сохранение evidence | M-04, C-17 sandbox, revoke grants (least privilege), изоляция сети/данных | QuarantineCase, forensic snapshot по policy |
| eradicate / neutralize | удаление угрозы: terminate (apoptosis), revoke credentials, purge, rollback poisoned artifacts | C-27, rollback, provenance-based purge | terminal record / purge report |
| recover | восстановление из trusted source и проверка | REGENERATE/REPLACE/ROLLBACK (`FAILURE_AND_RECOVERY.md`), I-13, I-14 | attestation после recovery |
| learn | post-incident review, причины, ложные срабатывания | I-07, false-positive budget I-16 | review record |
| update defenses | новое правило/playbook через change protocol | I-06, машина `change` (class=learning) | rule validation: precision, recall, blast radius |

Связи с базовыми контролями безопасности:

| Контроль | Роль в цикле |
|---|---|
| Identity / authentication | основа identify; каждое решение привязано к проверенному субъекту (I-03) |
| Authorization / least privilege | contain и neutralize: сужение и отзыв `CapabilityGrant`; attenuation при делегировании |
| Provenance | identify, neutralize и learn: определение затронутых объектов и точный purge (E-01) |
| Sandboxing и isolation | quarantine и безопасный анализ (C-17, M-04) |
| Trust boundaries | contain: разделение зон; поведение при пересечении границы (`BOUNDARY_AND_IDENTITY.md`) |
| Capability restrictions | временные ограничения вместо полного отключения |
| Rollback | recover: возврат artifact/policy/model к проверенной версии |
| Audit logs | все этапы; tamper-evident, без секретов; переживают потерю data plane |

Quarantine MUST прекращать новые high-risk actions, ограничивать network/data access, сохранять permitted evidence, работать без кооперации субъекта и поддерживать review ложных срабатываний. Автоматическая блокировка MUST иметь TTL и счётчик в false-positive budget; выход из quarantine по ложному срабатыванию — `QUARANTINED -> CLOSED` с review владельца.

## 4. Apoptosis и necrosis

Apoptosis — контролируемое завершение (8 шагов, машина `cell`, состояние `TERMINATING`):

1. Stop admission of new work.
2. Bound or cancel active work.
3. Revoke credentials, tokens and leases.
4. Seal egress.
5. Preserve policy-permitted forensic snapshot.
6. Release resources and remove discovery endpoint.
7. Emit signed terminal record.
8. Verify absence of live grants and replicas.

Necrosis — неконтролируемый отказ (`FAILED`): организм не может рассчитывать на кооперацию клетки. Контроль — lease expiry и fencing (revoke grants, fencing token/epoch, сверка side effects по idempotency key); затем `ISOLATED` и repair либо apoptosis. Различие критично: некрозу не выполнены шаги 3–8, поэтому enforcement выполняется внешним authority.

## 5. Oncological anti-patterns

| Anti-pattern | Digital sign | Required control |
|---|---|---|
| Uncontrolled proliferation | replicas/jobs exceed declared need | admission, quota, lineage inventory |
| Growth-signal independence | self-issued scale/capability grants | separate issuer and enforcer |
| Apoptosis resistance | ignored revoke/terminate | lease expiry, external kill authority |
| Resource capture | monopolized GPU/queue/storage | fair share, hard limits, preemption |
| Invasion/metastasis | execution outside assigned boundary | workload identity, network/data policy |
| Immune evasion | missing/deceptive telemetry | independent telemetry, attestation |
| Genome instability | unreviewed config/model mutation | signed immutable versions, repair |
| Recursive delegation / privilege amplification | delegated grant ⊄ parent grant, глубина > `max_delegation_depth` | attenuation, depth limit, lease |
| Self-replication | экземпляры вне inventory или lineage | `ecology.reproduction`, запрет credential cloning |
| Orphans | клетки без lease или родителя | lease TTL, fencing, termination |

## 6. Security observability

Минимум: authentication decisions, capability grants/revocations, policy version, ingress/egress decision, incident и quarantine transitions, artifact digest, data classification, admin/break-glass action, lifecycle transitions и clock/freshness status. Logs MUST NOT включать secrets или unrestricted chain-of-thought.

## 7. Threat classes

- prompt/data/model poisoning;
- identity spoofing and confused deputy;
- replay, duplicate side effects and stale grants;
- tool misuse and egress exfiltration;
- supply-chain compromise;
- memory poisoning and cross-tenant leakage;
- denial of resources and retry storms;
- malicious self-replication or policy mutation;
- sensor spoofing and actuator hijack;
- control-plane compromise and deceptive health.

Каждый класс отказа и атаки сопоставлен с detection, containment, recovery и verification в [FAILURE_AND_RECOVERY.md](FAILURE_AND_RECOVERY.md). Каждая implementation MUST иметь локальный threat model и не должна считать этот список исчерпывающим.
