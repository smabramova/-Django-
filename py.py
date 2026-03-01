import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Подключение базы данных (или создание, если не существует)
conn = sqlite3.connect(':memory:')  # Используем память для примера; замените на файл, если нужно
cursor = conn.cursor()

# Создаем таблицы
def create_tables():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role_id INTEGER NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_name TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Goods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            price REAL,
            discount_percent REAL,
            stock INTEGER
        )
    ''')
    conn.commit()

# Заполняем таблицы примерными данными
def insert_sample_data():
    cursor.execute("INSERT INTO Roles (role_name) VALUES ('Guest'), ('Client'), ('Manager'), ('Admin')")
    cursor.execute("INSERT INTO Users (username, password_hash, role_id) VALUES ('admin', 'admin', 4)")
    cursor.execute("INSERT INTO Goods (name, category, price, discount_percent, stock) VALUES\n\
        ('Товар 1', 'Категория A', 100.0, 10.0, 5),\n\
        ('Товар 2', 'Категория B', 200.0, 0.0, 0),\n\
        ('Товар 3', 'Категория A', 150.0, 5.0, 10),\n\
        ('Товар 4', 'Категория C', 300.0, 20.0, 2)"
    )
    conn.commit()

# Простая авторизация (для примера)
def simulate_login():
    return {'username': 'admin', 'role_id': 4}

# Главное окно приложения
class App(tk.Tk):
    def __init__(self, user):
        super().__init__()
        self.title("Система учета товаров")
        self.geometry("700x400")
        self.user = user

        # Создаем таблицу
        self.tree = ttk.Treeview(self, columns=("name", "category", "price", "discount", "stock"), show='headings')
        self.tree.heading("name", text="Наименование")
        self.tree.heading("category", text="Категория")
        self.tree.heading("price", text="Цена")
        self.tree.heading("discount", text="Скидка (%)")
        self.tree.heading("stock", text="Наличие")
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.load_data()

    def load_data(self):
        cursor.execute("SELECT name, category, price, discount_percent, stock FROM Goods")
        for row in cursor.fetchall():
            name, category, price, discount, stock = row
            tags = ()
            if discount > 0:
                tags += ('discount',)
            if stock > 0:
                tags += ('available',)
            self.tree.insert('', 'end', values=(name, category, price, discount, stock), tags=tags)

        # Настраиваем подсветку
        self.tree.tag_configure('discount', background='yellow')
        self.tree.tag_configure('available', background='lightgreen')

# Основная функция
def main():
    create_tables()
    insert_sample_data()

    # Ваша логика входа — здесь для примера авторизация симуляцией
    user = simulate_login()

    # Запуск главного окна
    app = App(user)
    app.mainloop()

if __name__ == "__main__":
    main()