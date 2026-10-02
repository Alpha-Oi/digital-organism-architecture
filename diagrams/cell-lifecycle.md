# Cell Lifecycle

## Простыми словами

Клетка — минимальная единица, которая выполняет работу (например, агент). Её допускают, запускают, и она работает. При подозрении клетку изолируют и ремонтируют, при сбое отключают. Завершение бывает двух видов: апоптоз (спокойное завершение по шагам) и некроз (аварийный отказ, после которого клетку принудительно отключают снаружи).

## Главный путь

```mermaid
flowchart TD
  DECLARED["Заявлена"]
  ADMITTED["Допущена"]
  PROVISIONED["Получила ресурсы"]
  STARTING["Запускается"]
  READY["Готова"]
  ACTIVE["Работает"]
  TERMINATING["Завершается"]
  TERMINATED["Завершена"]
  DECLARED --> ADMITTED
  ADMITTED --> PROVISIONED
  PROVISIONED --> STARTING
  STARTING --> READY
  READY --> ACTIVE
  ACTIVE --> TERMINATING
  TERMINATING --> TERMINATED
```

**Если что-то пошло не так:** `ACTIVE` → `SUSPECT` (подозрение) → `ISOLATED` (изоляция) → `REPAIRING` (ремонт) → `READY`. Если клетка упала или потеряла право существовать (lease), она попадает в `FAILED`, затем в `ISOLATED`.

## Что значит каждое состояние

| Состояние | Что это значит |
|---|---|
| `DECLARED` | клетка заявлена, но ещё не допущена |
| `ADMITTED` | допущена: квота, подпись и лимит потомков в порядке |
| `PROVISIONED` | ресурсы зарезервированы, права выданы |
| `STARTING` | запускается |
| `READY` | запущена и прошла проверки готовности |
| `ACTIVE` | работает, право существовать (lease) действует |
| `STRESSED` | локальный стресс, клетка реагирует сама |
| `SUSPECT` | подозрение: аномалия или сомнение в целостности |
| `ISOLATED` | изолирована, трафик и права ограничены |
| `REPAIRING` | ремонт из доверенного независимого источника |
| `QUIESCENT` | приостановлена после завершения текущей работы |
| `HIBERNATED` | «спит»: долго простаивала |
| `SENESCENT` | состарилась, ждёт готовой замены |
| `FAILED` | аварийно упала или потеряла lease (некроз) |
| `TERMINATING` | идёт контролируемое завершение (апоптоз) |
| `TERMINATED` | завершена окончательно |

## Полная схема

Здесь показаны все переходы. Схема мелкая, она нужна для справки: условия каждого перехода (проверка, кто разрешает, срок) собраны в таблице в [docs/LIFECYCLE.md, раздел 4](../docs/LIFECYCLE.md).

<details>
<summary>Показать полную схему</summary>

```mermaid
stateDiagram-v2
  [*] --> DECLARED
  DECLARED --> ADMITTED
  DECLARED --> TERMINATED
  ADMITTED --> PROVISIONED
  PROVISIONED --> STARTING
  STARTING --> READY
  STARTING --> FAILED
  READY --> ACTIVE
  ACTIVE --> STRESSED
  STRESSED --> ACTIVE
  STRESSED --> SUSPECT
  ACTIVE --> SUSPECT
  SUSPECT --> ACTIVE
  SUSPECT --> ISOLATED
  ISOLATED --> REPAIRING
  REPAIRING --> READY
  REPAIRING --> TERMINATING
  ISOLATED --> TERMINATING
  ACTIVE --> QUIESCENT
  QUIESCENT --> ACTIVE
  QUIESCENT --> HIBERNATED
  HIBERNATED --> STARTING
  ACTIVE --> SENESCENT
  SENESCENT --> TERMINATING
  READY --> TERMINATING
  ACTIVE --> TERMINATING
  ACTIVE --> FAILED
  STRESSED --> FAILED
  SUSPECT --> FAILED
  FAILED --> ISOLATED
  TERMINATING --> TERMINATED
  TERMINATED --> [*]
```

</details>

Apoptosis = последовательность в состоянии `TERMINATING`; necrosis = путь через `FAILED` с обязательным fencing.

Источник истины: `specifications/state-machines.yaml` (машина `cell`); валидатор проверяет совпадение рёбер.
