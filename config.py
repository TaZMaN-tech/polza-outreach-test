"""
Configuration module for email verification settings.
"""

# SMTP Configuration
SMTP_TIMEOUT = 10  # seconds
SMTP_PORT = 25
SMTP_FROM_EMAIL = "verify@example.com"  # Used for MAIL FROM command

# DNS Configuration
DNS_TIMEOUT = 5  # seconds
DNS_NAMESERVERS = None  # None = use system default, or list like ['8.8.8.8', '8.8.4.4']

# Logging Configuration
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Cache Configuration
ENABLE_MX_CACHE = True  # Cache MX records by domain in memory
