# AI Development Stack

**Контекст:** Ежедневная разработка с использованием AI как основного инструмента для планирования, генерации кода, ревью и тестирования.

---

## 1. IDE и AI-плагины

**Основной стек:**
- **IDE:** VS Code / Xcode (в зависимости от проекта)
- **AI-инструменты:** Claude (claude.ai) + ChatGPT (веб/API) + GitHub Copilot (для автокомплита)
- **Terminal integration:** Claude Code CLI для работы с кодовой базой напрямую из терминала
- **Workflow:** Claude для архитектурных решений и сложных задач → ChatGPT для быстрых правок и рутины → Copilot для inline suggestions во время набора кода
- **MCP серверы:** Использую Claude MCP для интеграции с GitHub (просмотр PR, issues), Figma (для UI-кода), filesystem access

**Почему такой микс:**
- Claude лучше держит контекст на длинных сессиях и дает более продуманную архитектуру
- ChatGPT быстрее для точечных fixes и рефакторинга
- Copilot удобен для автокомплита в IDE, но не заменяет планирование
- Claude Code позволяет работать с репозиторием без копирования кода в чат

---

## 2. Модели и задачи

**Claude Sonnet 3.5/4 (основная модель):**
- Архитектурное планирование (design docs, API contracts)
- Генерация сложных модулей (state management, networking layers)
- Code review (с чек-листами: security, performance, testability)
- Debugging сложных багов (multi-step reasoning)
- Рефакторинг legacy code (понимает контекст старого кода лучше)

**ChatGPT (GPT-4/GPT-4o):**
- Быстрые правки (typos, formatting, простые багфиксы)
- Генерация тестов (unit tests, mock data)
- Документация (README, inline comments, docstrings)
- SQL/regex/scripts (разовые утилиты, миграции)

**GitHub Copilot (в IDE):**
- Автокомплит повторяющихся паттернов (boilerplate, getters/setters)
- Генерация типичных функций (mappers, validators, formatters)
- НЕ использую для архитектурных решений (низкое качество)

**Критерий выбора модели:**
- Сложность >3 файлов → Claude
- Точечная правка 1 файла → ChatGPT
- Inline autocomplete → Copilot

---

## 3. MCP (Model Context Protocol)

**Используемые MCP серверы (через Claude):**

**GitHub MCP:**
- Просмотр PR, issues, commits без переключения в браузер
- Анализ diff перед code review
- Создание issues с контекстом (баг-репорты, feature requests)

**Filesystem MCP:**
- Навигация по проекту (поиск файлов, чтение структуры)
- Grep/поиск по кодовой базе
- Чтение нескольких файлов одновременно для контекста

**Figma MCP (для frontend):**
- Генерация UI-кода из Figma-макетов
- Синхронизация design tokens (цвета, шрифты, отступы)

**Browser MCP (Claude в Chrome):**
- Тестирование веб-приложений
- Скриншоты для bug reports
- Заполнение форм, E2E testing

**Преимущества MCP:**
- Не нужно копировать файлы в чат вручную
- AI видит актуальное состояние репозитория
- Меньше context switching (всё в одном интерфейсе)

---

## 4. System Instructions / .cursorrules

**Использую кастомные инструкции (аналог .cursorrules) через Claude Projects:**

### Основные правила

**1. Architecture & Code Style:**
```
- SOLID principles, избегай God Objects
- Prefer composition over inheritance
- Single source of truth (no duplicate logic)
- Явные имена (no abbreviations: usr → user, msg → message)
- Type hints везде (Python), строгая типизация (Swift/TS)
- Docstrings для всех публичных функций
```

**2. Development Process:**
```
- Small diffs: одна задача = один PR (<300 строк)
- Step-by-step: планирование → реализация → тесты → ревью
- Test first: критичные функции сначала покрыть тестами
- Avoid premature optimization (make it work → make it right → make it fast)
- No TODO comments (создавай issues вместо комментариев)
```

**3. Security & Performance:**
```
- Валидация всех входных данных (user input, API responses)
- No hardcoded secrets (env vars, config files)
- SQL injection prevention (prepared statements, ORM)
- XSS/CSRF protection (для веба)
- Timeout на всех сетевых операциях
- Graceful error handling (try-except-finally, no silent failures)
```

**4. AI-Specific Rules:**
```
- Verify by running: не принимать код без запуска
- Show your work: объяснять решения (почему этот подход, а не другой)
- Cite sources: линки на документацию/Stack Overflow, если использовал
- Flag assumptions: явно говорить, что предположено (например, "предполагаю, что API возвращает JSON")
- Ask when unclear: лучше уточнить ТЗ, чем додумывать
```

**5. Code Review Checklist (для AI-ревью):**
```
- Security: secrets, input validation, auth/authz
- Performance: N+1 queries, memory leaks, blocking operations
- Error handling: все exceptions обработаны, логирование
- Testability: можно ли покрыть unit-тестами
- Readability: понятен ли код через 6 месяцев
- Breaking changes: обратная совместимость API
```

