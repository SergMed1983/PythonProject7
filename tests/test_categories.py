from src.categories import process_bank_operations


def test_process_bank_operations():
    """Тест подсчета категорий"""
    data = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Перевод организации"},
        {"description": "Перевод с карты на карту"},
        {"description": "Оплата услуг"},
    ]

    categories = ["Перевод организации", "Открытие вклада", "Оплата услуг"]
    result = process_bank_operations(data, categories)

    assert result["Перевод организации"] == 2
    assert result["Открытие вклада"] == 1
    assert result["Оплата услуг"] == 1


def test_process_bank_operations_empty_data():
    """Тест с пустыми данными"""
    result = process_bank_operations([], ["Перевод организации"])
    assert result == {}


def test_process_bank_operations_empty_categories():
    """Тест с пустым списком категорий"""
    data = [{"description": "Перевод организации"}]
    result = process_bank_operations(data, [])
    assert result == {}


def test_process_bank_operations_no_matches():
    """Тест когда категорий нет в данных"""
    data = [{"description": "Перевод организации"}, {"description": "Открытие вклада"}]
    categories = ["Оплата услуг", "Пополнение"]
    result = process_bank_operations(data, categories)

    assert result["Оплата услуг"] == 0
    assert result["Пополнение"] == 0


def test_process_bank_operations_missing_description():
    """Тест когда в транзакции нет поля description"""
    data = [
        {"description": "Перевод организации"},
        {"id": 12345},  # Нет description
        {"description": "Перевод организации"},
    ]
    categories = ["Перевод организации"]
    result = process_bank_operations(data, categories)

    assert result["Перевод организации"] == 2


def test_process_bank_operations_case_sensitive():
    """Тест что подсчет чувствителен к регистру"""
    data = [
        {"description": "Перевод организации"},
        {"description": "перевод организации"},  # строчные буквы
        {"description": "Перевод организации"},
    ]
    categories = ["Перевод организации"]
    result = process_bank_operations(data, categories)

    # Так как строки должны совпадать точно, учитывается регистр
    assert result["Перевод организации"] == 2


def test_process_bank_operations_with_duplicates():
    """Тест с дублирующимися категориями"""
    data = [
        {"description": "Перевод организации"},
        {"description": "Перевод организации"},
        {"description": "Перевод организации"},
    ]
    categories = ["Перевод организации", "Открытие вклада"]
    result = process_bank_operations(data, categories)
    assert result["Перевод организации"] == 3
    assert result["Открытие вклада"] == 0


def test_process_bank_operations_multiple_categories():
    """Тест с несколькими категориями"""
    data = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Перевод организации"},
        {"description": "Оплата услуг"},
        {"description": "Оплата услуг"},
        {"description": "Перевод с карты"},
    ]
    categories = [
        "Перевод организации",
        "Оплата услуг",
        "Открытие вклада",
        "Пополнение",
    ]
    result = process_bank_operations(data, categories)

    assert result["Перевод организации"] == 2
    assert result["Оплата услуг"] == 2
    assert result["Открытие вклада"] == 1
    assert result["Пополнение"] == 0


def test_process_bank_operations_with_none_data():
    """Тест с None в данных"""
    data = [
        {"description": "Перевод организации"},
        None,
        {"description": "Перевод организации"},
    ]
    categories = ["Перевод организации"]
    result = process_bank_operations(data, categories)
    assert result["Перевод организации"] == 2


def test_process_bank_operations_large_data():
    """Тест с большим количеством данных"""
    data = [{"description": f"Категория {i}"} for i in range(100)]
    categories = ["Категория 0", "Категория 50", "Категория 99", "Категория 100"]
    result = process_bank_operations(data, categories)

    assert result["Категория 0"] == 1
    assert result["Категория 50"] == 1
    assert result["Категория 99"] == 1
    assert result["Категория 100"] == 0
