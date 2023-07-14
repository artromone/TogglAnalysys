def write_assists_gsheet(toggl, workspace_id, sheet_id):
    start_date = datetime.date(2023, 12, 27)
    yesterday_date = start_date + datetime.timedelta(days=20)
    data = utils.get_range_data(workspace_id, start_date, yesterday_date)
    report_data = toggl.getDetailedReport(data)

    print(report_data)

    if 'total_grand' not in report_data:
        print("Error: 'total_grand' key is missing in the credentials dictionary.")
        return

    gc = gspread.service_account(filename="../credentials/service_account.json")
    sheet = gc.open_by_key(sheet_id).sheet1

    existing_projects = sheet.col_values(1)[4:]

    new_projects = list(set([entry['project'] for entry in report_data['data']]) - set(existing_projects))

    start_row = len(existing_projects) + 5

    for project_name in new_projects:
        sheet.update_cell(start_row, 1, project_name)
        start_row += 1

