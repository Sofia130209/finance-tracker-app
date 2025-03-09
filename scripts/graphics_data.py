import csv

class DataPlotter:
    def __init__(self, file_path="data/week_data.csv"):
        self.file_path = file_path

    def get_data(self):
        try:
            weeks = []
            profits = []
            expenses = []

            with open(self.file_path, mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                for idx, row in enumerate(reader):
                    weeks.append(idx + 1)  # Неделя
                    profits.append(float(row[1]))  # Прибыль
                    expenses.append(float(row[2]))  # Расходы
            
            return weeks, profits, expenses
        except Exception as e:
            print(f"Ошибка при загрузке данных: {e}")
            return [], [], []
