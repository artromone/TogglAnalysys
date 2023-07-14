import datetime
import os

import gspread


def convert_millisec_to_hours(milliseconds):
    seconds = milliseconds / 1000
    minutes = seconds / 60
    hours = minutes / 60
    rounded_hours = int(hours * 1000) / 1000
    return rounded_hours


def get_previous_week_dates():
    today = datetime.date.today()
    current_weekday = today.weekday()
    start_of_week = today - datetime.timedelta(days=current_weekday + 7)
    start_date = start_of_week.strftime("%Y-%m-%d")
    end_of_week = today - datetime.timedelta(days=current_weekday + 1)
    end_date = end_of_week.strftime("%Y-%m-%d")
    return start_date, end_date


def get_range_data(workspace_id, start_date, end_date):
    return {
        'user_agent': 'TogglPy',
        'workspace_id': workspace_id,
        'since': start_date.strftime("%Y-%m-%d"),
        'until': end_date.strftime("%Y-%m-%d"),
    }


def read_service_account():
    credentials_file = os.path.abspath("../credentials/service_account.json")
    return gspread.service_account(filename=credentials_file)


def get_assist_list(sheet):
    return sheet.col_values(1)[4:]
