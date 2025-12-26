"""Module with config utils"""

import json
import os
import base64
import threading
from typing import NamedTuple

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_config_instance = None
_config_lock = threading.Lock()


class Config(NamedTuple):
    """Модель конфигурации приложения."""

    hmac_alg: str
    secret_key: bytes
    log_level: str
    listen: str
    max_msg_size_bytes: int


def load_config(path: str = "config.json") -> Config:
    """Загружает и валидирует конфигурацию."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Файл конфигурации не найден: {path}")

    with open(path, "r") as f:
        data: dict = json.load(f)

    if data.get("hmac_alg", "").upper() != "SHA256":
        raise ValueError("hmac_alg должен быть 'SHA256'")

    secret_str = data.get("secret")
    if not secret_str:
        raise ValueError("Поле 'secret' не найдено в конфиге.")

    try:
        secret_bytes = base64.b64decode(secret_str)
    except Exception as e:
        raise ValueError(
            f"Ошибка декодирования секрета (ожидается base64): {e}"
        )

    if len(secret_bytes) < 16 and len(secret_bytes) > 32:
        raise ValueError("Длина секрета должна быть от 16 до 32 байт.")

    try:
        max_msg_size_bytes = int(data.get("max_msg_size_bytes", 1048576))
    except (TypeError, ValueError):
        raise ValueError("Невалидное значение для 'max_msg_size_bytes'.")

    return Config(
        hmac_alg=data["hmac_alg"],
        secret_key=secret_bytes,
        log_level=data.get("log_level", "info").upper(),
        listen=data.get("listen", "0.0.0.0:8080"),
        max_msg_size_bytes=max_msg_size_bytes,
    )


def get_config() -> Config:
    global _config_instance
    if _config_instance is None:
        with _config_lock:
            if _config_instance is None:
                _config_instance = load_config()
    return _config_instance


_config_instance = get_config()
