import csv
import os
from typing import Dict, List, Union

import pandas as pd


def read_csv(file_path: str) -> List[Dict[str, Union[str, float]]]:
    """
    Считывает финансовые операции из CSV-файла и возвращает список словарей.
    """
    transactions: List[Dict[str, Union[str, float]]] = []

    # Проверяем существование файла (можно добавить try/except по желанию)
    if not os.path.exists(file_path):
        return []

    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Приводим числовые поля к float для единообразия (по аналогии с JSON)
            # Если поле 'amount' не число, оставляем строкой или обрабатываем ошибку
            try:
                row["amount"] = float(row["amount"])
            except (ValueError, TypeError, KeyError):
                pass
            transactions.append(row)

    return transactions


def read_excel(file_path: str) -> List[Dict[str, Union[str, float]]]:
    """
    Считывает финансовые операции из Excel-файла и возвращает список словарей.
    """
    if not os.path.exists(file_path):
        return []

    # Читаем Excel в DataFrame
    df = pd.read_excel(file_path)

    # Заменяем NaN на None или пустые строки, чтобы это корректно сериализовалось
    df = df.where(pd.notnull(df), None)

    # Преобразуем DataFrame в список словарей
    transactions = df.to_dict(orient="records")

    # Приводим суммы к float, если они есть
    for transaction in transactions:
        if "amount" in transaction and transaction["amount"] is not None:
            transaction["amount"] = float(transaction["amount"])

    return transactions
