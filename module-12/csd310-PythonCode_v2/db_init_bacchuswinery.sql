 /*
    Title: db_init_bacchuswinery.sql
    Author: Justin and Tabari
    Date: Updated 03/01/25
    Description: Bacchus Winery Database Intilization script for CSD-310 Module 11.1 Project
	Team Members: Justin, Tabari, Austin and Mark
	This code is adapted from the db_init_2022.sql by Professor Sue for the movies database initialization script.
*/ 

-- create the Bacchus Winery database if it doesn't exist
CREATE DATABASE IF NOT EXISTS bacchuswinery;

-- select the Bacchus Winery database for use
USE bacchuswinery;

-- drop database user if exists
DROP USER IF EXISTS 'winery_user'@'localhost';

-- create winery_user and grant them all privileges to the bacchus winery database 
CREATE USER 'winery_user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'Gr@pe$2025';

-- grant all privileges to the bacchus database to user winery_user on localhost
GRANT ALL PRIVILEGES ON bacchuswinery.* TO 'winery_user'@'localhost';

-- drop tables if they are present
-- https://stackoverflow.com/questions/65700447/cant-drop-table-because-of-a-foreign-key-but-also-cant-drop-foreign-key
SET foreign_key_checks = 0;
DROP TABLE IF EXISTS distributors;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS suppliers;
DROP TABLE IF EXISTS supplier_deliveries;
DROP TABLE IF EXISTS time_card;
DROP TABLE IF EXISTS wine_grape_variety;
DROP TABLE IF EXISTS wine_sales;
SET foreign_key_checks = 1;

-- create the distributors table
CREATE TABLE distributors (
    distributor_id INT NOT NULL AUTO_INCREMENT,
    distributor_name VARCHAR(255) NOT NULL,
    contact_info VARCHAR(255),
    PRIMARY KEY(distributor_id)
);

-- create the employees table
CREATE TABLE employees (
    employee_id INT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    position VARCHAR(255) NOT NULL,
    PRIMARY KEY(employee_id)
);

-- create the suppliers table
CREATE TABLE suppliers (
    supplier_id INT NOT NULL AUTO_INCREMENT,
    supplier_name VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    supplied_item_type VARCHAR(255) NOT NULL,
    PRIMARY KEY(supplier_id)
);

-- create the supplier deliveries table - removed the discrepancy field since we will calculate with MySQL query or Python code
CREATE TABLE supplier_deliveries (
    delivery_id INT NOT NULL AUTO_INCREMENT,
    supplier_id INT NOT NULL,
    item_type VARCHAR(255) NOT NULL,
    expected_delivery_date DATE NOT NULL,
    actual_delivery_date DATE,
    quantity_delivered INT NOT NULL,
    PRIMARY KEY(delivery_id),
    CONSTRAINT fk_supplier
        FOREIGN KEY(supplier_id)
        REFERENCES suppliers(supplier_id)
);

-- create the time_card table to track monthly hours worked for each employee. This table replaces the total_hours_worked previously in the employees table
CREATE TABLE time_card (
    time_card_id INT NOT NULL AUTO_INCREMENT,
    employee_id INT NOT NULL,
    month INT NOT NULL,
	year INT NOT NULL,
    hours_worked DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY(time_card_id),
    CONSTRAINT fk_employee
		FOREIGN KEY(employee_id)
        REFERENCES employees(employee_id)
);

-- create the wine and grape variety table
CREATE TABLE wine_grape_variety (
    product_id INT NOT NULL AUTO_INCREMENT,
    wine_name VARCHAR(255) NOT NULL,
    grape_variety VARCHAR(255) NOT NULL,
    vintage_year YEAR NOT NULL,
    PRIMARY KEY(product_id)
);

-- create the wine sales table
CREATE TABLE wine_sales (
    sale_id INT NOT NULL AUTO_INCREMENT,
    product_id INT NOT NULL,
    distributor_id INT NOT NULL,
    sales_quantity INT NOT NULL,
    sale_date DATE NOT NULL,
    price_per_unit DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY(sale_id),
    CONSTRAINT fk_product
        FOREIGN KEY(product_id)
        REFERENCES wine_grape_variety(product_id),
    CONSTRAINT fk_distributor
        FOREIGN KEY(distributor_id)
        REFERENCES distributors(distributor_id)
);

