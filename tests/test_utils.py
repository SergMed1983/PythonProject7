"""Тесты для модуля utils."""

import json
from unittest.mock import mock_open, patch

from src.utils import read_json_file


def test_read_json_file_success():
    """Тест успешного чтения JSON файла."""
    test_data = [
        {"id": 1, "amount": 100, "currency": "USD"},
        {"id": 2, "amount": 200, "currency": "EUR"}
    ]
    mock_json = json.dumps(test_data)

    with patch("builtins.open", mock_open(read_data=mock_json)):
        result = read_json_file("test.json")
        assert result == test_data


def test_read_json_file_empty():
    """Тест чтения пустого JSON файла."""
    with patch("builtins.open", mock_open(read_data="")):
        result = read_json_file("empty.json")
        assert result == []


def test_read_json_file_not_list():
    """Тест чтения JSON, который содержит не список."""
    with patch("builtins.open", mock_open(read_data='{"key": "value"}')):
        result = read_json_file("not_list.json")
        assert result == []


def test_read_json_file_not_found():
    """Тест чтения несуществующего файла."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = read_json_file("nonexistent.json")
        assert result == []


def test_read_json_file_invalid_json():
    """Тест чтения некорректного JSON."""
    with patch("builtins.open", mock_open(read_data="invalid json")):
        result = read_json_file("invalid.json")
        assert result == []
