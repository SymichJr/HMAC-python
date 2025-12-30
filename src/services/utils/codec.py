"""Module with codec functions"""

import base64
import re

from src.core.constants import BLOCK_SIZE, MATCH_B64_SYMBOLS


def base64_encode(data: bytes) -> str:
    if not isinstance(data, bytes):
        raise TypeError("Входные данные должны быть типа bytes.")
    encoded_bytes = base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")
    return encoded_bytes


def base64_decode(b64url_str: str) -> bytes:
    if not isinstance(b64url_str, str):
        raise TypeError("Ожидается строка для декодирования base64url.")
    if not re.fullmatch(MATCH_B64_SYMBOLS, b64url_str):
        raise ValueError("Строка содержит недопустимые символы для Base64URL.")
    b64url_bytes = b64url_str.encode("ascii")
    is_padding_needed = len(b64url_bytes) % BLOCK_SIZE
    if is_padding_needed:
        b64url_bytes += b"=" * (BLOCK_SIZE - is_padding_needed)
    try:
        return base64.urlsafe_b64decode(b64url_bytes)
    except base64.binascii.Error as e:
        raise ValueError(f"Невалидный формат base64url: {e}")
