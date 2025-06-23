import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Добавляем src в путь импорта
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Импортируем модуль и requests отдельно
from src.external_api import convert_to_rub
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
        mock_get.side_effect = requests.exceptions.RequestException("API error")

        transaction = {"amount": "100", "currency": "USD"}
        with self.assertRaises(ValueError) as context:
            convert_to_rub(transaction)

        self.assertIn("API error", str(context.exception))


# if __name__ == '__main__':
#     unittest.main()
