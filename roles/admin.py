from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap
from PyQt6.uic import loadUi

from db import conn


class Admin(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("manager_win.ui", self)
        self.pushButton.clicked.connect(self.back_to_auth)

        self.products_layout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.orders_layout = QVBoxLayout(self.scrollAreaWidgetContents_2)

        self.add_button = QPushButton("Создать")
        self.edit_button = QPushButton("Редактировать")
        self.delete_button = QPushButton("Удалить")
        buttons = QHBoxLayout()
        buttons.addWidget(self.add_button)
        buttons.addWidget(self.edit_button)
        buttons.addWidget(self.delete_button)
        self.verticalLayout.insertLayout(3, buttons)

        self.lineEdit.textChanged.connect(self.show_data)
        self.comboBox.currentIndexChanged.connect(self.show_data)
        self.tabWidget.currentChanged.connect(self.show_data)

        self.add_button.clicked.connect(self.create_item)
        self.edit_button.clicked.connect(self.edit_item)
        self.delete_button.clicked.connect(self.delete_item)

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
            SELECT products.product_id, products.product_name, products.description, products.price, products.stock_quantity, categories.category_name
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
        pid, name, description, price, stock, category = p

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
            f"Остаток: {stock}\n"
            f"Описание: {description}"
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

    def create_item(self):
        if self.tabWidget.currentIndex() == 0:
            self.create_product()
        else:
            self.create_order()

    def edit_item(self):
        if self.tabWidget.currentIndex() == 0:
            self.edit_product()
        else:
            self.edit_order()

    def delete_item(self):
        if self.tabWidget.currentIndex() == 0:
            self.delete_product()
        else:
            self.delete_order()

    def create_product(self):
        name, ok = QInputDialog.getText(self, "Товар", "Название")
        if not ok:
            return
        description, ok = QInputDialog.getText(self, "Товар", "Описание")
        if not ok:
            return
        price, ok = QInputDialog.getDouble(self, "Товар", "Цена", 0, 0, 1000000, 2)
        if not ok:
            return
        stock, ok = QInputDialog.getInt(self, "Товар", "Остаток", 0, 0, 1000000)
        if not ok:
            return

        cursor = conn.cursor()
        cursor.execute("SELECT category_id FROM categories LIMIT 1")
        category = cursor.fetchone()
        if not category:
            cursor.close()
            return

        cursor.execute(
            "INSERT INTO products (product_name, description, price, stock_quantity, category_id) VALUES (%s, %s, %s, %s, %s)",
            (name, description, price, stock, category[0]),
        )
        conn.commit()
        cursor.close()
        self.show_data()

    def edit_product(self):
        product_id, ok = QInputDialog.getInt(self, "Товар", "ID товара", 1, 1, 1000000)
        if not ok:
            return
        price, ok = QInputDialog.getDouble(self, "Товар", "Новая цена", 0, 0, 1000000, 2)
        if not ok:
            return

        cursor = conn.cursor()
        cursor.execute("UPDATE products SET price = %s WHERE product_id = %s", (price, product_id))
        conn.commit()
        cursor.close()
        self.show_data()

    def delete_product(self):
        product_id, ok = QInputDialog.getInt(self, "Товар", "ID товара", 1, 1, 1000000)
        if not ok:
            return

        cursor = conn.cursor()
        cursor.execute("DELETE FROM order_items WHERE product_id = %s", (product_id,))
        cursor.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
        conn.commit()
        cursor.close()
        self.show_data()

    def create_order(self):
        total, ok = QInputDialog.getDouble(self, "Заказ", "Сумма", 0, 0, 1000000, 2)
        if not ok:
            return

        cursor = conn.cursor()
        cursor.execute("INSERT INTO orders (user_id, status_id, created_at, total_amount) VALUES (%s, %s, NOW(), %s)", (1, 1, total))
        conn.commit()
        cursor.close()
        self.show_data()

    def edit_order(self):
        order_id, ok = QInputDialog.getInt(self, "Заказ", "ID заказа", 1, 1, 1000000)
        if not ok:
            return
        status_id, ok = QInputDialog.getInt(self, "Заказ", "ID статуса", 1, 1, 3)
        if not ok:
            return

        cursor = conn.cursor()
        cursor.execute("UPDATE orders SET status_id = %s WHERE order_id = %s", (status_id, order_id))
        conn.commit()
        cursor.close()
        self.show_data()

    def delete_order(self):
        order_id, ok = QInputDialog.getInt(self, "Заказ", "ID заказа", 1, 1, 1000000)
        if not ok:
            return

        cursor = conn.cursor()
        cursor.execute("DELETE FROM order_items WHERE order_id = %s", (order_id,))
        cursor.execute("DELETE FROM orders WHERE order_id = %s", (order_id,))
        conn.commit()
        cursor.close()
        self.show_data()

    def back_to_auth(self):
        from auth.registration import RegistrationWindow
        self.auth_window = RegistrationWindow()
        self.auth_window.show()
        self.close()
