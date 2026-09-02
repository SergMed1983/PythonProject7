"""
������� ������ ����������.
�������� ���������� ��� ������ � �����������
������������ � ������ �������.
"""

import os
from typing import Any, Dict, List

import pandas as pd

from src.processing import filter_by_state, sort_by_date


def test_function() -> None:
    """�������� ������� ��� �������� ����������."""
    print("�������� �������")


def run_text_reverser() -> None:
    """��������� ���������� ������� ������."""
    from src.text_utils import reverse_text

    text = input("������� ����� ����� ��� �������: ")
    print(reverse_text(text))


def load_transactions_from_json(filepath: str) -> List[Dict[str, Any]]:
    """��������� ���������� �� JSON-�����."""
    from src.transactions.file_reader import read_json_transactions

    transactions = read_json_transactions(filepath)
    if not transactions:
        print(f"���� {filepath} �� ������ ��� ����.")
    return transactions


def load_transactions_from_csv(filepath: str) -> List[Dict[str, Any]]:
    """��������� ���������� �� CSV-�����."""
    from src.transactions.file_reader import read_csv_transactions

    transactions = read_csv_transactions(filepath)
    if not transactions:
        print(f"���� {filepath} �� ������ ��� ����.")
    return transactions


def load_transactions_from_xlsx(filepath: str) -> List[Dict[str, Any]]:
    """
    ��������� ���������� �� XLSX-����� � ������� pandas.
    ��������� ������������ ����.
    """
    transactions: List[Dict[str, Any]] = []

    if not os.path.exists(filepath):
        print(f"���� {filepath} �� ������")
        return []

    try:
        df = pd.read_excel(filepath)

        print(f"������� �������: {list(df.columns)}")
        print(f"������� �����: {len(df)}")

        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].dt.strftime("%Y-%m-%d")
            elif df[col].dtype == "object":
                try:
                    sample = (
                        df[col].dropna().iloc[0] if len(df[col].dropna()) > 0 else None
                    )
                    if sample and isinstance(sample, str):
                        df[col] = pd.to_datetime(df[col], errors="coerce")
                        if pd.api.types.is_datetime64_any_dtype(df[col]):
                            df[col] = df[col].dt.strftime("%Y-%m-%d")
                except Exception:
                    pass

        df = df.where(pd.notnull(df), None)
        transactions = df.to_dict("records")

        print(f"������� ��������� {len(transactions)} ���������� �� XLSX")

    except ImportError:
        print(
            "���������� pandas �� �����������. "
            "����������: pip install pandas openpyxl"
        )
        return []
    except Exception as e:
        print(f"������ �������� XLSX: {e}")
        import traceback

        traceback.print_exc()
        return []

    return transactions


def generate_test_transactions() -> List[Dict[str, Any]]:
    """���������� �������� ����� ���������� ��� ������������."""
    return [
        {
            "id": 1,
            "date": "2019-12-08",
            "description": "�������� ������",
            "amount": 40542,
            "currency": "���.",
            "state": "EXECUTED",
        },
        {
            "id": 2,
            "date": "2019-11-12",
            "description": "������� � ����� �� �����",
            "amount": 130,
            "currency": "USD",
            "state": "EXECUTED",
        },
        {
            "id": 3,
            "date": "2018-07-18",
            "description": "������� �����������",
            "amount": 8390,
            "currency": "���.",
            "state": "CANCELED",
        },
        {
            "id": 4,
            "date": "2018-06-03",
            "description": "������� �� ����� �� ����",
            "amount": 8200,
            "currency": "EUR",
            "state": "PENDING",
        },
        {
            "id": 5,
            "date": "2020-01-01",
            "description": "������ ���������",
            "amount": 500,
            "currency": "���.",
            "state": "EXECUTED",
        },
    ]


