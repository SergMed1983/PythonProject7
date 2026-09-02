"""
Главный модуль приложения.
Содержит функционал для работы с банковскими
транзакциями и другие утилиты.
"""

import os
from typing import Any, Dict, List

import pandas as pd

from src.processing import filter_by_state, sort_by_date


def test_function() -> None:
    """Тестовая функция для проверки декоратора."""
    print("Тестовая функция")


def run_text_reverser() -> None:
    """Запускает функционал реверса текста."""
    from src.text_utils import reverse_text

    text = input("Введите любой текст для реверса: ")
    print(reverse_text(text))


def load_transactions_from_json(filepath: str) -> List[Dict[str, Any]]:
    """Загружает транзакции из JSON-файла."""
    from src.transactions.file_reader import read_json_transactions

    transactions = read_json_transactions(filepath)
    if not transactions:
        print(f"Файл {filepath} не найден или пуст.")
    return transactions


def load_transactions_from_csv(filepath: str) -> List[Dict[str, Any]]:
    """Загружает транзакции из CSV-файла."""
    from src.transactions.file_reader import read_csv_transactions

    transactions = read_csv_transactions(filepath)
    if not transactions:
        print(f"Файл {filepath} не найден или пуст.")
    return transactions


def load_transactions_from_xlsx(filepath: str) -> List[Dict[str, Any]]:
    """
    Загружает транзакции из XLSX-файла с помощью pandas.
    Корректно обрабатывает даты.
    """
    transactions: List[Dict[str, Any]] = []

    if not os.path.exists(filepath):
        print(f"Файл {filepath} не найден")
        return []

    try:
        df = pd.read_excel(filepath)

        print(f"Найдено колонок: {list(df.columns)}")
        print(f"Найдено строк: {len(df)}")

        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].dt.strftime("%Y-%m-%d")
            elif df[col].dtype == "object":
                try:
                    sample = (
                        df[col].dropna().iloc[0] if len(df[col].dropna()) > 0 else None
                    )
                    if sample and isinstance(sample, str):
                        df[col] = pd.to_datetime(df[col], errors="coerce")
                        if pd.api.types.is_datetime64_any_dtype(df[col]):
                            df[col] = df[col].dt.strftime("%Y-%m-%d")
                except Exception:
                    pass

        df = df.where(pd.notnull(df), None)
        transactions = df.to_dict("records")

        print(f"Успешно прочитано {len(transactions)} транзакций из XLSX")

    except ImportError:
        print(
            "Библиотека pandas не установлена. "
            "Установите: pip install pandas openpyxl"
        )
        return []
    except Exception as e:
        print(f"Ошибка загрузки XLSX: {e}")
        import traceback

        traceback.print_exc()
        return []

    return transactions


def generate_test_transactions() -> List[Dict[str, Any]]:
    """Генерирует тестовый набор транзакций для демонстрации."""
    return [
        {
            "id": 1,
            "date": "2019-12-08",
            "description": "Открытие вклада",
            "amount": 40542,
            "currency": "руб.",
            "state": "EXECUTED",
        },
        {
            "id": 2,
            "date": "2019-11-12",
            "description": "Перевод с карты на карту",
            "amount": 130,
            "currency": "USD",
            "state": "EXECUTED",
        },
        {
            "id": 3,
            "date": "2018-07-18",
            "description": "Перевод организации",
            "amount": 8390,
            "currency": "руб.",
            "state": "CANCELED",
        },
        {
            "id": 4,
            "date": "2018-06-03",
            "description": "Перевод со счета на счет",
            "amount": 8200,
            "currency": "EUR",
            "state": "PENDING",
        },
        {
            "id": 5,
            "date": "2020-01-01",
            "description": "Оплата интернета",
            "amount": 500,
            "currency": "руб.",
            "state": "EXECUTED",
        },
    ]