-- insert the distributors records
INSERT INTO distributors(distributor_name, contact_info)
VALUES('Austin Spirits', 'awiant@my365.bellevue.edu'),
      ('Makers Mark', 'majoiner@my365.bellevue.edu'),
      ('Just in Time', 'jumorrow@my365.bellevue.edu'),
      ('Tabari Distillery', 'tlharvey@my365.bellevue.edu');
	  
-- insert the employees records. This version moves the tot_hours_worked to a new time_card table that supports monthly hour reporting
INSERT INTO employees(first_name, last_name, position) 
VALUES('Janet', 'Collins', 'Finance Manager'),
      ('Roz', 'Murphy', 'Marketing Manager'),
      ('Bob', 'Ulrich', 'Marketing Assistant'),
      ('Henry', 'Doyle', 'Production Manager'),
      ('Maria', 'Costanza', 'Distribution Manager');

-- insert the suppliers records
INSERT INTO suppliers(supplier_name, location, supplied_item_type) 
VALUES('Put a cork in it', 'California', 'Bottles/Corks'),
      ('Label this', 'Nevada', 'Labels/Boxes'),
      ('Vat Man', 'Washington', 'Vats/ Tubing'),
      ('Barrel & Brew Co.', 'Wyoming', 'Wine Barrels'),
      ('Vineyard Essentials', 'California', 'Wine Barrels');

-- insert the time_card records for each employee. This new table takes the place of the total_hours_worked previously in the employees table
INSERT INTO time_card(employee_id, year, month, hours_worked) 
VALUES(1, 2024, 3, 150),
      (1, 2024, 4, 140),
      (1, 2024, 5, 160),
      (1, 2024, 6, 155),
      (1, 2024, 7, 165),
	  (1, 2024, 8, 140),
      (1, 2024, 9, 160),
      (1, 2024, 10, 150),
      (1, 2024, 11, 155),
      (1, 2024, 12, 150),
      (1, 2025, 1, 140),
      (1, 2025, 2, 145),
	  (2, 2024, 3, 130),
      (2, 2024, 4, 135),
      (2, 2024, 5, 125),
      (2, 2024, 6, 145), 
      (2, 2024, 7, 140),
      (2, 2024, 8, 150),
      (2, 2024, 9, 135),
      (2, 2024, 10, 130),
      (2, 2024, 11, 145),
      (2, 2024, 12, 130),
      (2, 2025, 1, 125),
      (2, 2025, 2, 130),
	  (3, 2024, 3, 100),
      (3, 2024, 4, 105),
      (3, 2024, 5, 110),
      (3, 2024, 6, 120),
      (3, 2024, 7, 115),
      (3, 2024, 8, 125),
      (3, 2024, 9, 110),
      (3, 2024, 10, 100),
      (3, 2024, 11, 105),
      (3, 2024, 12, 110),
      (3, 2025, 1, 105),
      (3, 2025, 2, 110),
	  (4, 2024, 3, 200),
      (4, 2024, 4, 190),
      (4, 2024, 5, 185),
      (4, 2024, 6, 180),
      (4, 2024, 7, 185), 
      (4, 2024, 8, 160),
      (4, 2024, 9, 120),
      (4, 2024, 10, 165),
      (4, 2024, 11, 190),
      (4, 2024, 12, 120),
      (4, 2025, 1, 80),
      (4, 2025, 2, 160),
	  (5, 2024, 3, 180),
      (5, 2024, 4, 175),
      (5, 2024, 5, 185),
      (5, 2024, 6, 190),
      (5, 2024, 7, 180),
      (5, 2024, 8, 195),
      (5, 2024, 9, 185),
      (5, 2024, 10, 180),
      (5, 2024, 11, 175),
      (5, 2024, 12, 160),
      (5, 2025, 1, 120),
      (5, 2025, 2, 160);
	  
