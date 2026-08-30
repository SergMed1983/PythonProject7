from datetime import datetime
from typing import Dict, List


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
        # Если ни один формат не подошел, возвращаем исходную строку
        return date_string
    except Exception:
        return date_string


def filter_by_state(transactions: List[Dict], state: str = "EXECUTED") -> List[Dict]:
    """Фильтрует транзакции по состоянию"""
    return [tx for tx in transactions if tx.get("state", "").upper() == state.upper()]


def sort_by_date(transactions: List[Dict], reverse: bool = True) -> List[Dict]:
    """Сортирует транзакции по дате"""

    def get_date_key(tx):
        date = tx.get("date", "")
        return date[:10] if date else ""

    return sorted(transactions, key=get_date_key, reverse=reverse)
