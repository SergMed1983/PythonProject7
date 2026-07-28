from typing import Any, Dict, List


def filter_by_state(
    operations: List[Dict[str, Any]], state: str = "EXECUTED"
) -> List[Dict[str, Any]]:
    """
    Фильтрует список операций по статусу.

    Возвращает новый список, содержащий только операции с указанным значением
    ключа 'state'. По умолчанию фильтрует по статусу 'EXECUTED'.

    :param operations: Список словарей с данными об операциях.
    :param state: Значение статуса для фильтрации (по умолчанию 'EXECUTED').
    :return: Отфильтрованный список операций.
    """
    return [op for op in operations if op.get("state") == state]


def sort_by_date(
    operations: List[Dict[str, Any]], reverse: bool = True
) -> List[Dict[str, Any]]:
    """
    Сортирует список операций по дате.

    Возвращает новый список, отсортированный по значению ключа 'date'.
    По умолчанию сортирует в порядке убывания (сначала самые свежие операции).

    :param operations: Список словарей с данными об операциях.
    :param reverse: Флаг порядка сортировки:
                    True — по убыванию (новые сначала),
                    False — по возрастанию (старые сначала).
    :return: Отсортированный список операций.
    """

    def _get_date_key(op: Dict[str, Any]) -> str:
        return op.get("date", "")

    return sorted(operations, key=_get_date_key, reverse=reverse)
