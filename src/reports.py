from toggl.TogglPy import Toggl
from src import credentials
from src.files import *


def generate_user_report(filename, since_date):
    api_key, workspace_id, file_name = credentials.read_credentials(filename)

    toggl = Toggl()
    toggl.setAPIKey(api_key)

    generate_report(toggl, workspace_id, file_name, since_date)


def generate_all_reports(since_date):

    directory = 'credentials'

    if os.path.exists(directory):
        files = os.listdir(directory)

        for filename in files:
            generate_user_report(filename, since_date)
    else:
        raise Exception("Директории не существует")


