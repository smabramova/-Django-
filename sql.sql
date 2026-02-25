CREATE DATABASE ShoeStoreDB;
USE ShoeStoreDB;

CREATE TABLE UserRoles (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(50) NOT NULL UNIQUE
);

INSERT INTO UserRoles(Name) VALUES ('Client'), ('Manager'), ('Admin');

CREATE TABLE Users (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    Login VARCHAR(50) NOT NULL UNIQUE,
    PasswordHash CHAR(64) NOT NULL, -- Предполагается использование хеш-функций
    RoleId INT NOT NULL,
    FOREIGN KEY (RoleId) REFERENCES UserRoles(Id)
);

CREATE TABLE Categories (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE Products (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    ProductCode VARCHAR(20) NOT NULL UNIQUE,
    Title VARCHAR(100) NOT NULL,
    Description TEXT,
    Price DECIMAL(10,2),
    CategoryId INT NOT NULL,
    StockCount INT DEFAULT 0,
    FOREIGN KEY (CategoryId) REFERENCES Categories(Id)
);

CREATE TABLE Orders (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    DateOrdered DATETIME NOT NULL,
    TotalAmount DECIMAL(10,2),
    Status ENUM('Placed', 'Shipped', 'Delivered'),
    UserId INT NOT NULL,
    FOREIGN KEY (UserId) REFERENCES Users(Id)
);

CREATE TABLE OrderDetails (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    OrderId INT NOT NULL,
    ProductId INT NOT NULL,
    Quantity INT NOT NULL CHECK (Quantity > 0),
    Subtotal DECIMAL(10,2),
    FOREIGN KEY (OrderId) REFERENCES Orders(Id),
    FOREIGN KEY (ProductId) REFERENCES Products(Id)
);