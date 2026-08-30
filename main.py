import json
import os
from typing import Any, Dict, List, Tuple

from src.processing import filter_by_state, get_date, mask_account_card, sort_by_date
from src.search import process_bank_search


def load_transactions_from_json(directory: str = "data") -> List[Dict[str, Any]]:
    """Загружает транзакции из JSON файлов в директории"""
    transactions: List[Dict[str, Any]] = []

    if not os.path.exists(directory):
        return transactions

    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    if isinstance(data, list):
                        transactions.extend(data)
                    elif isinstance(data, dict) and "transactions" in data:
                        transactions.extend(data["transactions"])
            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"Ошибка при загрузке {filename}: {e}")

    return transactions


def get_transaction_amount(transaction: Dict[str, Any]) -> Tuple[float, str]:
    """Извлекает сумму и валюту из транзакции"""
    amount = 0.0
    currency = ""

    # Проверяем вложенный словарь operationAmount
    if "operationAmount" in transaction:
        op_amount = transaction["operationAmount"]
        if isinstance(op_amount, dict):
            amount = op_amount.get("amount", 0)
            currency_obj = op_amount.get("currency", {})
            if isinstance(currency_obj, dict):
                currency = currency_obj.get("name", "")
                if not currency:
                    currency = currency_obj.get("code", "")

    # Если не нашли, проверяем корневые поля
    if not amount:
        amount = transaction.get("amount", 0)
    if not currency:
        currency = transaction.get("currency", "")
        if not currency:
            currency = transaction.get("currency_name", "")

    # Преобразуем сумму в число
    if isinstance(amount, str):
        try:
            amount = float(amount.replace(",", "."))
        except ValueError:
            amount = 0.0

    return amount, currency


def format_transaction(transaction: Dict[str, Any]) -> str:
    """Форматирует транзакцию для вывода"""
    date = transaction.get("date", "")
    description = transaction.get("description", "Без описания")

    amount, currency = get_transaction_amount(transaction)
    from_account = transaction.get("from", "")
    to_account = transaction.get("to", "")

    masked_from = mask_account_card(from_account)
    masked_to = mask_account_card(to_account)
    formatted_date = get_date(date)

    result = f"{formatted_date} {description}\n"
    result += f"{masked_from} -> {masked_to}\n"
    result += f"Сумма: {amount} {currency}\n"
    result += "-" * 50

    return result


def get_user_choice(prompt: str, options: List[str]) -> str:
    """Получает от пользователя выбор из списка опций"""
    while True:
        user_input = input(prompt).strip()
        if user_input.upper() in [opt.upper() for opt in options]:
            return user_input
        print(f"Некорректный ввод. Пожалуйста, выберите из: {', '.join(options)}")


def get_user_status() -> str:
    """Запрашивает у пользователя статус транзакций"""
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]

    while True:
        print("\nВведите статус, по которому необходимо выполнить фильтрацию.")
        print(f"Доступные для фильтровки статусы: {', '.join(valid_statuses)}")
        status = input().strip().upper()

        if status in [s.upper() for s in valid_statuses]:
            # Возвращаем в правильном регистре
            for valid in valid_statuses:
                if valid.upper() == status:
                    return valid
        else:
            print(f'Статус операции "{status}" недоступен.')


def filter_ruble_transactions(
    transactions: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Фильтрует только рублевые транзакции"""
    result: List[Dict[str, Any]] = []
    for tx in transactions:
        amount, currency = get_transaction_amount(tx)
        if currency and ("руб" in currency.lower() or "rub" in currency.lower()):
            result.append(tx)
    return result


def main() -> None:
    """Главная функция программы"""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")

    # 1. Выбор источника данных
    print("\nВыберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input().strip()
    if choice == "1":
        print("\nДля обработки выбран JSON-файл.")
        transactions: List[Dict[str, Any]] = load_transactions_from_json("data")
    else:
        print("Извините, поддержка CSV и XLSX пока не реализована.")
        print("Загружаем транзакции из JSON...")
        transactions = load_transactions_from_json("data")

    if not transactions:
        print("Не найдено ни одной транзакции.")
        return

    print(f"Загружено {len(transactions)} транзакций.")

    # 2. Фильтрация по статусу
    status = get_user_status()
    filtered_by_status = filter_by_state(transactions, status)
    print(f'Операции отфильтрованы по статусу "{status}"')

    if not filtered_by_status:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # 3. Сортировка по дате
    print("\nОтсортировать операции по дате? Да/Нет")
    sort_choice = get_user_choice("", ["да", "нет"])

    if sort_choice.lower() == "да":
        print("\nОтсортировать по возрастанию или по убыванию?")
        order = get_user_choice("", ["по возрастанию", "по убыванию"])
        reverse = order.lower() == "по убыванию"
        filtered_by_status = sort_by_date(filtered_by_status, reverse=reverse)
        print(f"Операции отсортированы по {order}.")

    # 4. Фильтр по рублевым транзакциям
    print("\nВыводить только рублевые транзакции? Да/Нет")
    ruble_choice = get_user_choice("", ["да", "нет"])

    if ruble_choice.lower() == "да":
        filtered_by_status = filter_ruble_transactions(filtered_by_status)
        print("Отфильтровано по рублевым транзакциям.")

    if not filtered_by_status:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # 5. Поиск по описанию
    print("\nОтфильтровать список транзакций по определенному слову в описании? Да/Нет")
    search_choice = get_user_choice("", ["да", "нет"])

    if search_choice.lower() == "да":
        search_word = input("Введите слово для поиска: ").strip()
        filtered_by_status = process_bank_search(filtered_by_status, search_word)
        print(f"Отфильтровано по слову '{search_word}'.")

        if not filtered_by_status:
            print(
                "Не найдено ни одной транзакции, подходящей под ваши условия фильтрации"
            )
            return

    # 6. Вывод результатов
    print("\nРаспечатываю итоговый список транзакций...")
    print(f"\nВсего банковских операций в выборке: {len(filtered_by_status)}\n")

    for tx in filtered_by_status:
        print(format_transaction(tx))
        print()


if __name__ == "__main__":
    main()
