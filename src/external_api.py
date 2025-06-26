import os
import requests
from typing import Dict
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")
BASE_URL = "https://apilayer.com/exchangerates_data-api"

def convert_to_rub(transaction: Dict) -> float:
    try:
        amount = float(transaction["amount"])
        currency = transaction["currency"].upper()

        if currency == "RUB":
            return amount

        if currency not in ("USD", "EUR"):
            raise ValueError(f"Unsupported currency: {currency}")

        response = requests.get(
            BASE_URL,
            params={"base": currency, "symbols": "RUB"},
            headers={"apikey": API_KEY},
            timeout=10
        )
        response.raise_for_status()

        rate = response.json()["rates"]["RUB"]
        return round(amount * rate, 2)

    except KeyError as e:
        raise ValueError(f"Missing field: {e}")
    except requests.exceptions.RequestException as e:
        raise ValueError(f"API error: {str(e)}")

