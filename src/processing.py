from typing import Dict, List


def filter_by_state(transactions: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
    Фильтрует список операций по статусу (state).

    Параметры:
    - transactions: Список словарей с операциями (каждый словарь может содержать ключ 'state').
    - state: Статус операции для фильтрации. По умолчанию 'EXECUTED'.

    Возвращает:
    - Новый список, содержащий только операции с указанным статусом.
    """
    filtered_transactions = []

    for transaction in transactions:
        if transaction.get("state") == state:
            filtered_transactions.append(transaction)

    return filtered_transactions


def sort_by_date(info_list: List[Dict]) -> List[Dict]:
    """Сортирует список операций по дате (date)

    Параметры:
    - info_list: Список словарей.
    - sorted: Сортирует любую коллекцию.

    Возвращает:
    - Новый список, отсортированный  по дате (date)
    """

    return sorted(info_list, key=lambda x: x["date"], reverse=False)
