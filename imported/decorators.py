"""Misc function decorators."""
from datetime import datetime
from functools import wraps
import logging
from loguru import logger
import sys
from time import perf_counter


class LogPrinter:
    '''LogPrinter class which serves to emulates a file object and logs whatever it gets sent to a Logger object at the level defined or INFO as default.

    https://wiki.python.org/moin/PythonDecoratorLibrary#Redirects_stdout_printing_to_python_standard_logging%2E
    '''
    def __init__(self, level=logging.INFO, name=''):
        '''Grabs the specific logger to use for logprinting.'''
        logger.remove()
        logger.add(sys.stdout, level=level, enqueue=True)
        self.ilogger = logger.opt(lazy=True)
        self.level = level
        self.name = name
        self.ilogger.log(level, name)

    def write(self, text):
        '''Logs written output to a specific logger'''
        self.ilogger.log(self.level, f'{self.name}|print\n{text}')


def logprint(*args, level=logging.INFO, name='', **kwargs):
    """Create decorator factory for logprint."""
    def logprintinfo(func):
        '''Wraps a method so that any calls made to print get logged instead.

        https://wiki.python.org/moin/PythonDecoratorLibrary#Unimplemented_function_replacement
        '''
        @wraps(func)
        def pwrapper(*arg, **kwargs):
            stdobak = sys.stdout
            lpinstance = LogPrinter(level, name)
            sys.stdout = lpinstance
            try:
                return timer(func)(*arg, **kwargs)
            finally:
                sys.stdout = stdobak
        return pwrapper

    return logprintinfo


def timer(func):
    """Time wrapped function."""
    @wraps(func)
    def wrapper(*arg, **kwargs):
        start_time = datetime.now()
        start_counter = perf_counter()
        print(f'{func.__name__} started at {start_time}.')
        results = func(*arg, **kwargs)
        end_time = datetime.now()
        end_counter = perf_counter()
        total_time = end_time - start_time
        print(f'Time elapsed: {total_time}.')
        total_sec = (end_counter - start_counter)
        print(f'Seconds elapsed: {total_sec}s.')
        return results
    return wrapper


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

        logger.opt(depth=depth,
                   exception=record.exc_info).log(level, record.getMessage())


logging.basicConfig(handlers=[InterceptHandler()], level=0)


if __name__ == '__main__':
    from time import sleep

    @logprint(level='INFO', name='func')
    def func(s: str):
        logger.info('test logger')
        sleep(1)
        logging.info('test logging')
        print(s)

    func(__name__)
