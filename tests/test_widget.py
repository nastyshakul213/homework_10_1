from src.widget import mask_account_card, get_date
import pytest

@pytest.mark.parametrize("value, expected", [
    ("Visa Platinum 1234567890123456", "Visa Platinum 1234 56** **** 3456"),
    ("Mastercard 1234 5678 9012 3456", "Mastercard 1234 56** **** 3456"),
    ("Счет 12345678901234567890", "Счет **7890"),
    ("Счет 1234", "Счет **1234"),
    ("American Express 123456789012345", "American Express **2345"),
    ("Карта 12 34 56 78 9012 3456", "Карта 1234 56** **** 3456"),
])

def test_mask_account_card(value, expected):
    assert mask_account_card(value) == expected

    with pytest.raises(ValueError):
        mask_account_card("Visa 123") == "Номер должен содержать минимум 4 цифры"

    with pytest.raises(ValueError):
        mask_account_card("Visa 1234abcd56789012") == "Номер должен содержать только цифры"

    with pytest.raises(ValueError):
        mask_account_card("") == "Введена пустая строка"

    with pytest.raises(ValueError):
        mask_account_card(1234567890123456) == "Введенные данные должны быть строкой"

    with pytest.raises(ValueError):
        mask_account_card("1234567890123456") == "Некорректный формат данных. Ожидается 'Тип Номер'"

@pytest.mark.parametrize(date_1, date_2, [
    ("2023-12-31T23:59:59", "31.12.2023"),
    ("2023-01-15", "15.01.2023")
])
def test_get_date(date_1, date_2):
    assert get_date(date_1) == date_2

    with pytest.raises(TypeError):
        get_date(123456789) == "Входные данные должны быть строкой"

    with pytest.raises(ValueError):
        get_date("31-12-2023") == "Неверный формат даты. Ожидается YYYY-MM-DD или YYYY-MM-DDTHH:MM:SS"

    with pytest.raises(ValueError):
        get_date("")

    with pytest.raises(ValueError):
        get_date("2023-02-30")