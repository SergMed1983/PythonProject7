from collections import Counter
from typing import List, Dict, Any


def process_bank_operations(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество операций по категориям.

    Args:
        data: Список словарей с транзакциями
        categories: Список категорий для подсчета

    Returns:
        Dict[str, int]: Словарь {категория: количество}
    """
    if not data or not categories:
        return {}

    # Собираем все описания транзакций
    descriptions = [tx.get('description', '') for tx in data]

    # Используем Counter для подсчета
    counter = Counter(descriptions)

    # Формируем результат только для указанных категорий
    result = {}
    for category in categories:
        result[category] = counter.get(category, 0)

    return result
