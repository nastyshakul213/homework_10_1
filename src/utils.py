import json
import logging
import os

# Настройка логгера
logger = logging.getLogger('utils')
logger.setLevel(logging.DEBUG)

# Настройка обработчика файла
file_handler = logging.FileHandler('logs/utils.log', mode='w', encoding='utf-8')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# Добавляем вывод в консоль для удобства
console_handler = logging.StreamHandler()
console_handler.setFormatter(file_formatter)
logger.addHandler(console_handler)


def financial_transactions(file_path: str) -> list[dict]:
    """
    Читает JSON-файл с транзакциями и возвращает список словарей.
    Детально логирует процесс выполнения и ошибки.
    """
    logger.debug("Запуск обработки транзакций")
    logger.info(f"Начало обработки файла: {file_path}")

    try:
        # Получаем абсолютный путь для логирования
        abs_path = os.path.abspath(file_path)
        logger.debug(f"Абсолютный путь к файлу: {abs_path}")

        # Проверка существования файла
        if not os.path.exists(file_path):
            logger.error(f"Файл не найден: {abs_path}")
            return []

        # Проверка размера файла
        if os.path.getsize(file_path) == 0:
            logger.warning(f"Файл пуст: {abs_path}")
            return []

        # Чтение файла
        with open(file_path, 'r', encoding='utf-8') as file:
            logger.debug("Открытие файла для чтения")
            data = json.load(file)
            logger.info(f"Успешно прочитано записей: {len(data) if isinstance(data, list) else 'N/A'}")

            # Проверка типа данных
            if not isinstance(data, list):
                logger.warning("Данные в файле не являются списком")
                return []

            logger.info(f"Успешно обработано транзакций: {len(data)}")
            return data

    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON: {str(e)}", exc_info=True)
        return []
    except Exception as e:
        logger.error(f"Непредвиденная ошибка: {str(e)}", exc_info=True)
        return []


if __name__ == '__main__':
    transactions = financial_transactions('operations.json')
    logger.info(f"Итоговое количество обработанных транзакций: {len(transactions)}")
    logger.info("Завершение работы программы")
