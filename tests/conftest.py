import pytest


@pytest.fixture(scope="session")
def base_route_v1():
    """Базовый префикс API."""
    return "/api/v1/hmac_sign"


@pytest.fixture(scope="session")
def sign_url(base_route_v1):
    """Полный путь для подписи."""
    return f"{base_route_v1}/sign"


@pytest.fixture(scope="session")
def verify_url(base_route_v1):
    """Полный путь для проверки."""
    return f"{base_route_v1}/verify"
