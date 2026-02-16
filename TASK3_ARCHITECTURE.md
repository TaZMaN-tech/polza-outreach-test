# Email Outreach System Architecture

**Target:** 1200 email accounts, multi-client, minimal infrastructure cost, high availability

---

## 1. System Components

```
┌─────────────────┐
│   API Gateway   │ ← Client requests (REST/GraphQL)
└────────┬────────┘
         │
┌────────▼────────┐
│  Queue Manager  │ ← Redis (task queue, rate limiting)
└────────┬────────┘
         │
┌────────▼────────────────────┐
│   Worker Pool (3-5 nodes)   │ ← Python workers (send emails)
└────────┬────────────────────┘
         │
┌────────▼────────┐
│  SMTP Rotator   │ ← 15-20 SMTP accounts (rotation logic)
└────────┬────────┘
         │
┌────────▼────────┐
│  External SMTP  │ ← Gmail Workspace, SendGrid, SMTP2GO
└─────────────────┘

Monitoring: Prometheus + Grafana + Sentry
Storage: PostgreSQL (campaigns, stats, deliverability)
```

---

## 2. Infrastructure

**Hosting:** DigitalOcean/Hetzner VPS (3 nodes)
- **Node 1:** API + PostgreSQL + Redis (4GB RAM, 2 vCPU) — $24/mo
- **Node 2-3:** Workers (2GB RAM, 1 vCPU each) — $12/mo × 2 = $24/mo

**Containerization:** Docker Compose (orchestration overkill for this scale)
- API container (FastAPI/Flask)
- Worker containers (Python + Celery)
- Redis container
- PostgreSQL container

**Deployment:** GitLab CI/CD → SSH deploy (no k8s needed)

---

## 3. SMTP Account Pool

**Strategy:** 15-20 accounts across 3-4 providers to distribute risk

### Provider Mix
- **Gmail Workspace:** 5 accounts ($6/user/mo × 5 = $30/mo)
  - Limit: 500 emails/day per account → 2,500/day total
  - Reputation: Excellent (Google IP pool)

- **SendGrid API:** Free tier + Paid ($20/mo)
  - Limit: 100/day free, then $0.0006/email
  - Use for transactional/high-priority

- **SMTP2GO/Mailgun:** 5 accounts ($10/mo total)
  - Limit: 1,000/day per account → 5,000/day
  - Fallback pool

- **Custom SMTP (if budget allows):** 5 accounts on separate VPS
  - VPS with Postfix: $6/mo
  - 5 different /24 IPs via proxy rotation

### Rotation Logic
```python
# Round-robin with health check
accounts = [acc for acc in smtp_pool if acc.is_healthy()]
account = accounts[campaign_id % len(accounts)]

# Respect daily limits
if account.today_sent >= account.daily_limit * 0.9:
    account = get_next_available()
```

### Domain Setup
- **5 domains:** $12/year × 5 = $5/mo
- SPF: `v=spf1 include:_spf.google.com include:sendgrid.net ~all`
- DKIM: Rotate keys every 3 months
- DMARC: `v=DMARC1; p=none; rua=mailto:dmarc@domain.com` (monitor first)

---

## 4. Queue & Rate Limiting

**Queue:** Redis + Celery
```python
# Campaign task
@celery.task(rate_limit='100/m')  # 100 emails/min system-wide
def send_email(recipient, template, smtp_account_id):
    account = get_smtp_account(smtp_account_id)

    # Per-account rate limiting
    if account.minute_sent >= 10:  # 10/min per account
        raise Retry(countdown=60)

    send_via_smtp(account, recipient, template)
```

**Rate Limits (to avoid spam flags):**
- **System-wide:** 100 emails/min
- **Per account:** 10 emails/min, 500/day (for Gmail)
- **Per domain:** 50 emails/day (target domain protection)
- **Per recipient domain:** Max 20 emails/day (e.g., @company.com)

**Backoff Strategy:**
- Failed send → retry after 5min, 15min, 1hr
- 3 failures → pause account for 24hrs
- 5XX errors → immediate fallback to next account

---

## 5. Monitoring

**Metrics (Prometheus):**
- Emails sent/failed per account (last 1h, 24h)
- Queue depth, worker utilization
- SMTP response codes (2XX, 4XX, 5XX)
- Delivery rate per domain
- Bounce rate per campaign

**Alerts (AlertManager → Telegram):**
- Account daily limit >80% → switch to backup
- Bounce rate >10% → pause campaign
- SMTP 5XX errors >5/min → health check account
- Worker down >5min → restart container

**Logging (ELK or Loki):**
- Structured logs: `{account_id, recipient_domain, smtp_code, timestamp}`
- Retention: 30 days

**Blacklist Monitoring:**
- Daily check: MXToolbox API ($50/mo) or self-hosted script
- Check all sending IPs against Spamhaus, SpamCop, Barracuda

---

## 6. Fault Tolerance

