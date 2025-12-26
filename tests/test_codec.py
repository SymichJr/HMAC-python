import pytest
from src.services.utils import codec


def test_base64url_encoding_no_padding():
    data = b"\xff\xfe\xfd"
    encoded = codec.base64_encode(data)
    assert "=" not in encoded
    assert "+" not in encoded
    assert "/" not in encoded


def test_is_valid_base64url():
    assert isinstance(codec.base64_decode("valid-signature_123"), bytes)
    with pytest.raises(ValueError):
        codec.base64_decode("invalid@signature")
    with pytest.raises(ValueError):
        codec.base64_decode("invalid_signature+")
