# src/main.py
from src.decorators.log_decorator import log


@log()
def test_function():
    print("Тестовая функция")


if __name__ == "__main__":

    test_function()

    text = input("Введите любой текст для реверса: ")
    print(reverse_text(text))
