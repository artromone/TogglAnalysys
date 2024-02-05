from src.log import SingletonLogger


def get_user_workspaces(toggl_instance):
    workspaces = toggl_instance.getWorkspaces()
    return workspaces


def select_workspace(workspaces, workspace_id):
    # singleton_logger_instance = SingletonLogger()
    # singleton_logger_instance.setup_logger()
    # logger = singleton_logger_instance.instance()
    print("Workspaces:")

    for workspace in workspaces:
        print(f"  - {workspace['name']} (ID: {workspace['id']})")

        if workspace['id'] == int(workspace_id):
            print(f"Selected workspace: {workspace['name']} (ID: {workspace['id']})")
            return workspace

    raise ValueError(f"Workspace '{workspace_id}' not found.")
