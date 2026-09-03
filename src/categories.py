from collections import Counter
from typing import Any, Dict, List


def process_bank_operations(
    data: List[Dict[str, Any]], categories: List[str]
) -> Dict[str, int]:
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

    # Собираем все описания транзакций, пропуская None
    descriptions = []
    for tx in data:
        if tx and isinstance(tx, dict):  # Проверяем, что tx не None и является словарем
            descriptions.append(tx.get("description", ""))
        # Если tx is None или не словарь - пропускаем

    # Используем Counter для подсчета
    counter = Counter(descriptions)

    # Формируем результат только для указанных категорий
    result = {}
    for category in categories:
        result[category] = counter.get(category, 0)

    return result