### Самые полезные правила (топ-3):

**1. "Small diffs" (PR <300 строк):**
- Заставляет AI фокусироваться на одной задаче
- Упрощает code review
- Меньше bugs в продакшн (проще найти причину при откате)

**2. "Verify by running" (запускать перед коммитом):**
- Выявляет hallucinations (AI "забыл" импорт, неправильный тип)
- Проверяет edge cases (пустые строки, null, граничные значения)
- На практике: 30% AI-кода требует правок после первого запуска

**3. "No duplicate logic" (DRY принцип):**
- AI любит копировать код вместо переиспользования
- Правило заставляет создавать helper functions/utilities
- Упрощает рефакторинг (одно место изменений вместо 5)

---

## Workflow: Типичная задача с AI

**Пример: "Добавить feature X в проект"**

**1. Planning (Claude):**
```
Prompt: "Нужно добавить {feature}. Проанализируй кодовую базу (MCP filesystem),
предложи архитектуру, покажи какие файлы затронуты, оцени risk/effort"
→ Получаю: design doc, список файлов, риски, альтернативные подходы
```

**2. Implementation (Claude step-by-step):**
```
Prompt: "Реализуй step 1: создай модель данных с валидацией"
→ Проверяю код, запускаю
Prompt: "Step 2: добавь API endpoint с rate limiting"
→ Проверяю, тесты
Prompt: "Step 3: интегрируй с существующим сервисом"
→ Финальная проверка
```

**3. Testing (ChatGPT для генерации):**
```
Prompt: "Создай unit-тесты для {module}, покрой edge cases"
→ Проверяю coverage (должно быть >80%)
```

**4. Review (Claude с чек-листом):**
```
Prompt: "Code review по чек-листу: security, performance, testability"
→ Исправляю замечания
```

**5. Documentation (ChatGPT):**
```
Prompt: "Обнови README: добавь секцию про {feature}, примеры использования"
→ Проверяю, коммичу
```

---

## Как я избегаю ошибок AI

### 1. Verify by Running
**Проблема:** AI hallucinations (неправильные API, несуществующие библиотеки)
**Решение:** Запускаю каждый сгенерированный фрагмент. Если не компилируется/не запускается — требую исправления с объяснением.
**Пример:** AI предложил `import nonexistent_lib` → ошибка импорта → переспросил "проверь, что эта библиотека существует в requirements.txt"

### 2. Small Diffs (PR <300 строк)
**Проблема:** AI генерирует большие куски кода, где трудно найти ошибки
**Решение:** Разбиваю задачу на шаги по 50-100 строк. Проверяю каждый шаг перед следующим.
**Пример:** Вместо "создай весь CRUD API" → "создай модель" → "создай GET endpoint" → "добавь POST" → "тесты"

### 3. Explicit Context (Single Source of Truth)
**Проблема:** AI "забывает" ранее согласованные решения в длинных сессиях
**Решение:** Использую Claude Projects (persistent context) или записываю решения в DECISIONS.md в репозитории.
**Пример:** "Мы договорились использовать Pydantic для валидации" → AI предложил jsonschema → отсылка к DECISIONS.md

### 4. Ask, Don't Assume
**Проблема:** AI додумывает требования, которых не было в ТЗ
**Решение:** Требую явно спрашивать при неясностях. Если AI что-то предположил — прошу обосновать.
**Пример:** AI добавил кеширование без запроса → "почему добавил кеш? В ТЗ этого не было" → либо убираю, либо добавляю в ТЗ

### 5. Test Edge Cases Manually
**Проблема:** AI-тесты часто проверяют happy path, игнорируя edge cases
**Решение:** Сам добавляю тесты на null, пустые строки, граничные значения, race conditions.
**Пример:** AI создал `def divide(a, b): return a / b` → я добавил тест `divide(1, 0)` → обнаружил отсутствие обработки ZeroDivisionError

---

## Метрики эффективности

**Ускорение разработки:** ~3x (задача 6 часов вручную → 2 часа с AI)
**Quality gate:** Code review всё равно обязателен (AI не заменяет senior ревью)
**Bug rate:** Примерно такой же, как при ручной разработке (при соблюдении "verify by running")
**Refactoring speed:** ~5x (AI быстро переименовывает/перемещает код через всю кодовую базу)

---

## Итоги

**AI как инструмент, а не замена:**
- Планирование остается за человеком (AI предлагает варианты, я выбираю)
- Архитектурные решения требуют контроля (AI может предложить overkill)
- Тестирование обязательно (AI-код не production-ready "из коробки")
- Security review критичен (AI может пропустить SQL injection, XSS)

**Главное правило:** AI ускоряет execution, но не отменяет ответственность за качество кода.
