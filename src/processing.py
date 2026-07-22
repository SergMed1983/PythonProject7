from typing import List, Dict, Any

def filter_by_state(operations: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Фильтрует список операций по значению ключа 'state'.

    :param operations: Список словарей с данными о банковских операциях.
    :param state: Значение для фильтрации по ключу 'state' (по умолчанию 'EXECUTED').
    :return: Список словарей, у которых ключ 'state' совпадает с переданным значением.
    """
    return [op for op in operations if op.get("state") == state]


def sort_by_date(operations: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует список операций по дате в поле 'date'.

    :param operations: Список словарей с данными о банковских операциях.
    :param reverse: Порядок сортировки (True — по убыванию, False — по возрастанию).
    :return: Новый список, отсортированный по дате.
    """
    # Даты в формате ISO 8601 корректно сортируются лексикографически как строки
    return sorted(operations, key=lambda x: x.get("date"), reverse=reverse)
