import pytest
from src.search import process_bank_search
from src.categories import process_bank_operations


def test_process_bank_search():
    """Тест функции поиска по описанию"""
    data = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Перевод с карты на карту"}
    ]

    result = process_bank_search(data, "перевод")
    assert len(result) == 2
    assert result[0]["description"] == "Перевод организации"
    assert result[1]["description"] == "Перевод с карты на карту"


def test_process_bank_search_empty():
    """Тест с пустыми данными"""
    assert process_bank_search([], "test") == []
    assert process_bank_search([{"description": "test"}], "") == []


def test_process_bank_operations():
    """Тест подсчета категорий"""
    data = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Перевод организации"},
        {"description": "Перевод с карты на карту"}
    ]

    categories = ["Перевод организации", "Открытие вклада", "Другое"]
    result = process_bank_operations(data, categories)

    assert result["Перевод организации"] == 2
    assert result["Открытие вклада"] == 1
    assert result["Другое"] == 0


def test_process_bank_operations_empty():
    """Тест с пустыми данными"""
    assert process_bank_operations([], ["test"]) == {}
    assert process_bank_operations([{"description": "test"}], []) == {}
