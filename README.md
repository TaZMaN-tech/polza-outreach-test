# Инструменты проверки Email и отправки в Telegram

Production-ready Python инструменты для проверки email и отправки сообщений в Telegram.

## Проекты

1. **Инструмент проверки Email** (Задача 1) — DNS MX lookup + SMTP handshake проверка
2. **Telegram Sender** (Задача 2) — Отправка текстовых файлов в Telegram через Bot API

---

# Задача 1: Инструмент проверки Email

Production-ready Python инструмент для проверки email с использованием DNS MX записей и SMTP handshake валидации.

## Возможности

- **Валидация формата email** — Проверка по RFC 5322 через regex
- **DNS MX record lookup** — Проверка домена и извлечение MX серверов
- **SMTP handshake проверка** — Выполнение EHLO → MAIL FROM → RCPT TO без отправки писем
- **In-memory MX кеширование** — Кеширование MX записей по доменам для производительности
- **Защита от зависания** — Настраиваемые таймауты для всех сетевых операций
- **Обработка ошибок** — Все исключения перехватываются и логируются
- **Несколько методов ввода** — CLI аргументы или файл
- **JSON экспорт** — Опциональный JSON вывод для автоматизации

## Установка

### Требования

- Python 3.11+
- pip

### Настройка

```bash
# Перейдите в директорию проекта
cd polza_outreach_test

# Установите зависимости
pip install -r requirements.txt
```

## Использование

### Базовое использование

**Проверка email из командной строки:**
```bash
python -m src.main --emails "test@example.com,user@gmail.com"
```

**Проверка email из файла:**
```bash
python -m src.main --file emails.txt
```

**Сохранение результатов в JSON:**
```bash
python -m src.main --emails "test@example.com" --json output.json
```

### Формат входного файла

Создайте текстовый файл с одним email на строку:

```text
test@example.com
user@gmail.com
admin@domain.org
```

### Вывод

**Консольный вывод:**
```
================================================================================
РЕЗУЛЬТАТЫ ПРОВЕРКИ EMAIL
================================================================================

1. Email: test@gmail.com
   Status: домен валиден
   Domain: gmail.com
   MX Records: gmail-smtp-in.l.google.com, alt1.gmail-smtp-in.l.google.com
   SMTP: verified
   SMTP Response: 250 2.1.5 OK

2. Email: invalid@nonexistentdomain12345.com
   Status: домен отсутствует
   Domain: nonexistentdomain12345.com
   Error: Domain does not exist in DNS

3. Email: badformat
   Status: домен отсутствует
   Error: Email format is invalid

4. Email: user@example.com
   Status: домен валиден
   Domain: example.com
   MX Records: mail.example.com
   SMTP: unavailable
   Error: SMTP connection timeout

================================================================================
```

**JSON вывод** (если указан `--json`):
```json
{
  "total": 3,
  "results": [
    {
      "email": "test@gmail.com",
      "status": "valid",
      "smtp_status": "verified",
      "domain": "gmail.com",
      "mx_records": ["gmail-smtp-in.l.google.com"],
      "smtp_response": "250 2.1.5 OK",
      "error_message": null
    },
    {
      "email": "invalid@nonexistentdomain12345.com",
      "status": "domain_not_found",
      "smtp_status": "not_checked",
      "domain": "nonexistentdomain12345.com",
      "mx_records": null,
      "smtp_response": null,
      "error_message": "Domain does not exist in DNS"
    },
    {
      "email": "rejected@example.com",
      "status": "smtp_rejected",
      "smtp_status": "rejected",
      "domain": "example.com",
      "mx_records": ["mail.example.com"],
      "smtp_response": "550 5.1.1 User unknown",
      "error_message": "Email rejected with code 550"
    }
  ]
}
```

## Статусы проверки

### Консольный вывод (согласно ТЗ)

**ТЗ указывает ТОЛЬКО 3 возможных статуса:**

| Статус | Описание | Когда показывается |
|--------|----------|-------------------|
| **домен валиден** | Домен валиден (имеет DNS записи и MX записи) | Домен существует + найдены MX записи |
| **домен отсутствует** | Домен не существует | Домен не найден ИЛИ неверный формат email |
| **MX-записи отсутствуют или некорректны** | MX записи отсутствуют или некорректны | Домен существует, но нет MX записей |

**Примечание:** Неверный формат email показывается как "домен отсутствует" (согласно ТЗ). Детали в поле Error.

### SMTP статус (отдельное поле)

| SMTP статус | Описание |
|-------------|----------|
| **verified** | SMTP сервер принял email (ответ 250) |
| **rejected** | SMTP сервер отклонил email (ответ 550) |
| **unavailable** | SMTP сервер недоступен/таймаут/заблокирован |
| **not checked** | SMTP проверка не выполнялась |

### JSON статусы (расширенные)