def filter_ruble_transactions(
    transactions: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Оставляет только рублевые транзакции."""
    return [tx for tx in transactions if tx.get("currency", "").lower() == "руб."]


def print_transactions(transactions: List[Dict[str, Any]]) -> None:
    """Красиво выводит список транзакций с маскировкой."""
    from src.processing import get_transaction_amount, mask_account_card

    if not transactions:
        print(
            "\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации"
        )
        return

    print(f"\nВсего банковских операций в выборке: {len(transactions)}")
    print("-" * 60)

    for tx in transactions:
        date = tx.get("date", "Дата не указана")
        if date and isinstance(date, str):
            date = date.split("T")[0].split(" ")[0]

        description = tx.get("description", "Без описания")
        amount, currency = get_transaction_amount(tx)

        from_account = tx.get("from", "")
        to_account = tx.get("to", "")

        if from_account:
            from_account = mask_account_card(from_account)
        if to_account:
            to_account = mask_account_card(to_account)

        print(f"{date} {description}")
        if from_account and to_account:
            print(f"{from_account} -> {to_account}")
        elif from_account:
            print(f"{from_account}")
        elif to_account:
            print(f"На {to_account}")
        print(f"Сумма: {amount} {currency}")
        print("-" * 60)


def run_bank_processor() -> None:
    """Запускает основной функционал программы для работы с банковскими транзакциями."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("\nВаш выбор: ").strip()
    transactions: List[Dict[str, Any]] = []

    if choice == "1":
        print("Для обработки выбран JSON-файл.")
        filepath = input(
            "Введите путь к JSON-файлу (или нажмите Enter для тестовых данных): "
        ).strip()
        if filepath:
            transactions = load_transactions_from_json(filepath)
        if not transactions:
            print("Файл не найден или пуст. Загружаю тестовые данные.")
            transactions = generate_test_transactions()
    elif choice == "2":
        print("Для обработки выбран CSV-файл.")
        filepath = input(
            "Введите путь к CSV-файлу (или нажмите Enter для тестовых данных): "
        ).strip()
        if filepath:
            transactions = load_transactions_from_csv(filepath)
        if not transactions:
            print("Файл не найден или пуст. Загружаю тестовые данные.")
            transactions = generate_test_transactions()
    elif choice == "3":
        print("Для обработки выбран XLSX-файл.")
        filepath = input(
            "Введите путь к XLSX-файлу (или нажмите Enter для data/transactions.xlsx): "
        ).strip()
        if not filepath:
            filepath = "data/transactions.xlsx"
        transactions = load_transactions_from_xlsx(filepath)
        if not transactions:
            print("Файл не найден или пуст. Загружаю тестовые данные.")
            transactions = generate_test_transactions()
    else:
        print("Неверный выбор. Загружаю тестовые данные.")
        transactions = generate_test_transactions()

    if not transactions:
        print("Не удалось загрузить транзакции.")
        return

    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        status_input = (
            input(
                "\nВведите статус, по которому необходимо выполнить фильтрацию.\n"
                "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n"
                "Ваш статус: "
            )
            .strip()
            .upper()
        )
        if status_input in valid_statuses:
            transactions = filter_by_state(transactions, status_input)
            print(f'Операции отфильтрованы по статусу "{status_input}"')
            break
        else:
            print(f'Статус операции "{status_input}" недоступен.')

    if not transactions:
        print("Не найдено ни одной транзакции с таким статусом.")
        return

    sort_choice = input("\nОтсортировать операции по дате? Да/Нет: ").strip().lower()
    if sort_choice in ["да", "yes", "y", "д"]:
        order = input("Отсортировать по возрастанию или по убыванию? ").strip().lower()
        ascending = order in ["по возрастанию", "возрастанию", "asc", "возраст"]
        transactions = sort_by_date(transactions, ascending)

    ruble_choice = (
        input("\nВыводить только рублевые транзакции? Да/Нет: ").strip().lower()
    )
    if ruble_choice in ["да", "yes", "y", "д"]:
        transactions = filter_ruble_transactions(transactions)

    if not transactions:
        print(
            "Не найдено ни одной транзакции, " "подходящей под ваши условия фильтрации"
        )
        return

    search_choice = (
        input(
            "\nОтфильтровать список транзакций по определенному слову в описании? Да/Нет: "
        )
        .strip()
        .lower()
    )
    if search_choice in ["да", "yes", "y", "д"]:
        search_word = input("Введите слово для поиска: ").strip()
        if search_word:
            from src.search import process_bank_search

            transactions = process_bank_search(transactions, search_word)

    print("\nРаспечатываю итоговый список транзакций...")
    print_transactions(transactions)


def main() -> None:
    """Основная функция программы."""
    print("Добро пожаловать в программу!")
    print("Выберите режим работы:")
    print("1. Работа с банковскими транзакциями")
    print("2. Реверс текста (тестовый режим)")

    mode = input("\nВаш выбор: ").strip()

    if mode == "1":
        run_bank_processor()
    elif mode == "2":
        test_function()
        run_text_reverser()
    else:
        print("Неверный выбор. Запускаю режим работы с банковскими транзакциями.")
        run_bank_processor()


if __name__ == "__main__":
    main()
