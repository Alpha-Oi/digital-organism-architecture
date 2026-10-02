# Embodied Safety States

## Простыми словами

Состояния безопасности физической системы (робот, станок). Аварийная остановка срабатывает независимо от ИИ и от сети. После остановки систему блокируют, человек осматривает её и разрешает сброс, и только потом она калибруется и может работать снова.

## Главный путь

```mermaid
flowchart TD
  INIT["Включение"]
  CALIBRATING["Калибровка"]
  READY["Готова"]
  ACTIVE["Работает"]
  SAFE_STOP["Аварийная остановка"]
  LOCKED_OUT["Заблокирована"]
  INSPECTED["Осмотрена человеком"]
  RESET_AUTHORIZED["Сброс разрешён"]
  INIT --> CALIBRATING
  CALIBRATING --> READY
  READY --> ACTIVE
  ACTIVE --> SAFE_STOP
  SAFE_STOP --> LOCKED_OUT
  LOCKED_OUT --> INSPECTED
  INSPECTED --> RESET_AUTHORIZED
  RESET_AUTHORIZED --> CALIBRATING
```

**Ограниченный режим:** при неопределённости, плохом датчике или близости (proximity) `ACTIVE` переходит в `LIMITED` и возвращается обратно, когда условие исчезло. Из `LIMITED` тоже возможна аварийная остановка.

## Что значит каждое состояние

| Состояние | Что это значит |
|---|---|
| `INIT` | включение, самопроверка оборудования |
| `CALIBRATING` | калибровка датчиков |
| `READY` | готова, задача ещё не разрешена |
| `ACTIVE` | работает штатно |
| `LIMITED` | ограниченный режим: неопределённость, плохой датчик или близость (proximity), в том числе человека |
| `SAFE_STOP` | аварийная остановка |
| `LOCKED_OUT` | заблокирована до осмотра |
| `INSPECTED` | человек осмотрел систему |
| `RESET_AUTHORIZED` | сброс разрешён, затем снова калибровка |

## Полная схема

Здесь показаны все переходы. Схема мелкая, она нужна для справки: условия каждого перехода (проверка, кто разрешает, срок) собраны в таблице в [docs/LIFECYCLE.md, раздел 10](../docs/LIFECYCLE.md).

<details>
<summary>Показать полную схему</summary>

```mermaid
stateDiagram-v2
  [*] --> INIT
  INIT --> CALIBRATING
  CALIBRATING --> READY
  READY --> ACTIVE
  ACTIVE --> LIMITED
  LIMITED --> ACTIVE
  ACTIVE --> SAFE_STOP
  LIMITED --> SAFE_STOP
  SAFE_STOP --> LOCKED_OUT
  LOCKED_OUT --> INSPECTED
  INSPECTED --> RESET_AUTHORIZED
  RESET_AUTHORIZED --> CALIBRATING
```

</details>

Независимо от LLM и сетевого control plane. Подробности — `docs/ROBOTICS_EXTENSION.md`.

Источник истины: `specifications/state-machines.yaml` (машина `embodied_safety`); валидатор проверяет совпадение рёбер.
