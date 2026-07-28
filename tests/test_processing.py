import pytest

from src.processing import filter_by_state, sort_by_date


def test_filter_by_state_executed(transactions):
    filtered = filter_by_state(transactions, "EXECUTED")
    assert len(filtered) == 2
    assert all(t["state"] == "EXECUTED" for t in filtered)


@pytest.mark.parametrize(
    "state,count",
    [
        ("EXECUTED", 2),
        ("CANCELED", 1),
        ("NEW", 1),
        ("UNKNOWN", 0),
    ],
)
def test_filter_by_state_parametrized(transactions, state, count):
    filtered = filter_by_state(transactions, state)
    assert len(filtered) == count


def test_sort_by_date_desc(transactions):
    sorted_list = sort_by_date(transactions, reverse=True)
    dates = [t["date"] for t in sorted_list]
    assert dates == sorted(dates, reverse=True)


def test_sort_by_date_asc(transactions):
    sorted_list = sort_by_date(transactions, reverse=False)
    dates = [t["date"] for t in sorted_list]
    assert dates == sorted(dates)
