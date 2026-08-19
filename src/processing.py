def filter_by_state(list_dict: list, state: str = "EXECUTED") -> list:
    """
    Фильтрует список словарей по значению ключа 'state'.

    Аргументы:
        list_dict: Список словарей для фильтрации
        state: Значение state для фильтрации (по умолчанию 'EXECUTED')

    Возвращает:
        Отфильтрованный список словарей
    """
    return [item for item in list_dict if item.get("state") == state]


def sort_by_date(list_dict: list, ascending: bool = True) -> list:
    """
    Сортирует список словарей по ключу 'date'.

    Аргументы:
        list_dict: Список словарей для сортировки
        ascending: Если True - по возрастанию, False - по убыванию

    Возвращает:
        Отсортированный список словарей
    """
    return sorted(list_dict, key=lambda x: x.get("date", ""), reverse=not ascending)
