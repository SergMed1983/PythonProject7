import os

import pandas as pd

# Создаём папку data, если её нет
os.makedirs("data", exist_ok=True)

# Полные данные с amount, currency, state
data = [
    {
        "id": 1,
        "date": "2019-12-08",
        "description": "Открытие вклада",
        "amount": 40542,
        "currency": "руб.",
        "state": "EXECUTED",
    },
    {
        "id": 2,
        "date": "2019-11-12",
        "description": "Перевод с карты на карту",
        "amount": 130,
        "currency": "USD",
        "state": "EXECUTED",
    },
    {
        "id": 3,
        "date": "2018-07-18",
        "description": "Перевод организации",
        "amount": 8390,
        "currency": "руб.",
        "state": "CANCELED",
    },
    {
        "id": 4,
        "date": "2018-06-03",
        "description": "Перевод со счета на счет",
        "amount": 8200,
        "currency": "EUR",
        "state": "PENDING",
    },
    {
        "id": 5,
        "date": "2020-01-01",
        "description": "Оплата интернета",
        "amount": 500,
        "currency": "руб.",
        "state": "EXECUTED",
    },
    {
        "id": 6,
        "date": "2020-03-15",
        "description": "Перевод с карты на карту",
        "amount": 15000,
        "currency": "руб.",
        "state": "EXECUTED",
    },
    {
        "id": 7,
        "date": "2020-05-20",
        "description": "Пополнение счета",
        "amount": 25000,
        "currency": "USD",
        "state": "PENDING",
    },
]

# Создаём DataFrame и сохраняем в Excel
df = pd.DataFrame(data)
df.to_excel("data/transactions.xlsx", index=False)

print("✅ Файл data/transactions.xlsx создан!")
print(f"📊 Создано {len(data)} транзакций")
print("\nСодержимое файла:")
print(df)
