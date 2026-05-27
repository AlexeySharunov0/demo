DROP DATABASE IF EXISTS fabric_store_2;
CREATE DATABASE fabric_store_2;
USE fabric_store_2;

CREATE TABLE roles (
    role_id INT PRIMARY KEY,
    role_name VARCHAR(30) NOT NULL
);

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    login VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role_id INT NOT NULL,
    FOREIGN KEY (role_id) REFERENCES roles(role_id)
);

CREATE TABLE categories (
    category_id INT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL
);

CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock_quantity INT NOT NULL,
    category_id INT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

CREATE TABLE order_statuses (
    status_id INT PRIMARY KEY,
    status_name VARCHAR(50) NOT NULL
);

CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    status_id INT NOT NULL,
    created_at DATETIME NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (status_id) REFERENCES order_statuses(status_id)
);

CREATE TABLE order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

INSERT INTO roles (role_id, role_name) VALUES
(1, 'user'),
(2, 'manager'),
(3, 'admin');

INSERT INTO categories (category_id, category_name) VALUES
(1, 'Куртки'),
(2, 'Джинсы'),
(3, 'Обувь');

INSERT INTO order_statuses (status_id, status_name) VALUES
(1, 'Новый'),
(2, 'В работе'),
(3, 'Завершен');

INSERT INTO users (user_id, login, password_hash, role_id) VALUES
(1, 'user', 'user123', 1),
(2, 'manager', 'manager123', 2),
(3, 'admin', 'admin123', 3);

INSERT INTO products (product_id, product_name, description, price, stock_quantity, category_id) VALUES
(1, 'Меховая куртка', 'Теплая зимняя куртка', 2421.00, 20, 1),
(2, 'Кожаная куртка', 'Классическая куртка из кожи', 1200.00, 12, 1),
(3, 'Джинсы', 'Повседневные синие джинсы', 500.00, 35, 2),
(4, 'Кроссовки', 'Удобные кроссовки для прогулок', 1500.00, 18, 3);

INSERT INTO orders (order_id, user_id, status_id, created_at, total_amount) VALUES
(1, 1, 1, '2026-05-27 12:00:00', 2421.00),
(2, 2, 2, '2026-05-27 13:00:00', 1500.00);

INSERT INTO order_items (order_item_id, order_id, product_id, quantity, unit_price) VALUES
(1, 1, 1, 1, 2421.00),
(2, 2, 4, 1, 1500.00);
