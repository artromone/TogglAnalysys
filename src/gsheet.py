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
        except Exception as e:
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
            # cell = sheet.cell(row, col)
            # cell.value = value
            sheet.update_cell(row, col, value)
            break
        except Exception as e:
            # log.warning("An error occurred while updating the cell data:", e)
            # log.warning("Retrying after " + str(retry_rate) + " seconds...")
            time.sleep(retry_rate)


def write_week(project_name, duration, assist_list, sheet, cell_column, retry_rate):
    for i, cell_value in enumerate(assist_list):
        if cell_value == project_name:
            cell_row = i + 5

            cell_value = read_cell_data(sheet, cell_row, cell_column, retry_rate)

            if cell_value is None:
                if duration == 0:
                    break
                current_value = 0
            else:
                current_value = float(cell_value.replace(',', '.'))

            hour_duration = utils.convert_millisec_to_hours(duration)
            current_value += hour_duration
            current_value = int(current_value * 1000) / 1000

            write_cell_data(sheet, cell_row, cell_column, str(current_value), retry_rate)


def fill_weeks_durations(toggl, workspace_id, sheet_id):
    # start_date = datetime.date(2021, 12, 27)
    # cell_column = 0
    start_date = datetime.date(2022, 12, 26)
    cell_column = 48 + 5

    current_date = datetime.date.today()

    retry_rate = 5

    sheet = open_sheet_by_key(sheet_id, retry_rate)
    assist_list = utils.get_assist_list(sheet)
    # print(assist_list) <- ['Maxim Kiselev', 'Konstantin Germanovich', 'Zahar Sotnikov', 'Leonid Melnikov', 'Yaroslav Syatkovsky']

    while start_date <= current_date:
        end_date = start_date + datetime.timedelta(days=6)
        data = utils.get_range_data(workspace_id, start_date, end_date)
        # print(data) <-
        # {'user_agent': 'TogglPy', 'workspace_id': '6900739', 'since': '2023-01-02', 'until': '2023-01-08'}
        # {'user_agent': 'TogglPy', 'workspace_id': '6900739', 'since': '2023-01-09', 'until': '2023-01-15'}
        # {'user_agent': 'TogglPy', 'workspace_id': '6900739', 'since': '2023-01-16', 'until': '2023-01-22'}
        # {'user_agent': 'TogglPy', 'workspace_id': '6900739', 'since': '2023-01-23', 'until': '2023-01-29'}
        # {'user_agent': 'TogglPy', 'workspace_id': '6900739', 'since': '2023-01-30', 'until': '2023-02-05'}
        # ...

        report = toggl.getDetailedReport(data)
        report_data = report['data']
        '''
        print(report_data) <-
        [
        {'id': 2830654406, 'pid': 187773401, 'tid': None, 'uid': 9006322,
           'description': 'Частота выходов постов в пабликах вк', 'start': '2023-02-03T19:02:25+03:00',
           'end': '2023-02-03T19:48:33+03:00', 'updated': '2023-02-03T19:48:34+03:00', 'dur': 2768000,
           'user': 'Maestrowork522', 'use_stop': False, 'client': None, 'project': 'Maxim Kiselev', 'project_color': '0',
           'project_hex_color': '#06a893', 'task': None, 'billable': None, 'is_billable': False, 'cur': None,
           'tags': []},
        {'id': 2823149293, 'pid': 187773401, 'tid': None, 'uid': 9006322,
           'description': 'Загрузка видео на YouTube, экспорт WWP', 'start': '2023-01-30T20:42:44+03:00',
           'end': '2023-01-30T20:55:37+03:00', 'updated': '2023-01-30T21:04:16+03:00', 'dur': 773000,
           'user': 'Maestrowork522', 'use_stop': False, 'client': None, 'project': 'Maxim Kiselev', 'project_color': '0',
           'project_hex_color': '#06a893', 'task': None, 'billable': None, 'is_billable': False, 'cur': None,
           'tags': []},
        {'id': 2823047719, 'pid': 187773401, 'tid': None, 'uid': 9006322,
           'description': 'Загрузка видео на YouTube, экспорт WWP', 'start': '2023-01-30T19:50:09+03:00',
           'end': '2023-01-30T20:00:19+03:00', 'updated': '2023-01-30T20:06:29+03:00', 'dur': 610000,
           'user': 'Maestrowork522', 'use_stop': False, 'client': None, 'project': 'Maxim Kiselev', 'project_color': '0',
           'project_hex_color': '#06a893', 'task': None, 'billable': None, 'is_billable': False, 'cur': None,
           'tags': []}
        ]
           '''

    for task_entry in report_data:
        project_name = task_entry['project']
        duration = task_entry['dur']

        write_week(project_name, duration, assist_list, sheet, cell_column, retry_rate)

    start_date += datetime.timedelta(weeks=1)
    cell_column += 1
