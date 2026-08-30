import re
from typing import List, Dict, Any


def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """
    Ищет транзакции по описанию с использованием регулярных выражений.

    Args:
        data: Список словарей с транзакциями
        search: Строка для поиска в описании

    Returns:
        List[Dict]: Список транзакций, где в описании есть искомая строка
    """
    if not data or not search:
        return []

    # Создаем паттерн для поиска (игнорируем регистр)
    pattern = re.compile(re.escape(search), re.IGNORECASE)

    result = []
    for transaction in data:
        description = transaction.get('description', '')
        if pattern.search(description):
            result.append(transaction)

    return result
