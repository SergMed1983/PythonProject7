from src.processing import filter_by_state, sort_by_date


def test_filter_by_state():
    """Тест фильтрации по состоянию."""
    data = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"},
        {"id": 3, "state": "EXECUTED"},
    ]
    result = filter_by_state(data)
    assert len(result) == 2
    assert all(item["state"] == "EXECUTED" for item in result)


def test_filter_by_state_custom():
    """Тест фильтрации с пользовательским состоянием."""
    data = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"},
    ]
    result = filter_by_state(data, "CANCELED")
    assert len(result) == 1
    assert result[0]["state"] == "CANCELED"


def test_sort_by_date_ascending():
    """Тест сортировки по возрастанию."""
    data = [
        {"date": "2023-01-02"},
        {"date": "2023-01-01"},
        {"date": "2023-01-03"},
    ]
    result = sort_by_date(data, ascending=True)
    assert result[0]["date"] == "2023-01-01"
    assert result[1]["date"] == "2023-01-02"
    assert result[2]["date"] == "2023-01-03"


def test_sort_by_date_descending():
    """Тест сортировки по убыванию."""
    data = [
        {"date": "2023-01-02"},
        {"date": "2023-01-01"},
        {"date": "2023-01-03"},
    ]
    result = sort_by_date(data, ascending=False)
    assert result[0]["date"] == "2023-01-03"
    assert result[1]["date"] == "2023-01-02"
    assert result[2]["date"] == "2023-01-01"
