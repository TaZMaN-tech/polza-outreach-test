# Testing Guide

Примеры команд для тестирования email verification tool.

## Перед запуском

Убедитесь, что зависимости установлены:
```bash
pip3 install -r requirements.txt
```

---

## Тестовые сценарии

### 1. Проверка валидного email (Gmail)

**Команда:**
```bash
python3 -m src.main --emails "test@gmail.com"
```

**Ожидаемый результат:**
- Status: `домен валиден`
- Domain: `gmail.com`
- MX Records: найдены (например, `gmail-smtp-in.l.google.com`)
- SMTP: `verified`
- SMTP Response: `250 2.1.5 OK` или подобное

**Что проверяется:**
- ✅ Формат email валиден
- ✅ Домен существует
- ✅ MX-записи найдены
- ✅ SMTP-сервер ответил положительно

---

### 2. Проверка несуществующего домена

**Команда:**
```bash
python3 -m src.main --emails "user@nonexistentdomain99999.com"
```

**Ожидаемый результат:**
- Status: `домен отсутствует`
- Domain: `nonexistentdomain99999.com`
- Error: "Domain does not exist in DNS"

**Что проверяется:**
- ✅ Формат email валиден
- ❌ Домен не найден в DNS

---

### 3. Проверка домена без MX-записей

**Команда:**
```bash
python3 -m src.main --emails "admin@example.com"
```

**Ожидаемый результат:**
- Status: `домен валиден` или `MX-записи отсутствуют или некорректны`
- Domain: `example.com`
- SMTP: `unavailable` (если MX найдены, но SMTP недоступен)

**Примечание:**
`example.com` существует в DNS, но может не иметь корректных MX-записей или доступных SMTP-серверов.

**Что проверяется:**
- ✅ Формат email валиден
- ✅ Домен существует
- ❌ MX-записи отсутствуют или SMTP недоступен

---

### 4. Проверка невалидного формата email

**Команда:**
```bash
python3 -m src.main --emails "invalid-email-format"
```

**Ожидаемый результат:**
- Status: `домен отсутствует`
- Error: "Email format is invalid"

**Примечание:**
Согласно ТЗ (только 3 статуса), невалидный формат показывается как "домен отсутствует". Детали в поле Error.

**Что проверяется:**
- ❌ Формат email невалиден (нет символа @)
- ✅ ТЗ-совместимый вывод (только 3 статуса)

---

### 5. Проверка нескольких email через запятую

**Команда:**
```bash
python3 -m src.main --emails "test@gmail.com,support@github.com,invalid@fake123.com"
```

**Ожидаемый результат:**
- 3 результата:
  1. `test@gmail.com` — валиден
  2. `support@github.com` — валиден
  3. `invalid@fake123.com` — домен отсутствует или SMTP недоступен

**Что проверяется:**
- ✅ Обработка нескольких email
- ✅ Кеширование MX-записей (если домены повторяются)

---

### 6. Проверка email из файла

**Создайте файл `test_emails.txt`:**
```
test@gmail.com
support@github.com
invalid@nonexistentdomain99999.com
admin@example.com
```

**Команда:**
```bash
python3 -m src.main --file test_emails.txt
```

**Ожидаемый результат:**
- 4 результата с различными статусами

**Что проверяется:**
- ✅ Чтение email из файла
- ✅ Batch-обработка

---

### 7. Сохранение результатов в JSON

**Команда:**
```bash
python3 -m src.main --emails "test@gmail.com,invalid@fake.com" --json results.json
```

**Ожидаемый результат:**
- Консольный вывод + файл `results.json`
- JSON содержит структурированные результаты

**Проверка JSON:**
```bash
cat results.json
```

**Что проверяется:**
- ✅ JSON-экспорт результатов
- ✅ Корректная сериализация

---

### 8. Проверка SMTP timeout/блокировки

**Команда:**
```bash
python3 -m src.main --emails "user@yahoo.com"
```

**Возможный результат:**
- Status: `SMTP недоступен/заблокирован`
- Причина: Yahoo может блокировать SMTP-верификацию или использовать greylisting

**Что проверяется:**
- ✅ Обработка SMTP timeout
- ✅ Обработка недоступных SMTP-серверов
- ✅ Graceful degradation

---

## Быстрый тест (все сценарии)

**Создайте файл `full_test.txt`:**
```
test@gmail.com
support@github.com
invalid@nonexistentdomain99999.com
admin@example.com
badformat
user@yahoo.com
```

**Запустите:**
```bash
python3 -m src.main --file full_test.txt --json full_results.json
```

**Проверьте:**
```bash
cat full_results.json | python3 -m json.tool
```

---

## Проверка логирования

Для более подробного вывода измените `LOG_LEVEL` в `config.py`:

```python
LOG_LEVEL = "DEBUG"  # Вместо INFO
```

Затем запустите любую команду и увидите детальные логи DNS/SMTP операций.

---

## Известные ограничения при тестировании

1. **Gmail/Yahoo/Outlook** — могут блокировать SMTP-верификацию или использовать greylisting
2. **Корпоративные сети** — могут блокировать исходящий порт 25
3. **Catch-all домены** — могут принимать любой email (ложноположительные результаты)
4. **Rate limiting** — при массовой проверке возможна блокировка по IP

---

## Отладка проблем

**Если SMTP всегда недоступен:**
1. Проверьте, что порт 25 не заблокирован файрволом:
   ```bash
   telnet gmail-smtp-in.l.google.com 25
   ```
2. Убедитесь, что ваш ISP не блокирует SMTP
3. Попробуйте другую сеть (не корпоративную)

**Если DNS не резолвится:**
1. Проверьте интернет-подключение
2. Попробуйте указать публичные DNS в `config.py`:
   ```python
   DNS_NAMESERVERS = ['8.8.8.8', '8.8.4.4']  # Google DNS
   ```

---

## Успешный запуск

Если хотя бы один из email (`test@gmail.com` или `support@github.com`) показывает статус `домен валиден`, значит инструмент работает корректно!
