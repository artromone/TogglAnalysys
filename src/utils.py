import datetime


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
