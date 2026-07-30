from typing import Generator, Dict, Any, List

def filter_by_currency(transactions: List[Dict[str, Any]], currency_code: str) -> Generator[Dict[str, Any], None, None]:
    for transaction in transactions:
        curr = transaction.get("operationAmount", {}).get("currency", {})
        if curr.get("code") == currency_code:
            yield transaction


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Generator[str, None, None]:
    for t in transactions:
        yield t.get("description", "Без описания")


def card_number_generator(start: int, stop: int) -> Generator[str, None, None]:
    for num in range(start, stop + 1):
        s = f"{num:016d}"
        yield f"{s[0:4]} {s[4:8]} {s[8:12]} {s[12:16]}"
