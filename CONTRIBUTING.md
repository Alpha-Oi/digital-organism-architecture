# Contributing to DOA

Digital Organism Architecture — нормативный метаархитектурный стандарт. Изменения оцениваются по проверяемости, совместимости и ясности, а не по количеству добавленных биологических аналогий.

## Типы изменений

- **Clarification** — устраняет неоднозначность без изменения требований.
- **Additive** — добавляет механизм, schema, evidence или профиль без нарушения v1 compatibility.
- **Normative** — изменяет `MUST`, contract, state machine, conformance profile или обязательное evidence.
- **Breaking** — делает существующее соответствие недействительным; требует следующей major version.

## Требования к Biology-to-IT mapping

Новый механизм принимается только если он фундаментально оправдан, архитектурно полезен и определены все колонки матрицы `docs/BIOLOGY_TO_IT_MAPPING.md`:

1. biological mechanism;
2. digital responsibility;
3. digital component;
4. contract;
5. protocol / state machine;
6. invariant;
7. failure mode;
8. security / safety control;
9. observability;
10. evidence;
11. нормативный статус (`Profile`): механизм без архитектурной необходимости получает `Pattern`, а не `Core`;
12. возможный implementation stack (Приложение A) без vendor lock-in.

Нормативная строка MUST быть связана с требованием в `specifications/requirements.yaml`, а новое состояние или переход — отражено в `specifications/state-machines.yaml`, схемах, диаграммах и `docs/LIFECYCLE.md`. Метафора без этих полей не является изменением стандарта.

## Рабочий процесс

1. Откройте issue с пользовательским сценарием, наблюдаемым результатом и gap в текущем стандарте.
2. Для normative change опишите compatibility и migration impact.
3. Измените минимальный связный набор документов и schemas.
4. Обновите `CHANGELOG.md` и при новой находке — `CHANGES_AND_NEW_FINDINGS.md`; для новой или изменённой схемы добавьте valid и invalid примеры в `reference/examples/`.
5. Запустите проверку:

   ```bash
   python -m pip install -r requirements-validation.txt
   python scripts/validate_repository.py
   git diff --check
   ```

6. В pull request приложите evidence и явно укажите непроверенные утверждения.

## Review requirements

- Clarification: минимум один maintainer review.
- Additive или normative change: review архитектуры, security implications и schema compatibility.
- Breaking change: ADR/RFC, migration plan и major-version decision.
- Изменение release criteria или governance не утверждается только автором изменения.

## Запрещённые сокращения процесса

- нельзя объявлять биологическую аналогию доказательством engineering correctness;
- нельзя добавлять secrets, credentials, private data или unrestricted reasoning traces;
- нельзя смешивать DOA с кодом конкретной реализации;
- нельзя ослаблять conformance requirement ради одного vendor stack;
- нельзя объявлять `VERIFIED` без ссылки на evidence pack.
