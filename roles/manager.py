from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap
from PyQt6.uic import loadUi

from db import conn


class Manager(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("manager_win.ui", self)
        self.pushButton.clicked.connect(self.back_to_auth)

        self.products_layout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.orders_layout = QVBoxLayout(self.scrollAreaWidgetContents_2)

        self.lineEdit.textChanged.connect(self.show_data)
        self.comboBox.currentIndexChanged.connect(self.show_data)
        self.tabWidget.currentChanged.connect(self.show_data)
        self.show_data()

    def show_data(self):
        if self.tabWidget.currentIndex() == 0:
            self.show_products()
        else:
            self.show_orders()

    def show_products(self):
        while self.products_layout.count():
            w = self.products_layout.takeAt(0).widget()
            if w:
                w.deleteLater()

        text = self.lineEdit.text().strip()
        sort_i = self.comboBox.currentIndex()

        order_by = "ORDER BY products.price ASC"
        if sort_i == 1:
            order_by = "ORDER BY products.price DESC"
        elif sort_i == 2:
            order_by = "ORDER BY products.product_name ASC"
        elif sort_i == 3:
            order_by = "ORDER BY products.product_name DESC"

        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT products.product_id, products.product_name, products.price, products.stock_quantity, categories.category_name
            FROM products
            JOIN categories ON categories.category_id = products.category_id
            WHERE products.product_name LIKE %s OR categories.category_name LIKE %s
            """
            + order_by,
            (f"%{text}%", f"%{text}%"),
        )
        products = cursor.fetchall()
        cursor.close()

        for p in products:
            self.products_layout.addWidget(self.product_card(p))

    def show_orders(self):
        while self.orders_layout.count():
            w = self.orders_layout.takeAt(0).widget()
            if w:
                w.deleteLater()

        text = self.lineEdit.text().strip()
        sort_i = self.comboBox.currentIndex()

        order_by = "ORDER BY orders.created_at ASC"
        if sort_i == 1:
            order_by = "ORDER BY orders.created_at DESC"
        elif sort_i == 2:
            order_by = "ORDER BY users.login ASC"
        elif sort_i == 3:
            order_by = "ORDER BY users.login DESC"

        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT orders.order_id, users.login, order_statuses.status_name, orders.created_at, orders.total_amount
            FROM orders
            LEFT JOIN users ON users.user_id = orders.user_id
            JOIN order_statuses ON order_statuses.status_id = orders.status_id
            WHERE users.login LIKE %s OR order_statuses.status_name LIKE %s
            """
            + order_by,
            (f"%{text}%", f"%{text}%"),
        )
        orders = cursor.fetchall()
        cursor.close()

        for o in orders:
            self.orders_layout.addWidget(self.order_card(o))

    def product_card(self, p):
        pid, name, price, stock, category = p

        card = QFrame()
        card.setFrameStyle(QFrame.Shape.Box)
        grid = QGridLayout(card)

        photo = QLabel()
        photo.setPixmap(QPixmap(f"data/{pid}.jpg").scaled(100, 100))
        grid.addWidget(photo, 0, 0, 4, 1)

        text = (
            f"ID: {pid}\n"
            f"Название: {name}\n"
            f"Категория: {category}\n"
            f"Цена: {price}\n"
            f"Остаток: {stock}"
        )
        grid.addWidget(QLabel(text), 0, 1)
        return card

    def order_card(self, order):
        number, client, status, date, total = order

        card = QFrame()
        card.setFrameStyle(QFrame.Shape.Box)
        layout = QVBoxLayout(card)

        if client is None:
            client = "Гость"

        text = (
            f"Заказ ID: {number}\n"
            f"Клиент: {client}\n"
            f"Статус: {status}\n"
            f"Дата: {date}\n"
            f"Сумма: {total}"
        )
        layout.addWidget(QLabel(text))
        return card

    def back_to_auth(self):
        from auth.registration import RegistrationWindow
        self.auth_window = RegistrationWindow()
        self.auth_window.show()
        self.close()
