from src.generators import filter_by_currency, transaction_descriptions, card_number_generator
import pytest

transactions = [
    {
        "id": 1,
        "operationAmount": {
            "amount": "100",
            "currency": {"code": "USD"}
        }
    },
    {
        "id": 2,
        "operationAmount": {
            "amount": "200",
            "currency": {"code": "EUR"}
        }
    },
    {
        "id": 3,
        "operationAmount": {
            "amount": "300",
            "currency": {"code": "USD"}
        }
    },
    {
        "id": 4,
        "operationAmount": {
            "amount": "400",
            "currency": {"code": "RUB"}
        }
    },
    {
        "id": 5,
        "operationAmount": {
            "amount": "500",
            "currency": {"code": "USD"}
        }
    }
]

# Проверка фильтрации транзакций по валюте USD
def test_filter_usd_transactions():
    transactions = [
        {"operationAmount": {"currency": {"code": "USD"}}},  # USD
        {"operationAmount": {"currency": {"code": "EUR"}}},  # EUR
        {"operationAmount": {"currency": {"code": "USD"}}},  # USD
        {"operationAmount": {"currency": {"code": "USD"}}}   # USD
    ]
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 3


# Проверка фильтрации транзакций по валюте EUR
def test_filter_eur_transactions():
    eur_transactions = filter_by_currency(transactions, "EUR")
    result = list(eur_transactions)
    assert len(result) == 1
    assert result[0]["id"] == 2

#  Проверка работы с пустым списком транзакций
def test_empty_transactions_list():
    empty_transactions = filter_by_currency([], "USD")
    result = list(empty_transactions)
    assert len(result) == 0

#  Проверка обработки отсутствия транзакций в заданной валюте (GBP)
def test_no_matching_currency():
    gbp_transactions = filter_by_currency(transactions, "GBP")
    result = list(gbp_transactions)
    assert len(result) == 0

# Проверка обработки транзакций без поля operationAmount
def test_missing_operation_amount():
    broken_transactions = [
        {"id": 6, "state": "EXECUTED"},
        {"id": 7, "operationAmount": None}
    ]
    usd_transactions = list(filter_by_currency(broken_transactions, "USD"))
    assert len(usd_transactions) == 0

#  Проверка обработки транзакций с некорректной валютой
def test_invalid_currency_structure():
    invalid_transactions = [
        {
            "id": 8,
            "operationAmount": {
                "amount": "600",
                "currency": None  # Валюты нет
            }
        },
        {
            "id": 9,
            "operationAmount": {
                "amount": "700",
                "currency": {"name": "USD"}  # Нет поля code
            }
        }
    ]
    usd_transactions = filter_by_currency(invalid_transactions, "USD")
    result = list(usd_transactions)
    assert len(result) == 0



# Тестовые данные
transactions = [
    {
        "id": 1,
        "description": "Перевод организации",
        "operationAmount": {"amount": "100", "currency": {"code": "USD"}}
    },
    {
        "id": 2,
        "description": "Перевод со счета на счет",
        "operationAmount": {"amount": "200", "currency": {"code": "EUR"}}
    },
    {
        "id": 3,
        "description": "Перевод с карты на карту",
        "operationAmount": {"amount": "300", "currency": {"code": "RUB"}}
    }
]


#  Проверка корректного возврата описаний
def test_return_correct_descriptions():
    desc_gen = transaction_descriptions(transactions)
    assert next(desc_gen) == "Перевод организации"
    assert next(desc_gen) == "Перевод со счета на счет"
    assert next(desc_gen) == "Перевод с карты на карту"


#  Проверка работы с пустым списком
def test_empty_transactions_list():
    desc_gen = transaction_descriptions([])
    with pytest.raises(StopIteration):
        next(desc_gen)


#  Проверка обработки транзакций без поля description
def test_missing_description_field():
    incomplete_transactions = [
        {"id": 4, "operationAmount": {"amount": "400"}},  # Нет description
        {"id": 5, "description": None}  # description есть, но None
    ]

    desc_gen = transaction_descriptions(incomplete_transactions)
    with pytest.raises(KeyError):
        next(desc_gen)


