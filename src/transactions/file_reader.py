import csv
import json
import os
from typing import Any, Dict, List, Union

import pandas as pd


def read_csv(file_path: str) -> List[Dict[str, Union[str, float]]]:
    """
    Считывает финансовые операции из CSV-файла и возвращает список словарей.
    """
    transactions: List[Dict[str, Union[str, float]]] = []

    if not os.path.exists(file_path):
        return []

    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                row["amount"] = float(row["amount"])
            except (ValueError, TypeError, KeyError):
                pass
            transactions.append(row)

    return transactions


def read_csv_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Алиас для read_csv. Считывает финансовые операции из CSV-файла.
    """
    return read_csv(file_path)


def read_excel(file_path: str) -> List[Dict[str, Union[str, float]]]:
    """
    Считывает финансовые операции из Excel-файла и возвращает список словарей.
    """
    if not os.path.exists(file_path):
        return []

    df = pd.read_excel(file_path)
    df = df.where(pd.notnull(df), None)
    transactions = df.to_dict(orient="records")

    for transaction in transactions:
        if "amount" in transaction and transaction["amount"] is not None:
            transaction["amount"] = float(transaction["amount"])

    return transactions


def read_json_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из JSON-файла и возвращает список словарей.
    """
    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            elif isinstance(data, dict) and "transactions" in data:
                return data["transactions"]
    except json.JSONDecodeError as e:
        print(f"Ошибка парсинга JSON: {e}")
        return []
    except Exception as e:
        print(f"Ошибка чтения JSON: {e}")
        return []

    return []
