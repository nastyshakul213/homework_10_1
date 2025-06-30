import logging
import os

# Настройка логгера
logger = logging.getLogger('masks')
logger.setLevel(logging.DEBUG)

# Абсолютный путь к логам
log_path = os.path.abspath('logs/masks.log')

# Создаем обработчик
file_handler = logging.FileHandler(log_path, mode='w', encoding='utf-8')
file_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
)
logger.addHandler(file_handler)

# Тестовый вызов
logger.info("Тестовое сообщение")

def get_mask_card_number(card_number: int | str) -> str:
    """Форматирует номер карты с маскировкой"""
    try:
        logger.debug(f"Начало обработки номера карты: {card_number}")

        card_str = str(card_number).replace(" ", "")

        # Валидация номера карты
        if card_number is None:
            error_msg = "Номер карты не может быть None"
            logger.error(error_msg)
            raise ValueError(error_msg)

        if len(card_str) < 16:
            error_msg = "Номер карты должен содержать минимум 16 цифр"
            logger.error(error_msg)
            raise ValueError(error_msg)

        if not card_str.isdigit():
            error_msg = "Номер карты должен содержать только цифры"
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Форматирование номера карты
        masked_number = f"{card_str[:4]} {card_str[4:6]}** **** {card_str[-4:]}"
        logger.info(f"Сформирована маска карты: {masked_number}")
        return masked_number

    except Exception as e:
        logger.exception("Ошибка при маскировании номера карты")
        raise


def get_mask_account(account_number: int | str) -> str:
    """Форматирует номер счета с маскировкой"""
    try:
        logger.debug(f"Начало обработки номера счета: {account_number}")

        account_str = str(account_number).replace(" ", "")

        # Валидация номера счета
        if account_number is None:
            error_msg = "Номер счета не может быть None"
            logger.error(error_msg)
            raise ValueError(error_msg)

        if len(account_str) < 16:
            error_msg = "Номер счета должен содержать минимум 16 цифр"
            logger.error(error_msg)
            raise ValueError(error_msg)

        if not account_str.isdigit():
            error_msg = "Номер счета должен содержать только цифры"
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Форматирование номера счета
        masked_account = f"**{account_str[-4:]}"
        logger.info(f"Сформирована маска счета: {masked_account}")
        return masked_account

    except Exception as e:
        logger.exception("Ошибка при маскировании номера счета")
        raise


if __name__ == '__main__':
    # Тестирование функции маскирования карт
    test_cards = [
        "1234567890123456",  # Валидный номер
        "1234 5678 9012 3456",  # С пробелами
        "123456789012345",  # Слишком короткий
        "1234abcd56789012",  # С буквами
        None  # None значение
    ]

    logger.info("\nТестирование маскирования карт:")
    for card in test_cards:
        try:
            print(f"Вход: {card} -> Выход: {get_mask_card_number(card)}")
        except ValueError as e:
            print(f"Вход: {card} -> Ошибка: {str(e)}")

