import csv
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QHeaderView

class DayDataTable:
    def __init__(self, table_widget: QtWidgets.QTableWidget):
        """Инициализация класса с переданным QTableWidget."""
        self.table_widget = table_widget
        self.setup_table_style()
        self.set_static_headers()

    def setup_table_style(self):
        """Настраивает стиль таблицы."""
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.setSortingEnabled(True)
        self.table_widget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_widget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)

    def set_static_headers(self):
        """Устанавливает статичные заголовки таблицы."""
        headers = ["День", "Прибыль", "Расходы", "Комментарии к расходам"]
        self.table_widget.setColumnCount(len(headers))
        self.table_widget.setHorizontalHeaderLabels(headers)

        header = self.table_widget.horizontalHeader()
        if header is not None:
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def load_data_from_csv(self, file_path="data/days_data.csv"):
        """Загружает данные из CSV-файла в таблицу."""
        try:
            with open(file_path, mode="r", encoding="utf-8") as file:
                reader = list(csv.reader(file))
                
            if len(reader) < 1:
                self.show_message("Ошибка", "Файл пуст или повреждён.", QtWidgets.QMessageBox.Icon.Warning)
                return

            data = reader

            self.table_widget.setRowCount(len(data))

            for row_idx, row in enumerate(data):
                for col_idx, value in enumerate(row):
                    if col_idx == 0:
                        value = str(row_idx + 1)
                    item = QtWidgets.QTableWidgetItem(value)
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    self.table_widget.setItem(row_idx, col_idx, item)

            self.table_widget.resizeColumnsToContents()
        except Exception as e:
            self.show_message("Ошибка", f"Не удалось загрузить данные: {e}", QtWidgets.QMessageBox.Icon.Critical)

    def show_message(self, title, message, icon):
        """Выводит окно сообщения."""
        msg = QtWidgets.QMessageBox()
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        msg.exec()
