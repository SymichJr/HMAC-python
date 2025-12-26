"""Module with HMAC sign functions"""

import hmac
import hashlib

from src.core.config import _config_instance
from src.core.log import log_hmac_operation
from src.services.utils.codec import base64_decode, base64_encode


class HMACSigner:
    """Class for HMAC sign and verify signature"""

    def __init__(self):
        self._key: bytes = _config_instance.secret_key
        self._hash_alg = hashlib.sha256

    def sign(self, msg: str) -> str:
        msg_bytes = msg.encode("utf-8")
        msg_len = len(msg_bytes)
        signature_bytes = hmac.new(
            self._key, msg_bytes, self._hash_alg
        ).digest()
        signature_b64url = base64_encode(signature_bytes)
        log_hmac_operation("SIGN", msg_len, "SUCCESS")

        return signature_b64url

    def verify(self, msg: str, signature: str) -> bool:
        msg_bytes = msg.encode("utf-8")
        msg_len = len(msg_bytes)

        input_signature_bytes: bytes
        try:
            input_signature_bytes = base64_decode(signature)
        except ValueError as e:
            log_hmac_operation(
                "VERIFY",
                msg_len,
                "FAIL",
                details=f"400: invalid_signature_format. Error: {e}",
            )
            raise

        recalculated_signature_bytes = hmac.new(
            self._key, msg_bytes, self._hash_alg
        ).digest()

        result = hmac.compare_digest(
            recalculated_signature_bytes, input_signature_bytes
        )

        if result:
            log_hmac_operation("VERIFY", msg_len, "SUCCESS")
        else:
            log_hmac_operation(
                "VERIFY", msg_len, "FAIL", "Mismatched signature"
            )
        return result


def get_hmac_service() -> HMACSigner:
    return HMACSigner()
