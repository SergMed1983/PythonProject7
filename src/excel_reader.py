# src/excel_reader.py
import os
from typing import Dict, List, Union

import pandas as pd


def read_excel(file_path: str) -> List[Dict[str, Union[str, float, int]]]:
    """
    Считывает финансовые операции из Excel-файла с помощью pandas.
    Корректно обрабатывает даты и другие типы данных.
    """
    transactions = []

    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден")
        return []

    try:
        # Читаем Excel-файл
        df = pd.read_excel(file_path)

        print(f"Найдено колонок: {list(df.columns)}")
        print(f"Найдено строк: {len(df)}")

        # Обрабатываем каждую колонку
        for col in df.columns:
            # Проверяем, является ли колонка датой
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                # Форматируем даты в строку ГГГГ-ММ-ДД
                df[col] = df[col].dt.strftime("%d.%m.%Y")
            elif df[col].dtype == "object":
                # Пробуем преобразовать строки в даты
                try:
                    # Проверяем, похожи ли значения на даты
                    sample = (
                        df[col].dropna().iloc[0] if len(df[col].dropna()) > 0 else None
                    )
                    if sample and isinstance(sample, str):
                        # Пробуем распарсить как дату
                        df[col] = pd.to_datetime(df[col], errors="coerce")
                        if pd.api.types.is_datetime64_any_dtype(df[col]):
                            df[col] = df[col].dt.strftime("%d.%m.%Y")
                except Exception:
                    pass

        # Заменяем NaN на None для корректного вывода
        df = df.where(pd.notnull(df), None)

        # Преобразуем DataFrame в список словарей
        transactions = df.to_dict("records")

        print(f"Успешно прочитано {len(transactions)} транзакций")

    except Exception as e:
        print(f"Ошибка при чтении Excel-файла: {e}")
        import traceback

        traceback.print_exc()

    return transactions
