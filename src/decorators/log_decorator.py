import functools
import logging
import sys
from typing import Any, Callable, Optional, Union


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования выполнения функций в простом формате.

    При успешном выполнении выводит: "<имя_функции> ok"
    При ошибке выводит: "<имя_функции> error:
    <тип_ошибки>. Inputs: <args>, <kwargs>"
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            logger = logging.getLogger(func.__name__)
            logger.setLevel(logging.INFO)

            if logger.hasHandlers():
                logger.handlers.clear()

            handler: Union[logging.FileHandler, logging.StreamHandler]
            if filename:
                handler = logging.FileHandler(filename, encoding="utf-8")
            else:
                handler = logging.StreamHandler(sys.stdout)

            formatter = logging.Formatter("%(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.propagate = False

            try:
                result = func(*args, **kwargs)
                logger.info(f"{func.__name__} ok")
                return result
            except Exception as e:
                error_msg = (
                    f"{func.__name__} error: {type(e).__name__}. "
                    f"Inputs: {args}, {kwargs}"
                )
                logger.error(error_msg)
                raise

        return wrapper

    return decorator
