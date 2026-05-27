from PyQt6.QtWidgets import *
from PyQt6.uic import *

from db import conn


class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        loadUi("ui/login_window.ui", self)

        self.pushButton_2_enter.clicked.connect(self.do_login)
        self.pushButton_enter.clicked.connect(self.go_to_register)

    def go_to_register(self):
        from auth.registration import RegistrationWindow
        self.register_window = RegistrationWindow()
        self.register_window.show()
        self.close()

    def do_login(self):
        from roles.user import User
        from roles.manager import Manager
        from roles.admin import Admin

        login = self.lineEdit_enter.text()
        password = self.lineEdit_2_enter.text()

        cursor = conn.cursor()
        cursor.execute(
            "SELECT role_id FROM users WHERE login = %s AND password_hash = %s",
            (login, password),
        )
        result = cursor.fetchone()
        cursor.close()

        if not result:
            return

        role_id = result[0]
        if role_id == 1:
            self.new_window = User()
        elif role_id == 2:
            self.new_window = Manager()
        elif role_id == 3:
            self.new_window = Admin()
        else:
            return

        self.new_window.show()
        self.close()