#  Проверка работы с одной транзакцией
def test_single_transaction():
    single_trans = [transactions[0]]
    desc_gen = transaction_descriptions(single_trans)
    assert next(desc_gen) == "Перевод организации"
    with pytest.raises(StopIteration):
        next(desc_gen)


#  Проверка порядка возврата описаний
def test_descriptions_order():
    desc_gen = transaction_descriptions(transactions)
    descriptions = list(desc_gen)
    assert descriptions == [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод с карты на карту"
    ]


#  Проверка генерации номеров в обычном диапазоне
def test_normal_range():
    generator = card_number_generator(1, 5)
    expected = [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005"
    ]
    assert list(generator) == expected

#  Проверка генерации одного номера
def test_single_value():
    generator = card_number_generator(42, 42)
    assert next(generator) == "0000 0000 0000 0042"
    with pytest.raises(StopIteration):
        next(generator)

#  Проверка генерации больших номеров
def test_large_range():
    generator = card_number_generator(1, 10000)
    for x in range(9995):  # Пропускаем 9995 номеров
        next(generator)
    assert next(generator) == "0000 0000 0000 9996"  # Следующий должен быть 9996


# Проверка корректности формата
def test_format_correctness():
    generator = card_number_generator(1234567890123456, 1234567890123456)
    card = next(generator)
    # Проверяем длину (16 цифр + 3 пробела)
    assert len(card) == 19
    # Проверяем группы по 4 цифры
    parts = card.split()
    assert len(parts) == 4
    assert all(len(part) == 4 for part in parts)
    # Проверяем, что все символы - цифры или пробелы
    assert all(c.isdigit() or c == ' ' for c in card)

# Проверка обработки недопустимого диапазона
def test_invalid_range():
    with pytest.raises(ValueError):
        list(card_number_generator(0, 5))  # start < 1
    with pytest.raises(ValueError):
        list(card_number_generator(5, 1))  # start > end


#  Проверка граничных случаев
def test_edge_cases():
    # Первый допустимый номер
    generator = card_number_generator(1, 1)
    assert next(generator) == "0000 0000 0000 0001"

    # Последний допустимый номер
    generator = card_number_generator(9999999999999999, 9999999999999999)
    assert next(generator) == "9999 9999 9999 9999"

#  Проверка работы с большим диапазоном (без загрузки в память)
def test_large_range() -> None:
    generator = card_number_generator(1, 10000)
    assert next(generator) == "0000 0000 0000 0001"
    assert next(generator) == "0000 0000 0000 0002"
    assert next(generator) == "0000 0000 0000 0003"
    assert next(generator) == "0000 0000 0000 0004"
    assert next(generator) == "0000 0000 0000 0005"

    # Пропускаем промежуточные значения
    for _ in range(9990):
        next(generator)

    # Проверяем последнее значение
    assert next(generator) == "0000 0000 0000 9996"


def test_filter_by_currency_edge_cases():
    # Тест с пустым списком
    assert list(filter_by_currency([], "USD")) == []

    # Тест с некорректными данными
    broken_data = [
        None,
        {"operationAmount": None},
        {"operationAmount": {"currency": None}},
        {"operationAmount": {"currency": "USD"}},  # Не dict
        {"operationAmount": {"currency": {"name": "USD"}}}  # Нет code
    ]
    assert list(filter_by_currency(broken_data, "USD")) == []


def test_card_number_generator_edges():
    # Тест минимального и максимального значений
    gen = card_number_generator(1, 1)
    assert next(gen) == "0000 0000 0000 0001"

    gen = card_number_generator(9999999999999999, 9999999999999999)
    assert next(gen) == "9999 9999 9999 9999"

    # Тест исключений
    with pytest.raises(ValueError):
        list(card_number_generator(0, 1))

    with pytest.raises(ValueError):
        list(card_number_generator(2, 1))

    with pytest.raises(ValueError):
        list(card_number_generator(10000000000000000, 10000000000000001))



