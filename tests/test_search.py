from src.search import process_bank_search


def test_process_bank_search():
    """Тест функции поиска по описанию"""
    data = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Перевод с карты на карту"},
        {"description": "Оплата услуг"},
    ]

    result = process_bank_search(data, "перевод")
    assert len(result) == 2
    assert result[0]["description"] == "Перевод организации"
    assert result[1]["description"] == "Перевод с карты на карту"


def test_process_bank_search_case_insensitive():
    """Тест регистронезависимого поиска"""
    data = [
        {"description": "Перевод организации"},
        {"description": "ПЕРЕВОД С карты"},
        {"description": "перевод на счет"},
    ]

    result = process_bank_search(data, "перевод")
    assert len(result) == 3


def test_process_bank_search_empty():
    """Тест с пустыми данными"""
    assert process_bank_search([], "test") == []
    assert process_bank_search([{"description": "test"}], "") == []


def test_process_bank_search_no_matches():
    """Тест когда совпадений нет"""
    data = [{"description": "Открытие вклада"}, {"description": "Оплата услуг"}]

    result = process_bank_search(data, "перевод")
    assert len(result) == 0


def test_process_bank_search_partial_match():
    """Тест частичного совпадения"""
    data = [
        {"description": "Перевод организации"},
        {"description": "Переводчик работает"},
    ]

    result = process_bank_search(data, "перевод")
    assert len(result) == 2


def test_process_bank_search_with_special_chars():
    """Тест с специальными символами"""
    data = [{"description": "Перевод (организации)"}, {"description": "Перевод [счет]"}]

    result = process_bank_search(data, "(организации)")
    assert len(result) == 1
    assert result[0]["description"] == "Перевод (организации)"


def test_process_bank_search_missing_description():
    """Тест когда в транзакции нет поля description"""
    data = [
        {"description": "Перевод организации"},
        {"id": 12345},  # Нет description
        {"description": "Перевод с карты"},
    ]

    result = process_bank_search(data, "перевод")
    assert len(result) == 2


def test_process_bank_search_with_empty_string():
    """Тест с пустой строкой поиска"""
    data = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
    ]
    result = process_bank_search(data, "")
    assert len(result) == 0


def test_process_bank_search_unicode():
    """Тест с юникод символами"""
    data = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
    ]
    result = process_bank_search(data, "вклад")
    assert len(result) == 1
    assert result[0]["description"] == "Открытие вклада"
