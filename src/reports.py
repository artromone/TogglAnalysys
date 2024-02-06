from toggl.TogglPy import Toggl
from credentials import read_credentials
from files import generate_report
import os

def generate_user_report(filename, since_date):
    api_key, workspace_id, file_name = read_credentials(filename)

    toggl = Toggl()
    toggl.setAPIKey(api_key)

    generate_report(toggl, workspace_id, file_name, since_date)


def generate_all_reports(since_date):

    directory = 'credentials'

    if not os.path.exists(directory):
        os.makedirs(directory)

    files = os.listdir(directory)

    for filename in files:
        generate_user_report(filename, since_date)


