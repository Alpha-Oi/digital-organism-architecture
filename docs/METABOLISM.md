# Metabolism

## 1. Resource model

DOA учитывает CPU-ms, GPU-ms, VRAM-seconds, memory, storage, network, tokens, joules, latency and currency. Каждая задача получает reservation и итоговый charge.

```text
utility = expected_task_value / (compute + latency + monetary + risk cost)
```

Эта формула является decision aid, а не универсальной функцией ценности; safety constraints не оптимизируются через простой trade-off.

## 2. Ingestion / digestion

```text
receive -> type detect -> decode -> malware scan -> parse
        -> normalize -> deduplicate -> chunk -> enrich -> classify
```

Parsers работают в bounded sandbox. Raw input и normalized representation сохраняют lineage.

## 3. Liver / detoxification

Classification, PII/secret detection, redaction, provenance enrichment, malformed-content neutralization и policy labeling происходят до передачи в trusted circulation/memory.

## 4. Kidney / excretion

Storage, queues, caches и temporary artifacts имеют watermarks, quotas, TTL, hold rules и disposal evidence. Forensic/legal hold имеет приоритет над автоматическим GC.

## 5. Respiration and heat

Capacity controller учитывает accelerator availability, power/thermal headroom, network bandwidth and cooling signals. При saturation сначала применяются backpressure и graceful degradation, затем bounded capacity expansion.

## 6. Energy reserves

Warm capacity, cached models и budget reserve используются для critical work. Reserve имеет отдельную policy и не расходуется обычной нагрузкой без replenishment plan.

## 7. Proteostasis

Artifacts, models, prompts and workflows проходят compatibility, integrity and behavior gates. Повторная сборка (`refold`) ограничена retry budget; persistent failure уходит в quarantine, а не бесконечный retry.

## 8. Metabolic failure modes

- resource leak and unbounded context;
- retry storm and queue collapse;
- cache poisoning or stale reserve;
- cost runaway;
- thermal/power throttling;
- premature disposal;
- hidden cross-subsidy between tenants;
- model loading thrash.

Все critical resource pools MUST публиковать capacity, allocation, saturation, rejection и recovery metrics.
