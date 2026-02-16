"""
File reading utilities for Telegram sender.
"""

from pathlib import Path
from typing import Optional

from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class FileReader:
    """
    Reads text files for sending to Telegram.
    """

    @staticmethod
    def read_file(file_path: str) -> Optional[str]:
        """
        Read text content from file.

        Args:
            file_path: Path to text file

        Returns:
            File content as string, or None if error

        Raises:
            FileNotFoundError: If file does not exist
            IOError: If file cannot be read
        """
        path = Path(file_path)

        # Check if file exists
        if not path.exists():
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")

        # Check if it's a file
        if not path.is_file():
            logger.error(f"Path is not a file: {file_path}")
            raise IOError(f"Path is not a file: {file_path}")

        # Read file content
        try:
            with path.open("r", encoding="utf-8") as f:
                content = f.read()

            logger.info(f"Successfully read file: {file_path} ({len(content)} characters)")
            return content

        except UnicodeDecodeError as e:
            logger.error(f"Failed to decode file as UTF-8: {file_path} - {e}")
            raise IOError(f"File encoding error: {e}")

        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            raise IOError(f"Failed to read file: {e}")

    @staticmethod
    def validate_content(content: Optional[str]) -> bool:
        """
        Validate that content is not empty.

        Args:
            content: Text content to validate

        Returns:
            True if content is valid, False otherwise
        """
        if content is None:
            logger.warning("Content is None")
            return False

        if not content.strip():
            logger.warning("Content is empty or whitespace only")
            return False

        return True
