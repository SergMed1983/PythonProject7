"""
Модуль для работы с финансовыми транзакциями из различных форматов файлов.
"""

from typing import Any, Dict, List

import pandas as pd


def read_transactions_from_csv(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из CSV-файла.

    Args:
        file_path (str): Путь к CSV-файлу

    Returns:
        List[Dict[str, Any]]: Список словарей с транзакциями

    Raises:
        FileNotFoundError: Если файл не найден
        pd.errors.EmptyDataError: Если файл пустой

    Example:
        >>> transactions = read_transactions_from_csv('data/transactions.csv')
        >>> len(transactions) > 0
        True
    """
    try:
        df = pd.read_csv(
            file_path,
            sep=";",  # или ',' — смотрите по вашему CSV
            encoding="utf-8",  # или 'cp1251'
            decimal=",",  # если числа с запятой
            dayfirst=True,  # для парсинга дат как ДД.ММ.ГГГГ
        )

        # Форматируем даты
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].dt.strftime("%d.%m.%Y")

        # Преобразуем DataFrame в список словарей
        transactions = df.to_dict("records")
        return transactions
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {file_path} не найден")
    except pd.errors.EmptyDataError:
        raise pd.errors.EmptyDataError(f"Файл {file_path} пустой")


def read_transactions_from_excel(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из Excel-файла.

    Args:
        file_path (str): Путь к Excel-файлу (.xlsx или .xls)

    Returns:
        List[Dict[str, Any]]: Список словарей с транзакциями

    Raises:
        FileNotFoundError: Если файл не найден
        pd.errors.EmptyDataError: Если файл пустой
        ValueError: Если файл имеет неподдерживаемый формат

    Example:
        >>> transactions = read_transactions_from_excel('data/transactions_excel.xlsx')
        >>> len(transactions) > 0
        True
    """
    try:
        df = pd.read_excel(file_path)

        # Форматируем даты
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].dt.strftime("%d.%m.%Y")

        # Преобразуем DataFrame в список словарей
        transactions = df.to_dict("records")
        return transactions
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {file_path} не найден")
    except pd.errors.EmptyDataError:
        raise pd.errors.EmptyDataError(f"Файл {file_path} пустой")
    except Exception as e:
        raise ValueError(f"Ошибка при чтении Excel-файла: {e}")
