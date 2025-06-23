import json


def financial_transactions(file_path: str) -> list[str]:
    """
    Читает JSON-файл с транзакциями и возвращает список словарей.

    Аргументы:
        file_path (str): Путь к JSON-файлу

    Возвращает:
        list: Список транзакций (словарей) или пустой список при ошибках
    """
    try:
        # Пытаемся открыть и прочитать файл
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

            # Проверяем, что данные - это список
            if isinstance(data, list):
                return data
            return []

    except (FileNotFoundError, json.JSONDecodeError):
        # Если файл не найден или невалидный JSON
        return []
    except Exception:
        # На случай других непредвиденных ошибок
        return []

# if __name__ == '__main__':
#     financial_transactions('operations.json')


