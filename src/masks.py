def get_mask_card_number(card_number: int | str) -> str:
    """Преобразуем номер карты в строку и удаляем все пробелы,
    Собираем результат со звездочками между частями
    """
    card_str = str(card_number).replace(" ", "")
    if len(card_str) < 16:
        raise ValueError("Номер карты должен содержать минимум 16 цифр")

    if not card_str.isdigit():
        raise ValueError("Номер карты должен содержать только цифры")

    if card_number is None:
        raise ValueError("Номер счёта не может быть пустым")

    # Формируем маскированные части
    number_part_1 = card_str[:4]
    number_part_2 = card_str[4:6] + "**"
    number_part_3 = "****"
    number_part_4 = card_str[-4:]

    return f"{number_part_1} {number_part_2} {number_part_3} {number_part_4}"




def get_mask_account(account_number: int | str) -> str:
    """Преобразуем номер счёта в строку и удаляем пробелы,
    Возвращаем маску: две звёздочки и последние 4 цифры
    """
    account_str = str(account_number).replace(" ", "")

    if len(account_str) < 16:
        raise ValueError("Номер карты должен содержать минимум 16 цифр")

    if not account_str.isdigit():
        raise ValueError("Номер карты должен содержать только цифры")

    if account_number is None:
        raise ValueError("Номер счёта не может быть пустым")


    return f"**{account_str[-4:]}"
