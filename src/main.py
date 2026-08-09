# src/main.py
from src.decorators.log_decorator import log
from src.text_utils import reverse_text


@log()
def test_function():
    print("Тестовая функция")


if __name__ == "__main__":
<<<<<<< HEAD
    # Тестирование декоратора
    test_function()

    # Основной функционал
=======
>>>>>>> 20b21f06fa4b8974ceb1b306040882814838ca09
    text = input("Введите любой текст для реверса: ")
    print(reverse_text(text))
