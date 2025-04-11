import unittest
import logging
from io import StringIO
from prompts import _logger

class TestLogger(unittest.TestCase):
    """Unit tests for the logger module.

    These tests verify that the logger configuration behaves as expected in quiet
    mode and with a specified log level.
    """
    def test_logger_quiet(self) -> None:
        """Test that logger.setup suppresses logging output when quiet is True."""
        # Clear any existing handlers
        logging.getLogger().handlers.clear()
        _logger.setup("DEBUG", quiet=True)
        stream = StringIO()
        handler = logging.StreamHandler(stream)
        logging.root.addHandler(handler)
        logging.debug("Test message")
        # In quiet mode, no output should be produced
        self.assertEqual(stream.getvalue(), "")

    def test_logger_loglevel(self) -> None:
        """Test that logger.setup sets the correct logging level when quiet is False."""
        # Clear any existing handlers
        logging.getLogger().handlers.clear()
        _logger.setup("INFO", quiet=False)
        root_logger = logging.getLogger()
        # The logger's effective level should be at least INFO
        self.assertGreaterEqual(root_logger.level, logging.INFO)
        stream = StringIO()
        handler = logging.StreamHandler(stream)
        logging.root.addHandler(handler)
        logging.info("Info message")
        self.assertIn("Info message", stream.getvalue())

