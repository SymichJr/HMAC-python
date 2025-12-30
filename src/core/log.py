import logging
import os
from typing import Optional

from src.core.config import BASE_DIR, Config, _config_instance

logger = logging.getLogger("hmac-service")


def setup_logging(config: Config, logger: logging.Logger):
    secret_len = len(config.secret_key)

    log_level = config.log_level.upper()
    try:
        level = logging._nameToLevel[log_level]
    except KeyError:
        level = logging.INFO
        logger.warning(
            f"Невалидный log_level '{config.log_level}'. Установлен 'INFO'."
        )

    logger.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    os.makedirs(f"{BASE_DIR}/logs/", exist_ok=True)
    fh = logging.FileHandler(f"{BASE_DIR}/logs/global.log", encoding="UTF-8")
    fh.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(fh)

    logger.info("--- Сервис HMAC-SHA256 стартует ---")
    logger.info(f"Логирование настроено. Уровень: {config.log_level.upper()}")
    logger.info(f"Конфигурация загружена. Длина секрета: {secret_len} байт.")
    logger.info(f"Макс. размер сообщения: {config.max_msg_size_bytes} байт.")


setup_logging(config=_config_instance, logger=logger)


def log_hmac_operation(
    operation: str, msg_len: int, status: str, details: Optional[str] = None
):
    log_msg = (
        f"Operation={operation}, Status={status}, Msg_Len={msg_len} bytes"
    )
    if details:
        log_msg += f", Details='{details}'"
    if status == "FAIL":
        logger.error(log_msg)
    elif status == "SUCCESS":
        logger.info(log_msg)
    else:
        logger.debug(log_msg)
