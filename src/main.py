from toggl.TogglPy import Toggl

from src import credentials
from src.api import get_user_workspaces, select_workspace
from src.log import SingletonLogger


def main():

    api_key, workspace_id, project_name, sheet_id = "", "", "", ""

    try:
        api_key, workspace_id, project_name, sheet_id = credentials.read_credentials()
    except Exception as e:
        logger.error(f"An error occurred: {e}")

    toggl = Toggl()
    toggl.setAPIKey(api_key)

    logger.debug(f"API Key: {api_key}")
    logger.debug(f"Workspace ID: {workspace_id}")
    logger.debug(f"Project Name: {project_name}")
    logger.debug("")

    workspaces = select_workspace(get_user_workspaces(toggl), workspace_id)


if __name__ == "__main__":

    singleton_logger_instance = SingletonLogger()
    singleton_logger_instance.setup_logger()
    logger = singleton_logger_instance.instance()

    logger.debug("LOG STARTED")
    logger.debug("")

    main()
