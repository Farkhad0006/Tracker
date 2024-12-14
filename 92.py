import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib import pyplot as plt
import datetime
import json

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Трекер расходов")
        self.expenses = []

        # Загрузка расходов из файла
        self.load_expenses()

        # Настройка стилей
        self.default_font = ("Arial", 12)
        self.heading_font = ("Arial", 14, "bold")

        style = ttk.Style()
        style.configure("TLabelframe.Label", font=self.heading_font)

        # Создание интерфейса
        self.setup_ui()

    def setup_ui(self):
        # Фрейм для ввода
        input_frame = ttk.LabelFrame(self.root, text="Добавить расход")
        input_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(input_frame, text="Сумма:", font=self.default_font).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.amount_entry = ttk.Entry(input_frame, font=self.default_font)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Категория:", font=self.default_font).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.category_combobox = ttk.Combobox(input_frame, values=["Еда", "Транспорт", "Развлечения", "Другое"], state="readonly", font=self.default_font)
        self.category_combobox.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Описание:", font=self.default_font).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.description_entry = ttk.Entry(input_frame, font=self.default_font)
        self.description_entry.grid(row=2, column=1, padx=5, pady=5)

        self.add_button = ttk.Button(input_frame, text="Добавить", command=self.add_expense)
        self.add_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Фрейм для списка расходов
        list_frame = ttk.LabelFrame(self.root, text="Список расходов")
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.expense_tree = ttk.Treeview(list_frame, columns=("Дата", "Сумма", "Категория", "Описание"), show="headings")
        self.expense_tree.heading("Дата", text="Дата", anchor="center")
        self.expense_tree.heading("Сумма", text="Сумма", anchor="center")
        self.expense_tree.heading("Категория", text="Категория", anchor="center")
        self.expense_tree.heading("Описание", text="Описание", anchor="center")
        self.expense_tree.pack(fill="both", expand=True, padx=5, pady=5)

        # Фрейм для фильтрации и анализа
        filter_frame = ttk.LabelFrame(self.root, text="Фильтр расходов")
        filter_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(filter_frame, text="Категория:", font=self.default_font).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.filter_combobox = ttk.Combobox(filter_frame, values=["Все расходы", "Еда", "Транспорт", "Развлечения", "Другое"], state="readonly", font=self.default_font)
        self.filter_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.filter_combobox.set("Все расходы")

        self.filter_button = ttk.Button(filter_frame, text="Фильтровать", command=self.filter_expenses)
        self.filter_button.grid(row=0, column=2, padx=5, pady=5)

        self.analyze_button = ttk.Button(filter_frame, text="Анализ", command=self.analyze_expenses)
        self.analyze_button.grid(row=0, column=3, padx=5, pady=5)

        # Фрейм для кнопок управления
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=10)

        self.total_label = ttk.Label(button_frame, text="Общая сумма: 0", font=self.heading_font)
        self.total_label.pack(side="left")

        ttk.Button(button_frame, text="Удалить выбранный", command=self.delete_selected_expense).pack(side="right", padx=5)
        ttk.Button(button_frame, text="Очистить все", command=self.clear_expenses).pack(side="right", padx=5)
        ttk.Button(button_frame, text="Выход", command=self.root.quit).pack(side="right", padx=5)

        # Обновить список расходов
        self.update_expense_list()

    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            category = self.category_combobox.get()
            description = self.description_entry.get()

            if not category:
                messagebox.showerror("Ошибка", "Категория не может быть пустой")
                return

            expense = {
                "date": datetime.date.today().strftime("%Y-%m-%d"),
                "amount": amount,
                "category": category,
                "description": description
            }

            self.expenses.append(expense)
            self.update_expense_list()
            self.save_expenses()

            self.amount_entry.delete(0, tk.END)
            self.category_combobox.set("")
            self.description_entry.delete(0, tk.END)

            messagebox.showinfo("Успех", "Расход добавлен")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректную сумму")

    def update_expense_list(self):
        for row in self.expense_tree.get_children():
            self.expense_tree.delete(row)

        total = 0
        for expense in self.expenses:
            self.expense_tree.insert("", tk.END, values=(expense["date"], expense["amount"], expense["category"], expense["description"]))
            total += expense["amount"]

        self.total_label.config(text=f"Общая сумма: {total}")

    def analyze_expenses(self):
        if not self.expenses:
            messagebox.showinfo("Анализ расходов", "Нет данных для анализа")
            return

        category_totals = {}
        for expense in self.expenses:
            category = expense["category"]
            amount = expense["amount"]
            category_totals[category] = category_totals.get(category, 0) + amount

        analysis_message = "Анализ расходов по категориям:\n"
        for category, total in category_totals.items():
            analysis_message += f"{category}: {total}\n"

        messagebox.showinfo("Анализ расходов", analysis_message)

        # Построение графика
        categories = list(category_totals.keys())
        totals = list(category_totals.values())
        plt.figure(figsize=(8, 6))
        plt.pie(totals, labels=categories, autopct="%1.1f%%", startangle=140)
        plt.title("Распределение расходов по категориям")
        plt.show()

    def delete_selected_expense(self):
        selected_items = self.expense_tree.selection()
        if not selected_items:
            messagebox.showerror("Ошибка", "Выберите расход для удаления")
            return

        for selected_item in selected_items:
            values = self.expense_tree.item(selected_item, "values")
            for expense in self.expenses:
                if (
                        expense["date"] == values[0]
                        and expense["amount"] == float(values[1])
                        and expense["category"] == values[2]
                        and expense["description"] == values[3]
                ):
                    self.expenses.remove(expense)
                    break

        self.update_expense_list()
        self.save_expenses()
        messagebox.showinfo("Успех", "Выбранный расход(ы) удалён")

    def clear_expenses(self):
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить все расходы?"):
            self.expenses.clear()
            self.update_expense_list()
            self.save_expenses()
            messagebox.showinfo("Успех", "Все расходы удалены")

    def filter_expenses(self):
        selected_category = self.filter_combobox.get()

        if selected_category == "Все расходы":
            filtered_expenses = self.expenses
        else:
            filtered_expenses = [expense for expense in self.expenses if expense["category"] == selected_category]

        self.expense_tree.delete(*self.expense_tree.get_children())

        total = 0
        for expense in filtered_expenses:
            self.expense_tree.insert("", tk.END, values=(expense["date"], expense["amount"], expense["category"], expense["description"]))
            total += expense["amount"]

        self.total_label.config(text=f"Общая сумма: {total}")

    def save_expenses(self):
        try:
            with open("expenses.json", "w") as file:
                json.dump(self.expenses, file)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {e}")

    def load_expenses(self):
        try:
            with open("expenses.json", "r") as file:
                self.expenses = json.load(file)
        except FileNotFoundError:
            self.expenses = []
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
