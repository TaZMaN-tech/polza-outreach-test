"""
Data models for email verification results.
"""

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Optional, List


class VerificationStatus(Enum):
    """Email verification status enumeration."""

    VALID = "valid"  # Email passed all checks
    INVALID_FORMAT = "invalid_format"  # Email format is incorrect
    DOMAIN_NOT_FOUND = "domain_not_found"  # Domain does not exist
    NO_MX_RECORDS = "no_mx_records"  # MX records missing or incorrect
    SMTP_UNAVAILABLE = "smtp_unavailable"  # SMTP server unreachable or blocked
    SMTP_REJECTED = "smtp_rejected"  # SMTP server rejected the email


class SMTPStatus(Enum):
    """SMTP verification status."""

    VERIFIED = "verified"  # SMTP verification successful (250)
    REJECTED = "rejected"  # SMTP rejected email (550)
    UNAVAILABLE = "unavailable"  # SMTP server unreachable/timeout
    NOT_CHECKED = "not_checked"  # SMTP check was not performed


@dataclass
class VerificationResult:
    """
    Result of email verification process.

    Attributes:
        email: The email address that was verified
        status: Verification status
        domain: Extracted domain from email
        mx_records: List of MX servers (if found)
        smtp_status: SMTP verification status
        smtp_response: SMTP server response message
        error_message: Error details (if any)
    """

    email: str
    status: VerificationStatus
    smtp_status: SMTPStatus = SMTPStatus.NOT_CHECKED
    domain: Optional[str] = None
    mx_records: Optional[List[str]] = None
    smtp_response: Optional[str] = None
    error_message: Optional[str] = None

    def to_dict(self) -> dict:
        """
        Convert result to dictionary for JSON serialization.

        Returns:
            Dictionary representation of the result
        """
        result = asdict(self)
        result["status"] = self.status.value
        result["smtp_status"] = self.smtp_status.value
        return result

    def get_domain_status(self) -> str:
        """
        Get domain status according to TZ requirements.

        TZ specifies ONLY 3 possible statuses:
        - "домен валиден"
        - "домен отсутствует"
        - "MX-записи отсутствуют или некорректны"

        Returns:
            Domain status message as per TZ specification (one of 3 values)
        """
        if self.status == VerificationStatus.INVALID_FORMAT:
            # Invalid format means domain doesn't exist (per TZ requirements)
            return "домен отсутствует"
        elif self.status == VerificationStatus.DOMAIN_NOT_FOUND:
            return "домен отсутствует"
        elif self.status == VerificationStatus.NO_MX_RECORDS:
            return "MX-записи отсутствуют или некорректны"
        else:
            # VALID, SMTP_UNAVAILABLE, SMTP_REJECTED all mean domain is valid
            return "домен валиден"

    def get_smtp_status_text(self) -> str:
        """
        Get SMTP status text.

        Returns:
            Human-readable SMTP status
        """
        status_map = {
            SMTPStatus.VERIFIED: "verified",
            SMTPStatus.REJECTED: "rejected",
            SMTPStatus.UNAVAILABLE: "unavailable",
            SMTPStatus.NOT_CHECKED: "not checked",
        }
        return status_map.get(self.smtp_status, "unknown")

    def get_human_readable_status(self) -> str:
        """
        Get human-readable status message (for backward compatibility).

        Returns:
            User-friendly status description
        """
        status_messages = {
            VerificationStatus.VALID: "домен валиден",
            VerificationStatus.INVALID_FORMAT: "неверный формат email",
            VerificationStatus.DOMAIN_NOT_FOUND: "домен отсутствует",
            VerificationStatus.NO_MX_RECORDS: "MX-записи отсутствуют или некорректны",
            VerificationStatus.SMTP_UNAVAILABLE: "домен валиден (SMTP недоступен)",
            VerificationStatus.SMTP_REJECTED: "домен валиден (SMTP отклонил адрес)",
        }
        return status_messages.get(self.status, "неизвестный статус")
