# Organism Boundary and Identity

**Версия:** DOA v1.0 (`DOA-FS-1.0`). Нормативный документ.

Этот документ определяет, где начинается и заканчивается цифровой организм, что считается его внутренним состоянием, как устанавливается доверие на границе и как сохраняется identity при замене компонентов. Он обязателен для multi-agent и distributed реализаций.

## 1. Определение организма

Организм — это множество компонентов, находящихся под **одним identity root, одним активным genome и одним policy authority**. Принадлежность определяется декларацией, а не расположением:

> Co-location (один хост, кластер, процесс, репозиторий, облачный аккаунт) MUST NOT создавать принадлежность к организму. Принадлежность создаёт только совокупность условий ниже.

Компонент **внутренний (SELF)**, если одновременно:

1. его artifact digest выводим из активного genome (организм, ткань, клетка из genome);
2. его identity выдана identity authority организма в его `trust_domain`;
3. его capabilities выдаются grant-сервисом организма;
4. его lifecycle управляется controllers организма (admission, supervision, termination);
5. его telemetry и audit попадают в observability организма под политикой организма.

Если хотя бы одно условие не выполнено, компонент **внешний** и MUST быть объявлен в `genome.spec.boundary.external_dependencies` (если организм от него зависит) или рассматриваться как environment.

## 2. Классы внешних сущностей

| Класс (`boundary.external_dependencies[].class`) | Что это | Trust class | Как взаимодействует | Политика отказа |
|---|---|---|---|---|
| `environment-actor` | пользователи, сенсорный мир, неподконтрольные источники | `UNKNOWN` | только через membrane/receptors (C-20, C-21, C-22) | fail-closed |
| `external-service` | SaaS, базы, directory, облачные API | `PARTNER` или `UNKNOWN` | через egress gateway по контракту (C-23) | по контракту: degrade / fail-closed |
| `foundation-model` | внешний LLM/модельный API как сменный когнитивный компонент | `PARTNER` | через adapter; вывод — proposal, не authority (N-05) | degrade / failover |
| `symbiont` | допущенные plugins/tools/агенты | `SYMBIONT` | `SymbiontContract` (E-12): identity, quota, revocation | isolate / revoke |
| `peer-organism` | другой организм | `PARTNER` | только через `Treaty` (E-16), если `ecology.federation=treaty-gated` | по treaty |
| `infrastructure` | вычислительный, сетевой, физический substrate | `PARTNER` | substrate не владеет policy организма (`diagrams/system-context.md`) | failover / degrade |

Для каждой внешней зависимости MUST быть указан контракт и failure policy. Зависимость без декларации является нарушением boundary (скрытый control path).

## 3. Внутреннее состояние и внешняя среда

| Внутреннее состояние организма | Внешняя среда (не внутреннее) |
|---|---|
| genome, epigenome overlays, lineage, continuity records | пользовательские запросы и контент до прохождения ingress |
| memory (все четыре типа) и MemoryRecord provenance | данные партнёров, не принятые consolidation protocol |
| credentials, ключи, trust root references | инфраструктурные секреты провайдера |
| runtime state клеток, leases, epochs | состояние внешних сервисов |
| audit/provenance, tombstones | внешние логи провайдера |
| homeostatic targets и control loops | чужие SLO, не заверенные treaty |

Данные пересекают границу только как типизированные envelope (`EventEnvelope`, `IngressEnvelope`, `EgressRequest`) с classification. Raw внешний вход MUST NOT становиться trusted memory, policy или identity fact напрямую.

## 4. Identity организма

Identity организма состоит из:

- `organism_id` — стабильное имя (`genome.spec.identity.organism_id`);
- `trust_domain` — домен доверия;
- `trust_root_ref` — ссылка на корень доверия, которым подписываются genome, grants и continuity records;
- lineage root — корень цепочки `LineageManifest`.

Identity организма **не** совпадает с identity ни одного компонента и не определяется конкретной моделью, процессом, хостом или контейнером. Модель — сменный когнитивный компонент (P3).

## 5. Identity continuity при замене компонентов

