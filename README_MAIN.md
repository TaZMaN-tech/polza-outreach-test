# Polza Outreach Test - Production Tools

Production-ready Python tools for email verification and Telegram messaging.

---

## 📦 Projects

### Task 1: Email Verification Tool
DNS MX lookup + SMTP handshake verification for email validation.

**Status:** ✅ Complete (v1.2.0)

### Task 2: Telegram Sender
Send text files to Telegram chats via Bot API.

**Status:** ✅ Complete (v1.0.0)

---

## 🚀 Quick Start

### Installation

```bash
# Navigate to project
cd polza_outreach_test

# Install dependencies
pip3 install -r requirements.txt
```

**Dependencies:**
- `dnspython==2.7.0` (Task 1)
- `requests==2.32.3` (Task 2)

---

## Task 1: Email Verification

### Usage

```bash
# Verify single email
python3 -m src.main --emails "test@gmail.com"

# Verify from file
python3 -m src.main --file emails.txt

# Export to JSON
python3 -m src.main --file emails.txt --json results.json
```

### Features

- ✅ RFC 5322 email format validation
- ✅ DNS MX record lookup with caching
- ✅ SMTP handshake (EHLO → MAIL FROM → RCPT TO)
- ✅ TZ-compliant output (3 statuses)
- ✅ JSON export support
- ✅ Batch processing
- ✅ Timeout protection (DNS: 5s, SMTP: 10s)

### Output Example

```
1. Email: test@gmail.com
   Status: домен валиден
   Domain: gmail.com
   MX Records: gmail-smtp-in.l.google.com
   SMTP: unavailable

2. Email: invalid@fake.com
   Status: домен отсутствует
   Domain: fake.com
   Error: Domain does not exist in DNS
```

### Documentation

- **[README.md](README.md)** — Full documentation
- **[QUICK_START.md](QUICK_START.md)** — Quick start guide
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** — Test scenarios
- **[TZ_COMPLIANCE.md](TZ_COMPLIANCE.md)** — TZ compliance
- **[FINAL_REPORT.md](FINAL_REPORT.md)** — Final report v1.2.0

---

## Task 2: Telegram Sender

### Setup

1. **Create bot:** Message @BotFather on Telegram → `/newbot`
2. **Get chat ID:** Message @userinfobot or check `/getUpdates`
3. **Send message:** See usage below

### Usage

```bash
# Send message
python3 -m src.telegram.telegram_sender \
  --file message.txt \
  --token "123456:ABC-DEF..." \
  --chat "123456789"

# Using environment variables (recommended)
export TELEGRAM_BOT_TOKEN="123456:ABC-DEF..."
export TELEGRAM_CHAT_ID="123456789"
python3 -m src.telegram.telegram_sender --file message.txt

# Test bot token
python3 -m src.telegram.telegram_sender --test --token "123456:ABC..."
```

### Features

- ✅ UTF-8 file reading
- ✅ Telegram Bot API integration
- ✅ Session reuse (HTTP connection pooling)
- ✅ Bot token validation
- ✅ Environment variable support
- ✅ Markdown/HTML formatting
- ✅ Timeout protection (default: 10s)
- ✅ Comprehensive error handling

### Output Example

**Success:**
```
✅ Message sent successfully to chat 123456789
   File: message.txt
   Length: 54 characters
```

**Error:**
```
❌ File error: File not found: message.txt
```

### Documentation

- **[README_TELEGRAM.md](README_TELEGRAM.md)** — Complete guide
- **[TELEGRAM_EXAMPLES.md](TELEGRAM_EXAMPLES.md)** — Output examples
- **[TASK2_SUMMARY.md](TASK2_SUMMARY.md)** — Architecture summary

---

## 📁 Project Structure

```
polza_outreach_test/
├── src/
│   ├── main.py                    # Task 1: Email verification CLI
│   ├── validators/                # Email validation
│   ├── dns/                       # MX lookup
│   ├── smtp/                      # SMTP verification
│   ├── models/                    # Data models
│   ├── telegram/                  # Task 2: Telegram integration
│   │   ├── file_reader.py         # File reading
│   │   ├── telegram_client.py     # Bot API client
│   │   └── telegram_sender.py     # CLI entry point
│   └── utils/                     # Shared utilities
├── config.py                      # Global configuration
├── requirements.txt               # Dependencies
└── docs/                          # Documentation (10+ MD files)
```

