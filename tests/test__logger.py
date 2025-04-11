import logging
import unittest
from prompts._logger import setup

class TestLogger(unittest.TestCase):
    """Unit tests for the logger configuration in prompts/_logger.py."""

    def test_quiet_logger(self) -> None:
        """Test that setting quiet=True sets the logging level to CRITICAL."""
        setup(loglevel="DEBUG", quiet=True)
        root_logger = logging.getLogger()
        # When quiet, the log level is forced to CRITICAL.
        self.assertEqual(root_logger.level, logging.CRITICAL)

    def test_non_quiet_logger(self) -> None:
        """Test that setting a specific loglevel works when quiet is False."""
        setup(loglevel="INFO", quiet=False)
        root_logger = logging.getLogger()
        self.assertEqual(root_logger.level, logging.INFO)

if __name__ == "__main__":
    unittest.main()
