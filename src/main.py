from toggl.TogglPy import Toggl

from src import credentials
from src.log import setup_logger


def main():

    try:

        api_key, workspace_id, project_name, sheet_id = credentials.read_credentials()
        toggl = Toggl()
        toggl.setAPIKey(api_key)

        logger.debug(f"API Key: {api_key}")
        logger.debug(f"Workspace ID: {workspace_id}")
        logger.debug(f"Project Name: {project_name}")

    except Exception as e:

        logger.error(f"An error occurred: {e}")


if __name__ == "__main__":

    logger = setup_logger()
    logger.debug("LOG STARTED")
    logger.debug("")

    main()
