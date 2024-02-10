import os
from datetime import datetime, timedelta


# import fitz

def generate_report(toggl_instance, workspace_id, rph, file_name, since_date):
    export_dir = "export"
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)

    # since_date = get_first_day_of_week()
    since_date_str = since_date.toPyDate().strftime('%Y-%m-%d')

    until_date = datetime.strptime(since_date_str, '%Y-%m-%d')
    until_date += timedelta(weeks=1) - timedelta(days=1)
    until_date_str = until_date.strftime('%Y-%m-%d')

    data = {
        'workspace_id': int(workspace_id),
        'since': since_date_str,
        'until': until_date_str,
    }

    since_date_formatted = datetime.strptime(data['since'], '%Y-%m-%d').strftime('%d.%m.%y')
    until_date_formatted = datetime.strptime(data['until'], '%Y-%m-%d').strftime('%d.%m.%y')
    file_name = f"{since_date_formatted}_{until_date_formatted}_{file_name}.pdf"

    # pdf_path_temp = os.path.join(export_dir, f"_{file_name}")
    pdf_path_final = os.path.join(export_dir, file_name)

    # toggl_instance.getWeeklyReportPDF(data, pdf_path_temp)
    # toggl_instance.getSummaryReportPDF(data, pdf_path_temp)
    #    toggl_instance.getDetailedReportPDF(data, pdf_path_final)

    data = toggl_instance.getDetailedReport(data)

    client_work_time = {}
    unspecified_client_time = 0

    for task in data['data']:
        client = task.get('client')
        duration = task['dur']

        if client:
            if client in client_work_time:
                client_work_time[client] += duration
            else:
                client_work_time[client] = duration
        else:
            unspecified_client_time += duration

    print("Суммарное время работы для каждого клиента:")

    first_read = True
    for client, time in client_work_time.items():
        client_file_name = "export/" + client + ".txt"

        time /= 3600_000
        line = client + " : " + str(time) + " s " + str(int(rph) * time) + " rubles.\n"

        try:
            with open(client_file_name, 'x') as f:
                f.write(line)

        except FileExistsError:

            try:
                with open(client_file_name, 'a') as f:
                    print(first_read)
                    if first_read:
                        f.truncate(0)
                        first_read = False
                    f.write(line)
            except Exception as e:
                print("Произошла ошибка:", e)

        except Exception as e:
            print("Произошла ошибка:", e)

    print("\nВремя работы для задач без указанного клиента:", unspecified_client_time, "ms")

    # doc = fitz.open(pdf_path_temp)
    # doc.save(pdf_path_final, garbage=4, deflate=True)
    # doc.close()
    # os.remove(pdf_path_temp)