### SMTP Account Failure
```
Account blocked → Mark unhealthy → Route to backup pool
Health check every 30min (test send to own address)
Auto-recover after 24hrs if health check passes
```

### Domain Reputation Drop
```
Bounce rate spike → Pause domain → Switch to backup domain
DMARC reports show failures → Fix SPF/DKIM immediately
```

### Worker/Server Failure
```
Node down → Celery tasks requeue automatically (Redis persistent)
PostgreSQL down → Read replica on Node 2 (async replication)
Redis down → Worker crashes graceful, restart with backlog
```

**Backup Strategy:**
- PostgreSQL: Daily dump to S3-compatible storage ($5/mo for 50GB)
- Redis: RDB snapshots every 6hrs
- Config/secrets: Encrypted in Git repo

---

## 7. Risk Mitigation

### Spam Detection
- **Warm-up:** New accounts start at 50/day, +50/day until limit
- **Content:** Avoid spam keywords, personalize with {name}/{company}
- **Unsubscribe link:** Required (legal + deliverability)
- **Engagement:** Track opens/clicks, remove non-engaged after 3 campaigns

### Blacklists
- **Prevention:** Respect bounces, clean lists (verify emails first with Task 1 tool)
- **Monitoring:** Daily IP/domain checks
- **Remediation:** Delist requests (manual, 24-48hr turnaround)

### DMARC/SPF/DKIM
- **SPF:** Include all provider IPs (`include:`)
- **DKIM:** Rotate keys quarterly, 2048-bit
- **DMARC:** Start `p=none` (monitor), move to `p=quarantine` after 1 month clean reports

### Reputation Management
- **Separate pools:** Transactional (Gmail) vs. cold outreach (SMTP2GO)
- **Feedback loops:** Subscribe to provider FBLs (Gmail Postmaster Tools)
- **List hygiene:** Remove hard bounces immediately, soft bounces after 3 attempts

### Legal Risks
- **GDPR:** Consent required (opt-in), unsubscribe in 1 click
- **CAN-SPAM:** Physical address in footer, honor opt-outs within 10 days
- **Data storage:** EU users → store in EU region (Hetzner Germany)

---

## 8. Cost Estimate (Monthly)

| Item | Details | Cost |
|------|---------|------|
| **VPS** | 3 nodes (DigitalOcean/Hetzner) | $48 |
| **PostgreSQL** | Included in VPS | $0 |
| **Redis** | Included in VPS | $0 |
| **SMTP Accounts** | 5× Gmail Workspace ($6/user) | $30 |
| **SMTP Accounts** | SendGrid Paid | $20 |
| **SMTP Accounts** | SMTP2GO/Mailgun | $10 |
| **Domains** | 5 domains @ $12/year | $5 |
| **Monitoring** | Grafana Cloud Free + Sentry Free | $0 |
| **Backup Storage** | S3-compatible (50GB) | $5 |
| **Blacklist Check** | MXToolbox API or self-hosted | $0-50 |
| **SSL Certs** | Let's Encrypt | $0 |
| **Proxy/IPs (optional)** | Rotating proxies for SMTP | $0-30 |
| **Total** | Base setup | **$118-168/mo** |

**Scale to 10k emails/day:** +$50/mo (more SMTP accounts, larger VPS)

---

## 9. Operational Flow

**Campaign Creation:**
```
1. Client → API: Upload CSV, template
2. API → Validate emails (Task 1 tool), save to PostgreSQL
3. API → Create Celery tasks (1 per recipient)
4. Queue → Assign SMTP account (rotation + health check)
5. Worker → Send email, log result
6. Retry failed → Exponential backoff
7. Update stats → PostgreSQL (sent, bounced, opened)
```

**Daily Maintenance:**
```
- Health check SMTP accounts (automated)
- Review DMARC reports (manual, 10min)
- Check blacklist status (automated alert)
- Analyze bounce rates per domain (dashboard)
```

---

## 10. Scaling Path

**0-5k emails/day:** Current architecture (3 nodes, 15 accounts)

**5k-20k emails/day:**
- Add 2 worker nodes (+$24/mo)
- Add 10 more SMTP accounts (+$60/mo)
- Upgrade Node 1 to 8GB RAM (+$24/mo)

**20k-100k emails/day:**
- Migrate to managed SMTP (SendGrid $80/mo for 40k)
- Add Redis Cluster (3 nodes for HA)
- Horizontal worker scaling (5-10 nodes)

---

## Summary

**Philosophy:** Start lean, scale incrementally. Avoid over-engineering (no Kubernetes for 1200 emails/day). Focus on deliverability over throughput—reputation is harder to rebuild than infrastructure.

**Key Success Metrics:**
- Delivery rate >95%
- Bounce rate <5%
- Zero blacklist incidents in first 3 months
- Uptime >99.5%

**Timeline to Production:** 2-3 weeks (1 week dev, 1 week testing/warm-up, 1 week monitoring)
