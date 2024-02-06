from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QCalendarWidget


class DateSelectionWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.calendar = QCalendarWidget()
        layout.addWidget(self.calendar)

        self.select_button = QPushButton('Применить')
        self.select_button.clicked.connect(self.onSelectDate)
        layout.addWidget(self.select_button)

        self.setLayout(layout)
        self.setWindowTitle('Выберите дату')

    def onSelectDate(self):
        selected_date = self.calendar.selectedDate()
        next_week_date = selected_date.addDays(7)
        self.main_window.showSelectedDate(selected_date, next_week_date)
        self.main_window.updateSelectedDate(selected_date)
        self.close()
