# Security Policy

## Supported versions

| Версия | Поддержка |
|---|---|
| 1.0.x (`DOA-FS-1.0`) | исправления security-связанных дефектов стандарта (errata) |
| ветка `main` | разработка следующей версии |

Поддерживаемые версии перечисляются здесь явно при каждом релизе.

## Reporting

Не публикуйте credentials, private data, working exploits или сведения, позволяющие обойти safety controls, в публичном issue.

Предпочтительный канал — GitHub private vulnerability reporting для этого репозитория, когда он доступен. Если канал недоступен, свяжитесь с владельцем репозитория через приватный канал GitHub до публикации деталей.

## Scope

Security report может относиться к:

- schema или contract, позволяющим privilege escalation;
- небезопасному self-modification или replication protocol;
- обходу quarantine, apoptosis или capability revocation;
- provenance/integrity gap;
- примеру, который создаёт опасную implementation guidance;
- CI workflow с избыточными permissions или supply-chain risk.

DOA является стандартом, а не работающим runtime. Уязвимости конкретной реализации также должны направляться владельцу этой реализации.
