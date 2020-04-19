"""Misc function decorators."""
from datetime import datetime
import logging
import sys
from time import perf_counter

from loguru import logger
from wrapt import decorator


class LogPrinter:
    """LogPrinter class.

    Emulates a file object and logs whatever it gets sent to a
    Logger object at the level defined or INFO as default.

    https://wiki.python.org/moin/PythonDecoratorLibrary#Redirects_stdout_printing_to_python_standard_logging%2E  # noqa
    """

    def __init__(self, level=logging.INFO):
        """Grabs the specific logger to use for logprinting."""
        logging.basicConfig(handlers=[self.InterceptHandler()], level=level)
        logger.remove()
        logger.add(sys.stdout, level=level, enqueue=True)
        logger.log(level, f"Level: {level}")
        self.level = level
        self.ilogger = logger

    def write(self, text):
        """Log written output to a specific logger."""
        self.ilogger.opt(depth=1).log(self.level, f":print: - {text}")

    @staticmethod
    def logprint(*args, level=logging.INFO, name="", **kwargs):
        """Create decorator factory for logprint."""

        @decorator
        def logprintinfo(wrapped, instance, args, kwargs):
            """Wrap a method so that calls to print get logged.

            https://wiki.python.org/moin/PythonDecoratorLibrary#Unimplemented_function_replacement  # noqa
            """
            stdobak = sys.stdout
            lpinstance = LogPrinter(level)
            sys.stdout = lpinstance
            try:
                return timer(wrapped)(*args, **kwargs)
            finally:
                sys.stdout = stdobak

        return logprintinfo

    class InterceptHandler(logging.Handler):
        """Intercepts logging calls.

        https://github.com/Delgan/loguru#entirely-compatible-with-standard-logging  # noqa
        """

        def emit(self, record):
            """Get corresponding Loguru level if it exists."""
            try:
                level = logger.level(record.levelname).name
            except (ValueError, AttributeError):  # pragma: no cover
                level = record.levelno

            # Find caller from where originated the logged message
            frame, depth = logging.currentframe(), 2
            while frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1

            logger.opt(lazy=True, depth=depth, exception=record.exc_info,).log(
                level, record.getMessage()
            )


@decorator
def timer(wrapped, instance, args, kwargs):
    """Time wrapped function."""
    start_time = datetime.now()
    start_counter = perf_counter()
    print(f"{wrapped.__name__} started at {start_time}.")
    results = wrapped(*args, **kwargs)
    end_time = datetime.now()
    end_counter = perf_counter()
    total_time = end_time - start_time
    print(f"Time elapsed: {total_time}.")
    total_sec = end_counter - start_counter
    print(f"Seconds elapsed: {total_sec}s.")
    return results
