from toggl.TogglPy import Toggl
import credentials
import gsheet


def main():
    read_credentials = credentials.read_credentials()
    api_key, workspace_id, project_name, sheet_id = read_credentials
    toggl = Toggl()
    toggl.setAPIKey(api_key)

    gsheet.fill_weeks_durations(toggl, workspace_id, sheet_id)


if __name__ == "__main__":
    main()
