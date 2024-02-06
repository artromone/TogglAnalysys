def get_user_workspaces(toggl_instance):
    workspaces = toggl_instance.getWorkspaces()
    return workspaces


def display_workspaces(workspaces):
    print("Workspaces:")
    for workspace in workspaces:
        print(f"  - {workspace['name']} (ID: {workspace['id']})")


def select_workspace_by_id(workspaces, workspace_id):
    display_workspaces(workspaces)
    for workspace in workspaces:
        if workspace['id'] == int(workspace_id):
            print(f"Selected workspace: {workspace['name']} (ID: {workspace['id']})")
            return workspace
    raise ValueError(f"Workspace '{workspace_id}' not found.")


def select_workspace_by_name(workspaces, workspace_name):
    display_workspaces(workspaces)
    for workspace in workspaces:
        if workspace['name'] == workspace_name:
            print(f"Selected workspace: {workspace['name']} (ID: {workspace['id']})")
            return workspace
    raise ValueError(f"Workspace '{workspace_name}' not found.")


def create_clients(toggl_instance):
    client_names = ['Client1', 'Client2', 'Client3']

    for client_name in client_names:
        toggl_instance.createClient(client_name)
