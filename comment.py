import tkinter as tk
from tkinter import ttk
import sqlite3

# Функция для инициализации базы данных и создания таблицы, если она не существует
def init_db():
    # Подключение к базе данных SQLite (или создание, если она не существует)
    conn = sqlite3.connect('business_orders.db')
    cur = conn.cursor()
    # Создание таблицы для заказов с колонками для id, имени клиента, деталей заказа и статуса
    cur.execute('''CREATE TABLE IF NOT EXISTS orders
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, customer_name TEXT NOT NULL, order_details TEXT NOT NULL, status TEXT NOT NULL)''')
    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()

# Функция для добавления нового заказа в базу данных
def add_order():
    # Подключение к базе данных
    conn = sqlite3.connect('business_orders.db')
    cur = conn.cursor()
    # Вставка нового заказа в таблицу orders
    cur.execute("INSERT INTO orders (customer_name, order_details, status) VALUES (?, ?, 'Новый')",
                (customer_name_entry.get(), order_details_entry.get()))
    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()
    # Очистка полей ввода после добавления заказа
    customer_name_entry.delete(0, tk.END)
    order_details_entry.delete(0, tk.END)
    # Обновление отображения списка заказов
    view_orders()

# Функция для получения и отображения всех заказов из базы данных
def view_orders():
    # Очистка текущего содержимого представления дерева заказов
    for i in tree.get_children():
        tree.delete(i)
    # Подключение к базе данных
    conn = sqlite3.connect('business_orders.db')
    cur = conn.cursor()
    # Выбор всех строк из таблицы orders
    cur.execute("SELECT * FROM orders")
    rows = cur.fetchall()
    # Вставка каждой строки в представление дерева заказов
    for row in rows:
        tree.insert("", tk.END, values=row)
    # Закрытие соединения с базой данных
    conn.close()

# Создание главного окна приложения
app = tk.Tk()
app.title("Система управления заказами")

# Создание метки и поля ввода для имени клиента
tk.Label(app, text="Имя клиента").pack()
customer_name_entry = tk.Entry(app)
customer_name_entry.pack()

# Создание метки и поля ввода для деталей заказа
tk.Label(app, text="Детали заказа").pack()
order_details_entry = tk.Entry(app)
order_details_entry.pack()

# Создание кнопки для добавления нового заказа, связанной с функцией add_order
add_button = tk.Button(app, text="Добавить заказ", command=add_order)
add_button.pack()

# Определение колонок для представления дерева и его создание
columns = ("id", "customer_name", "order_details", "status")
tree = ttk.Treeview(app, columns=columns, show="headings")

# Настройка колонок в представлении дерева
for column in columns:
    tree.heading(column, text=column)

# Добавление представления дерева в окно приложения
tree.pack()

# Инициализация базы данных и отображение текущих заказов
init_db()
view_orders()

# Запуск приложения
app.mainloop()