import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("План тренировок")
        self.root.geometry("800x600")
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Форма ввода
        tk.Label(self.root, text="Дата (ДД.ММ.ГГГГ):").pack()
        self.date_entry = tk.Entry(self.root)
        self.date_entry.pack()

        tk.Label(self.root, text="Тип тренировки:").pack()
        self.type_entry = tk.Entry(self.root)
        self.type_entry.pack()

        tk.Label(self.root, text="Длительность (мин):").pack()
        self.duration_entry = tk.Entry(self.root)
        self.duration_entry.pack()

        # Кнопка добавления
        tk.Button(self.root, text="Добавить тренировку", command=self.add_training).pack()

        # Список тренировок
        self.listbox = tk.Listbox(self.root, width=80, height=20)
        self.listbox.pack()

        # Фильтры
        tk.Label(self.root, text="Фильтр по типу:").pack()
        self.filter_type = tk.Entry(self.root)
        self.filter_type.pack()

        tk.Button(self.root, text="Применить фильтр", command=self.apply_filter).pack()

    def add_training(self):
        date = self.date_entry.get().strip()
        training_type = self.type_entry.get().strip()
        duration_str = self.duration_entry.get().strip()

        # Проверка на пустые поля
        if not date or not training_type or not duration_str:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
            return

        try:
            duration = int(duration_str)
            if duration <= 0:
                raise ValueError("Длительность должна быть положительной")
            if not self.validate_date(date):
                raise ValueError("Неверный формат даты (ДД.ММ.ГГГГ)")

            self.trainings.append({
                "date": date,
                "type": training_type,
                "duration": duration
            })
            self.save_data()
            self.update_list()
            # Очистка полей после добавления
            self.date_entry.delete(0, tk.END)
            self.type_entry.delete(0, tk.END)
            self.duration_entry.delete(0, tk.END)

        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def validate_date(self, date_str):
        try:
            datetime.strptime(date_str, "%d.%m.%Y")
            return True
        except ValueError:
            return False

    def update_list(self):
        self.listbox.delete(0, tk.END)
        for training in self.trainings:
            self.listbox.insert(tk.END, f"{training['date']} - {training['type']} ({training['duration']} мин)")

    def apply_filter(self):
        filter_text = self.filter_type.get().strip().lower()
        filtered = [t for t in self.trainings if filter_text in t['type'].lower()]
        self.listbox.delete(0, tk.END)
        for training in filtered:
            self.listbox.insert(tk.END, f"{training['date']} - {training['type']} ({training['duration']} мин)")

    def load_data(self):
        try:
            with open('trainings.json', 'r') as file:
                self.trainings = json.load(file)
                if not isinstance(self.trainings, list):
                    raise json.JSONDecodeError("Данные не являются списком", "", 0)
        except (FileNotFoundError, json.JSONDecodeError):
            self.trainings = []

    def save_data(self):
        try:
            with open('trainings.json', 'w') as file:
                json.dump(self.trainings, file, indent=4)
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить данные: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()