import os
import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QLabel, QPushButton, QApplication, QAbstractItemView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon, QColor, QFont
import database

class MainWindow(QMainWindow):
    def __init__(self, role, full_name):
        super().__init__()
        self.role = role
        self.full_name = full_name
        self.setWindowTitle(f"Управление товарами - роль: {role}")
        self.setWindowIcon(QIcon(os.path.join('resources', 'icon.png')))
        self.resize(1200, 600)

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Верхняя панель с логотипом, ФИО и кнопкой выхода
        top_layout = QHBoxLayout()

        # Логотип
        logo_label = QLabel()
        logo_pixmap = QPixmap(os.path.join('resources', 'logo.png'))
        if not logo_pixmap.isNull():
            logo_label.setPixmap(logo_pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        top_layout.addWidget(logo_label)

        top_layout.addStretch()

        # ФИО пользователя
        self.user_label = QLabel(f"<b>{full_name}</b>")
        self.user_label.setStyleSheet("font-size: 14px;")
        top_layout.addWidget(self.user_label)

        # Кнопка выхода
        self.btn_logout = QPushButton("Выход")
        self.btn_logout.clicked.connect(self.logout)
        top_layout.addWidget(self.btn_logout)

        main_layout.addLayout(top_layout)

        # Таблица товаров
        self.table = QTableWidget()
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # только чтение
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setAlternatingRowColors(True)
        main_layout.addWidget(self.table)

        # Настройка столбцов
        self.setup_table()
        self.load_products()

    def setup_table(self):
        """Настраивает заголовки и ширину колонок"""
        headers = [
            "Фото", "Наименование", "Категория", "Описание",
            "Производитель", "Поставщик", "Базовая цена",
            "Ед. изм.", "Кол-во", "Скидка (%)", "Цена со скидкой"
        ]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        # Устанавливаем растяжение колонок
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # фото
        header.setSectionResizeMode(1, QHeaderView.Stretch)          # наименование
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents) # категория
        header.setSectionResizeMode(3, QHeaderView.Stretch)          # описание
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents) # производитель
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents) # поставщик
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents) # базовая цена
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents) # ед. изм.
        header.setSectionResizeMode(8, QHeaderView.ResizeToContents) # кол-во
        header.setSectionResizeMode(9, QHeaderView.ResizeToContents) # скидка
        header.setSectionResizeMode(10, QHeaderView.ResizeToContents) # цена со скидкой

    def load_products(self):
        """Загружает данные из БД и заполняет таблицу"""
        products = database.get_all_products()
        self.table.setRowCount(len(products))

        for row, prod in enumerate(products):
            # Фото (иконка)
            self.set_product_image(row, prod.get('image_path'))

            # Наименование
            self.table.setItem(row, 1, QTableWidgetItem(prod['name']))

            # Категория
            self.table.setItem(row, 2, QTableWidgetItem(prod['category']))

            # Описание (обрезаем длинный текст)
            desc = prod['description'] or ""