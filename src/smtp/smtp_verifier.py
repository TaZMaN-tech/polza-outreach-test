"""
SMTP handshake verification without sending emails.
"""

import smtplib
import socket
from typing import Optional, Tuple

import config
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class SMTPVerifier:
    """
    Performs SMTP handshake to verify email deliverability.
    """

    def __init__(
        self,
        timeout: int = config.SMTP_TIMEOUT,
        from_email: str = config.SMTP_FROM_EMAIL,
    ):
        """
        Initialize SMTP verifier.

        Args:
            timeout: Connection timeout in seconds
            from_email: Email address to use in MAIL FROM command
        """
        self.timeout = timeout
        self.from_email = from_email

    def verify_email(self, email: str, mx_host: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Verify email address via SMTP handshake.

        Performs: EHLO -> MAIL FROM -> RCPT TO

        Args:
            email: Email address to verify
            mx_host: MX server hostname to connect to

        Returns:
            Tuple of (is_valid, smtp_response, error_message)
            smtp_response format: "CODE response_text" for all successful SMTP replies
        """
        smtp = None
        try:
            # Connect to SMTP server
            logger.debug(f"Connecting to SMTP server: {mx_host}:{config.SMTP_PORT}")
            smtp = smtplib.SMTP(timeout=self.timeout)
            smtp.connect(mx_host, config.SMTP_PORT)

            # EHLO/HELO
            logger.debug(f"Sending EHLO to {mx_host}")
            smtp.ehlo_or_helo_if_needed()

            # MAIL FROM
            logger.debug(f"Sending MAIL FROM: {self.from_email}")
            code, response = smtp.mail(self.from_email)
            if code != 250:
                response_text = response.decode() if isinstance(response, bytes) else str(response)
                smtp_response = f"{code} {response_text}"
                error_msg = f"MAIL FROM rejected with code {code}: {response_text}"
                logger.warning(error_msg)
                return False, smtp_response, error_msg

            # RCPT TO
            logger.debug(f"Sending RCPT TO: {email}")
            code, response = smtp.rcpt(email)

            # Decode response
            response_text = response.decode() if isinstance(response, bytes) else str(response)
            smtp_response = f"{code} {response_text}"

            # Analyze response code
            if code == 250:
                # Email accepted
                logger.info(f"Email {email} verified successfully on {mx_host}")
                return True, smtp_response, None
            elif code == 550:
                # Email rejected (user does not exist)
                error_msg = f"Email rejected with code {code}: {response_text}"
                logger.warning(error_msg)
                return False, smtp_response, error_msg
            else:
                # Other codes (temporary failure, greylisting, etc.)
                error_msg = f"Unexpected SMTP code {code}: {response_text}"
                logger.warning(error_msg)
                return False, smtp_response, error_msg

        except smtplib.SMTPServerDisconnected as e:
            error_msg = f"SMTP server disconnected: {e}"
            logger.error(error_msg)
            return False, None, error_msg

        except smtplib.SMTPResponseException as e:
            response_text = e.smtp_error.decode() if isinstance(e.smtp_error, bytes) else str(e.smtp_error)
            smtp_response = f"{e.smtp_code} {response_text}"
            error_msg = f"SMTP response error (code {e.smtp_code}): {response_text}"
            logger.error(error_msg)
            # Check if it's a 550 rejection
            if e.smtp_code == 550:
                return False, smtp_response, error_msg
            return False, smtp_response, error_msg

        except socket.timeout:
            error_msg = f"SMTP connection timeout to {mx_host}"
            logger.error(error_msg)
            return False, None, error_msg

        except socket.gaierror as e:
            error_msg = f"Failed to resolve SMTP host {mx_host}: {e}"
            logger.error(error_msg)
            return False, None, error_msg

        except ConnectionRefusedError:
            error_msg = f"SMTP connection refused by {mx_host}"
            logger.error(error_msg)
            return False, None, error_msg

        except OSError as e:
            error_msg = f"Network error connecting to {mx_host}: {e}"
            logger.error(error_msg)
            return False, None, error_msg

        except Exception as e:
            error_msg = f"Unexpected error during SMTP verification: {e}"
            logger.error(error_msg)
            return False, None, error_msg

        finally:
            # Always close the connection
            if smtp:
                try:
                    smtp.quit()
                    logger.debug(f"SMTP connection to {mx_host} closed")
                except Exception as e:
                    logger.debug(f"Error closing SMTP connection: {e}")

    def verify_with_fallback(self, email: str, mx_hosts: list) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Try to verify email with multiple MX hosts (fallback mechanism).

        Args:
            email: Email address to verify
            mx_hosts: List of MX server hostnames (ordered by priority)

        Returns:
            Tuple of (is_valid, smtp_response, error_message)
        """
        if not mx_hosts:
            return False, None, "No MX hosts provided"

        last_error = None
        last_response = None

        for mx_host in mx_hosts:
            logger.info(f"Attempting SMTP verification on {mx_host} for {email}")
            is_valid, response, error = self.verify_email(email, mx_host)

            if is_valid:
                return True, response, None

            # Store response and error
            if response:
                last_response = response

            # If explicitly rejected (550), no need to try other MX servers
            if response and response.startswith("550"):
                return False, response, error

            # Store last error for reporting
            last_error = error

        # All MX hosts failed
        error_msg = f"SMTP verification failed on all {len(mx_hosts)} MX host(s). Last error: {last_error}"
        logger.error(error_msg)
        return False, last_response, error_msg
