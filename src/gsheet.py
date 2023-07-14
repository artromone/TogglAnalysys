import datetime
import time
import gspread

# from log import logging as log
import utils


def open_sheet_by_key(sheet_id, retry_rate):
    while True:
        try:
            gc = utils.read_service_account()
            return gc.open_by_key(sheet_id).sheet1
        except gspread.exceptions.APIError as e:
            # log.warning("An error occurred while opening the sheet:", e)
            # log.warning("Retrying after " + str(retry_rate) + " seconds...")
            time.sleep(retry_rate)


def read_cell_data(sheet, row, col, retry_rate):
    while True:
        try:
            return sheet.cell(row, col).value
        except Exception as e:
            # log.warning("An error occurred while retrieving the cell data:", e)
            # log.warning("Retrying after " + str(retry_rate) + " seconds...")
            time.sleep(retry_rate)


def write_cell_data(sheet, row, col, value, retry_rate):
    while True:
        try:
            cell = sheet.cell(row, col)
            cell.value = value
            sheet.update_cell(row, col, value)
            break
        except Exception as e:
            # log.warning("An error occurred while updating the cell data:", e)
            # log.warning("Retrying after " + str(retry_rate) + " seconds...")
            time.sleep(retry_rate)


def write_week(project_name, duration, assist_list, sheet, count, retry_rate):
    for i, cell_value in enumerate(assist_list):
        if cell_value == project_name:
            cell_row = i + 5
            cell_column = count + 5

            cell_value = read_cell_data(sheet, cell_row, cell_column, retry_rate)

            if cell_value is None:
                if duration == 0:
                    break
                current_value = 0
            else:
                current_value = float(cell_value.replace(',', '.'))

            hour_duration = utils.convert_millisec_to_hours(duration)
            if current_value:
                current_value += hour_duration
            else:
                current_value = hour_duration

            current_value = int(current_value * 1000) / 1000
            write_cell_data(sheet, cell_row, cell_column, str(current_value), retry_rate)


def fill_weeks_durations(toggl, workspace_id, sheet_id):
    # start_date = datetime.date(2021, 12, 27)
    # count = 0
    start_date = datetime.date(2022, 12, 26)
    count = 48
    current_date = datetime.date.today()

    retry_rate = 5

    sheet = open_sheet_by_key(sheet_id, retry_rate)
    assist_list = utils.get_assist_list(sheet)

    while start_date <= current_date:
        end_date = start_date + datetime.timedelta(days=6)
        data = utils.get_range_data(workspace_id, start_date, end_date)

        report = toggl.getDetailedReport(data)
        report_data = report['data']

        for entry in report_data:
            project_name = entry['project']
            duration = entry['dur']

            write_week(project_name, duration, assist_list, sheet, count, retry_rate)

        start_date += datetime.timedelta(weeks=1)
        count += 1
