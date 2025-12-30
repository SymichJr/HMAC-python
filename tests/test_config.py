import pytest

from fastapi.testclient import TestClient

from src.app import app
from src.core.config import load_config

client = TestClient(app)


def test_config_validation_error_secret(mock_configs_path):
    with pytest.raises(ValueError):
        load_config(f"{mock_configs_path}/invalid_config_secret.json")


def test_config_validation_error_max_bytes(mock_configs_path):
    with pytest.raises(ValueError):
        load_config(f"{mock_configs_path}/invalid_config_max_bytes.json")


def test_config_validation_error_hmac_alg(mock_configs_path):
    with pytest.raises(ValueError):
        load_config(f"{mock_configs_path}/invalid_config_hmac_alg.json")


def test_config_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_config("non_existent.json")
