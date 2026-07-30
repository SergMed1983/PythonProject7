import pytest
from generators.main import filter_by_currency, transaction_descriptions, card_number_generator

@pytest.fixture
def transactions():
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "operationAmount": {"amount": "100", "currency": {"name": "USD", "code": "USD"}},
            "description": "USD Payment"
        },
        {
            "id": 2,
            "state": "EXECUTED",
            "operationAmount": {"amount": "200", "currency": {"name": "RUB", "code": "RUB"}},
            "description": "RUB Payment"
        },
        {
            "id": 3,
            "state": "CANCELED",
            "operationAmount": {"amount": "300", "currency": {"name": "USD", "code": "USD"}},
            "description": "Canceled USD"
        }
    ]

def test_filter_by_currency_usd(transactions):
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 2
    assert all(t["operationAmount"]["currency"]["code"] == "USD" for t in result)

def test_filter_by_currency_empty(transactions):
    result = list(filter_by_currency(transactions, "EUR"))
    assert len(result) == 0

def test_transaction_descriptions(transactions):
    descs = list(transaction_descriptions(transactions))
    assert len(descs) == 3
    assert descs[0] == "USD Payment"

def test_card_number_generator_format():
    gen = list(card_number_generator(1, 2))
    assert gen == [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002"
    ]
