import time


def read_cell_data(sheet, row, col, retry_rate):
    while True:
        try:
            cell_date = sheet.cell(row, col).value
            break
        except Exception as e:
            # print("An error occurred while retrieving the cell data:", e)
            # print("Retrying after " + str(retry_rate) + " seconds...")
            time.sleep(retry_rate)
    return cell_date


def write_cell_data(sheet, row, col, value, retry_rate):
    while True:
        try:
            cell = sheet.cell(row, col)
            cell.value = value
            sheet.update_cell(row, col, value)
            break
        except Exception as e:
            # print("An error occurred while updating the cell data:", e)
            # print("Retrying after " + str(retry_rate) + " seconds...")
            time.sleep(retry_rate)
