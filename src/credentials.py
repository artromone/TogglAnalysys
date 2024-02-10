import os
import configparser


def read_credentials(file_name):
    config = configparser.ConfigParser()
    credentials_file_path = os.path.abspath("credentials/" + file_name)

    if not os.path.exists(credentials_file_path):
        raise FileNotFoundError(f"Файл аутентификации не найдены в директории: {credentials_file_path}")

    config.read(credentials_file_path)

    required_keys = ["api_key", "workspace_id", "file_name", "rph"]
    credentials = {}

    for key in required_keys:
        try:
            credentials[key] = config.get("credentials", key)
        except configparser.NoOptionError:
            raise ValueError(f"Отсутствует {key} в файлах для аутентификации")

    return tuple(credentials.values())
