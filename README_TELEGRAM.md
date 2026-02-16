# Telegram Sender - Documentation

Production-ready tool for sending text files to Telegram chats via Bot API.

## Features

- ✅ Read text files (UTF-8)
- ✅ Send to private/group/channel chats
- ✅ Bot token validation
- ✅ HTTP timeout protection
- ✅ Error handling (network, API, file errors)
- ✅ Session reuse (requests.Session)
- ✅ Environment variable support
- ✅ Markdown/HTML formatting support
- ✅ Logging (INFO/ERROR)

---

## Installation

```bash
# Install dependencies
pip3 install -r requirements.txt
```

---

## Setup Telegram Bot

### 1. Create Bot with @BotFather

1. Open Telegram and search for **@BotFather**
2. Send `/newbot` command
3. Follow instructions to choose bot name and username
4. **Save the bot token** (looks like `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

### 2. Get Chat ID

#### Option A: For Private Chat (Direct Message)

1. Send any message to your bot
2. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
3. Find `"chat":{"id":123456789}` in the response
4. Use this number as `CHAT_ID`

#### Option B: For Group/Channel

1. Add bot to your group/channel
2. Send a message in the group
3. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. Find `"chat":{"id":-100123456789}` (note the minus sign)
5. Use this number (with minus) as `CHAT_ID`

#### Option C: Using a Bot (easier)

1. Add **@userinfobot** to your chat
2. It will show you the chat ID immediately

---

## Usage

### Basic Usage

```bash
python3 -m src.telegram.telegram_sender \
  --file message.txt \
  --token "123456:ABC-DEF..." \
  --chat "123456789"
```

### Using Environment Variables (Recommended)

```bash
# Set credentials once
export TELEGRAM_BOT_TOKEN="123456:ABC-DEF..."
export TELEGRAM_CHAT_ID="123456789"

# Send message
python3 -m src.telegram.telegram_sender --file message.txt
```

### With Markdown Formatting

```bash
python3 -m src.telegram.telegram_sender \
  --file message.txt \
  --parse-mode Markdown
```

### Test Bot Connection

```bash
python3 -m src.telegram.telegram_sender \
  --test \
  --token "123456:ABC-DEF..."
```

---

## CLI Arguments

| Argument | Description | Required | Alternative |
|----------|-------------|----------|-------------|
| `--file` | Path to text file | Yes (for sending) | - |
| `--token` | Bot token from @BotFather | Yes | `TELEGRAM_BOT_TOKEN` env var |
| `--chat` | Chat ID | Yes (for sending) | `TELEGRAM_CHAT_ID` env var |
| `--parse-mode` | Message format (Markdown/HTML) | No | - |
| `--test` | Test bot token only | No | - |
| `--timeout` | HTTP timeout in seconds | No (default: 10) | - |

---

## Examples

### Example 1: Send Simple Message

**Create file `message.txt`:**
```
Hello from Telegram Bot!
This is a test message.
```

**Send:**
```bash
python3 -m src.telegram.telegram_sender \
  --file message.txt \
  --token "YOUR_TOKEN" \
  --chat "YOUR_CHAT_ID"
```

**Expected output:**
```
✅ Message sent successfully to chat 123456789
   File: message.txt
   Length: 54 characters
```

---

### Example 2: Send with Markdown

**Create file `formatted.txt`:**
```
*Bold text*
_Italic text_
`Code block`
[Link](https://example.com)
```

**Send:**
```bash
python3 -m src.telegram.telegram_sender \
  --file formatted.txt \
  --token "YOUR_TOKEN" \
  --chat "YOUR_CHAT_ID" \
  --parse-mode Markdown
```

---

### Example 3: Test Bot Token

```bash
python3 -m src.telegram.telegram_sender \
  --test \
  --token "123456:ABC-DEF..."
```

**Expected output (success):**
```
✅ Bot token is valid. Connection test successful.
```

**Expected output (error):**
```
❌ Connection test failed: Unauthorized
```

---

### Example 4: Using Environment Variables

**Setup (add to `~/.bashrc` or `~/.zshrc`):**
```bash
export TELEGRAM_BOT_TOKEN="123456:ABC-DEF..."
export TELEGRAM_CHAT_ID="123456789"
```

**Usage:**
```bash
# Reload shell
source ~/.bashrc

# Send without credentials in command
python3 -m src.telegram.telegram_sender --file message.txt
```

---

## Error Handling

### Error: File not found

```
❌ File error: File not found: message.txt
```

**Solution:** Check file path is correct

---

### Error: Empty file

```
❌ File is empty or contains only whitespace
```

**Solution:** Add content to the file

---

### Error: Invalid bot token

```
❌ Connection test failed: Unauthorized
```

**Solution:**
- Check token is correct
- Ensure no extra spaces
- Token format: `123456:ABC-DEF...`

---

### Error: Invalid chat ID

```
❌ Failed to send message: Bad Request: chat not found
```

**Solution:**
- Verify chat ID is correct
- For groups, ensure ID starts with `-`
- Bot must be added to the group/channel

---

### Error: Network timeout

```
❌ Failed to send message: Request timeout after 10s
```

**Solution:**
- Check internet connection
- Increase timeout: `--timeout 30`

---

## Message Limits

- **Maximum message length:** 4096 characters
- **Files longer than 4096 chars:** Will be rejected by Telegram API
- **Solution:** Split large files into chunks (future feature)

---

## Architecture

```
src/telegram/
├── file_reader.py          # File reading + validation
├── telegram_client.py      # Telegram Bot API client
└── telegram_sender.py      # CLI entry point
```

**Design principles:**
- Separation of concerns (reading vs sending)
- Session reuse (HTTP connection pooling)
- Context manager support (`with` statement)
- Comprehensive error handling
- Timeout protection
- Logging at every step

---

## Advanced: Sending to Multiple Chats

**Create script `send_to_multiple.sh`:**
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

## Security Best Practices

1. **Never commit bot tokens to git:**
   ```bash
   # Add to .gitignore
   echo "*.env" >> .gitignore
   echo ".env" >> .gitignore
   ```

2. **Use environment variables:**
   ```bash
   # Create .env file (don't commit!)
   echo 'export TELEGRAM_BOT_TOKEN="..."' > .env
   echo 'export TELEGRAM_CHAT_ID="..."' >> .env

   # Load when needed
   source .env
   ```

3. **Rotate tokens regularly:**
   - Use @BotFather `/revoke` command
   - Generate new token

---

## Troubleshooting

### Bot doesn't respond in group

**Problem:** Bot added to group but not receiving messages

**Solution:**
1. Make bot admin (or disable privacy mode)
2. In @BotFather: `/mybots` → Select bot → Bot Settings → Group Privacy → Turn OFF

---

### "Forbidden: bot was blocked by the user"

**Problem:** User blocked the bot

**Solution:** Ask user to unblock and restart bot (`/start`)

---

### Rate limiting

**Problem:** Too many requests

**Solution:**
- Telegram allows ~30 messages/second to different chats
- Add delay between messages: `sleep 0.1`

---

## Logging

Logs are written to console with INFO/ERROR levels.

**Enable DEBUG logging:**

Edit `config.py`:
```python
LOG_LEVEL = "DEBUG"  # Instead of INFO
```

**Debug output example:**
```
DEBUG - Testing bot token with getMe
DEBUG - Sending message to chat 123456789 (length: 54 chars)
INFO - Message sent successfully to chat 123456789
```

---

## Future Enhancements (Extensibility)

The code is designed to be easily extended:

1. **Add file attachments:**
   ```python
   # In telegram_client.py
   def send_document(self, chat_id: str, file_path: str):
       # Implementation
   ```

2. **Add message chunking (for long files):**
   ```python
   # In file_reader.py
   def chunk_text(text: str, max_length: int = 4096):
       # Implementation
   ```

3. **Add retry logic:**
   ```python
   # In telegram_client.py
   def send_message_with_retry(self, chat_id: str, text: str, retries: int = 3):
       # Implementation
   ```

4. **Add message formatting:**
   ```python
   # In telegram_client.py
   def send_formatted_message(self, chat_id: str, text: str, bold: bool = False):
       # Implementation
   ```

---

## Complete Example

```bash
# 1. Install
pip3 install -r requirements.txt

# 2. Create message
echo "Hello from Telegram Bot!" > test_message.txt

# 3. Test bot token
python3 -m src.telegram.telegram_sender \
  --test \
  --token "123456:ABC-DEF..."

# 4. Send message
python3 -m src.telegram.telegram_sender \
  --file test_message.txt \
  --token "123456:ABC-DEF..." \
  --chat "123456789"
```

**Success output:**
```
✅ Bot token is valid. Connection test successful.
✅ Message sent successfully to chat 123456789
   File: test_message.txt
   Length: 26 characters
```

---

## API Reference

### Telegram Bot API Endpoints Used

- `POST /bot<token>/sendMessage` — Send text message
- `GET /bot<token>/getMe` — Test bot token

**Official Documentation:** https://core.telegram.org/bots/api

---

## Support

For Telegram-specific issues:
- Official Bot Documentation: https://core.telegram.org/bots
- Bot Support: @BotSupport (Telegram)
- API Updates: @BotNews (Telegram)
