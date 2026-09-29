# Reference Stack

Таблица содержит варианты, а не endorsements или mandatory dependencies. Конкретная реализация MUST проверять актуальные versions, licenses, support status and threat model.

| Capability | Possible stack |
|---|---|
| Schemas/contracts | JSON Schema 2020-12, Protobuf, OpenAPI, AsyncAPI, CloudEvents-compatible envelopes |
| Identity | OIDC/OAuth 2.x for users, SPIFFE/SPIRE or cloud workload identity for services, mTLS |
| Policy | OPA/Rego, Cedar, native ABAC/RBAC, admission controllers |
| Orchestration | Kubernetes, Nomad, systemd/process supervisor, RTOS/ROS 2 lifecycle |
| Circulation | Kafka, NATS JetStream, RabbitMQ Streams, gRPC/HTTP, transactional outbox |
| Workflow | Temporal, Argo Workflows, durable state machines, custom deterministic engine |
| Reasoning/inference | vLLM, TensorRT-LLM, ONNX Runtime, PyTorch, provider APIs behind adapter |
| Sandbox | Firecracker, gVisor, containers with seccomp/AppArmor, WASM runtime |
| Memory | PostgreSQL, object storage, event store, graph DB, vector index behind governed gateway |
| Observability | OpenTelemetry/OTLP, Prometheus-compatible metrics, trace/log backend, append-only audit store |
| Supply chain | OCI artifacts, SBOM, Sigstore/cosign, in-toto/SLSA provenance |
| Secrets/keys | KMS/HSM, Vault-class secret manager, short-lived credentials |
| Progressive delivery | canary controller, feature flags, model registry/evaluation harness |
| Robotics | ROS 2/DDS, real-time controller/PLC, independent safety interlock |

## Selection rules

1. Начинать с требуемого contract и failure model, а не продукта.
2. Не применять distributed component, если local durable implementation удовлетворяет SLO.
3. Избегать single vendor control over identity, policy, telemetry and recovery simultaneously.
4. Отделять experimental AI component от deterministic enforcement.
5. Документировать version, configuration, operational owner and exit strategy.
