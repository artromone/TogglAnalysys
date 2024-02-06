from toggl.TogglPy import Toggl

from src import credentials
from src.api import *
from src.files import *


def main():

    try:
        api_key, workspace_id, file_name = credentials.read_credentials()
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    toggl = Toggl()
    toggl.setAPIKey(api_key)

    print(f"API Key: {api_key}")
    print(f"Workspace ID: {workspace_id}")
    print(f"Assistant: {file_name}")
    print()

    workspace = select_workspace_by_id(get_user_workspaces(toggl), workspace_id)

    since_date = "2024-02-01"

    generate_report(toggl, workspace_id, since_date, file_name)


if __name__ == "__main__":
    main()
