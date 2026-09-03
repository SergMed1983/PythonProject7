import pytest

from src.decorators import log


def test_log_to_console_success(capsys):
    """Тест успешного выполнения с выводом в консоль."""

    @log()
    def add(a, b):
        return a + b

    add(2, 3)
    captured = capsys.readouterr()
    assert captured.out == "add ok\n"


def test_log_to_console_error(capsys):
    """Тест ошибки с выводом в консоль."""

    @log()
    def divide(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    captured = capsys.readouterr()
    expected = "divide error: ZeroDivisionError. Inputs: (10, 0), {}"
    assert expected in captured.out


def test_log_with_kwargs(capsys):
    """Тест функции с именованными аргументами."""

    @log()
    def greet(name, greeting="Hello"):
        return f"{greeting}, {name}!"

    greet("Alice", greeting="Hi")
    captured = capsys.readouterr()
    assert captured.out == "greet ok\n"


def test_log_to_file_success(tmp_path):
    """Тест успешного выполнения с записью в файл."""
    log_file = tmp_path / "test.log"

    @log(filename=str(log_file))
    def multiply(a, b):
        return a * b

    multiply(3, 4)
    content = log_file.read_text()
    assert "multiply ok" in content


def test_log_to_file_error(tmp_path):
    """Тест ошибки с записью в файл."""
    log_file = tmp_path / "test.log"

    @log(filename=str(log_file))
    def divide(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(5, 0)

    content = log_file.read_text()
    expected = "divide error: ZeroDivisionError. Inputs: (5, 0), {}"
    assert expected in content


def test_log_multiple_calls(tmp_path):
    """Тест множественных вызовов одной функции."""
    log_file = tmp_path / "test.log"

    @log(filename=str(log_file))
    def increment(x):
        return x + 1

    increment(1)
    increment(2)
    increment(3)

    content = log_file.read_text()
    assert content.count("increment ok") == 3
