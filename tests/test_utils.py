import unittest
from unittest.mock import mock_open, patch
import json
from src.utils import financial_transactions

class TestLoadTransactions(unittest.TestCase):
    def test_file_exists_and_valid(self):
        """Тест: файл существует и содержит валидный JSON-список"""
        test_data = [{"id": 1, "amount": 100}, {"id": 2, "amount": -50}]
        with patch("builtins.open", mock_open(read_data=json.dumps(test_data))):
            result = financial_transactions("data/operations.json")
            self.assertEqual(result, test_data)

    def test_file_not_found(self):
        """Тест: файл не существует"""
        with patch("builtins.open", side_effect=FileNotFoundError):
            result = financial_transactions("nonexistent.json")
            self.assertEqual(result, [])

    def test_empty_file(self):
        """Тест: файл пустой"""
        with patch("builtins.open", mock_open(read_data="")):
            result = financial_transactions("empty.json")
            self.assertEqual(result, [])

    def test_json_not_a_list(self):
        """Тест: JSON есть, но это не список (например, словарь)"""
        test_data = {"id": 1, "amount": 100}  # Это словарь, а не список!
        with patch("builtins.open", mock_open(read_data=json.dumps(test_data))):
            result = financial_transactions("not_a_list.json")
            self.assertEqual(result, [])

    def test_invalid_json(self):
        """Тест: файл содержит невалидный JSON"""
        with patch("builtins.open", mock_open(read_data="{invalid_json")):
            result = financial_transactions("broken.json")
            self.assertEqual(result, [])

