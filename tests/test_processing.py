"""
Модуль с тестами для функций обработки транзакций.
"""

import pytest

from src.processing import (
    count_transactions_by_categories,
    filter_by_state,
    search_transactions_by_description,
    sort_by_date,
)

# ============ ТЕСТЫ ДЛЯ ФУНКЦИЙ ИЗ ДЗ 13.1 ============


def test_filter_by_state():
    """Тест: фильтрация по статусу."""
    data = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"},
        {"id": 3, "state": "EXECUTED"},
        {"id": 4, "state": "PENDING"},
    ]
    result = filter_by_state(data, "EXECUTED")
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
    result = filter_by_state(data)  # По умолчанию "EXECUTED"
    assert len(result) == 2


def test_filter_by_state_custom():
    """Тест: фильтрация с пользовательским состоянием."""
    data = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"},
    ]
    result = filter_by_state(data, "CANCELED")
    assert len(result) == 1
    assert result[0]["state"] == "CANCELED"


def test_sort_by_date_ascending():
    """Тест: сортировка по дате по возрастанию."""
    data = [
        {"id": 1, "date": "2019-12-08"},
        {"id": 2, "date": "2018-07-18"},
        {"id": 3, "date": "2020-01-01"},
    ]
    result = sort_by_date(data, ascending=True)
    expected_dates = ["2018-07-18", "2019-12-08", "2020-01-01"]
    result_dates = [item["date"] for item in result]
    assert result_dates == expected_dates


def test_sort_by_date_descending():
    """Тест: сортировка по дате по убыванию."""
    data = [
        {"id": 1, "date": "2019-12-08"},
        {"id": 2, "date": "2018-07-18"},
        {"id": 3, "date": "2020-01-01"},
    ]
    result = sort_by_date(data, ascending=False)
    expected_dates = ["2020-01-01", "2019-12-08", "2018-07-18"]
    result_dates = [item["date"] for item in result]
    assert result_dates == expected_dates


# ============ НОВЫЕ ТЕСТЫ ДЛЯ ДЗ 13.2 ============

@pytest.fixture
def sample_transactions():
    """Фикстура с тестовыми данными для новых функций."""
    return [
        {"description": "Перевод организации", "amount": 100, "state": "EXECUTED"},
        {"description": "Оплата интернета", "amount": 500, "state": "CANCELED"},
        {"description": "Перевод с карты на карту", "amount": 130, "state": "EXECUTED"},
        {"description": "Открытие вклада", "amount": 40542, "state": "PENDING"},
        {"description": "Пополнение счета", "amount": 2000, "state": "EXECUTED"},
    ]


def test_search_transactions_by_description_found(sample_transactions):
    """Тест: поиск по существующей подстроке."""
    result = search_transactions_by_description(sample_transactions, "перевод")
    assert len(result) == 2
    assert "Перевод организации" in [tx["description"] for tx in result]
    assert "Перевод с карты на карту" in [tx["description"] for tx in result]


def test_search_transactions_by_description_not_found(sample_transactions):
    """Тест: поиск по отсутствующей подстроке."""
    result = search_transactions_by_description(sample_transactions, "покупка")
    assert len(result) == 0


def test_search_transactions_by_description_empty_string(sample_transactions):
    """Тест: пустая строка поиска возвращает все транзакции."""
    result = search_transactions_by_description(sample_transactions, "")
    assert len(result) == len(sample_transactions)


def test_search_transactions_by_description_case_insensitive(sample_transactions):
    """Тест: регистронезависимый поиск."""
    result = search_transactions_by_description(sample_transactions, "Организации")
    assert len(result) == 1
    assert result[0]["description"] == "Перевод организации"


def test_search_transactions_by_description_empty_transactions():
    """Тест: пустой список транзакций."""
    result = search_transactions_by_description([], "поиск")
    assert len(result) == 0


def test_count_transactions_by_categories(sample_transactions):
    """Тест: подсчет транзакций по категориям."""
    categories = ["перевод", "интернет", "вклад", "пополнение"]
    result = count_transactions_by_categories(sample_transactions, categories)
    expected = {"перевод": 2, "интернет": 1, "вклад": 1, "пополнение": 1}
    assert result == expected


def test_count_transactions_by_categories_empty_categories(sample_transactions):
    """Тест: пустой список категорий."""
    result = count_transactions_by_categories(sample_transactions, [])
    assert result == {}


def test_count_transactions_by_categories_no_matches(sample_transactions):
    """Тест: категории, которых нет в транзакциях."""
    categories = ["кредит", "ипотека"]
    result = count_transactions_by_categories(sample_transactions, categories)
    expected = {"кредит": 0, "ипотека": 0}
    assert result == expected


def test_count_transactions_by_categories_case_insensitive(sample_transactions):
    """Тест: регистронезависимый подсчет категорий."""
    categories = ["ПЕРЕВОД", "ИНТЕРНЕТ"]
    result = count_transactions_by_categories(sample_transactions, categories)
    expected = {"ПЕРЕВОД": 2, "ИНТЕРНЕТ": 1}
    assert result == expected


def test_count_transactions_by_categories_empty_transactions():
    """Тест: подсчет по категориям для пустого списка транзакций."""
    categories = ["перевод", "интернет"]
    result = count_transactions_by_categories([], categories)
    expected = {"перевод": 0, "интернет": 0}
    assert result == expected