| Статус | Описание |
|--------|----------|
| **valid** | Email прошел все проверки (формат, DNS, SMTP) |
| **invalid_format** | Неверный формат email |
| **domain_not_found** | Домен не существует в DNS |
| **no_mx_records** | MX записи отсутствуют или некорректны |
| **smtp_unavailable** | SMTP сервер недоступен или заблокирован |
| **smtp_rejected** | SMTP сервер отклонил email адрес |

## Конфигурация

Отредактируйте `config.py` для настройки:

```python
# SMTP конфигурация
SMTP_TIMEOUT = 10  # секунды
SMTP_PORT = 25
SMTP_FROM_EMAIL = "verify@example.com"

# DNS конфигурация
DNS_TIMEOUT = 5  # секунды
DNS_NAMESERVERS = None  # или ['8.8.8.8', '8.8.4.4']

# Логирование
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL

# Кеш
ENABLE_MX_CACHE = True
```

## Архитектура

```
src/
├── main.py                    # CLI точка входа, оркестрация
├── validators/
│   └── email_validator.py     # Валидация формата email и извлечение домена
├── dns/
│   └── mx_checker.py          # MX record lookup с кешированием
├── smtp/
│   └── smtp_verifier.py       # SMTP handshake проверка
├── models/
│   └── result.py              # Модели данных (VerificationResult, статусы)
└── utils/
    └── logger.py              # Конфигурация логирования
```

## Как это работает

1. **Валидация формата** — Проверка email по RFC 5322 regex
2. **Извлечение домена** — Извлечение домена из email адреса
3. **Проверка существования домена** — Проверка существования домена в DNS (A/AAAA записи)
4. **MX Lookup** — Получение и кеширование MX записей для домена
5. **SMTP Handshake** — Подключение к MX серверу и выполнение:
   - `EHLO` — Идентификация к серверу
   - `MAIL FROM` — Установка отправителя
   - `RCPT TO` — Проверка получателя
   - Анализ кодов ответа (250 = валиден, 550 = отклонен)
6. **Graceful Cleanup** — Всегда корректно закрывает SMTP соединения

## Обработка ошибок

- Все сетевые операции имеют таймауты (DNS: 5с, SMTP: 10с)
- Исключения перехватываются на каждом уровне
- SMTP соединения всегда закрываются (try-finally)
- Механизм fallback пробует несколько MX серверов
- Детальное логирование ошибок для отладки

## Ограничения

- Некоторые почтовые серверы используют greylisting или блокируют попытки проверки
- Корпоративные файрволы могут блокировать исходящий порт 25 (SMTP)
- Catch-all домены могут принимать любой email адрес
- При массовой проверке может возникнуть rate limiting

## Примеры тестирования

См. примеры ниже для тестирования инструмента.

---

# Задача 2: Telegram Sender

Отправка текстовых файлов в Telegram чаты через Bot API.

## Быстрый старт

**Установка:**
```bash
pip install -r requirements.txt
```

**Использование (с CLI аргументами):**
```bash
python -m src.telegram.telegram_sender \
  --file message.txt \
  --token "123456:ABC-DEF..." \
  --chat "123456789"
```

**Использование (с переменными окружения - рекомендуется):**
```bash
export TELEGRAM_BOT_TOKEN="123456:ABC-DEF..."
export TELEGRAM_CHAT_ID="123456789"
python -m src.telegram.telegram_sender --file message.txt
```

**Проверка bot token:**
```bash
python -m src.telegram.telegram_sender --test --token "123456:ABC-DEF..."
```

**Полная документация:** См. [README_TELEGRAM.md](README_TELEGRAM.md)

---

# Задача 3: Архитектура системы

Архитектура email outreach системы для 1200 аккаунтов (мульти-клиент, высокая доступность, минимальная стоимость).

**Документ:** [TASK3_ARCHITECTURE.md](TASK3_ARCHITECTURE.md)

**Ключевые моменты:**
- Инфраструктура: 3 VPS ноды ($48/мес) + SMTP аккаунты ($60/мес)
- SMTP пул: 15-20 аккаунтов у 3-4 провайдеров (ротация + health checks)
- Очередь: Redis + Celery (rate limiting 100/мин на всю систему)
- Мониторинг: Prometheus + Grafana + проверка blacklist
- Общая стоимость: **$118-168/мес**

---

# Задача 4: AI Development Stack

Персональный AI workflow для ежедневной разработки (Claude, ChatGPT, Copilot).

**Документ:** [TASK4_AI_STACK.md](TASK4_AI_STACK.md)

**Ключевые моменты:**
- **Workflow:** Claude для архитектуры → ChatGPT для правок → Copilot для автодополнения
- **MCP:** Интеграция GitHub, Filesystem, Figma, Browser
- **Топ правила:** Small diffs (<300 LOC), Verify by running, No duplicate logic
- **Контроль качества:** Пошаговое планирование, security чек-листы, тестирование edge cases
