from generators.main import (
    filter_by_currency,
    transaction_descriptions,
    card_number_generator,
)


def load_sample_transactions() -> list:
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод организации",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод со счета на счет",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Перевод со счета на счет",
        },
    ]


def main():
    print("=" * 40)
    print("ДЗ 11.1: Работа с генераторами")
    print("=" * 40)

    transactions = load_sample_transactions()

    print("\n--- Транзакции в USD (filter_by_currency) ---")
    usd_gen = filter_by_currency(transactions, "USD")
    for t in usd_gen:
        print(f"- {t['description']} ({t['operationAmount']['amount']})")

    print("\n--- Все описания транзакций (transaction_descriptions) ---")
    desc_gen = transaction_descriptions(transactions)
    for desc in desc_gen:
        print(f"- {desc}")

    print("\n--- Генерация номеров карт (card_number_generator) ---")
    card_gen = card_number_generator(1000, 1003)
    for card in card_gen:
        print(f"- {card}")

    print("\n" + "=" * 40)
    print("Демонстрация завершена.")
    print("=" * 40)


if __name__ == "__main__":
    main()
