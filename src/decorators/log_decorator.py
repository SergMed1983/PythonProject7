import logging
import functools
from typing import Callable, Any, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования выполнения функций.

    :param filename: Имя файла для логирования. Если None, логи идут в консоль.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Создаем отдельный логгер для каждой функции, чтобы не конфликтовать с другими
            logger = logging.getLogger(func.__name__)
            logger.setLevel(logging.INFO)

            # Очищаем старые хендлеры, чтобы не дублировать логи при повторных запусках тестов
            if logger.hasHandlers():
                logger.handlers.clear()

            # Настраиваем вывод: в файл ИЛИ в консоль (StreamHandler)
            if filename:
                handler = logging.FileHandler(filename, encoding='utf-8')
                # Важно: используем режим 'a' (append), чтобы не затирать логи предыдущих запусков в рамках одного теста
                handler.mode = 'a'
            else:
                handler = logging.StreamHandler()

            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)

            # Логирование начала
            logger.info(f"Start: {func.__name__}")
            logger.info(f"Args: {args}, Kwargs: {kwargs}")

            try:
                result = func(*args, **kwargs)
                logger.info(f"End: {func.__name__}. Result: {result}")
                return result
            except Exception as e:
                logger.error(f"Error in {func.__name__}: {str(e)}")
                logger.error(f"Inputs: args={args}, kwargs={kwargs}")
                raise

        return wrapper

    return decorator


