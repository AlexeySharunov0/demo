from PyQt6.QtWidgets import QDialog, QFrame, QGridLayout, QLabel, QVBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.uic import loadUi

from db import conn


class User(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("User")
        loadUi("ui/user_window.ui", self)

        self.layout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.pushButton.clicked.connect(self.return_to_auth)
        self.render_products()

    def render_products(self) -> None:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT products.product_id, products.product_name, products.price, products.stock_quantity, categories.category_name
                FROM products
                JOIN categories ON categories.category_id = products.category_id
                ORDER BY products.product_name ASC
                """
            )
            products = cursor.fetchall()

        for product in products:
            card = QFrame()
            card.setFrameStyle(QFrame.Shape.Box)
            grid = QGridLayout(card)

            photo = QLabel()
            photo.setPixmap(QPixmap(f"data/{product[0]}.jpg").scaled(100, 100))
            grid.addWidget(photo, 0, 0, 4, 1)

            text = (
                f"ID: {product[0]}\n"
                f"Название: {product[1]}\n"
                f"Категория: {product[4]}\n"
                f"Цена: {product[2]} руб.\n"
                f"Остаток: {product[3]}"
            )
            grid.addWidget(QLabel(text), 0, 1)
            self.layout.addWidget(card)

    def return_to_auth(self) -> None:
        from auth.registration import RegistrationWindow

        self.auth_window = RegistrationWindow()
        self.auth_window.show()
        self.close()
