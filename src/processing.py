"""
Модуль с функциями для обработки банковских транзакций.
Содержит функции для фильтрации, сортировки, поиска и подсчета.
"""

import csv
import json
import re
from collections import Counter
from typing import Any, Dict, List

# ============ ФУНКЦИИ ИЗ ДЗ 13.1 ============

def filter_by_state(list_dict: list, state: str = "EXECUTED") -> list:
    """
    Фильтрует список словарей по значению ключа 'state'.
    """
    return [item for item in list_dict if item.get("state") == state]


def sort_by_date(list_dict: list, ascending: bool = True) -> list:
    """
    Сортирует список словарей по ключу 'date'.
    """
    return sorted(list_dict, key=lambda x: x.get("date", ""), reverse=not ascending)


# ============ НОВЫЕ ФУНКЦИИ ДЛЯ ДЗ 13.2 ============

def search_transactions_by_description(
    transactions: List[Dict[str, Any]], search_string: str
) -> List[Dict[str, Any]]:
    """
    Ищет транзакции, в описании которых содержится искомая строка.
    """
    if not search_string:
        return transactions

    pattern = re.compile(re.escape(search_string), re.IGNORECASE)
    return [tx for tx in transactions if pattern.search(tx.get("description", ""))]


def count_transactions_by_categories(
    transactions: List[Dict[str, Any]], categories: List[str]
) -> Dict[str, int]:
    """
    Подсчитывает количество транзакций по заданным категориям.
    Использует поле 'category' для подсчета.
    """
    counter: Counter = Counter()

    for category in categories:
        counter[category] = 0

    for transaction in transactions:
        transaction_category = transaction.get("category", "").lower()
        for category in categories:
            if transaction_category == category.lower():
                counter[category] += 1
                break

    return dict(counter)


def read_csv_transactions(filename: str) -> List[Dict[str, Any]]:
    """Чтение транзакций из CSV файла."""
    transactions = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                cleaned_row = {key.strip(): value.strip() for key, value in row.items()}
                transactions.append(cleaned_row)
        return transactions
    except FileNotFoundError:
        print(f"Ошибка: Файл {filename} не найден")
        return []
    except Exception as e:
        print(f"Ошибка при чтении CSV файла: {e}")
        return []


def read_json_transactions(filename: str) -> List[Dict[str, Any]]:
    """Чтение транзакций из JSON файла."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            elif isinstance(data, dict) and 'transactions' in data:
                return data['transactions']
            else:
                print(f"Ошибка: Неверный формат JSON в файле {filename}")
                return []
    except FileNotFoundError:
        print(f"Ошибка: Файл {filename} не найден")
        return []
    except json.JSONDecodeError as e:
        print(f"Ошибка при чтении JSON файла: {e}")
        return []
    except Exception as e:
        print(f"Неизвестная ошибка при чтении JSON файла: {e}")
        return []
