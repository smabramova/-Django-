import sys
from PyQt5.QtWidgets import QApplication
from login_window import LoginWindow
from main_window import MainWindow
import os

def main():
    app = QApplication(sys.argv)

    # Убедимся, что папки resources и images существуют
    os.makedirs('resources', exist_ok=True)
    os.makedirs('images', exist_ok=True)

    # Показываем окно входа
    login = LoginWindow()
    if login.exec_() == LoginWindow.Accepted:
        # Успешный вход (или гость)
        window = MainWindow(login.role, login.full_name)
        window.show()
        sys.exit(app.exec_())
    else:
        # Диалог закрыт без входа
        sys.exit(0)

if name == '__main__':
    main()