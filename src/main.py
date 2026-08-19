from src.decorators.log_decorator import log
from src.text_utils import reverse_text


@log()
def test_function():
    print("Тестовая функция")


if __name__ == "__main__":
    # Тестирование декоратора
    test_function()

    # Основной функционал
    text = input("Введите любой текст для реверса: ")
    print(reverse_text(text))
