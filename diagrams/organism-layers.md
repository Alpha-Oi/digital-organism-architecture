# Organism Layers

## Простыми словами

Организм состоит из слоёв. Геном задаёт правила. Нервная и эндокринная системы управляют. Иммунитет и ремонт защищают. Память учится на опыте. Обмен веществ считает ресурсы. Циркуляция переносит сообщения. Органы, ткани и клетки выполняют работу. Наблюдаемость (observability) видит всё происходящее и возвращает сигналы управлению и иммунитету.

## Схема

```mermaid
flowchart TB
  G[Genome and Epigenome]
  C[Nervous / Endocrine Control]
  I[Immune / Repair]
  M[Memory / Learning]
  R[Metabolism / Resource Accounting]
  T[Circulation / Transport]
  O[Organs]
  TI[Tissues]
  CE[Cells]
  OBS[Observability / Audit]
  G --> C
  C --> O
  I --> O
  M --> C
  R --> O
  T <--> O
  O --> TI --> CE
  CE --> OBS
  O --> OBS
  OBS --> C
  OBS --> I
```
