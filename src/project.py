def get_project_by_name(toggl, read_credentials):
    api_key, workspace_id, project_name, sheet_id = read_credentials
    params = {
        "actual_hours": "true"
    }
    url = f"https://api.track.toggl.com/api/v8/workspaces/{workspace_id}/projects"
    response = toggl.request(url, parameters=params)

    project = find_project(response, project_name)
    return project


def find_project(response, project_name):
    for project in response:
        if project_name == project['name']:
            return project
    return None


def print_project_actual_hours(project, project_name):
    if project:
        actual_hours = project.get('actual_hours')
        print(f"Project name: {project_name}")
        if actual_hours is not None:
            print(f"Actual hours worked: {actual_hours}")
        else:
            print("Actual hours worked not specified")
        print()
    else:
        print(f"Project with name '{project_name}' not found")
