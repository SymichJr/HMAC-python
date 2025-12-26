from fastapi.testclient import TestClient
from http import HTTPStatus

from src.app import app

client = TestClient(app)


def test_full_client_success(sign_url, verify_url):
    msg = "hello world"
    responce_sign = client.post(url=sign_url, json={"msg": msg})
    assert responce_sign.status_code == HTTPStatus.OK
    sig = responce_sign.json()["signature"]
    response_verify = client.post(
        url=verify_url, json={"msg": msg, "signature": sig}
    )
    assert response_verify.status_code == HTTPStatus.OK
    assert response_verify.json() == {"ok": True}


def test_invalid_signature_format(verify_url):
    response = client.post(
        url=verify_url, json={"msg": "hello", "signature": "@@@"}
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "invalid_signature_format"


def test_sign(sign_url):
    msg = "@@@@@"
    responce_sign = client.post(url=sign_url, json={"msg": msg})
    assert responce_sign.status_code == HTTPStatus.OK


def test_unsupported_media_type_sign(sign_url):
    response = client.post(
        url=sign_url,
        content="plain text",
        headers={"Content-Type": "text/plain"},
    )
    assert response.status_code == HTTPStatus.UNSUPPORTED_MEDIA_TYPE


def test_unsupported_media_type_verify(verify_url):
    response = client.post(
        url=verify_url,
        content="plain text",
        headers={"Content-Type": "text/plain"},
    )
    assert response.status_code == HTTPStatus.UNSUPPORTED_MEDIA_TYPE


def test_payload_too_large_sign(sign_url):
    big_msg = "a" * (1024 * 1024 + 1)
    response = client.post(url=sign_url, json={"msg": big_msg})
    assert response.status_code == HTTPStatus.REQUEST_ENTITY_TOO_LARGE


def test_payload_too_large_verify(verify_url):
    big_msg = "a" * (1024 * 1024 + 1)
    response = client.post(
        url=verify_url,
        json={
            "msg": big_msg,
            "signature": "RyhD--ParT8TcY22-2_Le0BxmMkhOv8uyJv_M0apUw",
        },
    )
    assert response.status_code == HTTPStatus.REQUEST_ENTITY_TOO_LARGE


def test_empty_msg_sign(sign_url):
    response = client.post(url=sign_url, json={"msg": ""})
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_empty_msg_verify(verify_url):
    response = client.post(
        url=verify_url,
        json={
            "msg": "",
            "signature": "RyhD--ParT8TcY22-2_Le0BxmMkhOv8uyJv_M0apUw",
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_no_signature(verify_url):
    msg = "no signature"
    responce = client.post(url=verify_url, json={"msg": msg})
    assert responce.status_code == HTTPStatus.BAD_REQUEST


def test_changed_signature(sign_url, verify_url):
    msg = "hello world"
    responce_sign = client.post(url=sign_url, json={"msg": msg})
    assert responce_sign.status_code == HTTPStatus.OK
    sig = responce_sign.json()["signature"] + "i"
    response_verify = client.post(
        url=verify_url, json={"msg": msg, "signature": sig}
    )
    assert response_verify.status_code == HTTPStatus.OK
    assert response_verify.json() == {"ok": False}


def test_changed_msg(sign_url, verify_url):
    msg = "hello world"
    responce_sign = client.post(url=sign_url, json={"msg": msg})
    assert responce_sign.status_code == HTTPStatus.OK
    sig = responce_sign.json()["signature"]
    changed_msg = msg + "!"
    response_verify = client.post(
        url=verify_url, json={"msg": changed_msg, "signature": sig}
    )
    assert response_verify.status_code == HTTPStatus.OK
    assert response_verify.json() == {"ok": False}
