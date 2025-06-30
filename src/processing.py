from typing import Dict, List
from datetime import datetime


def filter_by_state(transactions: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
    Фильтрует список операций по статусу (state).

    Параметры:
    - transactions: Список словарей с операциями (каждый словарь может содержать ключ 'state').
    - state: Статус операции для фильтрации. По умолчанию 'EXECUTED'.

    Возвращает:
    - Новый список, содержащий только операции с указанным статусом.
    """
    if not isinstance(transactions, list):
        raise ValueError("Ошибка, нужно передать список операций.")

    filtered_transactions = []

    for transaction in transactions:
        if transaction.get("state") == state:
            filtered_transactions.append(transaction)

    return filtered_transactions


def sort_by_date(info_list: List[Dict], reverse: bool = True) -> List[Dict]:
    """Сортирует список операций по дате (date)

    Параметры:
    - info_list: Список словарей.
    - sorted: Сортирует любую коллекцию.

    Возвращает:
    - Новый список, отсортированный  по дате (date)

    Исключения:
        TypeError: Если info_list не является списком.
        KeyError: Если какой-то словарь не содержит ключа 'date'.
        ValueError: Если дата в неверном формате.
    """

    if not isinstance(info_list, list):
        raise TypeError("Данные должны быть списком")

    try:
        return sorted(info_list, key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"), reverse=reverse)
    except KeyError as e:
        raise KeyError(f"Отсутствует обязательный ключ 'date' в одном из элементов: {e}")
    except ValueError as e:
        raise ValueError(f"Неверный формат даты. Ожидается YYYY-MM-DD: {e}")
