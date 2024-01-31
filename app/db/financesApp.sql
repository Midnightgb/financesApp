
CREATE DATABASE finances_app CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE finances_app;

CREATE TABLE users (
    user_id CHAR(30) PRIMARY KEY,
    full_name VARCHAR(80),
    mail VARCHAR(100) UNIQUE, -- user_name
    hashed_password VARCHAR(140),
    user_role ENUM('admin','user'),
    user_status TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE category (
    category_id SMALLINT(3) AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50),
    category_description VARCHAR(120),
    category_status TINYINT(1) DEFAULT 1
);

CREATE TABLE transactions (
    transactions_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id CHAR(30),
    category_id SMALLINT(3),
    amount FLOAT(10,2), 
    t_description VARCHAR(120),
    t_type ENUM('revenue','expenses'),
    t_date DATE,
    FOREIGN KEY (user_id) REFERENCES users (user_id),
    FOREIGN KEY (category_id) REFERENCES category (category_id)
);

CREATE TABLE tokens (
    token CHAR(180) PRIMARY KEY,
    user_id CHAR(30),
    token_status TINYINT(1) DEFAULT 1,
    token_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);
