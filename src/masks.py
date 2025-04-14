def get_mask_card_number(card_number: int | str) -> str:
    """Преобразуем номер карты в строку и удаляем все пробелы"""
    card_str = str(card_number).replace(" ", "")

    # Формируем маскированные части
    number_part_1 = card_str[:4]
    number_part_2 = card_str[4:6] + "**"
    number_part_3 = "****"
    number_part_4 = card_str[-4:]

    """Собираем результат со звездочками между частями"""
    return f"{number_part_1} {number_part_2} {number_part_3} {number_part_4}"


print(get_mask_card_number(12344108430135874305))


def get_mask_account(account_number: int | str) -> str:
    """Преобразуем номер счёта в строку и удаляем пробелы"""
    account_str = str(account_number).replace(" ", "")

    """Возвращаем маску: две звёздочки и последние 4 цифры"""
    return f"**{account_str[-4:]}"


print(get_mask_account(73654108430135874305))
