"""
Telegram Bot API client for sending messages.
"""

from typing import Optional, Tuple
import requests

from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class TelegramClient:
    """
    Telegram Bot API client with session reuse.
    """

    API_BASE_URL = "https://api.telegram.org"
    DEFAULT_TIMEOUT = 10  # seconds

    def __init__(self, bot_token: str, timeout: int = DEFAULT_TIMEOUT):
        """
        Initialize Telegram client.

        Args:
            bot_token: Telegram bot token from @BotFather
            timeout: HTTP request timeout in seconds
        """
        self.bot_token = bot_token
        self.timeout = timeout
        self.session = requests.Session()
        self.base_url = f"{self.API_BASE_URL}/bot{bot_token}"

    def send_message(
        self, chat_id: str, text: str, parse_mode: Optional[str] = None
    ) -> Tuple[bool, Optional[str]]:
        """
        Send text message to Telegram chat.

        Args:
            chat_id: Telegram chat ID (can be user ID or channel/group ID)
            text: Message text to send
            parse_mode: Optional parse mode (Markdown, HTML)

        Returns:
            Tuple of (success: bool, error_message: Optional[str])
        """
        url = f"{self.base_url}/sendMessage"

        payload = {
            "chat_id": chat_id,
            "text": text,
        }

        if parse_mode:
            payload["parse_mode"] = parse_mode

        try:
            logger.debug(f"Sending message to chat {chat_id} (length: {len(text)} chars)")

            response = self.session.post(url, json=payload, timeout=self.timeout)

            # Check HTTP status
            if response.status_code == 200:
                logger.info(f"Message sent successfully to chat {chat_id}")
                return True, None

            # Handle error responses
            error_data = response.json() if response.headers.get("content-type") == "application/json" else {}
            error_description = error_data.get("description", f"HTTP {response.status_code}")

            logger.error(f"Telegram API error: {error_description}")
            return False, error_description

        except requests.exceptions.Timeout:
            error_msg = f"Request timeout after {self.timeout}s"
            logger.error(error_msg)
            return False, error_msg

        except requests.exceptions.ConnectionError as e:
            error_msg = f"Connection error: {e}"
            logger.error(error_msg)
            return False, error_msg

        except requests.exceptions.RequestException as e:
            error_msg = f"Request error: {e}"
            logger.error(error_msg)
            return False, error_msg

        except Exception as e:
            error_msg = f"Unexpected error: {e}"
            logger.error(error_msg)
            return False, error_msg

    def test_connection(self) -> Tuple[bool, Optional[str]]:
        """
        Test bot token by calling getMe endpoint.

        Returns:
            Tuple of (success: bool, error_message: Optional[str])
        """
        url = f"{self.base_url}/getMe"

        try:
            logger.debug("Testing bot token with getMe")
            response = self.session.get(url, timeout=self.timeout)

            if response.status_code == 200:
                data = response.json()
                bot_info = data.get("result", {})
                bot_username = bot_info.get("username", "unknown")
                logger.info(f"Bot token valid. Bot username: @{bot_username}")
                return True, None

            error_data = response.json() if response.headers.get("content-type") == "application/json" else {}
            error_description = error_data.get("description", f"HTTP {response.status_code}")
            logger.error(f"Invalid bot token: {error_description}")
            return False, error_description

        except requests.exceptions.RequestException as e:
            error_msg = f"Connection test failed: {e}"
            logger.error(error_msg)
            return False, error_msg

        except Exception as e:
            error_msg = f"Unexpected error during connection test: {e}"
            logger.error(error_msg)
            return False, error_msg

    def close(self) -> None:
        """Close the HTTP session."""
        self.session.close()
        logger.debug("Telegram client session closed")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - close session."""
        self.close()
