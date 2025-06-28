import unittest
from unittest.mock import patch, Mock
import requests
from src.external_api import convert_to_rub


class TestCurrencyConverter(unittest.TestCase):
    def setUp(self):
        # Валидная транзакция в USD
        self.valid_usd_transaction = {
            "operationAmount": {
                "amount": "100.0",
                "currency": {"code": "USD"}
            }
        }

        # Транзакция в RUB (не требует конвертации)
        self.rub_transaction = {
            "operationAmount": {
                "amount": "500.0",
                "currency": {"code": "RUB"}
            }
        }

        # Транзакция с отсутствующим amount
        self.missing_amount_transaction = {
            "operationAmount": {
                "currency": {"code": "USD"}
            }
        }

        # Транзакция с неподдерживаемой валютой
        self.unsupported_currency_transaction = {
            "operationAmount": {
                "amount": "200.0",
                "currency": {"code": "GBP"}
            }
        }

    @patch('src.external_api.requests.get')
    @patch('src.external_api.get_api_key')
    def test_convert_usd_to_rub_success(self, mock_get_key, mock_get):
        """Тест успешной конвертации USD в RUB."""
        # Настраиваем моки
        mock_get_key.return_value = 'fake_api_key'
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": True,
            "rates": {"RUB": 75.50}
        }
        mock_get.return_value = mock_response

        # Вызываем тестируемую функцию
        result = convert_to_rub(self.valid_usd_transaction)

        # Проверяем результат
        self.assertEqual(result, 7550.0)

    @patch('src.external_api.get_api_key')
    def test_convert_rub_to_rub(self, mock_get_key):
        """Тест транзакции в RUB (конвертация не требуется)."""
        mock_get_key.return_value = 'fake_api_key'
        result = convert_to_rub(self.rub_transaction)
        self.assertEqual(result, 500.0)

    @patch('src.external_api.requests.get')
    @patch('src.external_api.get_api_key')
    def test_api_error_response(self, mock_get_key, mock_get):
        """Тест обработки ошибки API."""
        mock_get_key.return_value = 'fake_api_key'
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": False,
            "error": {"info": "Invalid API key"}
        }
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError) as context:
            convert_to_rub(self.valid_usd_transaction)
        self.assertIn("API error", str(context.exception))

    @patch('src.external_api.requests.get')
    @patch('src.external_api.get_api_key')
    def test_api_connection_error(self, mock_get_key, mock_get):
        """Тест ошибки соединения с API."""
        mock_get_key.return_value = 'fake_api_key'
        mock_get.side_effect = requests.exceptions.RequestException("Timeout")

        with self.assertRaises(ValueError) as context:
            convert_to_rub(self.valid_usd_transaction)
        self.assertIn("API connection error", str(context.exception))

    @patch('src.external_api.get_api_key')
    def test_missing_amount_field(self, mock_get_key):
        """Тест отсутствия обязательного поля amount."""
        mock_get_key.return_value = 'fake_api_key'
        with self.assertRaises(ValueError) as context:
            convert_to_rub(self.missing_amount_transaction)
        self.assertIn("Missing required field", str(context.exception))

    @patch('src.external_api.get_api_key')
    def test_unsupported_currency(self, mock_get_key):
        """Тест неподдерживаемой валюты."""
        mock_get_key.return_value = 'fake_api_key'
        with self.assertRaises(ValueError) as context:
            convert_to_rub(self.unsupported_currency_transaction)
        self.assertIn("Unsupported currency", str(context.exception))

    @patch('src.external_api.get_api_key')
    def test_missing_api_key(self, mock_get_key):
        """Тест отсутствия API-ключа."""
        mock_get_key.return_value = None
        with self.assertRaises(ValueError) as context:
            convert_to_rub(self.valid_usd_transaction)
        self.assertIn("API key not configured", str(context.exception))


# if __name__ == '__main__':
#     unittest.main()
