import pytest
from src.core.config import load_config
from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_config_validation_error_secret():
    with pytest.raises(ValueError):
        load_config("tests/mock_configs/invalid_config_secret.json")


def test_config_validation_error_max_bytes():
    with pytest.raises(ValueError):
        load_config("tests/mock_configs/invalid_config_max_bytes.json")


def test_config_validation_error_hmac_alg():
    with pytest.raises(ValueError):
        load_config("tests/mock_configs/invalid_config_hmac_alg.json")


def test_config_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_config("non_existent.json")
