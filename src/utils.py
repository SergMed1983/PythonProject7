"""Модуль с утилитами для работы с JSON-файлами."""

import json
from typing import Any, Dict, List


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON-файл и возвращает список словарей с данными транзакций.

    Args:
        file_path (str): Путь к JSON-файлу.

    Returns:
        List[Dict[str, Any]]: Список словарей с данными транзакций.
        Если файл пустой, содержит не список или не найден - возвращает пустой список.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not data:
            return []

        if not isinstance(data, list):
            return []

        return data

    except (FileNotFoundError, json.JSONDecodeError):
        return []
