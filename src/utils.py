"""Модуль с утилитами для работы с JSON-файлами."""

import json
import logging
from typing import Any, Dict, List

# Импортируем настройку логгера
from src.logger_config import setup_logger

# Создаем логгер для модуля utils
logger = setup_logger('utils', 'utils.log', logging.DEBUG)


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON-файл и возвращает список словарей с данными транзакций.

    Args:
        file_path (str): Путь к JSON-файлу.

    Returns:
        List[Dict[str, Any]]: Список словарей с данными транзакций.
        Если файл пустой, содержит не список или не найден - возвращает пустой список.
    """
    logger.debug(f"Попытка чтения JSON-файла: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        logger.debug(f"Файл успешно прочитан: {file_path}")

        if not data:
            logger.warning(f"Файл {file_path} пустой или содержит пустые данные")
            return []

        if not isinstance(data, list):
            logger.error(
                f"Ошибка: данные в файле {file_path} не являются списком. "
                f"Тип данных: {type(data).__name__}"
            )
            return []

        logger.info(f"Успешно загружено {len(data)} транзакций из файла {file_path}")
        return data

    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        return []

    except json.JSONDecodeError as e:
        logger.error(
            f"Ошибка декодирования JSON в файле {file_path}: {e}",
            exc_info=True
        )
        return []

    except Exception as e:
        logger.error(
            f"Неожиданная ошибка при чтении файла {file_path}: {e}",
            exc_info=True
        )
        return []
