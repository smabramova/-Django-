import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'store.db')

def get_connection():
    """Возвращает соединение с БД (режим Row для доступа по именам колонок)"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def authenticate_user(login, password):
    """Проверяет логин/пароль, возвращает (успех, роль, ФИО) или (False, None, None)"""
    with get_connection() as conn:
        cursor = conn.execute(
            "SELECT role, full_name FROM Users WHERE login=? AND password=?",
            (login, password)
        )
        row = cursor.fetchone()
        if row:
            return True, row['role'], row['full_name']
        return False, None, None

def get_all_products():
    """
    Возвращает список товаров с названиями связанных сущностей.
    Каждый элемент — словарь с ключами:
    id, name, description, price, quantity, discount,
    category, manufacturer, supplier, unit, image_path
    """
    query = """
    SELECT
        p.id, p.name, p.description, p.price, p.quantity, p.discount,
        c.name AS category,
        m.name AS manufacturer,
        s.name AS supplier,
        u.name AS unit,
        p.image_path
    FROM Products p
    JOIN Categories c ON p.category_id = c.id
    JOIN Manufacturers m ON p.manufacturer_id = m.id
    JOIN Suppliers s ON p.supplier_id = s.id
    JOIN Units u ON p.unit_id = u.id
    ORDER BY p.id
    """
    with get_connection() as conn:
        cursor = conn.execute(query)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]