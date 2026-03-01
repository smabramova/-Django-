from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import database
import os

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход в систему")
        self.setWindowIcon(QIcon(os.path.join('resources', 'icon.png')))
        self.setFixedSize(300, 200)
        self.setModal(True)

        # Переменные для передачи данных
        self.role = None
        self.full_name = None

        # Основной layout
        layout = QVBoxLayout()

        # Логотип
        logo_label = QLabel()
        logo_pixmap = QPixmap(os.path.join('resources', 'logo.png'))
        if not logo_pixmap.isNull():
            logo_label.setPixmap(logo_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        # Поля ввода
        self.login_edit = QLineEdit()
        self.login_edit.setPlaceholderText("Логин")
        layout.addWidget(self.login_edit)

        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("Пароль")
        self.password_edit.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_edit)

        # Кнопки
        btn_layout = QHBoxLayout()
        self.btn_login = QPushButton("Войти")
        self.btn_login.clicked.connect(self.on_login)
        btn_layout.addWidget(self.btn_login)

        self.btn_guest = QPushButton("Войти как гость")
        self.btn_guest.clicked.connect(self.on_guest)
        btn_layout.addWidget(self.btn_guest)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def on_login(self):
        login = self.login_edit.text().strip()
        password = self.password_edit.text().strip()
        if not login or not password:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль")
            return

        success, role, full_name = database.authenticate_user(login, password)
        if success:
            self.role = role
            self.full_name = full_name
            self.accept()  # закрыть диалог с успехом
        else:
            QMessageBox.critical(self, "Ошибка", "Неверный логин или пароль")

    def on_guest(self):
        self.role = 'guest'
        self.full_name = 'Гость'
        self.accept()