import time
import gspread
import credentials
import utils
import project
from toggl.TogglPy import Toggl
import datetime


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

        report_data = report['credentials']

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

                            hour_duration = utils.convert_millisec_to_hours(duration)
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


def main():
    read_credentials = credentials.read_credentials()
    api_key, workspace_id, project_name, sheet_id = read_credentials
    toggl = Toggl()
    toggl.setAPIKey(api_key)


if __name__ == "__main__":
    main()
