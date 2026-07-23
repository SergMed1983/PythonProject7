# PythonProject7

Проект реализует функционал фильтрации операций по статусу и сортировки по дате. Код написан с использованием строгой типизации (type hints) и соответствует стандартам качества (flake8, mypy).

## Требования к окружению

- Python версии **3.14** или выше (версия проверена в проекте).
- Менеджер пакетов `pip`.

## Установка и запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/SergMed1983/PythonProject7.git
cd PythonProject7

## Тестирование

Для проверки корректности работы функций используется `pytest`.

1. Установите pytest (если ещё не установлен):
   ```powershell
   pip install pytest

## Проверка качества кода

Проект соответствует стандартам PEP 8 и строгой типизации:

- `flake8`: ошибок не найдено
- `mypy`: ошибок не найдено

Для проверки на своей машине можно запустить:
```powershell
flake8 src/
mypy src/

## Примеры использования функций модуля `src.processing`

### Фильтрация операций по статусу

Функция `filter_by_state` позволяет отбирать операции по полю `state`. По умолчанию фильтрует только выполненные операции (`EXECUTED`).

```python
from src.processing import filter_by_state

operations = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}
]

# Получаем только выполненные операции (по умолчанию)
executed_ops = filter_by_state(operations)

# Получаем только отмененные операции
canceled_ops = filter_by_state(operations, 'CANCELED')

from src.processing import sort_by_date

# Сортировка по убыванию (новые сначала) — поведение по умолчанию
newest_first = sort_by_date(operations)

# Сортировка по возрастанию (старые сначала)
oldest_first = sort_by_date(operations, reverse=False)

