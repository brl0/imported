"""Misc function decorators."""
from datetime import datetime
from functools import wraps
import logging
import sys
from time import perf_counter

from loguru import logger


class LogPrinter:
    '''LogPrinter class which serves to emulates a file object and logs whatever it gets sent to a Logger object at the level defined or INFO as default.

    https://wiki.python.org/moin/PythonDecoratorLibrary#Redirects_stdout_printing_to_python_standard_logging%2E
    '''
    def __init__(self, level=logging.INFO):
        '''Grabs the specific logger to use for logprinting.'''
        logging.basicConfig(handlers=[self.InterceptHandler()], level=level)
        logger.remove()
        logger.add(sys.stdout, level=level, enqueue=True)
        logger.log(level, f'Level: {level}')
        self.level = level
        self.ilogger = logger

    def write(self, text):
        '''Logs written output to a specific logger'''
        self.ilogger.opt(depth=1).log(self.level, f':print: - {text}')

    @staticmethod
    def logprint(*args, level=logging.INFO, name='', **kwargs):
        """Create decorator factory for logprint."""
        def logprintinfo(func):
            '''Wraps a method so that any calls made to print get logged instead.

            https://wiki.python.org/moin/PythonDecoratorLibrary#Unimplemented_function_replacement
            '''
            @wraps(func)
            def pwrapper(*arg, **kwargs):
                stdobak = sys.stdout
                lpinstance = LogPrinter(level)
                sys.stdout = lpinstance
                try:
                    return timer(func)(*arg, **kwargs)
                finally:
                    sys.stdout = stdobak
            return pwrapper

        return logprintinfo

    class InterceptHandler(logging.Handler):
        """https://github.com/Delgan/loguru#entirely-compatible-with-standard-logging"""
        def emit(self, record):
            # Get corresponding Loguru level if it exists
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            # Find caller from where originated the logged message
            frame, depth = logging.currentframe(), 2
            while frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1

            logger.opt(
                lazy=True,
                depth=depth,
                exception=record.exc_info,
                ).log(level, record.getMessage())


def timer(func):
    """Time wrapped function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        start_counter = perf_counter()
        print(f'{func.__name__} started at {start_time}.')
        results = func(*args, **kwargs)
        end_time = datetime.now()
        end_counter = perf_counter()
        total_time = end_time - start_time
        print(f'Time elapsed: {total_time}.')
        total_sec = (end_counter - start_counter)
        print(f'Seconds elapsed: {total_sec}s.')
        return results

    return wrapper


def rec_cycle(func):
    """Try to prevent recursive cycles."""
    r = dict()
    def tuplizer(*args, **kwargs):
        t = [*args]
        t.extend(list(kwargs.items()))
        return tuple(t)

    @wraps(func)
    def wrapper(*args, **kwargs):
        t = tuplizer(*args, **kwargs)
        if not t in r.keys():
            results = func(*args, **kwargs)
            r[t] = results
        else:
            print(f"Caught {t}")
            results = r[t]
        return results

    return wrapper


if __name__ == '__main__':
    from time import sleep

    @LogPrinter.logprint(level=logging.INFO)
    @timer
    def func(s: str):
        logger.info('test logger')
        logging.info('test logging')
        sleep(1)
        print(s)

    func(__name__)
