import os
import configparser


def read_credentials(file_name):
    config = configparser.ConfigParser()
    credentials_file_path = os.path.abspath("../credentials/" + file_name)

    if not os.path.exists(credentials_file_path):
        raise FileNotFoundError(f"Credentials file not found at: {credentials_file_path}")

    config.read(credentials_file_path)

    required_keys = ["api_key", "workspace_id", "file_name"]
    credentials = {}

    for key in required_keys:
        try:
            credentials[key] = config.get("credentials", key)
        except configparser.NoOptionError:
            raise ValueError(f"Missing {key} in the credentials file")

    return tuple(credentials.values())
