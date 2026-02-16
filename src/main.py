"""
Main entry point for email verification CLI.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List

import config
from src.models.result import VerificationResult, VerificationStatus, SMTPStatus
from src.validators.email_validator import EmailValidator
from src.dns.mx_checker import MXChecker
from src.smtp.smtp_verifier import SMTPVerifier
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class EmailVerificationService:
    """
    Orchestrates email verification process.
    """

    def __init__(self):
        """Initialize verification service with all components."""
        self.validator = EmailValidator()
        self.mx_checker = MXChecker(enable_cache=config.ENABLE_MX_CACHE)
        self.smtp_verifier = SMTPVerifier()

    def verify_email(self, email: str) -> VerificationResult:
        """
        Verify a single email address.

        Args:
            email: Email address to verify

        Returns:
            VerificationResult with status and details
        """
        logger.info(f"Starting verification for: {email}")

        # Step 1: Validate email format
        is_valid_format, domain = self.validator.validate_and_extract(email)
        if not is_valid_format:
            logger.warning(f"Invalid email format: {email}")
            return VerificationResult(
                email=email,
                status=VerificationStatus.INVALID_FORMAT,
                error_message="Email format is invalid",
            )

        # Step 2: Check if domain exists
        if not self.mx_checker.domain_exists(domain):
            logger.warning(f"Domain does not exist: {domain}")
            return VerificationResult(
                email=email,
                status=VerificationStatus.DOMAIN_NOT_FOUND,
                domain=domain,
                error_message="Domain does not exist in DNS",
            )

        # Step 3: Get MX records
        mx_records = self.mx_checker.get_mx_records(domain)
        if not mx_records:
            logger.warning(f"No MX records found for domain: {domain}")
            return VerificationResult(
                email=email,
                status=VerificationStatus.NO_MX_RECORDS,
                domain=domain,
                error_message="No MX records found for domain",
            )

        # Step 4: SMTP handshake verification
        is_valid, smtp_response, error_message = self.smtp_verifier.verify_with_fallback(
            email, mx_records
        )

        if is_valid:
            logger.info(f"Email verification successful: {email}")
            return VerificationResult(
                email=email,
                status=VerificationStatus.VALID,
                smtp_status=SMTPStatus.VERIFIED,
                domain=domain,
                mx_records=mx_records,
                smtp_response=smtp_response,
            )
        else:
            # Determine if SMTP was unavailable or rejected the email
            if smtp_response and smtp_response.startswith("550"):
                status = VerificationStatus.SMTP_REJECTED
                smtp_status = SMTPStatus.REJECTED
            else:
                status = VerificationStatus.SMTP_UNAVAILABLE
                smtp_status = SMTPStatus.UNAVAILABLE

            logger.warning(f"Email verification failed: {email} - {error_message}")
            return VerificationResult(
                email=email,
                status=status,
                smtp_status=smtp_status,
                domain=domain,
                mx_records=mx_records,
                smtp_response=smtp_response,
                error_message=error_message,
            )

    def verify_bulk(self, emails: List[str]) -> List[VerificationResult]:
        """
        Verify multiple email addresses.

        Args:
            emails: List of email addresses to verify

        Returns:
            List of VerificationResult objects
        """
        results = []
        total = len(emails)

        logger.info(f"Starting bulk verification for {total} email(s)")

        for idx, email in enumerate(emails, 1):
            logger.info(f"Processing {idx}/{total}: {email}")
            result = self.verify_email(email)
            results.append(result)

        logger.info(f"Bulk verification completed: {total} email(s) processed")
        return results


def load_emails_from_file(file_path: str) -> List[str]:
    """
    Load email addresses from a text file.

    Args:
        file_path: Path to file containing emails (one per line)

    Returns:
        List of email addresses

    Raises:
        FileNotFoundError: If file does not exist
        IOError: If file cannot be read
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not path.is_file():
        raise IOError(f"Path is not a file: {file_path}")

    with path.open("r", encoding="utf-8") as f:
        emails = [line.strip() for line in f if line.strip()]

    logger.info(f"Loaded {len(emails)} email(s) from file: {file_path}")
    return emails


def parse_emails_from_string(emails_str: str) -> List[str]:
    """
    Parse comma-separated email addresses from string.

    Args:
        emails_str: Comma-separated email addresses

    Returns:
        List of email addresses
    """
    emails = [email.strip() for email in emails_str.split(",") if email.strip()]
    logger.info(f"Parsed {len(emails)} email(s) from input string")
    return emails


def print_results_console(results: List[VerificationResult]) -> None:
    """
    Print verification results to console in human-readable format.

    Console output follows TZ requirements:
    - Status: only 3 values ("домен валиден", "домен отсутствует", "MX-записи отсутствуют или некорректны")
    - SMTP: separate field (verified/rejected/unavailable)

    Args:
        results: List of verification results
    """
    print("\n" + "=" * 80)
    print("EMAIL VERIFICATION RESULTS")
    print("=" * 80 + "\n")

    for idx, result in enumerate(results, 1):
        print(f"{idx}. Email: {result.email}")
        print(f"   Status: {result.get_domain_status()}")

        if result.domain:
            print(f"   Domain: {result.domain}")

        if result.mx_records:
            # Filter out empty MX records
            valid_mx = [mx for mx in result.mx_records if mx]
            if valid_mx:
                print(f"   MX Records: {', '.join(valid_mx)}")

        # Show SMTP status separately
        if result.smtp_status != SMTPStatus.NOT_CHECKED:
            print(f"   SMTP: {result.get_smtp_status_text()}")

        if result.smtp_response:
            print(f"   SMTP Response: {result.smtp_response}")

        if result.error_message:
            print(f"   Error: {result.error_message}")

        print()

    print("=" * 80)


def save_results_json(results: List[VerificationResult], output_path: str) -> None:
    """
    Save verification results to JSON file.

    Args:
        results: List of verification results
        output_path: Path to output JSON file
    """
    output = {
        "total": len(results),
        "results": [result.to_dict() for result in results],
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    logger.info(f"Results saved to JSON file: {output_path}")
    print(f"\nResults saved to: {output_path}")


def main() -> int:
    """
    Main entry point for CLI.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = argparse.ArgumentParser(
        description="Email verification tool with DNS and SMTP checks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.main --emails "test@example.com,user@domain.org"
  python -m src.main --file emails.txt
  python -m src.main --emails "test@gmail.com" --json output.json
        """,
    )

    # Input options (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "--emails",
        type=str,
        help="Comma-separated list of email addresses",
    )
    input_group.add_argument(
        "--file",
        type=str,
        help="Path to text file with email addresses (one per line)",
    )

    # Output options
    parser.add_argument(
        "--json",
        type=str,
        help="Save results to JSON file",
    )

    args = parser.parse_args()

    try:
        # Load emails
        if args.emails:
            emails = parse_emails_from_string(args.emails)
        else:
            emails = load_emails_from_file(args.file)

        if not emails:
            logger.error("No email addresses provided")
            print("Error: No email addresses found")
            return 1

        # Verify emails
        service = EmailVerificationService()
        results = service.verify_bulk(emails)

        # Print results to console
        print_results_console(results)

        # Save to JSON if requested
        if args.json:
            save_results_json(results, args.json)

        return 0

    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        print(f"Error: {e}")
        return 1

    except IOError as e:
        logger.error(f"IO error: {e}")
        print(f"Error: {e}")
        return 1

    except KeyboardInterrupt:
        logger.warning("Process interrupted by user")
        print("\n\nProcess interrupted by user")
        return 1

    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
