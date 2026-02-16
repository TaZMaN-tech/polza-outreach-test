# Telegram Sender - Документация

Production-ready инструмент для отправки текстовых файлов в Telegram чаты через Bot API.

## Возможности

- ✅ Чтение текстовых файлов (UTF-8)
- ✅ Отправка в приватные/групповые чаты/каналы
- ✅ Валидация токена бота
- ✅ Защита от HTTP таймаутов
- ✅ Обработка ошибок (сеть, API, файлы)
- ✅ Переиспользование сессий (requests.Session)
- ✅ Поддержка переменных окружения
- ✅ Поддержка форматирования Markdown/HTML
- ✅ Логирование (INFO/ERROR)

---

## Установка

```bash
# Установка зависимостей
pip3 install -r requirements.txt
```

---

## Настройка Telegram бота

### 1. Создание бота через @BotFather

1. Откройте Telegram и найдите **@BotFather**
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для выбора имени и username бота
4. **Сохраните токен бота** (выглядит как `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

### 2. Получение Chat ID

#### Вариант A: Для приватного чата (личное сообщение)

1. Отправьте любое сообщение вашему боту
2. Откройте: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
3. Найдите `"chat":{"id":123456789}` в ответе
4. Используйте это число как `CHAT_ID`

#### Вариант B: Для группы/канала

1. Добавьте бота в вашу группу/канал
2. Отправьте сообщение в группе
3. Откройте: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. Найдите `"chat":{"id":-100123456789}` (обратите внимание на минус)
5. Используйте это число (с минусом) как `CHAT_ID`

#### Вариант C: Использование бота (проще)

1. Добавьте **@userinfobot** в ваш чат
2. Он сразу покажет вам chat ID

---

## Использование

### Базовое использование

```bash
python3 -m src.telegram.telegram_sender \
  --file message.txt \
  --token "123456:ABC-DEF..." \
  --chat "123456789"
```

### Использование переменных окружения (рекомендуется)

```bash
# Установить учётные данные один раз
export TELEGRAM_BOT_TOKEN="123456:ABC-DEF..."
export TELEGRAM_CHAT_ID="123456789"

# Отправить сообщение
python3 -m src.telegram.telegram_sender --file message.txt
```

### С форматированием Markdown

```bash
python3 -m src.telegram.telegram_sender \
  --file message.txt \
  --parse-mode Markdown
```

### Тест подключения к боту

```bash
python3 -m src.telegram.telegram_sender \
  --test \
  --token "123456:ABC-DEF..."
```

---

## Аргументы CLI

| Аргумент | Описание | Обязательный | Альтернатива |
|----------|----------|--------------|--------------|
| `--file` | Путь к текстовому файлу | Да (для отправки) | - |
| `--token` | Токен бота от @BotFather | Да | Переменная окружения `TELEGRAM_BOT_TOKEN` |
| `--chat` | Chat ID | Да (для отправки) | Переменная окружения `TELEGRAM_CHAT_ID` |
| `--parse-mode` | Формат сообщения (Markdown/HTML) | Нет | - |
| `--test` | Только тест токена бота | Нет | - |
| `--timeout` | HTTP таймаут в секундах | Нет (по умолчанию: 10) | - |

---

## Примеры

### Пример 1: Отправка простого сообщения

**Создайте файл `message.txt`:**
```
Hello from Telegram Bot!
This is a test message.
```

**Отправка:**
```bash
python3 -m src.telegram.telegram_sender \
  --file message.txt \
  --token "YOUR_TOKEN" \
  --chat "YOUR_CHAT_ID"
```

**Ожидаемый вывод:**
```
✅ Message sent successfully to chat 123456789
   File: message.txt
   Length: 54 characters
```

---

### Пример 2: Отправка с Markdown

**Создайте файл `formatted.txt`:**
```
*Bold text*
_Italic text_
`Code block`
[Link](https://example.com)
```

**Отправка:**
```bash
python3 -m src.telegram.telegram_sender \
  --file formatted.txt \
  --token "YOUR_TOKEN" \
  --chat "YOUR_CHAT_ID" \
  --parse-mode Markdown
```

---

### Пример 3: Тест токена бота

```bash
python3 -m src.telegram.telegram_sender \
  --test \
  --token "123456:ABC-DEF..."
```

**Ожидаемый вывод (успех):**
```
✅ Bot token is valid. Connection test successful.
```

**Ожидаемый вывод (ошибка):**
```
❌ Connection test failed: Unauthorized
```

---

### Пример 4: Использование переменных окружения

**Настройка (добавьте в `~/.bashrc` или `~/.zshrc`):**
```bash
export TELEGRAM_BOT_TOKEN="123456:ABC-DEF..."
export TELEGRAM_CHAT_ID="123456789"
```

**Использование:**
```bash
# Перезагрузить shell
source ~/.bashrc

# Отправка без учётных данных в команде
python3 -m src.telegram.telegram_sender --file message.txt
```

---

## Обработка ошибок

### Ошибка: Файл не найден

```
❌ File error: File not found: message.txt
```

**Решение:** Проверьте, что путь к файлу правильный

---

### Ошибка: Пустой файл

```
❌ File is empty or contains only whitespace
```

**Решение:** Добавьте содержимое в файл

---

### Ошибка: Неверный токен бота

```
❌ Connection test failed: Unauthorized
```

**Решение:**
- Проверьте, что токен правильный
- Убедитесь, что нет лишних пробелов
- Формат токена: `123456:ABC-DEF...`

---

### Ошибка: Неверный chat ID

```
❌ Failed to send message: Bad Request: chat not found
```

**Решение:**
- Проверьте, что chat ID правильный
- Для групп убедитесь, что ID начинается с `-`
- Бот должен быть добавлен в группу/канал

---

### Ошибка: Network timeout

```
❌ Failed to send message: Request timeout after 10s
```

**Решение:**
- Проверьте интернет-соединение
- Увеличьте таймаут: `--timeout 30`

---

## Лимиты сообщений

- **Максимальная длина сообщения:** 4096 символов
- **Файлы длиннее 4096 символов:** Будут отклонены Telegram API
- **Решение:** Разделение больших файлов на части (будущая функция)

---

## Архитектура

```
src/telegram/
├── file_reader.py          # Чтение файлов + валидация
├── telegram_client.py      # Клиент Telegram Bot API
└── telegram_sender.py      # CLI точка входа
```

**Принципы дизайна:**
- Разделение ответственности (чтение vs отправка)
- Переиспользование сессий (HTTP connection pooling)
- Поддержка контекстного менеджера (`with`)
- Комплексная обработка ошибок
- Защита от таймаутов
- Логирование на каждом шаге

---

## Продвинутое использование: Отправка в несколько чатов

**Создайте скрипт `send_to_multiple.sh`:**
```bash
#!/bin/bash

FILE="message.txt"
TOKEN="123456:ABC-DEF..."

CHATS=(
  "123456789"
  "987654321"
  "-100123456789"
)

for CHAT in "${CHATS[@]}"; do
  echo "Sending to chat: $CHAT"
  python3 -m src.telegram.telegram_sender \
    --file "$FILE" \
    --token "$TOKEN" \
    --chat "$CHAT"
done
```

---

## Лучшие практики безопасности

1. **Никогда не коммитьте токены ботов в git:**
   ```bash
   # Добавьте в .gitignore
   echo "*.env" >> .gitignore
   echo ".env" >> .gitignore
   ```

2. **Используйте переменные окружения:**
   ```bash
   # Создайте .env файл (не коммитьте!)
   echo 'export TELEGRAM_BOT_TOKEN="..."' > .env
   echo 'export TELEGRAM_CHAT_ID="..."' >> .env

   # Загрузите при необходимости
   source .env
   ```

3. **Регулярно ротируйте токены:**
   - Используйте команду @BotFather `/revoke`
   - Сгенерируйте новый токен

---

## Решение проблем

### Бот не отвечает в группе

**Проблема:** Бот добавлен в группу, но не получает сообщения

**Решение:**
1. Сделайте бота админом (или отключите privacy mode)
2. В @BotFather: `/mybots` → Выберите бота → Bot Settings → Group Privacy → Turn OFF

---

### "Forbidden: bot was blocked by the user"

**Проблема:** Пользователь заблокировал бота

**Решение:** Попросите пользователя разблокировать и перезапустить бота (`/start`)

---

### Rate limiting

**Проблема:** Слишком много запросов

**Решение:**
- Telegram разрешает ~30 сообщений/секунду в разные чаты
- Добавьте задержку между сообщениями: `sleep 0.1`

---

## Логирование

Логи записываются в консоль с уровнями INFO/ERROR.

**Включение DEBUG логирования:**

Отредактируйте `config.py`:
```python
LOG_LEVEL = "DEBUG"  # Вместо INFO
```

**Пример DEBUG вывода:**
```
DEBUG - Testing bot token with getMe
DEBUG - Sending message to chat 123456789 (length: 54 chars)
INFO - Message sent successfully to chat 123456789
```

---

## Будущие улучшения (расширяемость)

Код спроектирован для лёгкого расширения:

1. **Добавить вложения файлов:**
   ```python
   # В telegram_client.py
   def send_document(self, chat_id: str, file_path: str):
       # Реализация
   ```

2. **Добавить разделение сообщений (для длинных файлов):**
   ```python
   # В file_reader.py
   def chunk_text(text: str, max_length: int = 4096):
       # Реализация
   ```

3. **Добавить логику повторов:**
   ```python
   # В telegram_client.py
   def send_message_with_retry(self, chat_id: str, text: str, retries: int = 3):
       # Реализация
   ```

4. **Добавить форматирование сообщений:**
   ```python
   # В telegram_client.py
   def send_formatted_message(self, chat_id: str, text: str, bold: bool = False):
       # Реализация
   ```

---

## Полный пример

```bash
# 1. Установка
pip3 install -r requirements.txt

# 2. Создание сообщения
echo "Hello from Telegram Bot!" > test_message.txt

# 3. Тест токена бота
python3 -m src.telegram.telegram_sender \
  --test \
  --token "123456:ABC-DEF..."

# 4. Отправка сообщения
python3 -m src.telegram.telegram_sender \
  --file test_message.txt \
  --token "123456:ABC-DEF..." \
  --chat "123456789"
```

**Успешный вывод:**
```
✅ Bot token is valid. Connection test successful.
✅ Message sent successfully to chat 123456789
   File: test_message.txt
   Length: 26 characters
```

---

## Справочник API

### Используемые endpoint'ы Telegram Bot API

- `POST /bot<token>/sendMessage` — Отправка текстового сообщения
- `GET /bot<token>/getMe` — Тест токена бота

**Официальная документация:** https://core.telegram.org/bots/api

---

## Поддержка

По вопросам, связанным с Telegram:
- Официальная документация ботов: https://core.telegram.org/bots
- Поддержка ботов: @BotSupport (Telegram)
- Обновления API: @BotNews (Telegram)
