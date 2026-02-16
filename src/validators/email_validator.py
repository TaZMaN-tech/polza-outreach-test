"""
Email format validation and domain extraction.
"""

import re
from typing import Optional, Tuple

from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class EmailValidator:
    """
    Validates email format and extracts domain.
    """

    # RFC 5322 compliant email regex (simplified)
    EMAIL_REGEX = re.compile(
        r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"
        r"@"
        r"[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
        r"(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
    )

    @staticmethod
    def validate_format(email: str) -> bool:
        """
        Validate email format using regex.

        Args:
            email: Email address to validate

        Returns:
            True if format is valid, False otherwise
        """
        if not email or not isinstance(email, str):
            return False

        email = email.strip().lower()

        # Basic length check
        if len(email) > 254:  # RFC 5321
            return False

        # Regex validation
        if not EmailValidator.EMAIL_REGEX.match(email):
            return False

        # Split and validate parts
        try:
            local, domain = email.rsplit("@", 1)
        except ValueError:
            return False

        # Local part length check
        if len(local) > 64:  # RFC 5321
            return False

        # Domain part length check
        if len(domain) > 253:  # RFC 1035
            return False

        return True

    @staticmethod
    def extract_domain(email: str) -> Optional[str]:
        """
        Extract domain from email address.

        Args:
            email: Email address

        Returns:
            Domain name or None if extraction fails
        """
        try:
            email = email.strip().lower()
            domain = email.rsplit("@", 1)[1]
            return domain
        except (IndexError, AttributeError) as e:
            logger.error(f"Failed to extract domain from '{email}': {e}")
            return None

    @staticmethod
    def validate_and_extract(email: str) -> Tuple[bool, Optional[str]]:
        """
        Validate email format and extract domain in one call.

        Args:
            email: Email address to validate

        Returns:
            Tuple of (is_valid, domain)
        """
        is_valid = EmailValidator.validate_format(email)
        domain = EmailValidator.extract_domain(email) if is_valid else None
        return is_valid, domain
