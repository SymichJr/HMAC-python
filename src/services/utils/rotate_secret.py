import os
import json
import secrets
import sys
import base64

CONFIG_FILE = "config.json"


def generate_secret(length_bytes: int = 32) -> str:
    secret_bytes = secrets.token_bytes(length_bytes)
    return base64.b64encode(secret_bytes).decode("ascii")


def rotate_secret(config_path: str = CONFIG_FILE, key_length: int = 32):

    if not os.path.exists(config_path):
        return "Отсуствует файл конфигурации"

    try:
        with open(config_path, "r") as f:
            config_data = json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        return f"Ошибка чтения файла конфигурации, {e}"

    new_secret = generate_secret(key_length)

    config_data["secret"] = new_secret

    try:
        old_mode = (
            os.stat(config_path).st_mode
            if os.path.exists(config_path)
            else None
        )
        with open(config_path, "w") as f:
            json.dump(config_data, f, indent=2)

        if sys.platform == "win32":
            print(
                "Настройте права доступа к файлу "
                "конфига в ручную на системе win32"
            )
            os._exit(1)
        if hasattr(os, "chmod") and old_mode is not None:
            new_mode = 0o600
            os.chmod(config_path, new_mode)

    except (IOError, OSError) as e:
        return f"Ошбика записи нового секрета, {e}"


rotate_secret()
