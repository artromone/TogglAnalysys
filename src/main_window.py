from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QProgressBar
from PyQt5.QtCore import Qt

import os
from datetime import datetime, timedelta

from date_selection_window import DateSelectionWindow
from reports import generate_all_reports


def get_first_day_of_week():
    today = datetime.today()
    first_day = today - timedelta(weeks=1) - timedelta(days=today.weekday())
    return first_day


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.selected_date = get_first_day_of_week()

    def updateSelectedDate(self, new_date):
        self.selected_date = new_date

    def initUI(self):
        layout = QVBoxLayout()

        self.select_date_button = QPushButton('Выбрать дату')
        self.select_date_button.clicked.connect(self.openDateSelectionWindow)
        layout.addWidget(self.select_date_button)

        self.date_label = QLabel('Выбранная дата: ')
        layout.addWidget(self.date_label)

        self.export_button = QPushButton('Экспорт')
        self.export_button.clicked.connect(self.exportToFile)
        self.export_button.setEnabled(False)
        layout.addWidget(self.export_button)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)
        self.setWindowTitle('FavorIT Assistants | t.me/art_rom')
        self.setMinimumWidth(400)

    def openDateSelectionWindow(self):
        self.date_selection_window = DateSelectionWindow(self)
        self.date_selection_window.show()

    def showSelectedDate(self, selected_date, next_week_date):
        self.date_label.setText('Начало диапазона: ' + selected_date.toString(Qt.DefaultLocaleLongDate))
        self.date_label.setText(
            self.date_label.text() + '\nКонец диапазона: ' + next_week_date.toString(Qt.DefaultLocaleLongDate))

        self.export_button.setEnabled(True if selected_date.isValid() else False)

    def exportToFile(self):
        #self.export_button.setVisible(False)
        #self.progress_bar.setVisible(True)

        try:
            generate_all_reports(self.selected_date)

            export_dir = os.path.dirname(os.path.dirname(__file__)) + "/export"
            QMessageBox.information(self, 'Экспорт завершен', f'Данные успешно экспортированы в {export_dir}')

        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось экспортировать данные: {str(e)}')

        # finally:
        #     self.export_button.setVisible(True)
        #     self.progress_bar.setVisible(False)
