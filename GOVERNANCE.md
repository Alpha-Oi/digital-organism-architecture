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

Документ `DOA_STANDARD_v1.0.md` после tag `v1.0.0` считается frozen: tag не переписывается, а нормативное содержание не меняется на месте. Исправления выпускаются новой версией (`1.0.x` для errata, `1.x` для additive, `2.0` для breaking).

### Политика совместимости

- Идентификаторы механизмов (`C-01`…), требований (`REQ-…`), схем (`$id`) и состояний в `state-machines.yaml` стабильны в пределах major-версии: удаление или переименование — только в major.
- Minor-релиз MAY добавлять механизмы, требования, необязательные поля схем и состояния/переходы, не делающие существующие допустимые реализации недействительными. Новое обязательное требование для существующего профиля считается breaking; оно вводится как `Pattern`/optional либо в major.
- Patch-релиз содержит только clarifications, исправления опечаток и errata без изменения semantics.
- Дефект (противоречие между документами) исправляется errata по порядку приоритета из `docs/TERMINOLOGY.md`.

### Normative changes

Изменение `MUST`/`MUST NOT`, contract, state machine, схемы или conformance profile проходит: issue (concrete scenario, observable outcome) → proposal с полной карточкой Biology-to-IT (12 колонок) → review архитектуры, security и compatibility → обновление реестра требований, примеров valid/invalid, `CHANGELOG.md` → прохождение `scripts/validate_repository.py` → решение maintainer с документированным несогласием.

## 5. Release gates

Release MUST иметь:

- clean validation workflow;
- актуальные version и changelog;
- валидные schemas и example genome;
- проверенные локальные ссылки и diagrams;
- review normative diff;
- release-readiness status `ГОТОВО`;
- отсутствие known blocking security или compatibility defects;
- `VERSION`, `CHANGELOG.md`, README и канонический стандарт указывают одну версию;
- tag `vX.Y.Z` указывает на commit, на котором прошёл validation workflow; owner approval на tag и GitHub Release.

Рекомендуемая защита `main`: pull request с review (CODEOWNERS), обязательный status check `validate`, запрет force-push и удаления ветки, защита tags `v*`. Это настройки репозитория, а не содержимое стандарта.

## 6. Conformance claims

Claim принадлежит реализации, а не DOA repository. Он MUST указывать standard version, profiles, scope, exclusions, evidence, verification date, assessor и responsible owner. Статусы: `UNVERIFIED`, `PARTIAL`, `VERIFIED`. Соответствие определяется не наличием термина «DOA», а требованиями `specifications/requirements.yaml` и evidence по `docs/CONFORMANCE.md`; claim проверяется `scripts/check_conformance_claim.py`. DOA repository не сертифицирует реализации.

## 7. Security and disclosure

Security issue не публикуется с exploit details до triage. Используйте GitHub private vulnerability reporting, если оно включено, либо согласованный приватный канал владельца репозитория. Secrets немедленно отзываются; удаление из Git history не заменяет revocation.

## 8. Conflict of interest

Автор implementation-specific предложения раскрывает зависимость от vendor/product. Reference stack остаётся неэксклюзивным; коммерческая распространённость не является основанием для normative requirement.
