from src.masks import get_mask_card_number, get_mask_account
import pytest



def test_get_mask_card_number(valid_card_mask):
    assert get_mask_card_number("1234567890123456") == valid_card_mask

    with pytest.raises(ValueError):
        get_mask_card_number("12345678") == "Номер карты должен содержать минимум 16 цифр"

    with pytest.raises(ValueError):
        get_mask_card_number("abcd1234") == "Номер карты должен содержать только цифры"

    with pytest.raises(ValueError):
        get_mask_card_number(" ") == "Номер счёта не может быть пустым"



def test_get_mask_account(number):
    assert get_mask_account("1234 5678 1234 4567 1234") == "**1234"

    with pytest.raises(ValueError):
        get_mask_account("123") == "Номер карты должен содержать минимум 16 цифр"

    with pytest.raises(ValueError):
        get_mask_account("nmh123") == "Номер карты должен содержать только цифры"

    with pytest.raises(ValueError):
        get_mask_account(" ")  == "Номер счёта не может быть пустым"