-- insert the supplier deliveries records. Adjusted the totals and made the deliveries as semi annual
INSERT INTO supplier_deliveries(supplier_id, item_type, expected_delivery_date, actual_delivery_date, quantity_delivered) 
VALUES
    ((SELECT supplier_id FROM suppliers WHERE supplier_name = 'Put a cork in it'), 'Bottles', '2024-02-05', '2024-02-05', 40000),
    ((SELECT supplier_id FROM suppliers WHERE supplier_name = 'Put a cork in it'), 'Corks', '2024-02-05', '2024-02-15', 40000),	
    ((SELECT supplier_id FROM suppliers WHERE supplier_name = 'Label this'), 'Labels', '2024-02-10', '2024-02-10', 5000),
    ((SELECT supplier_id FROM suppliers WHERE supplier_name = 'Label this'), 'Boxes', '2024-02-15', '2024-02-20', 5000),
    ((SELECT supplier_id FROM suppliers WHERE supplier_name = 'Vat Man'), 'Vats', '2024-02-12', '2024-02-20', 500),
    ((SELECT supplier_id FROM suppliers WHERE supplier_name = 'Vat Man'), 'Tubing', '2024-02-12', '2024-02-12', 800),
    ((SELECT supplier_id FROM suppliers WHERE supplier_name = 'Barrel & Brew Co.'), 'Wine Barrels', '2024-03-15', '2024-03-16', 400),
    ((SELECT supplier_id FROM suppliers WHERE supplier_name = 'Vineyard Essentials'), 'Wine Barrels', '2024-04-10', '2024-04-12', 300),
	((SELECT supplier_id FROM suppliers WHERE supplier_name = 'Put a cork in it'), 'Bottles', '2024-07-05', '2024-07-05', 60000),
    ((SELECT supplier_id FROM suppliers WHERE supplier_name = 'Put a cork in it'), 'Corks', '2024-07-05', '2024-07-15', 60000),	
    ((SELECT supplier_id FROM suppliers WHERE supplier_name = 'Label this'), 'Labels', '2024-07-10', '2024-07-10', 7500),
    ((SELECT supplier_id FROM suppliers WHERE supplier_name = 'Label this'), 'Boxes', '2024-08-15', '2024-08-20', 8000),
    ((SELECT supplier_id FROM suppliers WHERE supplier_name = 'Vat Man'), 'Vats', '2024-09-12', '2024-10-20', 700),
    ((SELECT supplier_id FROM suppliers WHERE supplier_name = 'Vat Man'), 'Tubing', '2024-11-12', '2024-11-12', 650),
    ((SELECT supplier_id FROM suppliers WHERE supplier_name = 'Barrel & Brew Co.'), 'Wine Barrels', '2025-10-15', '2025-10-16', 700),
    ((SELECT supplier_id FROM suppliers WHERE supplier_name = 'Vineyard Essentials'), 'Wine Barrels', '2025-12-10', '2025-12-12', 500);

-- insert the wines and grape varieties records
INSERT INTO wine_grape_variety(wine_name, grape_variety, vintage_year)
VALUES('Austins Merlot Mystique', 'Merlot', 2015),
      ('Marks Zinfandel Zen', 'Zinfandel', 2010),
      ('Justins Chardonnay Charm', 'Chardonnay', 2017),
      ('Tabari Breeze', 'Sauvignon Blanc', 2012),
      ('Micheal Calm', 'Gamay', 2008),
      ('Tammy Oasis', 'Bual', 2014);

