"""Script to test decorators module output."""

import logging

from loguru import logger

from decorators import LogPrinter, timer

if __name__ == "__main__":

    @LogPrinter.logprint(level=logging.INFO)
    def func():
        """Test wrappers."""
        logger.info("test_logger")
        logging.info("test_logging")
        print("test_print")

    func()
