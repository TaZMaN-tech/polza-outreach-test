# Email Verification & Telegram Tools

Production-ready Python tools for email verification and Telegram messaging.

## Projects

1. **Email Verification Tool** (Task 1) — DNS MX lookup + SMTP handshake verification
2. **Telegram Sender** (Task 2) — Send text files to Telegram via Bot API

---

# Task 1: Email Verification Tool

Production-ready Python tool for email verification using DNS MX records and SMTP handshake validation.

## Features

- **Email format validation** — RFC 5322 compliant regex validation
- **DNS MX record lookup** — Verifies domain and extracts MX servers
- **SMTP handshake verification** — Performs EHLO → MAIL FROM → RCPT TO without sending emails
- **In-memory MX caching** — Caches MX records by domain for performance
- **Timeout protection** — Network operations have configurable timeouts
- **Graceful error handling** — All exceptions caught and logged
- **Multiple input methods** — CLI arguments or file input
- **JSON export** — Optional JSON output for automation

## Installation

### Prerequisites

- Python 3.11+
- pip

### Setup

```bash
# Clone or navigate to project directory
cd polza_outreach_test

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Basic Usage

**Verify emails from command line:**
```bash
python -m src.main --emails "test@example.com,user@gmail.com"
```

**Verify emails from file:**
```bash
python -m src.main --file emails.txt
```

**Save results to JSON:**
```bash
python -m src.main --emails "test@example.com" --json output.json
```

### Input File Format

Create a text file with one email per line:

```text
test@example.com
user@gmail.com
admin@domain.org
```

### Output

**Console output:**
```
================================================================================
EMAIL VERIFICATION RESULTS
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

**JSON output** (if `--json` specified):
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

## Verification Statuses

### Console Output (as per TZ requirements)

**TZ specifies ONLY 3 possible statuses:**

| Status | Description | When shown |
|--------|-------------|------------|
| **домен валиден** | Domain is valid (has DNS records and MX records) | Domain exists + MX records found |
| **домен отсутствует** | Domain does not exist | Domain not found OR invalid email format |
| **MX-записи отсутствуют или некорректны** | MX records are missing or incorrect | Domain exists but no MX records |

**Note:** Invalid email format is shown as "домен отсутствует" (per TZ). Details appear in Error field.

### SMTP Status (separate field)

| SMTP Status | Description |
|-------------|-------------|
| **verified** | SMTP server accepted the email (250 response) |
| **rejected** | SMTP server rejected the email (550 response) |
| **unavailable** | SMTP server unreachable/timeout/blocked |
| **not checked** | SMTP verification was not performed |

### JSON Output Statuses (extended)

| Status | Description |
|--------|-------------|
| **valid** | Email passed all checks (format, DNS, SMTP) |
| **invalid_format** | Email format is incorrect |
| **domain_not_found** | Domain does not exist in DNS |
| **no_mx_records** | MX records are missing or incorrect |
| **smtp_unavailable** | SMTP server is unreachable or blocked |
| **smtp_rejected** | SMTP server rejected the email address |

## Configuration

Edit `config.py` to customize settings:

```python
# SMTP Configuration
SMTP_TIMEOUT = 10  # seconds
SMTP_PORT = 25
SMTP_FROM_EMAIL = "verify@example.com"

# DNS Configuration
DNS_TIMEOUT = 5  # seconds
DNS_NAMESERVERS = None  # or ['8.8.8.8', '8.8.4.4']

# Logging
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL

# Cache
ENABLE_MX_CACHE = True
```

## Architecture

```
src/
├── main.py                    # CLI entry point, orchestration
├── validators/
│   └── email_validator.py     # Email format validation & domain extraction
├── dns/
│   └── mx_checker.py          # MX record lookup with caching
├── smtp/
│   └── smtp_verifier.py       # SMTP handshake verification
├── models/
│   └── result.py              # Data models (VerificationResult, statuses)
└── utils/
    └── logger.py              # Logging configuration
```

## How It Works

1. **Format Validation** — Validates email using RFC 5322 regex
2. **Domain Extraction** — Extracts domain from email address
3. **Domain Existence Check** — Verifies domain exists in DNS (A/AAAA records)
4. **MX Lookup** — Retrieves and caches MX records for the domain
5. **SMTP Handshake** — Connects to MX server and performs:
   - `EHLO` — Identify to server
   - `MAIL FROM` — Set sender
   - `RCPT TO` — Verify recipient
   - Analyzes response codes (250 = valid, 550 = rejected)
6. **Graceful Cleanup** — Always closes SMTP connections properly

## Error Handling

- All network operations have timeouts (DNS: 5s, SMTP: 10s)
- Exceptions are caught at every layer
- SMTP connections are always closed (try-finally)
- Fallback mechanism tries multiple MX servers
- Detailed error logging for debugging

## Limitations

- Some mail servers use greylisting or block verification attempts
- Corporate firewalls may block outbound port 25 (SMTP)
- Catch-all domains may accept any email address
- Rate limiting may occur with bulk verification

## Testing Examples

See examples below for testing the tool.

---

# Task 2: Telegram Sender

Send text files to Telegram chats via Bot API.

## Quick Start

**Installation:**
```bash
pip install -r requirements.txt
```

**Usage (with CLI arguments):**
```bash
python -m src.telegram.telegram_sender \
  --file message.txt \
  --token "123456:ABC-DEF..." \
  --chat "123456789"
```

**Usage (with environment variables - recommended):**
```bash
export TELEGRAM_BOT_TOKEN="123456:ABC-DEF..."
export TELEGRAM_CHAT_ID="123456789"
python -m src.telegram.telegram_sender --file message.txt
```

**Test bot token:**
```bash
python -m src.telegram.telegram_sender --test --token "123456:ABC-DEF..."
```

**Full Documentation:** See [README_TELEGRAM.md](README_TELEGRAM.md)

---

# Task 3: System Architecture

Email outreach system architecture for 1200 accounts (multi-client, high availability, minimal cost).

**Document:** [TASK3_ARCHITECTURE.md](TASK3_ARCHITECTURE.md)

**Key Points:**
- Infrastructure: 3 VPS nodes ($48/mo) + SMTP accounts ($60/mo)
- SMTP Pool: 15-20 accounts across 3-4 providers (rotation + health checks)
- Queue: Redis + Celery (rate limiting 100/min system-wide)
- Monitoring: Prometheus + Grafana + blacklist checks
- Total Cost: **$118-168/mo**

---

# Task 4: AI Development Stack

Personal AI workflow for daily development (Claude, ChatGPT, Copilot).

**Document:** [TASK4_AI_STACK.md](TASK4_AI_STACK.md)

**Key Points:**
- **Workflow:** Claude for architecture → ChatGPT for fixes → Copilot for autocomplete
- **MCP:** GitHub, Filesystem, Figma, Browser integration
- **Top Rules:** Small diffs (<300 LOC), Verify by running, No duplicate logic
- **Quality Control:** Step-by-step planning, security checklists, test edge cases

---

## License

MIT License
