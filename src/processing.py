"""
Модуль с функциями для обработки банковских транзакций.
Содержит функции для фильтрации, сортировки, поиска и подсчета.
"""

import re
from collections import Counter
from typing import Any, Dict, List

# ============ ФУНКЦИИ ИЗ ДЗ 13.1 ============


def filter_by_state(list_dict: list, state: str = "EXECUTED") -> list:
    """
    Фильтрует список словарей по значению ключа 'state'.

    Аргументы:
        list_dict: Список словарей для фильтрации
        state: Значение state для фильтрации (по умолчанию 'EXECUTED')

    Возвращает:
        Отфильтрованный список словарей

    Пример:
        >>> data = [{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "CANCELED"}]
        >>> filter_by_state(data, "EXECUTED")
        [{"id": 1, "state": "EXECUTED"}]
    """
    return [item for item in list_dict if item.get("state") == state]


def sort_by_date(list_dict: list, ascending: bool = True) -> list:
    """
    Сортирует список словарей по ключу 'date'.

    Аргументы:
        list_dict: Список словарей для сортировки
        ascending: Если True - по возрастанию, False - по убыванию

    Возвращает:
        Отсортированный список словарей

    Пример:
        >>> data = [{"date": "2023-01-02"}, {"date": "2023-01-01"}]
        >>> sort_by_date(data, ascending=True)
        [{"date": "2023-01-01"}, {"date": "2023-01-02"}]
    """
    return sorted(list_dict, key=lambda x: x.get("date", ""), reverse=not ascending)


# ============ НОВЫЕ ФУНКЦИИ ДЛЯ ДЗ 13.2 ============

def search_transactions_by_description(
    transactions: List[Dict[str, Any]], search_string: str
) -> List[Dict[str, Any]]:
    """
    Ищет транзакции, в описании которых содержится искомая строка.

    Функция использует библиотеку re для регистронезависимого поиска подстроки
    в поле 'description' каждой транзакции.

    Аргументы:
        transactions (List[Dict[str, Any]]): Список словарей с данными о транзакциях.
        search_string (str): Строка для поиска в описании.

    Возвращает:
        List[Dict[str, Any]]: Список транзакций, у которых в описании есть искомая строка.

    Пример:
        >>> data = [{"description": "Перевод организации"}, {"description": "Оплата услуг"}]
        >>> search_transactions_by_description(data, "организации")
        [{"description": "Перевод организации"}]
    """
    if not search_string:
        return transactions

    # Используем re для регистронезависимого поиска
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)
    return [tx for tx in transactions if pattern.search(tx.get("description", ""))]


def count_transactions_by_categories(
    transactions: List[Dict[str, Any]], categories: List[str]
) -> Dict[str, int]:
    """
    Подсчитывает количество транзакций по заданным категориям.

    Функция использует Counter из библиотеки collections.

    Аргументы:
        transactions (List[Dict[str, Any]]): Список словарей с данными о транзакциях.
        categories (List[str]): Список категорий для подсчета.

    Возвращает:
        Dict[str, int]: Словарь с количеством транзакций по каждой категории.

    Пример:
        >>> data = [{"description": "Оплата еды"}, {"description": "Транспорт"}]
        >>> count_transactions_by_categories(data, ["еда", "транспорт"])
        {'еда': 1, 'транспорт': 1}
    """
    # Инициализируем счетчик
    counter = Counter()

    # Устанавливаем начальные значения для всех категорий
    for category in categories:
        counter[category] = 0

    # Подсчитываем транзакции по категориям (регистронезависимо)
    for transaction in transactions:
        description = transaction.get("description", "").lower()
        for category in categories:
            if category.lower() in description:
                counter[category] += 1

    return dict(counter)
