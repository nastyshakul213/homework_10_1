from src.masks import get_mask_card_number, get_mask_account
import pytest
from src.masks import get_mask_account



def test_get_mask_card_number(valid_card_mask):
    assert get_mask_card_number("1234567890123456") == valid_card_mask

    with pytest.raises(ValueError):
        get_mask_card_number("12345678") == "Номер карты должен содержать минимум 16 цифр"

    with pytest.raises(ValueError):
        get_mask_card_number("abcd1234") == "Номер карты должен содержать только цифры"

    with pytest.raises(ValueError):
        get_mask_card_number(" ") == "Номер счёта не может быть пустым"



@pytest.mark.parametrize("account, expected", [
    ("1234567890123456", "**3456"),  # Ровно 16 цифр
    ("12345678901234567890", "**7890"),  # Более 16
    ("0000000000000000", "**0000")  # Граничный случай
])
def test_get_mask_account(account: str, expected: str):
    assert get_mask_account(account) == expected









