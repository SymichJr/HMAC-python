import hmac
from src.services.hmac_service import HMACSigner


def test_determinism():
    signer = HMACSigner()
    msg = "hello"
    assert signer.sign(msg) == signer.sign(msg)


def test_verify_integrity():
    signer = HMACSigner()
    msg = "hello"
    sig = signer.sign(msg)

    assert signer.verify(msg, sig) is True
    assert signer.verify("hallo", sig) is False
    assert (
        signer.verify(msg, "RyhD--ParT8TcY22-2_Le0BxmMkhOv8uyJv_M0apUw")
        is False
    )


def test_constant_time_usage(mocker):
    spy = mocker.spy(hmac, "compare_digest")
    signer = HMACSigner()
    signer.verify("msg", "sig")
    assert spy.called
