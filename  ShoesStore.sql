CREATE DATABASE ShoesStore;
USE ShoesStore;

-- Таблица пользователей
CREATE TABLE Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Login VARCHAR(50) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Role ENUM('guest', 'client', 'manager', 'admin') NOT NULL
);

-- Таблица товаров
CREATE TABLE Goods (
    ProductID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Description TEXT,
    Price DECIMAL(10,2) NOT NULL,
    Stock INT NOT NULL
);

-- Таблица заказов
CREATE TABLE Orders (
    OrderID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    Date DATETIME DEFAULT CURRENT_TIMESTAMP,
    Status VARCHAR(50) NOT NULL,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

-- Таблица элементов заказа
CREATE TABLE OrderItems (
    OrderItemID INT AUTO_INCREMENT PRIMARY KEY,
    OrderID INT NOT NULL,
    ProductID INT NOT NULL,
    Quantity INT NOT NULL,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID) ON DELETE CASCADE,
    FOREIGN KEY (ProductID) REFERENCES Goods(ProductID) ON DELETE CASCADE
);

-- Добавляем пользователей
INSERT INTO Users (Login, Password, Role) VALUES
('admin', 'admin_password', 'admin'),
('manager1', 'manager_password', 'manager'),
('client1', 'client_password', 'client');

-- Добавляем товары
INSERT INTO Goods (Name, Description, Price, Stock) VALUES
('Обувь кроссовки', 'Легкие спортивные кроссовки', 2500.00, 10),
('Обувь ботинки', 'Кожаные зимние ботинки', 4000.00, 5),
('Обувь босоножки', 'Летние босоножки', 1200.00, 20);

CREATE DATABASE ShoesStore;
USE ShoesStore;