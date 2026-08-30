from datetime import datetime
from typing import Any, Dict, List, Tuple


def get_transaction_amount(transaction: Dict[str, Any]) -> Tuple[float, str]:
    """
    Извлекает сумму и валюту из транзакции.
    Поддерживает JSON (operationAmount) и CSV/XLSX (прямые поля).
    """
    amount = 0.0
    currency = ""

    # 1. Для JSON: данные внутри operationAmount
    if "operationAmount" in transaction:
        op_amount = transaction["operationAmount"]
        if isinstance(op_amount, dict):
            amount = op_amount.get("amount", 0)
            currency_obj = op_amount.get("currency", {})
            if isinstance(currency_obj, dict):
                currency = currency_obj.get("name", "")
                if not currency:
                    currency = currency_obj.get("code", "")

    # 2. Если не нашли — проверяем корневые поля (CSV/XLSX)
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


def mask_account_card(account_info: str) -> str:
    """Маскирует номер счета или карты"""
    if not account_info:
        return "Неизвестно"

    parts = account_info.split()
    if len(parts) < 2:
        return account_info

    name = " ".join(parts[:-1])
    number = parts[-1]

    if not number.isdigit():
        return account_info

    if len(number) == 16:  # Карта
        masked_number = f"{number[:4]} {number[4:6]}** **** {number[-4:]}"
        return f"{name} {masked_number}"
    elif len(number) == 20:  # Счет
        masked_number = f"**{number[-4:]}"
        return f"{name} {masked_number}"
    else:
        return account_info


def get_date(date_string: str) -> str:
    """Преобразует дату в формат ДД.ММ.ГГГГ"""
    if not date_string:
        return ""

    try:
        for fmt in ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f"]:
            try:
                date_obj = datetime.strptime(date_string, fmt)
                return date_obj.strftime("%d.%m.%Y")
            except ValueError:
                continue
        return date_string
    except Exception:
        return date_string


def filter_by_state(
    transactions: List[Dict[str, Any]], state: str = "EXECUTED"
) -> List[Dict[str, Any]]:
    """Фильтрует транзакции по состоянию"""
    return [tx for tx in transactions if tx.get("state", "").upper() == state.upper()]


def sort_by_date(
    transactions: List[Dict[str, Any]], reverse: bool = True
) -> List[Dict[str, Any]]:
    """Сортирует транзакции по дате"""

    def get_date_key(tx: Dict[str, Any]) -> str:
        date = tx.get("date", "")
        return date[:10] if date else ""

    return sorted(transactions, key=get_date_key, reverse=reverse)
