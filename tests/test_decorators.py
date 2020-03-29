"""Test for decorators module."""

import logging
import sys

from loguru import logger

from imported.decorators import LogPrinter


def test_decorators():
    @LogPrinter.logprint(level=logging.INFO)
    def func():
        """Test wrappers."""
        logger.info("test logger")
        logging.info("test logging")
        print("test print")
        return True

    assert func()


def test_script(env):
    result = env.run(
        sys.executable,
        "imported/decorators_test_script.py",
        expect_error=True,
    )

    output = result.stdout + "\n" + result.stderr

    # Test logger object
    assert "test_logger" in output

    # Test logging library interception
    assert "test_logging" in output

    # Test print interception
    assert "test_print" in output

    # Test timer output
    assert " - :print: - Time elapsed: " in output
