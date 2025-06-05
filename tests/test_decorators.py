import pytest
import os
from typing import Any
from decorators import log

def test_log_to_console_success(capsys: pytest.CaptureFixture[str]) -> None:
    """Тестируем логирование успешного выполнения в консоль"""
    @log()
    def add(a: int, b: int) -> int:
        return a + b

    result = add(2, 3)
    captured = capsys.readouterr()

    assert result == 5
    assert captured.out == "add returned 5\n"
    assert captured.err == ""

def test_log_to_console_error(capsys: pytest.CaptureFixture[str]) -> None:
    """Тестируем логирование ошибки в консоль"""
    @log()
    def divide(a: int, b: int) -> float:
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(4, 0)

    captured = capsys.readouterr()

    assert captured.out == ""
    assert "divide raised ZeroDivisionError" in captured.err
    assert "with args: (4, 0), kwargs: {}" in captured.err

def test_log_to_file_success(tmp_path: Any) -> None:
    """Тестируем логирование успешного выполнения в файл"""
    log_file = tmp_path / "test.log"

    @log(filename=str(log_file))
    def multiply(a: int, b: int) -> int:
        return a * b

    result = multiply(3, 4)
    log_content = log_file.read_text()

    assert result == 12
    assert log_content == "multiply returned 12\n"

def test_log_to_file_error(tmp_path: Any) -> None:
    """Тестируем логирование ошибки в файл"""
    log_file = tmp_path / "test.log"

    @log(filename=str(log_file))
    def divide(a: int, b: int) -> float:
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(4, 0)

    log_content = log_file.read_text()

    assert "divide raised ZeroDivisionError" in log_content
    assert "with args: (4, 0), kwargs: {}" in log_content

def test_log_with_kwargs(capsys: pytest.CaptureFixture[str]) -> None:
    """Тестируем логирование функций с kwargs"""
    @log()
    def greet(name: str, greeting: str = "Hello") -> str:
        return f"{greeting}, {name}!"

    result = greet(name="Alice", greeting="Hi")
    captured = capsys.readouterr()

    assert result == "Hi, Alice!"
    assert captured.out == "greet returned Hi, Alice!\n"
    assert "kwargs: {'name': 'Alice', 'greeting': 'Hi'}" not in captured.out
