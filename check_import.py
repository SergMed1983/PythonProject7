import sys

print(f"Рабочий каталог: {sys.path}")
print("\nПути поиска (sys.path):")
for i, p in enumerate(sys.path):
    print(f"{i}: {p}")

print("\nПопытка импорта...")
try:
    from text_utils import reverse_text
    print("\n✅ УСПЕХ: Импорт сработал!")
    print(f"   Тест функции: {reverse_text('hello')}")
except ImportError as e:
    print(f"\n❌ ОШИБКА: Импорт не сработал.")
    print(f"   Текст ошибки: {e}")
