import datetime

from toggl.TogglPy import Toggl
from credentials import read_credentials
from files import generate_report
import os

from api import select_workspace_by_name


# from libs.toggl_target.togglapi.api import TogglAPI


def find_id_by_name(data, name):
    for item in data:
        if item['name'] == name:
            return item['id']
    return None

def generate_user_report(filename, since_date):
    api_key, workspace_id, file_name, rph = read_credentials(filename)

    toggl = Toggl()
    toggl.setAPIKey(api_key)

    # offset = datetime.timedelta(hours=3)
    # tz = datetime.timezone(offset, name='МСК')
    # TogglAPI(toggl, tz)

    # if file_name == "test":
    #     workspace = select_workspace_by_name(toggl.getWorkspaces(), "FavorIT_Assistants")
    #     # TogglAPI.get_time_entries()
    #
    #
    #     cl = toggl.getClients()
    #     pr = toggl.getClientProjects(find_id_by_name(cl, "Artem_Romanovich"))
    #
    #     print(pr)
    #     print(toggl.getProjectTasks(pr[0]['id']))

    generate_report(toggl, workspace_id, rph, file_name, since_date)


def generate_all_reports(since_date):
    directory = 'credentials'

    if not os.path.exists(directory):
        os.makedirs(directory)

    files = os.listdir(directory)

    if len(files) == 0:
        raise FileNotFoundError(f"Файлы для аутентификации не найдены в директории: {os.path.abspath(directory)}")

    for filename in files:
        generate_user_report(filename, since_date)
