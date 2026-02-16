"""
MX record resolution and caching.
"""

from typing import List, Optional, Dict
import dns.resolver
import dns.exception

import config
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class MXChecker:
    """
    Checks MX records for domains with in-memory caching.
    """

    def __init__(self, enable_cache: bool = True):
        """
        Initialize MX checker.

        Args:
            enable_cache: Whether to cache MX records by domain
        """
        self.enable_cache = enable_cache
        self._cache: Dict[str, Optional[List[str]]] = {}
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = config.DNS_TIMEOUT
        self.resolver.lifetime = config.DNS_TIMEOUT

        if config.DNS_NAMESERVERS:
            self.resolver.nameservers = config.DNS_NAMESERVERS

    def get_mx_records(self, domain: str) -> Optional[List[str]]:
        """
        Get MX records for a domain.

        Args:
            domain: Domain name to check

        Returns:
            List of MX server hostnames (sorted by priority) or None if not found
        """
        # Check cache
        if self.enable_cache and domain in self._cache:
            logger.debug(f"Using cached MX records for domain: {domain}")
            return self._cache[domain]

        # Query MX records
        mx_records = self._query_mx_records(domain)

        # Cache result
        if self.enable_cache:
            self._cache[domain] = mx_records

        return mx_records

    def _query_mx_records(self, domain: str) -> Optional[List[str]]:
        """
        Query MX records from DNS.

        Args:
            domain: Domain name to query

        Returns:
            List of MX server hostnames or None if not found
        """
        try:
            logger.debug(f"Querying MX records for domain: {domain}")
            answers = self.resolver.resolve(domain, "MX")

            # Sort by priority (lower is better) and extract hostnames
            mx_records = sorted(answers, key=lambda x: x.preference)
            mx_hosts = [str(mx.exchange).rstrip(".") for mx in mx_records]

            if mx_hosts:
                logger.info(f"Found {len(mx_hosts)} MX record(s) for {domain}: {mx_hosts}")
                return mx_hosts
            else:
                logger.warning(f"No MX records found for domain: {domain}")
                return None

        except dns.resolver.NoAnswer:
            logger.warning(f"No MX records in DNS response for domain: {domain}")
            return None

        except dns.resolver.NXDOMAIN:
            logger.warning(f"Domain does not exist: {domain}")
            return None

        except dns.resolver.Timeout:
            logger.error(f"DNS timeout while querying MX records for domain: {domain}")
            return None

        except dns.exception.DNSException as e:
            logger.error(f"DNS error while querying MX records for {domain}: {e}")
            return None

        except Exception as e:
            logger.error(f"Unexpected error while querying MX records for {domain}: {e}")
            return None

    def domain_exists(self, domain: str) -> bool:
        """
        Check if domain exists (has any DNS records).

        Args:
            domain: Domain name to check

        Returns:
            True if domain exists, False otherwise
        """
        try:
            # Try A record first
            self.resolver.resolve(domain, "A")
            return True
        except dns.resolver.NoAnswer:
            # Try AAAA record
            try:
                self.resolver.resolve(domain, "AAAA")
                return True
            except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.DNSException):
                pass
        except dns.resolver.NXDOMAIN:
            logger.warning(f"Domain does not exist: {domain}")
            return False
        except dns.exception.DNSException as e:
            logger.error(f"DNS error while checking domain existence for {domain}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error while checking domain {domain}: {e}")
            return False

        return False

    def clear_cache(self) -> None:
        """Clear the MX records cache."""
        self._cache.clear()
        logger.debug("MX cache cleared")

    def get_cache_size(self) -> int:
        """
        Get current cache size.

        Returns:
            Number of cached domains
        """
        return len(self._cache)
