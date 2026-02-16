"""
CLI tool for sending text files to Telegram.
"""

import argparse
import os
import sys

from src.telegram.file_reader import FileReader
from src.telegram.telegram_client import TelegramClient
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


def main() -> int:
    """
    Main entry point for Telegram sender CLI.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = argparse.ArgumentParser(
        description="Send text file content to Telegram chat",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Environment Variables:
  TELEGRAM_BOT_TOKEN    Bot token from @BotFather (alternative to --token)
  TELEGRAM_CHAT_ID      Chat ID to send message to (alternative to --chat)

Examples:
  # Using CLI arguments
  python -m src.telegram.telegram_sender --file message.txt --token YOUR_TOKEN --chat YOUR_CHAT_ID

  # Using environment variables
  export TELEGRAM_BOT_TOKEN="123456:ABC-DEF..."
  export TELEGRAM_CHAT_ID="123456789"
  python -m src.telegram.telegram_sender --file message.txt

  # Test connection
  python -m src.telegram.telegram_sender --test --token YOUR_TOKEN
        """,
    )

    # File input
    parser.add_argument(
        "--file",
        type=str,
        help="Path to text file to send",
    )

    # Telegram credentials
    parser.add_argument(
        "--token",
        type=str,
        help="Telegram bot token (or set TELEGRAM_BOT_TOKEN env var)",
    )

    parser.add_argument(
        "--chat",
        type=str,
        help="Telegram chat ID (or set TELEGRAM_CHAT_ID env var)",
    )

    # Optional parameters
    parser.add_argument(
        "--parse-mode",
        type=str,
        choices=["Markdown", "HTML"],
        help="Message parse mode (Markdown or HTML)",
    )

    parser.add_argument(
        "--test",
        action="store_true",
        help="Test bot token without sending message",
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="HTTP request timeout in seconds (default: 10)",
    )

    args = parser.parse_args()

    try:
        # Get bot token from args or env
        bot_token = args.token or os.getenv("TELEGRAM_BOT_TOKEN")
        if not bot_token:
            logger.error("Bot token not provided. Use --token or set TELEGRAM_BOT_TOKEN")
            print("Error: Bot token required. Use --token or set TELEGRAM_BOT_TOKEN environment variable")
            return 1

        # Test mode
        if args.test:
            logger.info("Running connection test")
            with TelegramClient(bot_token, timeout=args.timeout) as client:
                success, error = client.test_connection()

            if success:
                print("✅ Bot token is valid. Connection test successful.")
                return 0
            else:
                print(f"❌ Connection test failed: {error}")
                return 1

        # Get chat ID from args or env
        chat_id = args.chat or os.getenv("TELEGRAM_CHAT_ID")
        if not chat_id:
            logger.error("Chat ID not provided. Use --chat or set TELEGRAM_CHAT_ID")
            print("Error: Chat ID required. Use --chat or set TELEGRAM_CHAT_ID environment variable")
            return 1

        # File is required for sending
        if not args.file:
            logger.error("File path not provided")
            print("Error: --file is required for sending messages")
            parser.print_help()
            return 1

        # Read file content
        logger.info(f"Reading file: {args.file}")
        content = FileReader.read_file(args.file)

        # Validate content
        if not FileReader.validate_content(content):
            logger.error("File content is empty")
            print("Error: File is empty or contains only whitespace")
            return 1

        # Send message to Telegram
        logger.info(f"Sending message to Telegram chat {chat_id}")
        with TelegramClient(bot_token, timeout=args.timeout) as client:
            success, error = client.send_message(
                chat_id=chat_id,
                text=content,
                parse_mode=args.parse_mode,
            )

        if success:
            logger.info("Message sent successfully")
            print(f"✅ Message sent successfully to chat {chat_id}")
            print(f"   File: {args.file}")
            print(f"   Length: {len(content)} characters")
            return 0
        else:
            logger.error(f"Failed to send message: {error}")
            print(f"❌ Failed to send message: {error}")
            return 1

    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        print(f"❌ File error: {e}")
        return 1

    except IOError as e:
        logger.error(f"IO error: {e}")
        print(f"❌ IO error: {e}")
        return 1

    except KeyboardInterrupt:
        logger.warning("Process interrupted by user")
        print("\n\n⚠️  Process interrupted by user")
        return 1

    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"❌ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
