from typing import Dict, Any, Iterator, List

Transaction = Dict[str, Any]
TransactionIter = Iterator[Transaction]
DescriptionIter = Iterator[str]
CardNumberIter = Iterator[str]


def filter_by_currency(transactions: list[Dict[str, Any]], currency_code: str) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует транзакции по валюте с обработкой крайних случаев

    Args:
        transactions: Список транзакций
        currency_code: Код валюты (например, "USD")

    Returns:
        Итератор транзакций с указанной валютой
    """
    for transaction in transactions:
        try:
            op_amount = transaction.get("operationAmount", {})
            currency = op_amount.get("currency", {}) if isinstance(op_amount, dict) else {}
            if isinstance(currency, dict) and currency.get("code") == currency_code:
                yield transaction
        except (AttributeError, TypeError):
            continue


def transaction_descriptions(transactions: List[Transaction]) -> DescriptionIter:
    """
    Генератор, который возвращает описания транзакций по одной.

    :param transactions: Список словарей с транзакциями
    :yield: Описание транзакции (строка)
    """
    for transaction in transactions:
        yield transaction["description"]


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генерирует номера карт с валидацией параметров

    Args:
        start: начальный номер (1-9999999999999999)
        end: конечный номер (>= start)

    Returns:
        Итератор номеров карт в формате "XXXX XXXX XXXX XXXX"

    Raises:
        ValueError: при неверных параметрах
    """
    if not (1 <= start <= 9999999999999999):
        raise ValueError("Начальный номер должен быть от 1 до 9999999999999999")
    if not (1 <= end <= 9999999999999999):
        raise ValueError("Конечный номер должен быть от 1 до 9999999999999999")
    if start > end:
        raise ValueError("Начальный номер не может быть больше конечного")

    for number in range(start, end + 1):
        num_str = f"{number:016d}"
        yield f"{num_str[:4]} {num_str[4:8]} {num_str[8:12]} {num_str[12:16]}"
