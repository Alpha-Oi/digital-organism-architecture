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

## 3. Quarantine protocol

```text
OBSERVED -> SUSPECT -> CONTAINED -> EVIDENCE_PRESERVED
         -> ANALYZED -> RELEASED | REMEDIATED | TERMINATED
```

Quarantine MUST прекращать новые high-risk actions, ограничивать network/data access, сохранять permitted evidence и поддерживать appeal/review для false positive.

## 4. Apoptosis protocol

1. Stop admission of new work.
2. Bound or cancel active work.
3. Revoke credentials, tokens and leases.
4. Seal egress.
5. Preserve policy-permitted forensic snapshot.
6. Release resources and remove discovery endpoint.
7. Emit signed terminal record.
8. Verify absence of live grants and replicas.

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

## 6. Security observability

Минимум: authentication decisions, capability grants/revocations, policy version, ingress/egress decision, quarantine transition, artifact digest, data classification, admin/break-glass action и clock/freshness status. Logs MUST NOT включать secrets или unrestricted chain-of-thought.

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

Каждая implementation MUST иметь локальный threat model и не должна считать этот список исчерпывающим.
