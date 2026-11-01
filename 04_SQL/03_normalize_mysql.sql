USE retail_analytics;
-- Populate dimensions before facts to satisfy FK constraints. Keep a NULL customer ID unknown rather than inventing a key.
INSERT INTO dim_customer(CustomerID) SELECT DISTINCT CustomerID FROM retail_transactions WHERE CustomerID IS NOT NULL;
INSERT INTO dim_product(StockCode,Description) SELECT StockCode,MAX(Description) FROM retail_transactions GROUP BY StockCode;
INSERT INTO dim_country(Country) SELECT DISTINCT Country FROM retail_transactions;
INSERT INTO retail_sales_fact(InvoiceNo,StockCode,CustomerID,Country,InvoiceDate,Quantity,UnitPrice,IsCancellation,LineRevenue)
SELECT InvoiceNo,StockCode,CustomerID,Country,InvoiceDate,Quantity,UnitPrice,IsCancellation,LineRevenue FROM retail_transactions;
-- Example star-schema join query
SELECT p.Description,c.Country,SUM(f.Quantity*f.UnitPrice) AS gross_sales
FROM retail_sales_fact f JOIN dim_product p ON f.StockCode=p.StockCode JOIN dim_country c ON f.Country=c.Country
WHERE f.IsCancellation=0 AND f.Quantity>0 AND f.UnitPrice>0
GROUP BY p.Description,c.Country ORDER BY gross_sales DESC LIMIT 25;