-- insert sample records for wine sales. This new version is changed from showing an annual total to quarterly totals
INSERT INTO wine_sales(product_id, distributor_id, sales_quantity, sale_date, price_per_unit) 
VALUES((SELECT product_id FROM wine_grape_variety WHERE wine_name = 'Austins Merlot Mystique'), (SELECT distributor_id FROM distributors WHERE distributor_name = 'Austin Spirits'), 30000, '2024-01-02', 20.99),
      ((SELECT product_id FROM wine_grape_variety WHERE wine_name = 'Marks Zinfandel Zen'), (SELECT distributor_id FROM distributors WHERE distributor_name = 'Makers Mark'), 30000, '2024-01-05', 15.50),
	  ((SELECT product_id FROM wine_grape_variety WHERE wine_name = 'Justins Chardonnay Charm'), (SELECT distributor_id FROM distributors WHERE distributor_name = 'Just in Time'), 30000, '2024-01-02', 25.49),
	  ((SELECT product_id FROM wine_grape_variety WHERE wine_name = 'Tabari Breeze'), (SELECT distributor_id FROM distributors WHERE distributor_name = 'Tabari Distillery'), 30000, '2024-01-10', 22.00),
	  ((SELECT product_id FROM wine_grape_variety WHERE wine_name = 'Micheal Calm'), (SELECT distributor_id FROM distributors WHERE distributor_name = 'Tabari Distillery'), 3000, '2024-01-10', 16.00),
	  ((SELECT product_id FROM wine_grape_variety WHERE wine_name = 'Tammy Oasis'), (SELECT distributor_id FROM distributors WHERE distributor_name = 'Tabari Distillery'), 3000, '2024-01-10', 15.50),
      ((SELECT product_id FROM wine_grape_variety WHERE wine_name = 'Austins Merlot Mystique'), (SELECT distributor_id FROM distributors WHERE distributor_name = 'Austin Spirits'), 30000, '2024-03-08', 20.99),
      ((SELECT product_id FROM wine_grape_variety WHERE wine_name = 'Marks Zinfandel Zen'), (SELECT distributor_id FROM distributors WHERE distributor_name = 'Makers Mark'), 30000, '2024-03-02', 15.50),
	  ((SELECT product_id FROM wine_grape_variety WHERE wine_name = 'Justins Chardonnay Charm'), (SELECT distributor_id FROM distributors WHERE distributor_name = 'Just in Time'), 30000, '2024-03-15', 25.49),
	  ((SELECT product_id FROM wine_grape_variety WHERE wine_name = 'Tabari Breeze'), (SELECT distributor_id FROM distributors WHERE distributor_name = 'Tabari Distillery'), 30000, '2024-03-12', 22.00),  
      ((SELECT product_id FROM wine_grape_variety WHERE wine_name = 'Austins Merlot Mystique'), (SELECT distributor_id FROM distributors WHERE distributor_name = 'Austin Spirits'), 30000, '2024-06-05', 20.99),
      ((SELECT product_id FROM wine_grape_variety WHERE wine_name = 'Marks Zinfandel Zen'), (SELECT distributor_id FROM distributors WHERE distributor_name = 'Makers Mark'), 30000, '2024-06-08', 15.50),
	  ((SELECT product_id FROM wine_grape_variety WHERE wine_name = 'Justins Chardonnay Charm'), (SELECT distributor_id FROM distributors WHERE distributor_name = 'Just in Time'), 30000, '2024-06-02', 25.49),
	  ((SELECT product_id FROM wine_grape_variety WHERE wine_name = 'Tabari Breeze'), (SELECT distributor_id FROM distributors WHERE distributor_name = 'Tabari Distillery'), 30000, '2024-06-01', 22.00),
	  ((SELECT product_id FROM wine_grape_variety WHERE wine_name = 'Austins Merlot Mystique'), (SELECT distributor_id FROM distributors WHERE distributor_name = 'Austin Spirits'), 30000, '2024-10-15', 20.99),
      ((SELECT product_id FROM wine_grape_variety WHERE wine_name = 'Marks Zinfandel Zen'), (SELECT distributor_id FROM distributors WHERE distributor_name = 'Makers Mark'), 30000, '2024-09-12', 15.50),
	  ((SELECT product_id FROM wine_grape_variety WHERE wine_name = 'Justins Chardonnay Charm'), (SELECT distributor_id FROM distributors WHERE distributor_name = 'Just in Time'), 30000, '2024-10-02', 25.49),
	  ((SELECT product_id FROM wine_grape_variety WHERE wine_name = 'Tabari Breeze'), (SELECT distributor_id FROM distributors WHERE distributor_name = 'Tabari Distillery'), 30000, '2024-09-01', 22.00),
	  ((SELECT product_id FROM wine_grape_variety WHERE wine_name = 'Austins Merlot Mystique'), (SELECT distributor_id FROM distributors WHERE distributor_name = 'Austin Spirits'), 30000, '2025-01-03', 20.99),
      ((SELECT product_id FROM wine_grape_variety WHERE wine_name = 'Marks Zinfandel Zen'), (SELECT distributor_id FROM distributors WHERE distributor_name = 'Makers Mark'), 30000, '2025-01-03', 15.50),
	  ((SELECT product_id FROM wine_grape_variety WHERE wine_name = 'Justins Chardonnay Charm'), (SELECT distributor_id FROM distributors WHERE distributor_name = 'Just in Time'), 30000, '2025-01-02', 25.49),
	  ((SELECT product_id FROM wine_grape_variety WHERE wine_name = 'Tabari Breeze'), (SELECT distributor_id FROM distributors WHERE distributor_name = 'Tabari Distillery'), 30000, '2025-01-05', 22.00);