"""Тесты для модуля external_api."""

import json
from unittest.mock import Mock, patch

import pytest
import requests

from src.external_api import convert_currency


@pytest.fixture
def mock_transaction_usd():
    """Фикстура транзакции в USD."""
    return {
        "id": 1,
        "amount": 100.0,
        "currency": "USD",
        "description": "Test transaction"
    }


@pytest.fixture
def mock_transaction_eur():
    """Фикстура транзакции в EUR."""
    return {
        "id": 2,
        "amount": 150.0,
        "currency": "EUR",
        "description": "Test transaction"
    }


@pytest.fixture
def mock_transaction_rub():
    """Фикстура транзакции в RUB."""
    return {
        "id": 3,
        "amount": 5000.0,
        "currency": "RUB",
        "description": "Test transaction"
    }


def test_convert_currency_usd(mock_transaction_usd):
    """Тест конвертации USD в RUB."""
    mock_response = Mock()
    mock_response.json.return_value = {
        "success": True,
        "result": 9200.5
    }
    mock_response.raise_for_status = Mock()

    with patch("src.external_api.API_KEY", "test_api_key"):
        with patch("requests.get", return_value=mock_response):
            result = convert_currency(mock_transaction_usd)
            assert result == 9200.5


def test_convert_currency_eur(mock_transaction_eur):
    """Тест конвертации EUR в RUB."""
    mock_response = Mock()
    mock_response.json.return_value = {
        "success": True,
        "result": 13500.75
    }
    mock_response.raise_for_status = Mock()

    with patch("src.external_api.API_KEY", "test_api_key"):
        with patch("requests.get", return_value=mock_response):
            result = convert_currency(mock_transaction_eur)
            assert result == 13500.75


def test_convert_currency_rub(mock_transaction_rub):
    """Тест для RUB - должна возвращаться сумма без конвертации."""
    # Для RUB не нужен API ключ, поэтому не используем patch
    result = convert_currency(mock_transaction_rub)
    assert result == 5000.0


def test_convert_currency_no_api_key(mock_transaction_usd):
    """Тест обработки отсутствия API ключа."""
    with patch("src.external_api.API_KEY", None):
        with pytest.raises(ValueError, match="API ключ не найден"):
            convert_currency(mock_transaction_usd)


def test_convert_currency_api_error(mock_transaction_usd):
    """Тест обработки ошибки API."""
    mock_response = Mock()
    mock_response.json.return_value = {
        "success": False,
        "error": {
            "info": "Invalid API key"
        }
    }
    mock_response.raise_for_status = Mock()

    with patch("src.external_api.API_KEY", "test_api_key"):
        with patch("requests.get", return_value=mock_response):
            with pytest.raises(ValueError, match="Ошибка API"):
                convert_currency(mock_transaction_usd)


def test_convert_currency_request_exception(mock_transaction_usd):
    """Тест обработки исключения при запросе."""
    with patch("src.external_api.API_KEY", "test_api_key"):
        with patch("requests.get", side_effect=requests.exceptions.RequestException("Network error")):
            with pytest.raises(ValueError, match="Ошибка при запросе к API"):
                convert_currency(mock_transaction_usd)


def test_convert_currency_missing_fields():
    """Тест обработки транзакции без обязательных полей."""
    transaction = {"id": 1}  # Нет amount и currency
    with patch("src.external_api.API_KEY", "test_api_key"):
        with pytest.raises(ValueError, match="Транзакция не содержит сумму или валюту"):
            convert_currency(transaction)


def test_convert_currency_unsupported_currency():
    """Тест обработки неподдерживаемой валюты."""
    transaction = {
        "id": 4,
        "amount": 100.0,
        "currency": "GBP"
    }
    with patch("src.external_api.API_KEY", "test_api_key"):
        with pytest.raises(ValueError, match="Конвертация валюты GBP не поддерживается"):
            convert_currency(transaction)


def test_convert_currency_json_decode_error(mock_transaction_usd):
    """Тест обработки ошибки парсинга JSON."""
    mock_response = Mock()
    mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
    mock_response.raise_for_status = Mock()

    with patch("src.external_api.API_KEY", "test_api_key"):
        with patch("requests.get", return_value=mock_response):
            with pytest.raises(ValueError, match="Ошибка парсинга ответа API"):
                convert_currency(mock_transaction_usd)
