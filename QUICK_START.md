# Quick Start Guide

## Установка

```bash
# Перейдите в директорию проекта
cd polza_outreach_test

# Установите зависимости
pip3 install -r requirements.txt
```

## Примеры использования

### 1. Проверка одного email

```bash
python3 -m src.main --emails "test@gmail.com"
```

### 2. Проверка нескольких email (через запятую)

```bash
python3 -m src.main --emails "test@gmail.com,support@github.com,invalid@fake.com"
```

### 3. Проверка email из файла

```bash
python3 -m src.main --file test_emails.txt
```

### 4. Сохранение результатов в JSON

```bash
python3 -m src.main --emails "test@gmail.com" --json results.json
```

### 5. Batch-проверка с JSON выводом

```bash
python3 -m src.main --file test_emails.txt --json output.json
```

## Тестовые примеры

### Пример 1: Несуществующий домен

```bash
python3 -m src.main --emails "user@nonexistentdomain99999.com"
```

**Ожидаемый результат:**
```
Status: домен отсутствует
Domain: nonexistentdomain99999.com
Error: Domain does not exist in DNS
```

### Пример 2: Невалидный формат email

```bash
python3 -m src.main --emails "invalid-email-without-at-sign"
```

**Ожидаемый результат:**
```
Status: домен отсутствует
Error: Email format is invalid
```

**Примечание:** Согласно ТЗ, невалидный формат показывается как "домен отсутствует" (детали в Error).

### Пример 3: Несколько email с разными статусами

```bash
python3 -m src.main --emails "test@gmail.com,invalid@fake123.com,badformat"
```

**Ожидаемый результат:**
- Email 1: `домен валиден` + SMTP может быть недоступен (блокировка порта 25)
- Email 2: `домен отсутствует` (домен не найден)
- Email 3: `домен отсутствует` (неверный формат, детали в Error)

### Пример 3: Несколько email с разными статусами

```bash
python3 -m src.main --emails "test@gmail.com,invalid@fake123.com,badformat"
```

**Ожидаемый результат:**
- Email 1: SMTP может быть недоступен (блокировка порта 25)
- Email 2: Домен отсутствует
- Email 3: Неверный формат

## Интерпретация результатов

### Статусы (согласно ТЗ - ТОЛЬКО 3 статуса)

| Статус | Описание | Когда показывается |
|--------|----------|-------------------|
| **домен валиден** | ✅ Домен существует и имеет MX-записи | Формат OK + DNS OK + MX OK |
| **домен отсутствует** | ❌ Домен не существует ИЛИ неверный формат | NXDOMAIN в DNS или невалидный формат email |
| **MX-записи отсутствуют или некорректны** | ❌ Нет MX-записей | Домен есть, но MX нет |

**Примечание:** Невалидный формат email показывается как "домен отсутствует". Детали в поле Error.

### SMTP Статусы (отдельное поле)

| SMTP Статус | Описание | Причина |
|-------------|----------|---------|
| **verified** | ✅ SMTP подтвердил email | Код 250 от сервера |
| **rejected** | ❌ SMTP отклонил email | Код 550 (user not found) |
| **unavailable** | ⚠️ SMTP недоступен | Timeout, firewall, connection refused |
| **not checked** | — SMTP не проверялся | Домен отсутствует или нет MX |

### Частые причины "SMTP недоступен"

1. **Блокировка порта 25** — ISP или корпоративный файрволл блокирует исходящие SMTP-соединения
2. **Greylisting** — Mail-сервер временно блокирует неизвестные источники
3. **Anti-verification** — Сервер блокирует SMTP-верификацию (Gmail, Yahoo, Outlook часто делают это)
4. **Network issues** — Проблемы с сетью или DNS-резолвингом

## Решение проблем

### SMTP всегда недоступен?

**Проверьте доступность порта 25:**
```bash
telnet gmail-smtp-in.l.google.com 25
```

Если не подключается — ваш ISP или сеть блокирует SMTP.

**Решение:**
- Используйте другую сеть (не корпоративную)
- Запустите на VPS/облачном сервере
- Обратитесь к ISP для разблокировки порта 25

### DNS не резолвится?

**Используйте публичные DNS-серверы:**

Отредактируйте `config.py`:
```python
DNS_NAMESERVERS = ['8.8.8.8', '8.8.4.4']  # Google DNS
```

## Структура проекта

```
polza_outreach_test/
├── src/
│   ├── main.py                 # CLI + оркестрация
│   ├── validators/
│   │   └── email_validator.py  # Валидация формата email
│   ├── dns/
│   │   └── mx_checker.py       # DNS MX lookup + кеш
│   ├── smtp/
│   │   └── smtp_verifier.py    # SMTP handshake
│   ├── models/
│   │   └── result.py           # Модели результатов
│   └── utils/
│       └── logger.py           # Логирование
├── config.py                   # Конфигурация
├── requirements.txt            # Зависимости
├── README.md                   # Полная документация
├── TESTING_GUIDE.md            # Детальные тестовые сценарии
└── test_emails.txt             # Пример входного файла
```

## Подробная документация

- **README.md** — Полная документация с описанием архитектуры
- **TESTING_GUIDE.md** — 8 тестовых сценариев с ожидаемыми результатами
- **config.py** — Настройка таймаутов, логирования, DNS

## Дополнительно

### Включить DEBUG-логи

Отредактируйте `config.py`:
```python
LOG_LEVEL = "DEBUG"  # Вместо INFO
```

Теперь будут видны все DNS/SMTP операции:
```
DEBUG - Connecting to SMTP server: gmail-smtp-in.l.google.com:25
DEBUG - Sending EHLO to gmail-smtp-in.l.google.com
DEBUG - Sending MAIL FROM: verify@example.com
DEBUG - Sending RCPT TO: test@gmail.com
```

### Изменить MAIL FROM адрес

Отредактируйте `config.py`:
```python
SMTP_FROM_EMAIL = "your-email@yourdomain.com"
```

Некоторые SMTP-серверы проверяют валидность MAIL FROM.

## Успешный запуск

Инструмент работает корректно, если:
1. ✅ Невалидный формат распознается
2. ✅ Несуществующие домены обнаруживаются
3. ✅ MX-записи извлекаются для существующих доменов
4. ✅ Логирование работает
5. ✅ JSON-экспорт создается

Даже если SMTP заблокирован (статус "SMTP недоступен"), это нормально и показывает, что код работает правильно, но порт 25 заблокирован на уровне сети.
