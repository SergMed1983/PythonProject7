import pytest
from src.decorators.log_decorator import log
import os


def test_log_decorator_console_via_file(tmp_path):
    """
    Тест логирования. Так как мы используем logging, а не print,
    мы проверяем содержимое временного файла.
    """
    log_file = tmp_path / "console_test.log"

    @log(filename=str(log_file))  # Эмулируем консоль, записывая во временный файл для проверки
    def test_func():
        return "Результат работы"

    result = test_func()
    assert result == "Результат работы"

    with open(log_file, "r", encoding="utf-8") as f:
        content = f.read()
        assert "Start: test_func" in content
        assert "Result: Результат работы" in content


def test_log_decorator_file(tmp_path):
    log_file = tmp_path / "real_file.log"

    @log(filename=str(log_file))
    def test_func():
        return "Финальный результат"

    test_func()

    with open(log_file, "r", encoding="utf-8") as f:
        content = f.read()
        assert "Start: test_func" in content
        assert "Result: Финальный результат" in content


def test_log_decorator_error(tmp_path):
    log_file = tmp_path / "error.log"

    @log(filename=str(log_file))
    def divide(x, y):
        return x / y

    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    with open(log_file, "r", encoding="utf-8") as f:
        content = f.read()
        assert "Error in divide" in content
        assert "Inputs: args=(1, 0)" in content
