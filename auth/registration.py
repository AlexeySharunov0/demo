from PyQt6.QtWidgets import *
from PyQt6.uic import *

from db import conn


class RegistrationWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registration")
        loadUi("ui/registration_window.ui", self)

        self.pushButton.clicked.connect(self.go_as_guest)
        self.pushButton_2.clicked.connect(self.go_to_login)
        self.pushButton_3.clicked.connect(self.do_registration)

    def go_to_login(self):
        from auth.login import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    def do_registration(self):
        login = self.lineEdit.text()
        password = self.lineEdit_2.text()

        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (login, password_hash, role_id) VALUES (%s, %s, %s)",
            (login, password, 1),
        )
        conn.commit()
        cursor.close()
        self.go_to_login()

    def go_as_guest(self):
        from roles.guest import Guest
        self.guest_window = Guest()
        self.guest_window.show()
        self.close()
