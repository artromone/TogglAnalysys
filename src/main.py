from toggl.TogglPy import Toggl
import credentials
from src.project import *


#import gsheet


def main():

    try:
        read_credentials = credentials.read_credentials()
    except Exception as e:
        print("No credentials found: " + str(e))
        return

    api_key, workspace_id, project_name, sheet_id = read_credentials
    toggl = Toggl()
    toggl.setAPIKey(api_key)

    pr = get_project_by_name(toggl, read_credentials, "1")
    print_project_actual_hours(pr)

    #gsheet.fill_weeks_durations(toggl, workspace_id, sheet_id)


if __name__ == "__main__":
    main()
