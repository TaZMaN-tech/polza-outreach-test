# Project Structure

Complete overview of the `polza_outreach_test` project.

---

## Project Overview

**Repository:** `polza_outreach_test`

**Tasks:**
1. **Email Verification Tool** — DNS MX lookup + SMTP handshake validation
2. **Telegram Sender** — Send text files to Telegram via Bot API

---

## File Structure

```
polza_outreach_test/
│
├── config.py                      # Global configuration (timeouts, DNS, SMTP, logging)
├── requirements.txt               # Python dependencies (dnspython, requests)
│
├── src/                           # Source code
│   ├── __init__.py
│   │
│   ├── main.py                    # Task 1: Email verification CLI entry point
│   │
│   ├── validators/                # Email validation
│   │   ├── __init__.py
│   │   └── email_validator.py     # RFC 5322 email format validation
│   │
│   ├── dns/                       # DNS MX lookup
│   │   ├── __init__.py
│   │   └── mx_checker.py          # MX record lookup + in-memory cache
│   │
│   ├── smtp/                      # SMTP verification
│   │   ├── __init__.py
│   │   └── smtp_verifier.py       # SMTP handshake (EHLO→MAIL FROM→RCPT TO)
│   │
│   ├── models/                    # Data models
│   │   ├── __init__.py
│   │   └── result.py              # VerificationResult + statuses
│   │
│   ├── telegram/                  # Task 2: Telegram integration
│   │   ├── __init__.py
│   │   ├── file_reader.py         # File reading + validation
│   │   ├── telegram_client.py     # Telegram Bot API client
│   │   └── telegram_sender.py     # CLI entry point
│   │
│   └── utils/                     # Shared utilities
│       ├── __init__.py
│       └── logger.py              # Logging configuration
│
├── tests/                         # Tests (placeholder)
│   └── __init__.py
│
├── test_emails.txt                # Sample email list for Task 1
├── test_message.txt               # Sample message for Task 2
│
└── Documentation/                 # Markdown docs
    ├── README.md                  # Main project README
    ├── README_TELEGRAM.md         # Task 2: Telegram setup guide
    │
    ├── QUICK_START.md             # Task 1: Quick start guide
    ├── TESTING_GUIDE.md           # Task 1: Test scenarios
    ├── TZ_COMPLIANCE.md           # Task 1: TZ compliance doc
    │
    ├── CHANGELOG.md               # Task 1: Version history
    ├── SUMMARY.md                 # Task 1: v1.1.0 summary
    ├── FINAL_REPORT.md            # Task 1: v1.2.0 final report
    │
    ├── TASK2_SUMMARY.md           # Task 2: Summary
    ├── TELEGRAM_EXAMPLES.md       # Task 2: Output examples
    │
    └── PROJECT_STRUCTURE.md       # This file
```

---

## Module Dependencies

### Task 1: Email Verification

```
main.py
  ├─> validators/email_validator.py
  ├─> dns/mx_checker.py
  ├─> smtp/smtp_verifier.py
  ├─> models/result.py
  └─> utils/logger.py

External:
  └─> dnspython (MX lookup)
```

### Task 2: Telegram Sender

```
telegram_sender.py
  ├─> telegram/file_reader.py
  ├─> telegram/telegram_client.py
  └─> utils/logger.py

External:
  └─> requests (HTTP client)
```

---

## Entry Points

### Task 1: Email Verification

```bash
python3 -m src.main --emails "test@gmail.com"
python3 -m src.main --file test_emails.txt --json results.json
```

### Task 2: Telegram Sender

```bash
python3 -m src.telegram.telegram_sender --file message.txt --token "..." --chat "..."
```

---

