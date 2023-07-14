import time

import gspread
from toggl.TogglPy import Toggl
import datetime


def read_credentials():
    api_key = ""
    workspace_id = ""
    project_name = ""
    sheet_id = ""
    sheet_api_key = ""

    with open("credentials.txt", "r") as file:
        for line in file:
            if line.startswith("api_key"):
                api_key = line.split('"')[1]
            elif line.startswith("workspace_id"):
                workspace_id = line.split('"')[1]
            elif line.startswith("project_name"):
                project_name = line.split('"')[1]
            elif line.startswith("sheet_id"):
                sheet_id = line.split('"')[1]
            elif line.startswith("sheet_api_key"):
                sheet_api_key = line.split('"')[1]

    return api_key, workspace_id, project_name, sheet_id, sheet_api_key


def get_project_info(api_key, workspace_id, project_name, toggl):
    params = {
        "actual_hours": "true"
    }

    response = toggl.request(f"https://api.track.toggl.com/api/v8/workspaces/{workspace_id}/projects",
                             parameters=params)

    for project in response:
        if project_name == project['name']:
            actual_hours = project.get('actual_hours')
            print(f"Название проекта: {project_name}")
            if actual_hours is not None:
                print(f"Фактически отработанные часы: {actual_hours}")
            else:
                print("Фактически отработанных часов не указано")
            print()
            break
    else:
        print(f"Проект с названием '{project_name}' не найден")


def convert_millisec_to_hours(milliseconds):
    seconds = milliseconds / 1000
    minutes = seconds / 60
    hours = minutes / 60
    rounded_hours = int(hours * 1000) / 1000
    return rounded_hours


def print_detailed_report(workspace_id, sheet_id):
    toggl = Toggl()

    start_date = datetime.date(2021, 12, 27)
    count = 0
    start_date = datetime.date(2022, 12, 26)
    count = 48
    current_date = datetime.date.today()

    gc = gspread.service_account(filename="service_account.json")
    spreadsheet = gc.open_by_key(sheet_id)
    sheet = spreadsheet.sheet1

    assist_list = sheet.col_values(1)[4:]

    retry_rate = 5

    while start_date <= current_date:
        end_date = start_date + datetime.timedelta(days=6)
        data = {
            'user_agent': 'TogglPy',
            'workspace_id': workspace_id,
            'since': start_date.strftime("%Y-%m-%d"),
            'until': end_date.strftime("%Y-%m-%d"),
        }

        report = toggl.getDetailedReport(data)

        report_data = report['data']

        while True:
            try:
                cell_date = sheet.cell(3, count + 5).value
                break
            except Exception as e:
                # print("An error occurred while retrieving the cell_date:", e)
                # print("Retrying after " + str(retry_rate) + " seconds...")
                time.sleep(retry_rate)

        # time.sleep(5)

        for entry in report_data:
            project_name = entry['project']
            duration = entry['dur']

            for i, cell_value in enumerate(assist_list):

                if cell_value == project_name and start_date.strftime("%d.%m.%y") == cell_date:
                    cell_row = i + 5
                    cell_column = count + 5

                    while True:
                        try:
                            cell = sheet.cell(cell_row, cell_column)
                            if cell.value is None:
                                if duration == 0:
                                    break
                                current_value = 0
                            else:
                                current_value = float(cell.value.replace(',', '.'))

                            hour_duration = convert_millisec_to_hours(duration)
                            if current_value:
                                current_value += hour_duration
                            else:
                                current_value = hour_duration

                            current_value = int(current_value * 1000) / 1000
                            cell.value = str(current_value)
                            sheet.update_cell(cell_row, cell_column, str(current_value))

                            break
                        except gspread.exceptions.APIError as e:
                            if e.response.status_code == 429:
                                # print("Retrying after " + str(retry_rate) + " seconds...")
                                time.sleep(retry_rate)
                            else:
                                print("An error occurred while updating the cell:", e)
                                break

        start_date += datetime.timedelta(weeks=1)
        count += 1


def write_assists_gsheet(toggl, workspace_id, sheet_id):
    start_date = datetime.date(2021, 12, 27)
    yesterday_date = start_date + datetime.timedelta(days=1)
    data_ = {
        'user_agent': 'TogglPy',
        'workspace_id': workspace_id,
        'since': start_date.strftime("%Y-%m-%d"),
        'until': yesterday_date.strftime("%Y-%m-%d"),
    }
    data = toggl.getDetailedReport(data_)

    if 'total_grand' not in data:
        print("Error: 'total_grand' key is missing in the data dictionary.")
        return

    gc = gspread.service_account(filename="service_account.json")
    sheet = gc.open_by_key(sheet_id).sheet1

    existing_projects = sheet.col_values(1)[4:]

    new_projects = list(set([entry['project'] for entry in data['data']]) - set(existing_projects))

    start_row = len(existing_projects) + 5

    for project_name in new_projects:
        sheet.update_cell(start_row, 1, project_name)
        start_row += 1


def get_previous_week_dates():
    today = datetime.date.today()
    current_weekday = today.weekday()
    start_of_week = today - datetime.timedelta(days=current_weekday + 7)
    start_date = start_of_week.strftime("%Y-%m-%d")
    end_of_week = today - datetime.timedelta(days=current_weekday + 1)
    end_date = end_of_week.strftime("%Y-%m-%d")
    return start_date, end_date


def main():
    api_key, workspace_id, project_name, sheet_id, sheet_api_key = read_credentials()
    toggl = Toggl()
    toggl.setAPIKey(api_key)
    # get_project_info(api_key, workspace_id, project_name, toggl)

    start_date, end_date = get_previous_week_dates()

    print_detailed_report(workspace_id, sheet_id)

    # write_assists_gsheet(toggl, workspace_id, sheet_id)


if __name__ == "__main__":
    main()
