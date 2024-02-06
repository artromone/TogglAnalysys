from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import Qt

import os

from date_selection_window import DateSelectionWindow
from reports import generate_all_reports


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

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

        self.setLayout(layout)
        self.setWindowTitle('FavorIT Assistants | t.me/art_rom')
        self.setMinimumWidth(400)

    def openDateSelectionWindow(self):
        self.date_selection_window = DateSelectionWindow(self)
        self.date_selection_window.show()

    def showSelectedDate(self, selected_date, next_week_date):
        self.date_label.setText('Начало диапазона: ' + selected_date.toString(Qt.DefaultLocaleLongDate))
        self.date_label.setText(self.date_label.text() + '\nКонец диапазона: ' + next_week_date.toString(Qt.DefaultLocaleLongDate))

        self.export_button.setEnabled(True if selected_date.isValid() else False)

    def exportToFile(self):
        try:
            generate_all_reports()
            export_dir = os.path.dirname(os.path.dirname(__file__)) + "/export"
            QMessageBox.information(self, 'Экспорт завершен', f'Данные успешно экспортированы в {export_dir}')
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось экспортировать данные: {str(e)}')
