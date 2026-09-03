from src.categories import process_bank_operations
from src.processing import filter_by_state, get_date, mask_account_card, sort_by_date
from src.search import process_bank_search

# ============ ТЕСТЫ ДЛЯ ФИЛЬТРАЦИИ ==================


def test_filter_by_state():
    """Тест: фильтрация по статусу."""
    data = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"},
        {"id": 3, "state": "EXECUTED"},
        {"id": 4, "state": "PENDING"},
    ]
    result = filter_by_state(data, state="EXECUTED")
    assert len(result) == 2
    for item in result:
        assert item["state"] == "EXECUTED"


def test_filter_by_state_default():
    """Тест: фильтрация со значением по умолчанию."""
    data = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"},
        {"id": 3, "state": "EXECUTED"},
    ]
    result = filter_by_state(data)
    assert len(result) == 2
    for item in result:
        assert item["state"] == "EXECUTED"


def test_filter_by_state_case_insensitive():
    """Тест: регистронезависимая фильтрация."""
    data = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"},
        {"id": 3, "state": "executed"},
    ]
    result = filter_by_state(data, state="EXECUTED")
    assert len(result) == 2


def test_filter_by_state_empty():
    """Тест: фильтрация с пустым списком."""
    result = filter_by_state([], "EXECUTED")
    assert result == []


def test_filter_by_state_no_matches():
    """Тест: фильтрация без совпадений."""
    transactions = [
        {"state": "CANCELED", "description": "test1"},
        {"state": "PENDING", "description": "test2"},
    ]
    result = filter_by_state(transactions, "EXECUTED")
    assert result == []


# ============ ТЕСТЫ ДЛЯ СОРТИРОВКИ ==================


def test_sort_by_date():
    """Тест: сортировка по дате."""
    data = [
        {"id": 1, "date": "2023-01-15"},
        {"id": 2, "date": "2023-02-20"},
        {"id": 3, "date": "2023-01-01"},
    ]
    result = sort_by_date(data, reverse=True)
    assert result[0]["date"] == "2023-02-20"
    assert result[1]["date"] == "2023-01-15"
    assert result[2]["date"] == "2023-01-01"


def test_sort_by_date_ascending():
    """Тест: сортировка по возрастанию."""
    data = [
        {"id": 1, "date": "2023-01-15"},
        {"id": 2, "date": "2023-02-20"},
        {"id": 3, "date": "2023-01-01"},
    ]
    result = sort_by_date(data, reverse=False)
    assert result[0]["date"] == "2023-01-01"
    assert result[1]["date"] == "2023-01-15"
    assert result[2]["date"] == "2023-02-20"


def test_sort_by_date_empty():
    """Тест: сортировка пустого списка."""
    result = sort_by_date([], reverse=True)
    assert result == []


def test_sort_by_date_missing_date():
    """Тест: сортировка с отсутствующей датой."""
    transactions = [
        {"date": "2020-01-01", "description": "first"},
        {"description": "second"},  # без даты
        {"date": "2019-01-01", "description": "third"},
    ]
    result = sort_by_date(transactions, reverse=True)
    # Транзакции без даты должны быть в конце
    assert result[-1]["description"] == "second"


# ============ ТЕСТЫ ДЛЯ ПОИСКА ==================


def test_search_transactions_by_description():
    """Тест: поиск по описанию (использует re)."""
    data = [
        {"description": "Перевод на карту"},
        {"description": "Оплата покупки"},
        {"description": "Перевод другу"},
    ]
    result = process_bank_search(data, "Перевод")
    assert len(result) == 2
    for item in result:
        assert "перевод" in item["description"].lower()


def test_search_transactions_by_description_case_insensitive():
    """Тест: регистронезависимый поиск."""
    data = [
        {"description": "Перевод на карту"},
        {"description": "ПЕРЕВОД другу"},
        {"description": "перевод с карты"},
    ]
    result = process_bank_search(data, "перевод")
    assert len(result) == 3