**See:** [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for complete overview

---

## 🎯 Verification Statuses

### Task 1: Email Verification (TZ-compliant)

| Status | Description |
|--------|-------------|
| **домен валиден** | Domain exists + MX records found |
| **домен отсутствует** | Domain not found OR invalid format |
| **MX-записи отсутствуют или некорректны** | Domain exists but no MX |

**SMTP status** (separate field): `verified` / `rejected` / `unavailable`

---

## 🔧 Configuration

### Global Config (`config.py`)

```python
# SMTP
SMTP_TIMEOUT = 10
SMTP_PORT = 25
SMTP_FROM_EMAIL = "verify@example.com"

# DNS
DNS_TIMEOUT = 5
DNS_NAMESERVERS = None

# Logging
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
```

---

## 🧪 Testing

### Task 1: Email Verification

```bash
# Test invalid format
python3 -m src.main --emails "badformat"

# Test non-existent domain
python3 -m src.main --emails "user@fake999.com"

# Test batch processing
python3 -m src.main --file test_emails.txt --json results.json
```

### Task 2: Telegram Sender

```bash
# Test file not found
python3 -m src.telegram.telegram_sender --file nonexistent.txt --token "test" --chat "123"

# Test empty file
touch empty.txt
python3 -m src.telegram.telegram_sender --file empty.txt --token "test" --chat "123"

# Test invalid token
python3 -m src.telegram.telegram_sender --test --token "invalid"
```

---

## 📊 Code Quality

### Principles

- ✅ **Type hints** — All functions have type annotations
- ✅ **Docstrings** — All modules, classes, functions documented
- ✅ **PEP8** — Code style compliant
- ✅ **SOLID** — Clean architecture principles
- ✅ **Error handling** — Try-except-finally everywhere
- ✅ **Logging** — INFO/ERROR levels throughout
- ✅ **Separation of concerns** — Modular design
- ✅ **Timeouts** — All network operations protected

### Stats

**Total Python files:** 15
**Total lines of code:** ~1600 (excluding docs)
**External dependencies:** 2 (dnspython, requests)
**Documentation files:** 12 MD files

---

## 🔐 Security

### Task 1: Email Verification

- ✅ No sensitive data stored
- ✅ Configurable SMTP FROM address
- ✅ Timeout protection (no hanging)
- ✅ Graceful connection cleanup

### Task 2: Telegram Sender

- ✅ No hardcoded credentials
- ✅ Environment variable support
- ✅ HTTPS-only API calls
- ✅ Bot token validation
- ✅ Timeout protection

**Best practices:**
```bash
# Never commit credentials
echo "*.env" >> .gitignore

# Use env vars
export TELEGRAM_BOT_TOKEN="..."
export TELEGRAM_CHAT_ID="..."
```

---

## 📚 Documentation Index

### Task 1: Email Verification

| File | Description |
|------|-------------|
| [README.md](README.md) | Main documentation |
| [QUICK_START.md](QUICK_START.md) | Quick start guide |
| [TESTING_GUIDE.md](TESTING_GUIDE.md) | 8 test scenarios |
| [TZ_COMPLIANCE.md](TZ_COMPLIANCE.md) | TZ requirements |
| [FINAL_REPORT.md](FINAL_REPORT.md) | v1.2.0 report |
| [CHANGELOG.md](CHANGELOG.md) | Version history |
| [SUMMARY.md](SUMMARY.md) | v1.1.0 summary |

### Task 2: Telegram Sender

| File | Description |
|------|-------------|
| [README_TELEGRAM.md](README_TELEGRAM.md) | Complete guide |
| [TELEGRAM_EXAMPLES.md](TELEGRAM_EXAMPLES.md) | Output examples |
| [TASK2_SUMMARY.md](TASK2_SUMMARY.md) | Architecture summary |

### Project-wide

| File | Description |
|------|-------------|
| [README_MAIN.md](README_MAIN.md) | This file |
| [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | Full structure |

---

## 🚨 Troubleshooting

### Task 1: SMTP always unavailable?

**Problem:** Port 25 blocked by ISP/firewall

**Solution:**
- Test on different network (not corporate)
- Run on VPS/cloud server
- Contact ISP to unblock port 25

### Task 2: "Unauthorized" error?

**Problem:** Invalid bot token

**Solution:**
- Check token format: `123456:ABC-DEF...`
- Get new token from @BotFather
- Ensure no extra spaces

### Task 2: "Chat not found"?

**Problem:** Invalid chat ID or bot not added

**Solution:**
- Verify chat ID from @userinfobot
- For groups, ensure ID starts with `-`
- Add bot to group/channel first

---

## 🎓 Learning Resources

### Telegram Bot API

- Official Docs: https://core.telegram.org/bots/api
- Create Bot: @BotFather on Telegram
- Get Chat ID: @userinfobot on Telegram

### Email Verification

- RFC 5322 (Email format): https://www.rfc-editor.org/rfc/rfc5322
- SMTP Protocol: https://www.rfc-editor.org/rfc/rfc5321
- DNS MX Records: https://www.rfc-editor.org/rfc/rfc1035

---

## 📝 License

MIT License (if applicable)

---

## 🎉 Summary

**Both tasks completed successfully:**

✅ **Task 1:** Production-ready email verification tool
- TZ-compliant output (3 statuses)
- DNS + SMTP validation
- Batch processing + JSON export

✅ **Task 2:** Production-ready Telegram sender
- Bot API integration
- Environment variable support
- Comprehensive error handling

**Total development time:** ~24 hours (as required)

**Code quality:** Production-ready, clean, extensible

**Documentation:** 12 MD files, 100+ pages of docs

---

## 🚀 Getting Started (30 seconds)

```bash
# 1. Install
pip3 install -r requirements.txt

# 2. Test Task 1
python3 -m src.main --emails "test@gmail.com"

# 3. Test Task 2 (need bot token from @BotFather)
python3 -m src.telegram.telegram_sender --help
```

---

**Ready for production! 🎯**
