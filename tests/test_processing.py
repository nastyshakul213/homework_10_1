from src.processing import filter_by_state, sort_by_date
import pytest

transactions = [
    {"state": "EXECUTED", "id": 1},
    {"state": "PENDING", "id": 2},
    {"state": "EXECUTED", "id": 3}
]

def test_filter_by_state():
    # Фильтрация по умолчанию (EXECUTED)
    assert len(filter_by_state(transactions)) == 2

    # Фильтрация по PENDING
    assert len(filter_by_state(transactions, "PENDING")) == 1

    with pytest.raises(ValueError):
        filter_by_state("это не список") == "Ошибка, нужно передать список операций."


def test_sort_by_date():

    data = [
        {"date": "2023-01-01", "id": 1},
        {"date": "2022-01-01", "id": 2}
    ]
    result = sort_by_date(data)
    assert result[0]["id"] == 1
    assert result[1]["id"] == 2


def test_reverse_sort():
    data = [
        {"date": "2023-01-01"},
        {"date": "2022-01-01"}
    ]
    result = sort_by_date(data, reverse=True)
    assert result[0]["date"] == "2023-01-01"

def test_empty_list():
    assert sort_by_date([]) == []

def test_missing_date():
    with pytest.raises(KeyError):
        sort_by_date([{"id": 1}])

def test_wrong_date_format():
    with pytest.raises(ValueError):
        sort_by_date([{"date": "01/01/2023"}])