Замена любого компонента (клетки, органа, модели, хоста, узла кластера) MUST сохранять `organism_id` и `trust_domain` при выполнении всех условий:

1. цепочка `LineageManifest` непрерывна (у каждой клетки поколения ≥ 1 есть родитель);
2. trust root не менялся либо ротирован подписанной ротацией (`identity_continuity.mode = rotated`, `rotation_record_ref`);
3. заменяющий компонент прошёл admission и attestation как SELF;
4. замена зафиксирована как lifecycle transition с guard evidence.

Режимы `identity_continuity.mode`:

| Режим | Когда | Требования |
|---|---|---|
| `continuous` | обычная замена компонентов | условия 1–4 |
| `rotated` | плановая ротация trust root | подписанная ротация старым и новым корнем, `rotation_record_ref` |
| `new-identity` | reproduction, компрометация trust root, катастрофическое восстановление без доказанной непрерывности | новая identity; `predecessor`/`succeeded_by` фиксируют связь; credentials не наследуются |

**Anti-resurrection.** После перехода `TERMINATED` организм или клетка получает tombstone. Восстановление из состояния, созданного до tombstone, MUST быть отклонено; новое существование возможно только как `new-identity` с новым epoch и lineage-связью (E-04). Catastrophic recovery (E-06) увеличивает epoch организма (`organism.epoch`); сообщения старого epoch MUST отклоняться fencing.

## 6. Trust boundaries и установление доверия

Границы (вложенные): environment → organism → organ → cell. Пересечение любой границы MUST быть опосредовано enforcement point (membrane, gateway, adapter) и MUST быть аудируемо.

Классы доверия (`trust_class`, используются в `IdentityAssertion`, `MemoryRecord.provenance`, `boundary.external_dependencies`):

| Class | Значение | Допустимые действия по умолчанию |
|---|---|---|
| `SELF` | внутренний компонент организма | capabilities по grant |
| `SYMBIONT` | допущенный guest | только quota-bound capabilities по `SymbiontContract` |
| `PARTNER` | другой организм/сервис по контракту или treaty | только предмет контракта; transitive trust запрещён |
| `UNKNOWN` | всё остальное | ничего, кроме ingress в quarantine/ingestion; deny-by-default |

Доверие устанавливается: (1) проверкой identity (attestation, mTLS, подпись); (2) классификацией; (3) явной ограниченной выдачей (`ToleranceGrant`, `SymbiontContract`, `Treaty`) с owner, scope и expiry; (4) мониторингом и revocation. Network location и принадлежность к одному кластеру доверия не создают.

## 7. Multi-agent и distributed реализации

- Агент является клеткой организма, **только если** удовлетворяет условиям раздела 1. Агент другого владельца или с другим identity root — это внешний `peer-organism` или `symbiont`; взаимодействие — через treaty/contract.
- Организм MAY физически распределяться по регионам, хостам и процессам; граница при этом определяется genome, а не топологией. Каждый failure domain MUST быть объявлен (`genome.spec.topology`).
- Делегирование полномочий между агентами подчиняется attenuation: делегированный `CapabilityGrant` ⊆ родительского, глубина ≤ `growth_control.max_delegation_depth`, lease истекает (N-11).
- При потере связи периферийные агенты работают в пределах `DelegationGrant` и MUST сверяться при reconnect (reconcile); решения вне делегированных прав недействительны.

Применение этих правил к control plane над внешними агентами разобрано в [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md), раздел 1 (informative).

## 8. Нормативные требования

Реализация MUST: (a) объявить boundary в genome (`boundary`); (b) иметь инвентарь ingress/egress; (c) классифицировать каждую внешнюю зависимость; (d) подтвердить identity continuity тестом замены компонента; (e) отклонять restore после tombstone и считать непроверенными чужие credentials из восстановленного состояния, пока их внешний статус не подтверждён. Evidence — `REQ-CORE-01`, `REQ-CORE-02`, `REQ-CORE-22`, `REQ-CORE-25` (см. `CONFORMANCE.md`).
