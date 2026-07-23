# Функция, которая принимает текст и возвращает его развернутым
def reverse_text(text):
    return text[::-1]

# Проверяем работу функции
original = "Привет, Skypro!"
result = reverse_text(original)

print("Оригинал:", original)
print("Реверс:", result)

