import logging
import time

logging.basicConfig(filename='decorator.log', level=logging.INFO)
logger = logging.getLogger(__name__)


def log_func_decorator(func, log_level=logging.INFO):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        logger.log(log_level, f'Function {func.__name__} called')
        logger.log(log_level, f"Called with args: {args}, kwargs: {kwargs}")
        logger.log(log_level, f'Start time: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start))}')
        logger.log(log_level, f'Time elapsed: {end - start:.6f}')
        logger.log(log_level, f'Result: {result}')

        return result

    return wrapper


def log_object_created(cls, log_level=logging.INFO):
    class Wrapper(cls):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            logger.log(log_level, f'Created object of class {cls.__name__}')
    return Wrapper
