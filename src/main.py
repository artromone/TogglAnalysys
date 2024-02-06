from toggl.TogglPy import Toggl
from src import credentials
from src.files import *


def done_user_work(filename):
    try:
        api_key, workspace_id, file_name = credentials.read_credentials(filename)
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    toggl = Toggl()
    toggl.setAPIKey(api_key)

    since_date = "2024-02-01"

    generate_report(toggl, workspace_id, since_date, file_name)


def main():
    for filename in os.listdir("../credentials"):
        done_user_work(filename)


if __name__ == "__main__":
    main()
