import unittest
from unittest.mock import patch, MagicMock


# Импортируем модуль и requests отдельно
from src.external_api import convert_to_rub, BASE_URL, API_KEY
import requests


class TestCurrencyConversion(unittest.TestCase):
    def test_rub_transaction(self):
        transaction = {"amount": "100", "currency": "RUB"}
        self.assertEqual(convert_to_rub(transaction), 100.0)

    @patch('src.external_api.requests.get')
    def test_usd_conversion(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"rates": {"RUB": 75.0}}
        mock_get.return_value = mock_response

        transaction = {"amount": "10", "currency": "USD"}
        self.assertEqual(convert_to_rub(transaction), 750.0)
        mock_get.assert_called_once()

    @patch('src.external_api.requests.get')
    def test_api_failure(self, mock_get):
        """Тест обработки ошибки соединения с API"""
        # 1. Подготовка тестовых данных
        test_amount = "100"
        test_currency = "USD"
        transaction = {"amount": test_amount, "currency": test_currency}
        expected_error_msg = "API error: Connection timeout"

        # 2. Настройка мока
        mock_get.side_effect = requests.exceptions.RequestException("Connection timeout")

        # 3. Выполнение и проверки
        with self.assertRaises(ValueError) as context:
            convert_to_rub(transaction)

        # 4. Проверка сообщения об ошибке
        self.assertIn(expected_error_msg, str(context.exception))

        # 5. Проверка параметров вызова
        mock_get.assert_called_once_with(
            BASE_URL,
            params={"base": test_currency, "symbols": "RUB"},
            headers={"apikey": API_KEY},
            timeout=10
        )


if __name__ == '__main__':
    unittest.main()



