"""Модуль для работы с внешними API."""

import json
import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Получаем API ключ из переменных окружения
API_KEY = os.getenv("EXCHANGE_RATES_API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data/convert"


def convert_currency(transaction: Dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли, если валюта USD или EUR.

    Args:
        transaction (Dict[str, Any]): Словарь с данными о транзакции.
            Должен содержать ключи 'amount' и 'currency'.

    Returns:
        float: Сумма транзакции в рублях.

    Raises:
        ValueError: Если отсутствует API ключ или произошла ошибка при запросе.
    """
    amount = transaction.get("amount")
    currency = transaction.get("currency")

    if not amount or not currency:
        raise ValueError("Транзакция не содержит сумму или валюту")

    # Если валюта уже в рублях, возвращаем сумму (API ключ не нужен)
    if currency.upper() == "RUB":
        return float(amount)

    # Для USD и EUR проверяем наличие API ключа
    if not API_KEY:
        raise ValueError("API ключ не найден. Проверьте файл .env")

    # Конвертируем только USD и EUR
    if currency.upper() not in ["USD", "EUR"]:
        raise ValueError(f"Конвертация валюты {currency} не поддерживается")

    try:
        # Формируем запрос к API
        url = BASE_URL
        params = {
            "from": currency.upper(),
            "to": "RUB",
            "amount": amount
        }
        headers = {
            "apikey": API_KEY
        }

        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()

        data = response.json()

        # Проверяем успешность ответа
        if not data.get("success", False):
            error_info = data.get("error", {}).get("info", "Неизвестная ошибка")
            raise ValueError(f"Ошибка API: {error_info}")

        # Получаем сконвертированную сумму
        converted_amount = data.get("result")
        if converted_amount is None:
            raise ValueError("Не удалось получить сконвертированную сумму")

        return float(converted_amount)

    except requests.exceptions.RequestException as e:
        raise ValueError(f"Ошибка при запросе к API: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Ошибка парсинга ответа API: {e}")
