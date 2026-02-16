# Changelog

## Version 1.1.0 - SMTP Format Fix & TZ-Compliant Output

### Fixed

**1. SMTP Response Format (Issue: 550 detection не работал)**

**Проблема:**
- `smtp_response` не содержал код ответа, только текст
- Проверки `if "550" in smtp_response` не срабатывали
- Классификация SMTP rejected/unavailable была некорректной

**Решение:**
- SMTP response теперь формата: `"{code} {response_text}"`
- Все ветки (250, 550, другие коды, exceptions) возвращают единый формат
- Проверки изменены на `smtp_response.startswith("550")`

**Изменённые файлы:**
- `src/smtp/smtp_verifier.py` — форматирование всех SMTP ответов
- `src/main.py` — проверка на 550 через `startswith()`

**Пример:**
```python
# Было:
smtp_response = "User unknown"  # ❌ код потерян

# Стало:
smtp_response = "550 5.1.1 User unknown"  # ✅ код + текст
```

---

**2. Console Output Format (Соответствие требованиям ТЗ)**

**Проблема:**
- В консоль выводились внутренние статусы (`SMTP недоступен/заблокирован`)
- Не соответствовало ТЗ (требует только 3 статуса домена)

**Решение:**
- Введён метод `get_domain_status()` — возвращает статус по ТЗ:
  - "домен валиден"
  - "домен отсутствует"
  - "MX-записи отсутствуют или некорректны"
  - "неверный формат email"
- SMTP результат вынесен в отдельное поле: `SMTP: verified/rejected/unavailable`
- JSON сохраняет расширенные статусы (`status` + `smtp_status`)

**Изменённые файлы:**
- `src/models/result.py` — добавлен `SMTPStatus` enum и методы
- `src/main.py` — обновлён `print_results_console()`, добавлено поле `smtp_status`

**Пример консольного вывода:**
```
1. Email: test@gmail.com
   Status: домен валиден          # ← статус домена (ТЗ)
   Domain: gmail.com
   MX Records: gmail-smtp-in.l.google.com
   SMTP: unavailable              # ← отдельный SMTP статус
   Error: SMTP connection timeout
```

**Пример JSON:**
```json
{
  "email": "test@gmail.com",
  "status": "smtp_unavailable",      // расширенный статус
  "smtp_status": "unavailable",      // отдельное поле SMTP
  "domain": "gmail.com",
  "mx_records": ["gmail-smtp-in.l.google.com"],
  "smtp_response": null
}
```

---

### Added

- `SMTPStatus` enum — типизированные SMTP статусы (verified/rejected/unavailable/not_checked)
- `get_domain_status()` — метод для получения статуса по ТЗ
- `get_smtp_status_text()` — человекочитаемый SMTP статус
- Фильтрация пустых MX записей в консольном выводе

---

### Changed

- **SMTP response format:** все коды теперь в формате `"CODE text"`
- **Console output:** разделены domain status (ТЗ) и SMTP status (отдельно)
- **JSON output:** добавлено поле `smtp_status`
- **550 detection:** `startswith("550")` вместо `"550" in response`

---

### Documentation

- Обновлён `README.md` — новые примеры вывода
- Обновлён `TESTING_GUIDE.md` — скорректированы ожидаемые результаты
- Обновлён `QUICK_START.md` — добавлена таблица SMTP статусов

---

## Version 1.0.0 - Initial Release

### Features

- Email format validation (RFC 5322)
- DNS MX record lookup with caching
- SMTP handshake verification (EHLO → MAIL FROM → RCPT TO)
- CLI interface (`--emails`, `--file`, `--json`)
- Timeout protection (DNS: 5s, SMTP: 10s)
- Graceful error handling
- Logging (INFO/ERROR levels)
- Type hints and docstrings
- Production-ready code structure
