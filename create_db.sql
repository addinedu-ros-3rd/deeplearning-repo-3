DROP database IF exists AIstore;

CREATE DATABASE IF NOT EXISTS AIstore;
USE AIstore;

-- 테이블 생성: custom
DROP TABLE IF EXISTS customer;
CREATE TABLE customer (
    customerID INT PRIMARY KEY,
    personality VARCHAR(32),
    point DOUBLE,
    address VARCHAR(32),
    phoneNumber INT
);

-- 테이블 생성: enterence
DROP TABLE IF EXISTS enterence;
CREATE TABLE enterence (
    enterID INT AUTO_INCREMENT PRIMARY KEY,
    customerID INT,
    enterenceTime TIMESTAMP,
    enterStatus CHAR,
    FOREIGN KEY (customerID) REFERENCES customer(customerID)
);

-- 테이블 생성: fruits
DROP TABLE IF EXISTS fruits;
CREATE TABLE fruits (
    fruitID INT PRIMARY KEY,
    fruitName VARCHAR(16),
    price INT,
    stockStand INT,
    expirationDate DATETIME
);

-- 테이블 생성: shoppingBasket
DROP TABLE IF EXISTS shoppingBasket;
CREATE TABLE shoppingBasket (
    shoppingID INT PRIMARY KEY,
    customerID int,
    fruitID int,
    outQuantity int,
    FOREIGN KEY (customerID) REFERENCES customer(customerID)
);

-- 테이블 생성: payment
DROP TABLE IF EXISTS payment;
CREATE TABLE payment (
    paymentID INT PRIMARY KEY,
    shoppingID INT,
    paymentTime TIMESTAMP,
    totalAmount INT,
    FOREIGN KEY (shoppingID) REFERENCES shoppingBasket(shoppingID)
);

-- 테이블 생성: productOut
DROP TABLE IF EXISTS productOut;
CREATE TABLE productOut (
    fruitOutLog INT AUTO_INCREMENT PRIMARY KEY,
    fruitID INT,
    outDate TIMESTAMP,
    outQuantity INT,
    FOREIGN KEY (fruitID) REFERENCES fruits(fruitID)
);

-- 테이블 생성: productIn
DROP TABLE IF EXISTS productIn;
CREATE TABLE productIn (
    fruitInLog INT AUTO_INCREMENT PRIMARY KEY,
    fruitID INT,
    inDate TIMESTAMP,
    inQuantity INT,
    FOREIGN KEY (fruitID) REFERENCES fruits(fruitID)
);

-- 테이블 생성: actionRecognition
DROP TABLE IF EXISTS actionRecognition;
CREATE TABLE actionRecognition (
    fruitID INT,
    actionTime TIMESTAMP,
    actionType VARCHAR(16),
    FOREIGN KEY (fruitID) REFERENCES fruits(fruitID)
);

DROP TABLE IF EXISTS mismatchActionStand;
CREATE TABLE mismatchActionStand (
    mismatchID INT AUTO_INCREMENT PRIMARY KEY,
    standFruitID INT,
    actionFruitID INT,
    mismatch TIMESTAMP
);

insert into customer values 
	(0, 'getrfid0', 100.0, '서울특별시 양천구 목동서로 291', 01012344321),
	(1, 'getrfid1', 20.0, '서울특별시 양천구 목동서로 292', 01012341234),
	(2, 'getrfid2', 30.0, '서울특별시 양천구 목동서로 293', 01012345464),
	(3, 'getrfid3', 10.5, '서울특별시 양천구 목동서로 294', 01012341235),
	(4, 'getrfid4', 120.0, '서울특별시 양천구 목동서로 295', 01012347756),
	(5, 'getrfid5', 60.0, '서울특별시 양천구 목동서로 291', 01012347765),
	(6, 'getrfid6', 80.0, '서울특별시 양천구 목동서로 292', 01012344456),
	(7, 'getrfid7', 40.0, '서울특별시 양천구 목동서로 293', 01012348876),
	(8, 'getrfid8', 5.5, '서울특별시 양천구 목동서로 297', 01012341327),
	(9, 'getrfid9', 20.5, '서울특별시 양천구 목동서로 298', 01012340097);
    
insert into fruits values
	(0, '바나나', 2990, 2, '2023-12-21 15:30:00'),
    (1, '사과', 1250, 5, '2023-12-22 15:30:00'),
    (2, '오렌지', 750, 10, '2023-12-31 15:30:00'),
    (5, null, null, null, null);
    