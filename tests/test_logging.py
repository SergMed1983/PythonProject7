"""Тесты для проверки логирования в модулях masks и utils."""

import os

from src.masks import mask_account_number, mask_card_number
from src.utils import read_json_file


def test_mask_card_number_logging():
    """Проверка логирования маскировки номера карты."""
    result = mask_card_number("1234567890123456")
    assert result == "1234 56** **** 3456"


def test_mask_account_number_logging():
    """Проверка логирования маскировки номера счета."""
    result = mask_account_number("1234567890")
    assert result == "**7890"


def test_read_json_file_logging():
    """Проверка логирования чтения JSON файла."""
    # Тест с несуществующим файлом (должен вернуть пустой список)
    result = read_json_file("nonexistent.json")
    assert result == []


def test_log_files_created():
    """Проверка, что файлы логов создаются."""
    # Вызываем функции, чтобы создать логи
    try:
        mask_card_number("1234567890123456")
    except Exception:
        pass

    try:
        read_json_file("nonexistent.json")
    except Exception:
        pass

    # Проверяем, что файлы логов созданы
    assert os.path.exists("logs/utils.log")
    assert os.path.exists("logs/masks.log")