def test_search_transactions_by_description_empty():
    """Тест: поиск с пустыми данными."""
    assert process_bank_search([], "Перевод") == []
    assert process_bank_search([{"description": "test"}], "") == []


def test_search_transactions_by_description_no_matches():
    """Тест: поиск без совпадений."""
    data = [{"description": "Открытие вклада"}, {"description": "Оплата услуг"}]
    result = process_bank_search(data, "перевод")
    assert len(result) == 0


def test_search_transactions_by_description_partial_match():
    """Тест: частичное совпадение."""
    data = [
        {"description": "Перевод организации"},
        {"description": "Переводчик работает"},
    ]
    result = process_bank_search(data, "перевод")
    assert len(result) == 2


def test_search_transactions_by_description_with_special_chars():
    """Тест: со специальными символами."""
    data = [{"description": "Перевод (организации)"}, {"description": "Перевод [счет]"}]
    result = process_bank_search(data, "(организации)")
    assert len(result) == 1
    assert result[0]["description"] == "Перевод (организации)"


# ============ ТЕСТЫ ДЛЯ ПОДСЧЕТА КАТЕГОРИЙ ==================


def test_count_transactions_by_categories():
    """Тест: подсчет транзакций по категориям (использует Counter)."""
    data = [
        {"description": "Оплата еды"},
        {"description": "Транспорт"},
        {"description": "Еда в кафе"},
        {"description": "Развлечения"},
    ]
    categories = ["Оплата еды", "Транспорт", "Развлечения"]
    result = process_bank_operations(data, categories)
    assert result["Оплата еды"] == 1
    assert result["Транспорт"] == 1
    assert result["Развлечения"] == 1


def test_count_transactions_by_categories_empty():
    """Тест: подсчет с пустыми данными."""
    assert process_bank_operations([], ["Еда"]) == {}
    assert process_bank_operations([{"description": "test"}], []) == {}


def test_count_transactions_by_categories_no_matches():
    """Тест: подсчет без совпадений."""
    data = [
        {"description": "Оплата еды"},
        {"description": "Транспорт"},
    ]
    categories = ["Покупки", "Зарплата"]
    result = process_bank_operations(data, categories)
    assert result["Покупки"] == 0
    assert result["Зарплата"] == 0


# ============ ТЕСТЫ ДЛЯ МАСКИРОВКИ ==================


def test_mask_account_card_card():
    """Тест: маскировка карты."""
    result = mask_account_card("Maestro 1596837868705199")
    assert result == "Maestro 1596 83** **** 5199"


def test_mask_account_card_account():
    """Тест: маскировка счета."""
    result = mask_account_card("Счет 64686473678894779589")
    assert result == "Счет **9589"


def test_mask_account_card_empty():
    """Тест: маскировка пустой строки."""
    assert mask_account_card("") == "Неизвестно"


def test_mask_account_card_no_space():
    """Тест: маскировка без пробела."""
    result = mask_account_card("1596837868705199")
    assert result == "1596837868705199"


def test_mask_account_card_short():
    """Тест: маскировка короткого номера."""
    result = mask_account_card("1234")
    assert result == "1234"


# ============ ТЕСТЫ ДЛЯ ФОРМАТИРОВАНИЯ ДАТЫ ==================


def test_get_date_full_format():
    """Тест: преобразование даты с временем."""
    result = get_date("2019-08-26T10:50:58.294041")
    assert result == "26.08.2019"


def test_get_date_simple_format():
    """Тест: преобразование простой даты."""
    result = get_date("2019-08-26")
    assert result == "26.08.2019"


def test_get_date_empty():
    """Тест: преобразование пустой даты."""
    assert get_date("") == ""


def test_get_date_invalid():
    """Тест: преобразование невалидной даты."""
    result = get_date("invalid date")
    assert result == "invalid date"
