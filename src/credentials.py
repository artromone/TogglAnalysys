import configparser


def read_credentials():
    config = configparser.ConfigParser()
    config.read("../data/credentials.txt")

    api_key = "api_key"
    workspace_id = "workspace_id"
    project_name = "project_name"
    sheet_id = "sheet_id"

    credentials = {
        api_key: config.get("credentials", api_key),
        workspace_id: config.get("credentials", workspace_id),
        project_name: config.get("credentials", project_name),
        sheet_id: config.get("credentials", sheet_id),
    }

    return tuple(credentials.values())
