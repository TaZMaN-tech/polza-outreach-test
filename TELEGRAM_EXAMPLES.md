# Telegram Sender - Output Examples

## Successful Outputs

### Example 1: Successful Message Send

**Command:**
```bash
python3 -m src.telegram.telegram_sender \
  --file test_message.txt \
  --token "123456:ABC-DEF..." \
  --chat "123456789"
```

**Output:**
```
2026-02-16 11:40:30,123 - __main__ - INFO - Reading file: test_message.txt
2026-02-16 11:40:30,124 - src.telegram.file_reader - INFO - Successfully read file: test_message.txt (196 characters)
2026-02-16 11:40:30,124 - __main__ - INFO - Sending message to Telegram chat 123456789
2026-02-16 11:40:30,456 - src.telegram.telegram_client - INFO - Message sent successfully to chat 123456789
2026-02-16 11:40:30,456 - __main__ - INFO - Message sent successfully
✅ Message sent successfully to chat 123456789
   File: test_message.txt
   Length: 196 characters
```

---

### Example 2: Successful Token Test

**Command:**
```bash
python3 -m src.telegram.telegram_sender \
  --test \
  --token "123456:ABC-DEF..."
```

**Output:**
```
2026-02-16 11:40:35,123 - __main__ - INFO - Running connection test
2026-02-16 11:40:35,456 - src.telegram.telegram_client - INFO - Bot token valid. Bot username: @MyTestBot
✅ Bot token is valid. Connection test successful.
```

---

### Example 3: Using Environment Variables

**Setup:**
```bash
export TELEGRAM_BOT_TOKEN="123456:ABC-DEF..."
export TELEGRAM_CHAT_ID="123456789"
```

**Command:**
```bash
python3 -m src.telegram.telegram_sender --file test_message.txt
```

**Output:**
```
2026-02-16 11:40:40,123 - __main__ - INFO - Reading file: test_message.txt
2026-02-16 11:40:40,124 - src.telegram.file_reader - INFO - Successfully read file: test_message.txt (196 characters)
2026-02-16 11:40:40,124 - __main__ - INFO - Sending message to Telegram chat 123456789
2026-02-16 11:40:40,456 - src.telegram.telegram_client - INFO - Message sent successfully to chat 123456789
✅ Message sent successfully to chat 123456789
   File: test_message.txt
   Length: 196 characters
```

---

## Error Outputs

### Error 1: File Not Found

**Command:**
```bash
python3 -m src.telegram.telegram_sender \
  --file nonexistent.txt \
  --token "123456:ABC" \
  --chat "123"
```

**Output:**
```
2026-02-16 11:40:11,157 - __main__ - INFO - Reading file: nonexistent.txt
2026-02-16 11:40:11,157 - src.telegram.file_reader - ERROR - File not found: nonexistent.txt
2026-02-16 11:40:11,157 - __main__ - ERROR - File error: File not found: nonexistent.txt
❌ File error: File not found: nonexistent.txt
```

**Exit code:** `1`

---

### Error 2: Empty File

**Command:**
```bash
touch empty.txt
python3 -m src.telegram.telegram_sender \
  --file empty.txt \
  --token "123456:ABC" \
  --chat "123"
```

**Output:**
```
2026-02-16 11:40:24,065 - __main__ - INFO - Reading file: empty.txt
2026-02-16 11:40:24,065 - src.telegram.file_reader - INFO - Successfully read file: empty.txt (0 characters)
2026-02-16 11:40:24,065 - src.telegram.file_reader - WARNING - Content is empty or whitespace only
2026-02-16 11:40:24,065 - __main__ - ERROR - File content is empty
❌ File is empty or contains only whitespace
```

**Exit code:** `1`

---

### Error 3: Missing Bot Token

**Command:**
```bash
python3 -m src.telegram.telegram_sender --file test_message.txt
```

**Output:**
```
2026-02-16 11:40:28,037 - __main__ - ERROR - Bot token not provided. Use --token or set TELEGRAM_BOT_TOKEN
Error: Bot token required. Use --token or set TELEGRAM_BOT_TOKEN environment variable
```

**Exit code:** `1`

---

### Error 4: Missing Chat ID

**Command:**
```bash
python3 -m src.telegram.telegram_sender \
  --file test_message.txt \
  --token "123456:ABC-DEF..."
```

**Output:**
```
2026-02-16 11:40:50,123 - __main__ - ERROR - Chat ID not provided. Use --chat or set TELEGRAM_CHAT_ID
Error: Chat ID required. Use --chat or set TELEGRAM_CHAT_ID environment variable
```

**Exit code:** `1`

---

### Error 5: Invalid Bot Token

**Command:**
```bash
python3 -m src.telegram.telegram_sender \
  --test \
  --token "invalid_token"
```

**Output:**
```
2026-02-16 11:40:55,123 - __main__ - INFO - Running connection test
2026-02-16 11:40:55,456 - src.telegram.telegram_client - ERROR - Invalid bot token: Unauthorized
❌ Connection test failed: Unauthorized
```

**Exit code:** `1`

---

### Error 6: Network Timeout

**Command:**
```bash
python3 -m src.telegram.telegram_sender \
  --file test_message.txt \
  --token "123456:ABC" \
  --chat "123" \
  --timeout 1
```

