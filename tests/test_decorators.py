import os
from typing import Any

import pytest
from decorators import log

# Вспомогательная функция для чтения файла
def read_file(filename: str) -> str:
    with open(filename, 'r') as file:
        return file.read()

# Тест для фиксирования в консоль (успешный случай)
def test_log_to_console_success(capsys: pytest.CaptureFixture[str]) -> None:
    @log()
    def add(a: int, b: int) -> int:
        return a + b

    result = add(2, 3)
    captured = capsys.readouterr()

    assert result == 5
    assert "add started" in captured.out
    assert "add finished successfully" in captured.out
    assert "Result: 5" in captured.out

# Тест для фиксировани в консоль (ошибка)
def test_log_to_console_error(capsys: pytest.CaptureFixture[str]) -> None:
    @log()
    def divide(a: int, b: int) -> float:
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(4, 0)

    captured = capsys.readouterr()

    # Проверяем stdout (начало выполнения)
    assert "divide started" in captured.out

    # Проверяем stderr (ошибка)
    assert "divide failed with error" in captured.err  # Изменено с out на err
    assert "ZeroDivisionError" in captured.err

# Тест для фиксировани в файл (успешный случай)
def test_log_to_file_success(tmp_path: Any) -> None:
    log_file = str(tmp_path / "test_log.txt")

    @log(filename=log_file)
    def multiply(a: int, b: int) -> int:
        return a * b

    result = multiply(3, 4)

    assert result == 12
    log_content = read_file(log_file)
    assert "multiply started" in log_content
    assert "multiply finished successfully" in log_content
    assert "Result: 12" in log_content

# Тест для фиксировани в файл (ошибка)
def test_log_to_file_error(tmp_path: Any) -> None:
    log_file = str(tmp_path / "test_log.txt")

    @log(filename=log_file)
    def divide(a: int, b: int) -> float:
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(4, 0)

    log_content = read_file(log_file)
    assert "divide started" in log_content
    assert "divide failed with error" in log_content
    assert "ZeroDivisionError" in log_content
