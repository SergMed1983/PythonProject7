import logging

from src.logger_config import setup_logger

# Создаем логгер для модуля masks
logger = setup_logger('masks', 'masks.log', logging.DEBUG)


def mask_card_number(card_number: str) -> str:
    """Маскирует номер карты (видит только первые 6 и последние 4 цифры)"""
    try:
        logger.debug(f"Попытка маскировки номера карты: {card_number[:4]}****")

        if not card_number or len(card_number) < 16:
            raise ValueError("Неверный формат номера карты")

        # Логика маскировки
        masked = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"

        logger.info(f"Номер карты успешно замаскирован: {masked}")
        return masked

    except Exception as e:
        logger.error(f"Ошибка маскировки номера карты: {e}", exc_info=True)
        raise


def mask_account_number(account_number: str) -> str:
    """Маскирует номер счета (видит только последние 4 цифры)"""
    try:
        logger.debug(f"Попытка маскировки номера счета: {account_number[:4]}****")

        if not account_number or len(account_number) < 4:
            raise ValueError("Неверный формат номера счета")

        masked = f"**{account_number[-4:]}"

        logger.info(f"Номер счета успешно замаскирован: {masked}")
        return masked

    except Exception as e:
        logger.error(f"Ошибка маскировки номера счета: {e}", exc_info=True)
        raise
