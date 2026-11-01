-- MySQL 8.0+ schema: staging ledger for import, plus normalized dimensions/fact with PK/FKs.
CREATE DATABASE IF NOT EXISTS retail_analytics CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE retail_analytics;
DROP TABLE IF EXISTS retail_sales_fact;
DROP TABLE IF EXISTS dim_product;
DROP TABLE IF EXISTS dim_country;
DROP TABLE IF EXISTS dim_customer;
DROP TABLE IF EXISTS retail_transactions;
CREATE TABLE retail_transactions (
  row_id BIGINT AUTO_INCREMENT PRIMARY KEY,
  InvoiceNo VARCHAR(20) NOT NULL,
  StockCode VARCHAR(30) NOT NULL,
  Description VARCHAR(255),
  Quantity INT NOT NULL,
  InvoiceDate DATETIME NOT NULL,
  UnitPrice DECIMAL(12,4) NOT NULL,
  CustomerID INT NULL,
  Country VARCHAR(80) NOT NULL,
  IsCancellation BOOLEAN NOT NULL,
  LineRevenue DECIMAL(14,4) NOT NULL,
  INDEX ix_invoice_date (InvoiceDate), INDEX ix_customer (CustomerID),
  INDEX ix_country (Country), INDEX ix_stock (StockCode)
);
CREATE TABLE dim_customer (CustomerID INT PRIMARY KEY);
CREATE TABLE dim_product (StockCode VARCHAR(30) PRIMARY KEY, Description VARCHAR(255));
CREATE TABLE dim_country (Country VARCHAR(80) PRIMARY KEY);
CREATE TABLE retail_sales_fact (
  LineID BIGINT AUTO_INCREMENT PRIMARY KEY,
  InvoiceNo VARCHAR(20) NOT NULL,
  StockCode VARCHAR(30) NOT NULL,
  CustomerID INT NULL,
  Country VARCHAR(80) NOT NULL,
  InvoiceDate DATETIME NOT NULL,
  Quantity INT NOT NULL,
  UnitPrice DECIMAL(12,4) NOT NULL,
  IsCancellation BOOLEAN NOT NULL,
  LineRevenue DECIMAL(14,4) NOT NULL,
  CONSTRAINT fk_fact_product FOREIGN KEY (StockCode) REFERENCES dim_product(StockCode),
  CONSTRAINT fk_fact_customer FOREIGN KEY (CustomerID) REFERENCES dim_customer(CustomerID),
  CONSTRAINT fk_fact_country FOREIGN KEY (Country) REFERENCES dim_country(Country),
  INDEX ix_fact_date (InvoiceDate)
);
-- `retail_transactions` is an importable flat staging table; normalized dimensional tables are populated via 03_normalize_mysql.sql.
