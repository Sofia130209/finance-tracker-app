import sys, csv, os
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QIcon
from scripts.data_table import DataTable
from scripts.day_data_table import DayDataTable
from scripts.graphics_data import DataPlotter
from scripts.day_graphics_data import DayDataPlotter
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class DataWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        uic.loadUi("forms/TableWidget.ui", self)
        
        self.tableWidget = self.findChild(QtWidgets.QTableWidget, 'tableWidget')

        self.data_table = DataTable(self.tableWidget)
        self.data_table.load_data_from_csv()

class DayDataWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        uic.loadUi("forms/TableWidget.ui", self)
        
        self.tableWidget = self.findChild(QtWidgets.QTableWidget, 'tableWidget')

        self.data_table = DayDataTable(self.tableWidget)
        self.data_table.load_data_from_csv()

class GraphWindow(QtWidgets.QWidget):
    def __init__(self, data_plotter, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        uic.loadUi("forms/GraphEditor.ui", self)
        
        self.plotWidget = self.findChild(QtWidgets.QWidget, 'plotWidget')

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        
        layout = QtWidgets.QVBoxLayout(self.plotWidget)
        layout.addWidget(self.canvas)
        
        self.data_plotter = data_plotter
        self.plot_data()

    def plot_data(self):
        weeks, profits, expenses = self.data_plotter.get_data()
        if not weeks:
            return

        self.ax.clear()
        self.ax.plot(weeks, profits, marker='o', linestyle='-', label='Прибыль', color='green')
        self.ax.plot(weeks, expenses, marker='s', linestyle='--', label='Расходы', color='red')
        
        self.ax.set_xlabel("Неделя")
        self.ax.set_ylabel("Сумма")
        self.ax.set_title("Прибыль и расходы по неделям")
        self.ax.legend()
        self.ax.grid(True)
        
        self.canvas.draw()

class DayGraphWindow(QtWidgets.QWidget):
    def __init__(self, day_data_plotter, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        uic.loadUi("forms/GraphEditor.ui", self)
        
        self.plotWidget = self.findChild(QtWidgets.QWidget, 'plotWidget')

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        
        layout = QtWidgets.QVBoxLayout(self.plotWidget)
        layout.addWidget(self.canvas)
        
        self.data_plotter = day_data_plotter
        self.plot_data()

    def plot_data(self):
        weeks, profits, expenses = self.data_plotter.get_data()
        if not weeks:
            return

        self.ax.clear()
        self.ax.plot(weeks, profits, marker='o', linestyle='-', label='Прибыль', color='green')
        self.ax.plot(weeks, expenses, marker='s', linestyle='--', label='Расходы', color='red')
        
        self.ax.set_xlabel("День")
        self.ax.set_ylabel("Сумма")
        self.ax.set_title("Прибыль и расходы по дням")
        self.ax.legend()
        self.ax.grid(True)
        
        self.canvas.draw()

class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        uic.loadUi('forms/MainPage.ui', self)
        self.setWindowIcon(QIcon('images/icon.png'))
        
        self.today_profit = self.findChild(QtWidgets.QLineEdit, 'today_profit')
        self.week_profit = self.findChild(QtWidgets.QLineEdit, 'week_profit')
        self.today_spent = self.findChild(QtWidgets.QLineEdit, 'today_spent')
        self.today_spent_commentary = self.findChild(QtWidgets.QLineEdit, 'today_spent_commentary')
        self.week_spent = self.findChild(QtWidgets.QLineEdit, 'week_spent')
        self.count_income_btn = self.findChild(QtWidgets.QPushButton, 'count_income')
        self.save_week_data_btn = self.findChild(QtWidgets.QPushButton, 'save_week_data_btn')
        self.open_data_btn = self.findChild(QtWidgets.QPushButton, 'open_data')
        self.show_plot_btn = self.findChild(QtWidgets.QPushButton, 'show_plot_btn')
        self.show_day_plot_btn = self.findChild(QtWidgets.QPushButton, 'show_day_plot_btn')
        self.middle_day_income = self.findChild(QtWidgets.QLabel, 'middle_week_income')
        self.income = self.findChild(QtWidgets.QLabel, 'income')
        self.save_day_data_btn = self.findChild(QtWidgets.QPushButton, 'save_day_data_btn')
        self.show_day_data_btn = self.findChild(QtWidgets.QPushButton, 'show_day_data_btn')
        
        #! Обнуление значений
        self.today_profit_value = 0
        self.today_spent_value = 0
        self.week_profit_value = 0
        self.week_spent_value = 0
        
        self.income.setText('')
        
        self.count_income_btn.clicked.connect(self.count_middle_day_income)
        self.save_week_data_btn.clicked.connect(self.save_data_to_csv)
        self.open_data_btn.clicked.connect(self.open_data_window)
        self.save_day_data_btn.clicked.connect(self.save_today_data_to_csv)
        self.show_day_data_btn.clicked.connect(self.open_day_data_window)
        self.show_plot_btn.clicked.connect(self.open_plot_window)
        self.show_day_plot_btn.clicked.connect(self.open_day_plot_window)
    
    def open_data_window(self):
        self.data_window = DataWindow()
        self.data_window.show()
    
    def open_day_data_window(self):
        self.day_data_window = DayDataWindow()
        self.day_data_window.show()
    
    def open_plot_window(self):
        data_plotter = DataPlotter()
        self.graph_window = GraphWindow(data_plotter)
        self.graph_window.show()
    
    def open_day_plot_window(self):
        day_data_plotter = DayDataPlotter()
        self.day_graph_window = DayGraphWindow(day_data_plotter)
        self.day_graph_window.show()

    def get_week_money(self):
        try:
            self.week_profit_value = float(self.week_profit.text().strip())
            self.week_spent_value = float(self.week_spent.text().strip())
        except Exception:
            self.show_error_message('Ошибка!', 'Пожалуйста, заполните все колонки с данными и убедитесь, что ваши данные представлены в виде чисел.')
            return False

        return True

    def get_today_money(self):
        try:
            self.today_profit_value = float(self.today_profit.text().strip())
            self.today_spent_value = float(self.today_spent.text().strip())
            self.today_spent_comm = str(self.today_spent_commentary.text())
        except Exception:
            self.show_error_message('Ошибка!', 'Пожалуйста, заполните все колонки с данными и убедитесь, что ваши данные представлены в виде чисел.')
            return False
        
        return True

    def count_middle_day_income(self):
        try:
            if not self.get_week_money():
                return

            self.middle_day_income_value = round((self.week_profit_value - self.week_spent_value) / 7, 2)
            self.income.setText(str(self.middle_day_income_value))

        except Exception as e:
            self.show_error_message("Ошибка!", f"Произошла непредвиденная ошибка: {e}")

    def save_data_to_csv(self):
        try:
            if not self.get_week_money():
                return
            
            week_number = self.get_next_week_number()
            
            data = [
                [week_number, self.week_profit_value, self.week_spent_value, self.middle_day_income_value]
            ]

            with open("data/week_data.csv", mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerows(data)
                self.show_done_message('Успех!', 'Данные успешно сохранены!')
        except Exception as e:
            self.show_error_message("Ошибка!", f"Произошла ошибка при сохранении данных: {e}")
    
    def save_today_data_to_csv(self):
        try:
            if not self.get_today_money():
                return
            
            day_number = self.get_next_day_number()
            
            data = [
                [day_number, self.today_profit_value, self.today_spent_value, self.today_spent_comm]
            ]

            with open("data/days_data.csv", mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerows(data)
                self.show_done_message('Успех!', 'Данные успешно сохранены!')
        except Exception as e:
            self.show_error_message("Ошибка!", f"Произошла ошибка при сохранении данных: {e}")

    def get_next_week_number(self):
        if not os.path.exists("data/week_data.csv"):
            return 1

        try:
            with open("data/week_data.csv", "r", encoding="utf-8") as file:
                reader = list(csv.reader(file))
                if len(reader) > 1:
                    last_week = int(reader[-1][0])
                    return last_week + 1
        except Exception:
            return 1
        
        return 1
    
    def get_next_day_number(self):
        if not os.path.exists("data/days_data.csv"):
            return 1

        try:
            with open("data/days_data.csv", "r", encoding="utf-8") as file:
                reader = list(csv.reader(file))
                if len(reader) > 1:
                    last_day = int(reader[-1][0])
                    return last_day + 1
        except Exception:
            return 1
        
        return 1

    def show_error_message(self, title, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    def show_done_message(self, title, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

#! ЗАПУСК ПРОГРАММЫ
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())