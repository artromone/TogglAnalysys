import os
import fitz
from toggl.TogglPy import Toggl

from datetime import datetime
from src import credentials
from src.api import *


def main():
    api_key, workspace_id, file_name = "", "", ""

    try:
        api_key, workspace_id, file_name = credentials.read_credentials()
    except Exception as e:
        logger.error(f"An error occurred: {e}")

    toggl = Toggl()
    toggl.setAPIKey(api_key)

    logger.debug(f"API Key: {api_key}")
    logger.debug(f"Workspace ID: {workspace_id}")
    logger.debug(f"Assistant: {file_name}")
    logger.debug("")

    # workspace = select_workspace(get_user_workspaces(toggl), workspace_id)

    data = {
        'workspace_id': int(workspace_id),
        'since': '2024-01-29',
        'until': '2024-02-04',
    }

    since_date = datetime.strptime(data['since'], '%Y-%m-%d').strftime('%d.%m.%y')
    until_date = datetime.strptime(data['until'], '%Y-%m-%d').strftime('%d.%m.%y')
    file_name = since_date + "_" + until_date + "_" + file_name + ".pdf"

    toggl.getSummaryReportPDF(data, "_" + file_name)

    doc = fitz.open("_" + file_name)
    doc.save(file_name, garbage=4, deflate=True)
    doc.close()
    os.remove("_" + file_name)


if __name__ == "__main__":
    singleton_logger_instance = SingletonLogger()
    singleton_logger_instance.setup_logger()
    logger = singleton_logger_instance.instance()

    logger.debug("LOG STARTED")
    logger.debug("")

    main()
