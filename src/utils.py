def convert_millisec_to_hours(milliseconds):
    seconds = milliseconds / 1000
    minutes = seconds / 60
    hours = minutes / 60
    rounded_hours = int(hours * 1000) / 1000
    return rounded_hours
