# DOA Governance

## 1. Scope

Governance охватывает каноническую терминологию, normative requirements, schemas, conformance profiles, release process и compatibility policy DOA.

DOA остаётся независимым от конкретных продуктов. Реализации могут заявлять соответствие, но не получают право единолично менять стандарт.

## 2. Roles

### Maintainer

- triage issues и pull requests;
- требует evidence для normative claims;
- обеспечивает compatibility и release discipline;
- не объявляет собственную реализацию автоматически соответствующей.

### Contributor

- формулирует concrete scenario и observable outcome;
- предоставляет mapping, risks, evidence и ограничения;
- отвечает на review без скрытого расширения scope.

### Implementation owner

- публикует conformance claim;
- хранит evidence pack;
- отмечает exclusions и `UNVERIFIED` areas;
- переоценивает claim после изменения стандарта или реализации.

## 3. Decision model

Приоритет решения:

1. safety и integrity invariants;
2. проверяемость contract/protocol/evidence;
3. backward compatibility;
4. переносимость между implementation stacks;
5. операционная простота;
6. полнота биологической аналогии.

Consensus предпочтителен. При его отсутствии maintainer документирует решение и несогласие в issue/PR. Breaking change переносится в следующую major version.

## 4. Versioning

- Patch: clarifications, editorial fixes, non-normative examples.
- Minor: additive backwards-compatible contracts и profiles.
- Major: несовместимые normative changes или пересмотр conformance semantics.

Документ `DOA_STANDARD_v1.0.md` после tag `v1.0.0` считается frozen. Исправления выпускаются новой версией, а не переписыванием истории tag.

## 5. Release gates

Release MUST иметь:

- clean validation workflow;
- актуальные version и changelog;
- валидные schemas и example genome;
- проверенные локальные ссылки и diagrams;
- review normative diff;
- release-readiness status `ГОТОВО`;
- отсутствие known blocking security или compatibility defects;
- owner approval на tag и GitHub Release.

## 6. Conformance claims

Claim принадлежит реализации, а не DOA repository. Он MUST указывать standard version, profiles, scope, exclusions, evidence, verification date и responsible owner. Статусы: `UNVERIFIED`, `PARTIAL`, `VERIFIED`.

## 7. Security and disclosure

Security issue не публикуется с exploit details до triage. Используйте GitHub private vulnerability reporting, если оно включено, либо согласованный приватный канал владельца репозитория. Secrets немедленно отзываются; удаление из Git history не заменяет revocation.

## 8. Conflict of interest

Автор implementation-specific предложения раскрывает зависимость от vendor/product. Reference stack остаётся неэксклюзивным; коммерческая распространённость не является основанием для normative requirement.
