from unittest.mock import mock_open, patch

import pandas as pd

# Импорт функций из ВАШЕГО файла
from src.transactions.file_reader import read_csv, read_excel


def test_read_csv_success():
    """Проверяет корректное чтение и парсинг CSV."""
    mock_csv_content = "id,amount,description\n1,100.5,Покупка\n2,200.0,Оплата"
    m = mock_open(read_data=mock_csv_content)

    # ДОБАВЛЕНА СТРОКА: подменяем os.path.exists, чтобы он вернул True
    with patch("src.transactions.file_reader.os.path.exists", return_value=True):
        with patch("src.transactions.file_reader.open", m):
            result = read_csv("fake_file.csv")

    expected = [
        {"id": "1", "amount": 100.5, "description": "Покупка"},
        {"id": "2", "amount": 200.0, "description": "Оплата"},
    ]
    assert result == expected


def test_read_csv_file_not_found():
    """Проверяет обработку отсутствующего CSV-файла."""
    # ИСПРАВЛЕНО: file_reader вместо csv_excel_reader
    with patch("src.transactions.file_reader.os.path.exists", return_value=False):
        result = read_csv("non_existent.csv")
    assert result == []


def test_read_excel_success():
    """Проверяет корректное чтение и парсинг Excel."""
    mock_df = pd.DataFrame(
        {"id": [1, 2], "amount": [100.5, 200.0], "description": ["Покупка", "Оплата"]}
    )

    # ИСПРАВЛЕНО: file_reader вместо csv_excel_reader
    with patch("src.transactions.file_reader.pd.read_excel") as mock_read_excel:
        mock_read_excel.return_value = mock_df
        with patch("src.transactions.file_reader.os.path.exists", return_value=True):
            result = read_excel("fake_file.xlsx")

    expected = [
        {"id": 1, "amount": 100.5, "description": "Покупка"},
        {"id": 2, "amount": 200.0, "description": "Оплата"},
    ]
    assert result == expected


def test_read_excel_file_not_found():
    """Проверяет обработку отсутствующего Excel-файла."""
    # ИСПРАВЛЕНО: file_reader вместо csv_excel_reader
    with patch("src.transactions.file_reader.os.path.exists", return_value=False):
        result = read_excel("non_existent.xlsx")
    assert result == []
