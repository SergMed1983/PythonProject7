import pytest
from src.processing import (
    count_transactions_by_categories,
    filter_by_state,
    search_transactions_by_description,
    sort_by_date,
    read_csv_transactions,
    read_json_transactions,
)

# ============ ТЕСТЫ ДЛЯ ФУНКЦИЙ ИЗ ДЗ 13.1 ==================

def test_filter_by_state():
    """Тест: фильтрация по статусу."""
    data = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"},
        {"id": 3, "state": "EXECUTED"},
        {"id": 4, "state": "PENDING"},
    ]
    result = filter_by_state(data, state="EXECUTED")
    assert len(result) == 2
    for item in result:
        assert item["state"] == "EXECUTED"

def test_filter_by_state_default():
    """Тест: фильтрация со значением по умолчанию."""
    data = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"},
        {"id": 3, "state": "EXECUTED"},
    ]
    result = filter_by_state(data)
    assert len(result) == 2
    for item in result:
        assert item["state"] == "EXECUTED"

def test_sort_by_date():
    """Тест: сортировка по дате."""
    data = [
        {"id": 1, "date": "2023-01-15"},
        {"id": 2, "date": "2023-02-20"},
        {"id": 3, "date": "2023-01-01"},
    ]
    result = sort_by_date(data, ascending=False)
    assert result[0]["date"] == "2023-02-20"
    assert result[1]["date"] == "2023-01-15"
    assert result[2]["date"] == "2023-01-01"

def test_search_transactions_by_description():
    """Тест: поиск по описанию."""
    data = [
        {"description": "Перевод на карту"},
        {"description": "Оплата покупки"},
        {"description": "Перевод другу"},
    ]
    result = search_transactions_by_description(data, "Перевод")
    assert len(result) == 2
    for item in result:
        assert "перевод" in item["description"].lower()

def test_count_transactions_by_categories():
    """Тест: подсчет транзакций по категориям."""
    data = [
        {"description": "Оплата еды", "category": "Еда"},
        {"description": "Транспорт", "category": "Транспорт"},
        {"description": "Еда в кафе", "category": "Еда"},
        {"description": "Развлечения", "category": "Развлечения"},
    ]
    categories = ["Еда", "Транспорт"]
    result = count_transactions_by_categories(data, categories)
    assert result["Еда"] == 2
    assert result["Транспорт"] == 1

# ============ ТЕСТЫ ДЛЯ ЧТЕНИЯ ФАЙЛОВ ==================

def test_read_csv_transactions():
    """Тест: чтение CSV файла."""
    # Измени путь с "../данные/transactions.csv" на "данные/transactions.csv"
    transactions = read_csv_transactions("данные/transactions.csv")
    assert len(transactions) > 0
    assert "id" in transactions[0]
    assert "description" in transactions[0]
    assert "category" in transactions[0]

def test_read_json_transactions():
    """Тест: чтение JSON файла."""
    # Измени путь с "../данные/transactions.json" на "данные/transactions.json"
    transactions = read_json_transactions("данные/transactions.json")
    assert len(transactions) > 0
    assert "id" in transactions[0]
    assert "description" in transactions[0]
    assert "category" in transactions[0]
