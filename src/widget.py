from src.masks import get_mask_account, get_mask_card_number
from datetime import datetime


def mask_account_card(account: str) -> str:
    """Функция, которая маскирует номер карты или счета при вводе данных
    Параметры:
        account: Строка в формате "Visa Platinum 1234567890123456" или "Счет 12345678901234567890"

    Возвращает:
        Строку с маскированным номером типа "Visa Platinum 1234 56** **** 3456" или "Счет **7890"

    Исключения:
        ValueError: Если входные данные некорректны
    """
    if not isinstance(account, str):
        raise ValueError("Введенные данные должны быть строкой")

    if not account.strip():
        raise ValueError("Введена пустая строка")

    parts = account.split()
    if len(parts) < 2:
        raise ValueError("Некорректный формат данных. Ожидается 'Тип Номер'")

    number = ''.join([p for p in parts if p.isdigit()])
    account_type = ' '.join([p for p in parts if not p.isdigit()])

    if not number.isdigit():
        raise ValueError("Номер должен содержать только цифры")

    if len(number) == 16:
        masked_number = f"{number[:4]} {number[4:6]}** **** {number[-4:]}"
        return f"{account_type} {masked_number}"

    elif len(number) >= 4:
        return f"{account_type} **{number[-4:]}"

    raise ValueError("Номер должен содержать минимум 4 цифры")



def get_date(date_str: str) -> str:
    """
    Преобразует строку с датой в формате ISO (YYYY-MM-DD) или ISO с временем (YYYY-MM-DDTHH:MM:SS)
    в строку формата DD.MM.YYYY.

    Параметры:
        date_str: Строка с датой

    Возвращает:
        Строку с датой в формате DD.MM.YYYY

    Исключения:
        ValueError: Если входная строка имеет неверный формат
        TypeError: Если переданы данные не строкового типа
    """
    if not isinstance(date_str, str):
        raise TypeError("Входные данные должны быть строкой")

    try:
        for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
            try:
                date_obj = datetime.strptime(date_str, fmt)
                return date_obj.strftime("%d.%m.%Y")
            except ValueError:
                continue
        raise ValueError("Неверный формат даты. Ожидается YYYY-MM-DD или YYYY-MM-DDTHH:MM:SS")
    except Exception as e:
        raise ValueError(f"Ошибка преобразования даты: {e}")



