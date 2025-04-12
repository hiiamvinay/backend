/*creating database */
CREATE DATABASE board_plan;

/* using database */
USE board_plan;


/* creating users table */
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(15) NOT NULL,
    password VARCHAR(255) NOT NULL,
    parent_id INT DEFAULT NULL,
    level INT DEFAULT 0,
    FOREIGN KEY (parent_id) REFERENCES users(id)
)  AUTO_INCREMENT=100;


CREATE TABLE sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    quantity INT NOT NULL,  -- Track number of sales instead of amount
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE koupean_codes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    koupean_code VARCHAR(12) NOT NULL UNIQUE
);