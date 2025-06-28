import os
import requests
from typing import Dict

def get_api_key():
    """Функция для получения API ключа"""
    return os.getenv('EXCHANGE_RATE_API_KEY')

BASE_URL = "https://api.apilayer.com/exchangerates_data/latest"
BASE_CURRENCY = "RUB"
SUPPORTED_CURRENCIES = ("USD", "EUR")

def convert_to_rub(transaction: Dict) -> float:
    """Конвертирует сумму транзакции из исходной валюты в рубли по текущему курсу."""
    try:
        api_key = get_api_key()
        if not api_key:
            raise ValueError("API key not configured")

        # Остальной код функции остается без изменений
        amount = float(transaction["operationAmount"]["amount"])
        currency = transaction["operationAmount"]["currency"]["code"].upper()

        if currency == BASE_CURRENCY:
            return amount

        if currency not in SUPPORTED_CURRENCIES:
            raise ValueError(f"Unsupported currency: {currency}")

        response = requests.get(
            BASE_URL,
            params={'base': currency, 'symbols': BASE_CURRENCY},
            headers={'apikey': api_key},
            timeout=10
        )

        response.raise_for_status()

        try:
            data = response.json()
        except ValueError as e:
            raise ValueError(f"Invalid API response (not JSON): {str(e)}")

        if not data.get('success', False):
            error_info = data.get('error', {}).get('info', 'Unknown API error')
            raise ValueError(f"API error: {error_info}")

        if 'rates' not in data or BASE_CURRENCY not in data['rates']:
            raise ValueError("Invalid API response format")

        return round(amount * data['rates'][BASE_CURRENCY], 2)

    except KeyError as e:
        raise ValueError(f"Missing required field in transaction: {e}")
    except requests.exceptions.RequestException as e:
        raise ValueError(f"API connection error: {str(e)}")