def filter_ruble_transactions(
    transactions: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """��������� ������ �������� ����������."""
    return [tx for tx in transactions if tx.get("currency", "").lower() == "���."]


def print_transactions(transactions: List[Dict[str, Any]]) -> None:
    """������� ������� ������ ���������� � �����������."""
    from src.processing import get_transaction_amount, mask_account_card

    if not transactions:
        print(
            "\n�� ������� �� ����� ����������, ���������� ��� ���� ������� ����������"
        )
        return

    print(f"\n����� ���������� �������� � �������: {len(transactions)}")
    print("-" * 60)

    for tx in transactions:
        date = tx.get("date", "���� �� �������")
        if date and isinstance(date, str):
            date = date.split("T")[0].split(" ")[0]

        description = tx.get("description", "��� ��������")
        amount, currency = get_transaction_amount(tx)

        from_account = tx.get("from", "")
        to_account = tx.get("to", "")

        if from_account:
            from_account = mask_account_card(from_account)
        if to_account:
            to_account = mask_account_card(to_account)

        print(f"{date} {description}")
        if from_account and to_account:
            print(f"{from_account} -> {to_account}")
        elif from_account:
            print(f"{from_account}")
        elif to_account:
            print(f"�� {to_account}")
        print(f"�����: {amount} {currency}")
        print("-" * 60)


def run_bank_processor() -> None:
    """��������� �������� ���������� ��������� ��� ������ � ����������� ������������."""
    print("������! ����� ���������� � ��������� ������ � ����������� ������������.")
    print("�������� ����������� ����� ����:")
    print("1. �������� ���������� � ����������� �� JSON-�����")
    print("2. �������� ���������� � ����������� �� CSV-�����")
    print("3. �������� ���������� � ����������� �� XLSX-�����")

    choice = input("\n��� �����: ").strip()
    transactions: List[Dict[str, Any]] = []

    if choice == "1":
        print("��� ��������� ������ JSON-����.")
        filepath = input(
            "������� ���� � JSON-����� (��� ������� Enter ��� �������� ������): "
        ).strip()
        if filepath:
            transactions = load_transactions_from_json(filepath)
        if not transactions:
            print("���� �� ������ ��� ����. �������� �������� ������.")
            transactions = generate_test_transactions()
    elif choice == "2":
        print("��� ��������� ������ CSV-����.")
        filepath = input(
            "������� ���� � CSV-����� (��� ������� Enter ��� �������� ������): "
        ).strip()
        if filepath:
            transactions = load_transactions_from_csv(filepath)
        if not transactions:
            print("���� �� ������ ��� ����. �������� �������� ������.")
            transactions = generate_test_transactions()
    elif choice == "3":
        print("��� ��������� ������ XLSX-����.")
        filepath = input(
            "������� ���� � XLSX-����� (��� ������� Enter ��� data/transactions.xlsx): "
        ).strip()
        if not filepath:
            filepath = "data/transactions.xlsx"
        transactions = load_transactions_from_xlsx(filepath)
        if not transactions:
            print("���� �� ������ ��� ����. �������� �������� ������.")
            transactions = generate_test_transactions()
    else:
        print("�������� �����. �������� �������� ������.")
        transactions = generate_test_transactions()

    if not transactions:
        print("�� ������� ��������� ����������.")
        return

    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        status_input = (
            input(
                "\n������� ������, �� �������� ���������� ��������� ����������.\n"
                "��������� ��� ���������� �������: EXECUTED, CANCELED, PENDING\n"
                "��� ������: "
            )
            .strip()
            .upper()
        )
        if status_input in valid_statuses:
            transactions = filter_by_state(transactions, status_input)
            print(f'�������� ������������� �� ������� "{status_input}"')
            break
        else:
            print(f'������ �������� "{status_input}" ����������.')

    if not transactions:
        print("�� ������� �� ����� ���������� � ����� ��������.")
        return

    sort_choice = input("\n������������� �������� �� ����? ��/���: ").strip().lower()
    if sort_choice in ["��", "yes", "y", "�"]:
        order = input("������������� �� ����������� ��� �� ��������? ").strip().lower()
        ascending = order in ["�� �����������", "�����������", "asc", "�������"]
        transactions = sort_by_date(transactions, ascending)

    ruble_choice = (
        input("\n�������� ������ �������� ����������? ��/���: ").strip().lower()
    )
    if ruble_choice in ["��", "yes", "y", "�"]:
        transactions = filter_ruble_transactions(transactions)

    if not transactions:
        print(
            "�� ������� �� ����� ����������, " "���������� ��� ���� ������� ����������"
        )
        return

    search_choice = (
        input(
            "\n������������� ������ ���������� �� ������������� ����� � ��������? ��/���: "
        )
        .strip()
        .lower()
    )
    if search_choice in ["��", "yes", "y", "�"]:
        search_word = input("������� ����� ��� ������: ").strip()
        if search_word:
            from src.search import process_bank_search

            transactions = process_bank_search(transactions, search_word)

    print("\n������������ �������� ������ ����������...")
    print_transactions(transactions)


def main() -> None:
    """�������� ������� ���������."""
    print("����� ���������� � ���������!")
    print("�������� ����� ������:")
    print("1. ������ � ����������� ������������")
    print("2. ������ ������ (�������� �����)")

    mode = input("\n��� �����: ").strip()

    if mode == "1":
        run_bank_processor()
    elif mode == "2":
        test_function()
        run_text_reverser()
    else:
        print("�������� �����. �������� ����� ������ � ����������� ������������.")
        run_bank_processor()


if __name__ == "__main__":
    main()