## Configuration

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
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Cache
ENABLE_MX_CACHE = True
```

---

## Documentation Files

### Task 1: Email Verification

| File | Purpose |
|------|---------|
| `README.md` | Main documentation, features, usage |
| `QUICK_START.md` | Quick start guide, examples |
| `TESTING_GUIDE.md` | 8 test scenarios with expected results |
| `TZ_COMPLIANCE.md` | TZ requirements compliance |
| `CHANGELOG.md` | Version history (v1.0.0 → v1.2.0) |
| `SUMMARY.md` | v1.1.0 summary (SMTP fixes) |
| `FINAL_REPORT.md` | v1.2.0 final report (TZ compliance) |

### Task 2: Telegram Sender

| File | Purpose |
|------|---------|
| `README_TELEGRAM.md` | Complete guide (setup, usage, troubleshooting) |
| `TELEGRAM_EXAMPLES.md` | Success/error output examples |
| `TASK2_SUMMARY.md` | Architecture, features, testing |

### Project-wide

| File | Purpose |
|------|---------|
| `PROJECT_STRUCTURE.md` | This file - project overview |

---

## Code Statistics

### Task 1: Email Verification

**Files:** 6 Python modules + 1 CLI entry point
**Lines of code:** ~1200 (excluding docs)

| Module | LOC | Purpose |
|--------|-----|---------|
| `email_validator.py` | ~80 | RFC 5322 validation |
| `mx_checker.py` | ~150 | MX lookup + cache |
| `smtp_verifier.py` | ~180 | SMTP handshake |
| `result.py` | ~120 | Data models + statuses |
| `main.py` | ~310 | CLI + orchestration |
| `logger.py` | ~40 | Logging setup |

### Task 2: Telegram Sender

**Files:** 3 Python modules
**Lines of code:** ~400 (excluding docs)

| Module | LOC | Purpose |
|--------|-----|---------|
| `file_reader.py` | ~70 | File reading + validation |
| `telegram_client.py` | ~150 | Telegram Bot API client |
| `telegram_sender.py` | ~180 | CLI entry point |

---

## Dependencies

```
dnspython==2.7.0   # Task 1: DNS MX lookup
requests==2.32.3   # Task 2: HTTP client
```

**Total:** 2 external dependencies (minimal)

---

## Features Summary

### Task 1: Email Verification

- ✅ Email format validation (RFC 5322)
- ✅ DNS MX record lookup (dnspython)
- ✅ SMTP handshake (EHLO → MAIL FROM → RCPT TO)
- ✅ In-memory MX caching
- ✅ Timeout protection (DNS: 5s, SMTP: 10s)
- ✅ TZ-compliant output (3 statuses)
- ✅ JSON export
- ✅ Batch processing
- ✅ Comprehensive logging

### Task 2: Telegram Sender

- ✅ Read text files (UTF-8)
- ✅ Send to Telegram via Bot API
- ✅ Bot token validation
- ✅ Session reuse (requests.Session)
- ✅ HTTP timeout protection
- ✅ Environment variable support
- ✅ Markdown/HTML formatting
- ✅ Comprehensive error handling

---

## Usage Examples

### Task 1: Email Verification

```bash
# Single email
python3 -m src.main --emails "test@gmail.com"

# Multiple emails
python3 -m src.main --emails "a@b.com,c@d.com"

# From file
python3 -m src.main --file emails.txt

# With JSON output
python3 -m src.main --file emails.txt --json results.json
```

### Task 2: Telegram Sender

```bash
# Send message
python3 -m src.telegram.telegram_sender \
  --file message.txt \
  --token "123456:ABC..." \
  --chat "123456789"

# Test bot token
python3 -m src.telegram.telegram_sender \
  --test \
  --token "123456:ABC..."

# Using environment variables
export TELEGRAM_BOT_TOKEN="123456:ABC..."
export TELEGRAM_CHAT_ID="123456789"
python3 -m src.telegram.telegram_sender --file message.txt
```

---

## Development Principles

### Code Quality

- ✅ Type hints everywhere
- ✅ Docstrings for all functions/classes
- ✅ PEP8 compliant
- ✅ Comprehensive error handling
- ✅ Logging at every step
- ✅ Separation of concerns
- ✅ SOLID principles

### Architecture

- ✅ Modular structure (easy to extend)
- ✅ No hardcoded credentials
- ✅ Configuration externalized (`config.py`)
- ✅ Minimal dependencies
- ✅ Production-ready error handling
- ✅ Resource cleanup (try-finally, context managers)
- ✅ Timeout protection (no hanging)

### Documentation

- ✅ README for each task
- ✅ Usage examples (success + errors)
- ✅ Setup guides
- ✅ Troubleshooting sections
- ✅ API references
- ✅ Architecture docs

---

## Testing

### Task 1: Manual Testing

8 test scenarios covered in `TESTING_GUIDE.md`:
1. Valid email (Gmail)
2. Non-existent domain
3. Domain without MX records
4. Invalid email format
5. Multiple emails (batch)
6. File input
7. JSON export
8. SMTP timeout/blocked

### Task 2: Manual Testing

4 test scenarios:
1. Successful message send
2. File not found error
3. Empty file error
4. Invalid bot token

---

## Exit Codes

Both tools use standard exit codes:
- `0` — Success
- `1` — Error (check error message)

---

## Future Enhancements

### Task 1: Email Verification

- [ ] Parallel email processing
- [ ] Catch-all domain detection
- [ ] Disposable email detection
- [ ] Rate limiting support
- [ ] Redis cache (instead of in-memory)

### Task 2: Telegram Sender

- [ ] File attachments (photos, documents)
- [ ] Message chunking (>4096 chars)
- [ ] Retry logic with exponential backoff
- [ ] Batch sending to multiple chats
- [ ] Message formatting helpers

---

## Version History

### Task 1

- **v1.0.0** — Initial release (email validation + SMTP)
- **v1.1.0** — SMTP 550 detection fix + console output update
- **v1.2.0** — Strict TZ compliance (3 statuses only)

### Task 2

- **v1.0.0** — Initial release (Telegram sender)

---

## Installation

```bash
# 1. Navigate to project
cd polza_outreach_test

# 2. Install dependencies
pip3 install -r requirements.txt

# 3. Test Task 1
python3 -m src.main --emails "test@gmail.com"

# 4. Test Task 2 (need bot token)
python3 -m src.telegram.telegram_sender --help
```

---

**Both tasks are production-ready and fully documented! 🚀**
