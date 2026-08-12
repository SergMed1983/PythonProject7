"""Тесты для модуля external_api."""

from unittest.mock import Mock, patch

import pytest
import requests

from src.external_api import convert_currency


def test_convert_currency_usd():
    """Тест конвертации USD в рубли."""
    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {
                "code": "USD"
            }
        }
    }

    # Мокаем API_KEY, чтобы он был доступен в функции
    with patch('src.external_api.API_KEY', 'test_api_key'):
        with patch('src.external_api.requests.get') as mock_get:
            # Создаем мок-ответ
            mock_response = Mock()
            mock_response.json.return_value = {
                "success": True,
                "result": 9050.0
            }
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response

            result = convert_currency(transaction)
            assert result == 9050.0


def test_convert_currency_eur():
    """Тест конвертации EUR в рубли."""
    transaction = {
        "operationAmount": {
            "amount": "50.00",
            "currency": {
                "code": "EUR"
            }
        }
    }

    # Мокаем API_KEY, чтобы он был доступен в функции
    with patch('src.external_api.API_KEY', 'test_api_key'):
        with patch('src.external_api.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {
                "success": True,
                "result": 5000.0
            }
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response

            result = convert_currency(transaction)
            assert result == 5000.0


def test_convert_currency_rub():
    """Тест, что RUB не конвертируется."""
    transaction = {
        "operationAmount": {
            "amount": "500.00",
            "currency": {
                "code": "RUB"
            }
        }
    }

    result = convert_currency(transaction)
    assert result == 500.0


def test_convert_currency_missing_amount():
    """Тест на ошибку при отсутствии суммы."""
    transaction = {
        "operationAmount": {
            "currency": {
                "code": "USD"
            }
        }
    }

    with pytest.raises(ValueError, match="Транзакция не содержит сумму или валюту"):
        convert_currency(transaction)


def test_convert_currency_missing_currency():
    """Тест на ошибку при отсутствии валюты."""
    transaction = {
        "operationAmount": {
            "amount": "100.00"
        }
    }

    with pytest.raises(ValueError, match="Транзакция не содержит сумму или валюту"):
        convert_currency(transaction)


def test_convert_currency_unsupported_currency():
    """Тест на ошибку при неподдерживаемой валюте."""
    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {
                "code": "GBP"
            }
        }
    }

    # Мокаем API_KEY, чтобы он был доступен в функции
    with patch('src.external_api.API_KEY', 'test_api_key'):
        with pytest.raises(ValueError, match="Конвертация валюты GBP не поддерживается"):
            convert_currency(transaction)


def test_convert_currency_missing_api_key():
    """Тест на ошибку при отсутствии API ключа."""
    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {
                "code": "USD"
            }
        }
    }

    # Мокаем API_KEY как None (отсутствует)
    with patch('src.external_api.API_KEY', None):
        with pytest.raises(ValueError, match="API ключ не найден"):
            convert_currency(transaction)


def test_convert_currency_api_error():
    """Тест на ошибку при неудачном запросе к API."""
    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {
                "code": "USD"
            }
        }
    }

    # Мокаем API_KEY и requests.get
    with patch('src.external_api.API_KEY', 'test_api_key'):
        with patch('src.external_api.requests.get') as mock_get:
            # Имитируем ошибку запроса
            mock_get.side_effect = requests.exceptions.RequestException("Connection error")

            with pytest.raises(ValueError, match="Ошибка при запросе к API"):
                convert_currency(transaction)
