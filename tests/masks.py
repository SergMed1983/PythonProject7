import pytest

# Правильный импорт из src.masks
from src.masks import mask_account_number, mask_card_number


@pytest.mark.parametrize(
    "card,expected",
    [
        ("4276123456789012", "4276 12** **** 9012"),
        ("5559123412341234", "5559 12** **** 1234"),
        ("1234567890123456", "1234 56** **** 3456"),
        ("12345", None),  # Функция вызовет ValueError
        ("", None),  # Функция вызовет ValueError
    ],
)
def test_mask_card_number(card, expected):
    if expected is None:
        with pytest.raises(ValueError):
            mask_card_number(card)
    else:
        assert mask_card_number(card) == expected


@pytest.mark.parametrize(
    "account,expected",
    [
        ("40817810000000000001", "**0001"),
        ("30101810000000000002", "**0002"),
        ("123", None),  # Функция вызовет ValueError
        ("", None),  # Функция вызовет ValueError
    ],
)
def test_mask_account_number(account, expected):
    if expected is None:
        with pytest.raises(ValueError):
            mask_account_number(account)
    else:
        assert mask_account_number(account) == expected
