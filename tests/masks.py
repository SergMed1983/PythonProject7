import pytest

# Внимание: если твои файлы лежат в src, импорт может быть таким:
from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "card,expected",
    [
        # ВАЖНО: Замени строки в кавычках справа
        # на тот формат, который реально выдает твоя функция!
        ("4276123456789012", "4276 ** **** 9012"),
        ("5559123412341234", "5559 ** **** 1234"),
        ("12345", None),  # Или "" или raise Exception - зависит
        # от твоего кода
        ("", None),
    ],
)
def test_get_mask_card_number(card, expected):
    assert get_mask_card_number(card) == expected


@pytest.mark.parametrize(
    "account,expected",
    [
        ("40817810000000000001", "4081 7810 0000 0000 0001"),
        ("30101810000000000002", "3010 1810 0000 0000 0002"),
        ("123", None),
        ("", None),
    ],
)
def test_get_mask_account(account, expected):
    assert get_mask_account(account) == expected
