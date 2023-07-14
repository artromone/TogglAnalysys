import datetime
from toggl.TogglPy import Toggl
import credentials
import gsheet
import utils


def print_detailed_report(toggl, workspace_id, sheet_id):
    left_date = datetime.date(2021, 12, 27)
    start_date = datetime.date(2021, 12, 27)  # datetime.date(2022, 12, 26)
    count = 0  # utils.adjust_count(left_date, start_date)
    retry_rate = 5

    current_date = datetime.date.today()

    gc = utils.read_service_account()
    sheet = gc.open_by_key(sheet_id).sheet1
    assist_list = utils.get_assist_list(sheet)

    while start_date <= current_date:
        end_date = start_date + datetime.timedelta(days=6)
        data = utils.get_range_data(workspace_id, start_date, end_date)

        report = toggl.getDetailedReport(data)
        report_data = report['data']

        # cell_date = read_cell_data(sheet, 3, count + 5, retry_rate)

        for entry in report_data:
            project_name = entry['project']
            duration = entry['dur']

            process_report_entry(project_name, duration, assist_list, sheet, count, retry_rate)

        start_date += datetime.timedelta(weeks=1)
        count += 1


def process_report_entry(project_name, duration, assist_list, sheet, count, retry_rate):
    for i, cell_value in enumerate(assist_list):
        if cell_value == project_name:
            cell_row = i + 5
            cell_column = count + 5

            # cell_date = gsheet.read_cell_data(sheet, 3, cell_column, retry_rate)
            # if cell_date is None:
            #    break

            cell = gsheet.read_cell_data(sheet, cell_row, cell_column, retry_rate)
            if cell is None or cell.value is None:
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
            gsheet.write_cell_data(sheet, cell_row, cell_column, str(current_value), retry_rate)


def main():
    read_credentials = credentials.read_credentials()
    api_key, workspace_id, project_name, sheet_id = read_credentials
    toggl = Toggl()
    toggl.setAPIKey(api_key)

    print_detailed_report(toggl, workspace_id, sheet_id)


if __name__ == "__main__":
    main()
