"""Script to test decorators module output."""
import logging

from loguru import logger

try:
    from decorators import LogPrinter
except ImportError:  # pragma: no cover
    try:
        from .decorators import LogPrinter
    except ImportError:
        from imported.decorators import LogPrinter


if __name__ == "__main__":

    @LogPrinter.logprint(level=logging.INFO)
    def func():
        """Test wrappers."""
        logger.info("test_logger")
        logging.info("test_logging")
        print("test_print")

    func()