**Output (if network is slow):**
```
2026-02-16 11:41:00,123 - __main__ - INFO - Reading file: test_message.txt
2026-02-16 11:41:00,124 - src.telegram.file_reader - INFO - Successfully read file: test_message.txt (196 characters)
2026-02-16 11:41:00,124 - __main__ - INFO - Sending message to Telegram chat 123
2026-02-16 11:41:01,124 - src.telegram.telegram_client - ERROR - Request timeout after 1s
2026-02-16 11:41:01,124 - __main__ - ERROR - Failed to send message: Request timeout after 1s
❌ Failed to send message: Request timeout after 1s
```

**Exit code:** `1`

---

### Error 7: Invalid Chat ID

**Command:**
```bash
python3 -m src.telegram.telegram_sender \
  --file test_message.txt \
  --token "123456:ABC-DEF..." \
  --chat "999999999"
```

**Output:**
```
2026-02-16 11:41:05,123 - __main__ - INFO - Reading file: test_message.txt
2026-02-16 11:41:05,124 - src.telegram.file_reader - INFO - Successfully read file: test_message.txt (196 characters)
2026-02-16 11:41:05,124 - __main__ - INFO - Sending message to Telegram chat 999999999
2026-02-16 11:41:05,456 - src.telegram.telegram_client - ERROR - Telegram API error: Bad Request: chat not found
2026-02-16 11:41:05,456 - __main__ - ERROR - Failed to send message: Bad Request: chat not found
❌ Failed to send message: Bad Request: chat not found
```

**Exit code:** `1`

---

### Error 8: Connection Error (No Internet)

**Command:**
```bash
# Disconnect from internet, then run:
python3 -m src.telegram.telegram_sender \
  --file test_message.txt \
  --token "123456:ABC" \
  --chat "123"
```

**Output:**
```
2026-02-16 11:41:10,123 - __main__ - INFO - Reading file: test_message.txt
2026-02-16 11:41:10,124 - src.telegram.file_reader - INFO - Successfully read file: test_message.txt (196 characters)
2026-02-16 11:41:10,124 - __main__ - INFO - Sending message to Telegram chat 123
2026-02-16 11:41:20,456 - src.telegram.telegram_client - ERROR - Connection error: [Errno 8] nodename nor servname provided, or not known
2026-02-16 11:41:20,456 - __main__ - ERROR - Failed to send message: Connection error: [Errno 8] nodename nor servname provided, or not known
❌ Failed to send message: Connection error: [Errno 8] nodename nor servname provided, or not known
```

**Exit code:** `1`

---

### Error 9: Bot Blocked by User

**Command:**
```bash
python3 -m src.telegram.telegram_sender \
  --file test_message.txt \
  --token "123456:ABC-DEF..." \
  --chat "123456789"
```

**Output (if user blocked the bot):**
```
2026-02-16 11:41:25,123 - __main__ - INFO - Reading file: test_message.txt
2026-02-16 11:41:25,124 - src.telegram.file_reader - INFO - Successfully read file: test_message.txt (196 characters)
2026-02-16 11:41:25,124 - __main__ - INFO - Sending message to Telegram chat 123456789
2026-02-16 11:41:25,456 - src.telegram.telegram_client - ERROR - Telegram API error: Forbidden: bot was blocked by the user
2026-02-16 11:41:25,456 - __main__ - ERROR - Failed to send message: Forbidden: bot was blocked by the user
❌ Failed to send message: Forbidden: bot was blocked by the user
```

**Exit code:** `1`

---

### Error 10: File Too Large (>4096 chars)

**Command:**
```bash
# Create large file
python3 -c "print('A' * 5000)" > large.txt

python3 -m src.telegram.telegram_sender \
  --file large.txt \
  --token "123456:ABC-DEF..." \
  --chat "123456789"
```

**Output:**
```
2026-02-16 11:41:30,123 - __main__ - INFO - Reading file: large.txt
2026-02-16 11:41:30,124 - src.telegram.file_reader - INFO - Successfully read file: large.txt (5000 characters)
2026-02-16 11:41:30,124 - __main__ - INFO - Sending message to Telegram chat 123456789
2026-02-16 11:41:30,456 - src.telegram.telegram_client - ERROR - Telegram API error: Bad Request: message is too long
2026-02-16 11:41:30,456 - __main__ - ERROR - Failed to send message: Bad Request: message is too long
❌ Failed to send message: Bad Request: message is too long
```

**Exit code:** `1`

---

## Exit Codes

| Exit Code | Meaning |
|-----------|---------|
| `0` | Success - message sent or test passed |
| `1` | Error - check error message for details |

---

## Quick Reference

### Check if command succeeded in bash script:

```bash
#!/bin/bash

if python3 -m src.telegram.telegram_sender --file message.txt --token "$TOKEN" --chat "$CHAT"; then
    echo "Success!"
else
    echo "Failed with exit code: $?"
    exit 1
fi
```

### Capture output:

```bash
OUTPUT=$(python3 -m src.telegram.telegram_sender --file message.txt --token "$TOKEN" --chat "$CHAT" 2>&1)
echo "$OUTPUT"
```

### Silent mode (no logs):

```bash
python3 -m src.telegram.telegram_sender \
  --file message.txt \
  --token "$TOKEN" \
  --chat "$CHAT" 2>/dev/null
```
