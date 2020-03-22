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

    # Test logger object
    assert " - test logger" in result.stdout

    # Test logging library interception
    assert " - test logging" in result.stdout

    # Test print interception
    assert ":print: - test print" in result.stdout

    # Test timer output
    assert " - :print: - Time elapsed: " in result.stdout
