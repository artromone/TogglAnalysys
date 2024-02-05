import os
import configparser


def read_credentials():
    config = configparser.ConfigParser()
    credentials_file_path = os.path.abspath("../credentials/credentials.txt")

    if not os.path.exists(credentials_file_path):
        raise FileNotFoundError(f"Credentials file not found at: {credentials_file_path}")

    config.read(credentials_file_path)

    required_keys = ["api_key", "workspace_id", "project_name", "sheet_id"]
    credentials = {}

    for key in required_keys:
        try:
            credentials[key] = config.get("credentials", key)
        except configparser.NoOptionError:
            raise ValueError(f"Missing {key} in the credentials file")

    return tuple(credentials.values())
