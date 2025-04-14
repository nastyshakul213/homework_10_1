from masks import get_mask_account
from masks import get_mask_card_number


def mask_account_card(account: str) -> str:
    """Функция, которая маскирует номер карты или счета при вводе данных"""
    account_split = account.split()

    if "счет" in account.lower():
        return f"счет {get_mask_account(" ".join(account_split))}"
    else:
        card_name = ' '.join(account_split[:-1])
        card_number = account_split[-1]
        return f"{card_name} {get_mask_card_number(card_number)}"

print(mask_account_card("Visa Platinum 7000792289606361"))


def get_date(date: str) -> str:
    """Функция, которая принимает на вход строку с датой, а возвращает в формате даты"""
    date_split = date.split("T")[0]
    year, month, day = date_split.split("-")
    return f"{day}.{month}.{year}"

print(get_date("2024-03-11T02:26:18.671407"))



