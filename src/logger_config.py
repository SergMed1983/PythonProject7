import logging
import os


def setup_logger(name: str, log_file: str, level=logging.DEBUG):
    """Настройка логгера с записью в файл"""

    # Создаем папку logs, если её нет
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Полный путь к файлу лога
    log_path = os.path.join(log_dir, log_file)

    # Создаем логгер
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Очищаем старые обработчики, чтобы не дублировались
    if logger.handlers:
        logger.handlers.clear()

    # Создаем файловый обработчик (с перезаписью при каждом запуске)
    file_handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
    file_handler.setLevel(level)

    # Создаем форматтер
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(formatter)

    # Добавляем обработчик к логгеру
    logger.addHandler(file_handler)

    return logger
