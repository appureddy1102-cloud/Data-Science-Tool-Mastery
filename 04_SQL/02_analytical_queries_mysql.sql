USE retail_analytics;
-- 01: Basic data sample
SELECT * FROM retail_transactions LIMIT 20;
-- 02: Revenue by month
SELECT DATE_FORMAT(InvoiceDate,'%Y-%m') AS month, SUM(LineRevenue) AS gross_sales FROM retail_transactions WHERE IsCancellation=0 AND Quantity>0 AND UnitPrice>0 GROUP BY month ORDER BY month;
-- 03: Revenue by country
SELECT Country,SUM(LineRevenue) sales FROM retail_transactions WHERE IsCancellation=0 AND Quantity>0 AND UnitPrice>0 GROUP BY Country ORDER BY sales DESC;
-- 04: Order count per country
SELECT Country,COUNT(DISTINCT InvoiceNo) orders FROM retail_transactions WHERE IsCancellation=0 GROUP BY Country ORDER BY orders DESC;
-- 05: Top 20 products
SELECT StockCode,MAX(Description) product,SUM(Quantity) units,SUM(LineRevenue) revenue FROM retail_transactions WHERE IsCancellation=0 AND Quantity>0 AND UnitPrice>0 GROUP BY StockCode ORDER BY revenue DESC LIMIT 20;
-- 06: Average invoice value
SELECT AVG(invoice_total) avg_order_value FROM (SELECT InvoiceNo,SUM(LineRevenue) invoice_total FROM retail_transactions WHERE IsCancellation=0 AND Quantity>0 AND UnitPrice>0 GROUP BY InvoiceNo) x;
-- 07: Daily KPIs
SELECT DATE(InvoiceDate) sales_date,COUNT(DISTINCT InvoiceNo) orders,SUM(Quantity) units,SUM(LineRevenue) sales FROM retail_transactions WHERE IsCancellation=0 AND Quantity>0 AND UnitPrice>0 GROUP BY DATE(InvoiceDate) ORDER BY sales_date;
-- 08: Customers with at least 5 orders (HAVING)
SELECT CustomerID,COUNT(DISTINCT InvoiceNo) order_count,SUM(LineRevenue) revenue FROM retail_transactions WHERE CustomerID IS NOT NULL AND IsCancellation=0 AND Quantity>0 GROUP BY CustomerID HAVING COUNT(DISTINCT InvoiceNo)>=5 ORDER BY revenue DESC;
-- 09: Cancellation count by month
SELECT DATE_FORMAT(InvoiceDate,'%Y-%m') month,COUNT(DISTINCT InvoiceNo) cancellation_invoices FROM retail_transactions WHERE IsCancellation=1 GROUP BY month ORDER BY month;
-- 10: Returns/negative quantities by country
SELECT Country,COUNT(*) return_lines,SUM(-Quantity*UnitPrice) return_value FROM retail_transactions WHERE Quantity<0 GROUP BY Country ORDER BY return_value DESC;
-- 11: CASE-based transaction status
SELECT CASE WHEN IsCancellation=1 THEN 'Cancellation' WHEN Quantity<0 THEN 'Return' ELSE 'Sale/Other' END status,COUNT(*) rows,SUM(LineRevenue) signed_value FROM retail_transactions GROUP BY status;
-- 12: Country revenue share using CTE
WITH c AS (SELECT Country,SUM(LineRevenue) revenue FROM retail_transactions WHERE IsCancellation=0 AND Quantity>0 AND UnitPrice>0 GROUP BY Country), t AS (SELECT SUM(revenue) total FROM c) SELECT c.Country,c.revenue,ROUND(100*c.revenue/t.total,2) share_pct FROM c CROSS JOIN t ORDER BY c.revenue DESC;
-- 13: Products priced above global average (subquery)
SELECT StockCode,MAX(Description) product,AVG(UnitPrice) avg_price FROM retail_transactions WHERE IsCancellation=0 AND UnitPrice>0 GROUP BY StockCode HAVING AVG(UnitPrice)>(SELECT AVG(UnitPrice) FROM retail_transactions WHERE IsCancellation=0 AND UnitPrice>0) ORDER BY avg_price DESC LIMIT 30;
-- 14: Window rank country sales
WITH c AS (SELECT Country,SUM(LineRevenue) revenue FROM retail_transactions WHERE IsCancellation=0 AND Quantity>0 GROUP BY Country) SELECT Country,revenue,DENSE_RANK() OVER(ORDER BY revenue DESC) country_rank FROM c;
-- 15: Monthly country rank (window function)
WITH m AS (SELECT DATE_FORMAT(InvoiceDate,'%Y-%m') month,Country,SUM(LineRevenue) revenue FROM retail_transactions WHERE IsCancellation=0 AND Quantity>0 AND UnitPrice>0 GROUP BY month,Country) SELECT month,Country,revenue,ROW_NUMBER() OVER(PARTITION BY month ORDER BY revenue DESC) rn FROM m;
-- 16: Customer recency/frequency/monetary (RFM-style)
SELECT CustomerID,DATEDIFF((SELECT MAX(InvoiceDate) FROM retail_transactions),MAX(InvoiceDate)) recency_days,COUNT(DISTINCT InvoiceNo) frequency,SUM(LineRevenue) monetary FROM retail_transactions WHERE CustomerID IS NOT NULL AND IsCancellation=0 AND Quantity>0 GROUP BY CustomerID ORDER BY monetary DESC;
-- 17: Average unit price by country
SELECT Country,AVG(UnitPrice) mean_unit_price FROM retail_transactions WHERE IsCancellation=0 AND UnitPrice>0 GROUP BY Country ORDER BY mean_unit_price DESC;
-- 18: Revenue by weekday
SELECT DAYNAME(InvoiceDate) weekday,SUM(LineRevenue) revenue FROM retail_transactions WHERE IsCancellation=0 AND Quantity>0 AND UnitPrice>0 GROUP BY WEEKDAY(InvoiceDate),DAYNAME(InvoiceDate) ORDER BY WEEKDAY(InvoiceDate);
-- 19: Sales with missing customer IDs
SELECT COUNT(*) unidentified_rows,SUM(LineRevenue) unidentified_revenue FROM retail_transactions WHERE CustomerID IS NULL AND IsCancellation=0 AND Quantity>0;
-- 20: Repeat-customer cohort size (CTE)
WITH f AS (SELECT CustomerID,COUNT(DISTINCT InvoiceNo) n FROM retail_transactions WHERE CustomerID IS NOT NULL AND IsCancellation=0 AND Quantity>0 GROUP BY CustomerID) SELECT CASE WHEN n=1 THEN 'One order' ELSE 'Repeat' END cohort,COUNT(*) customers FROM f GROUP BY cohort;
-- 21: Create reusable view
CREATE OR REPLACE VIEW valid_sales AS SELECT *,Quantity*UnitPrice AS GrossRevenue FROM retail_transactions WHERE IsCancellation=0 AND Quantity>0 AND UnitPrice>0;
-- 22: Query reusable view
SELECT Country,SUM(GrossRevenue) revenue FROM valid_sales GROUP BY Country ORDER BY revenue DESC LIMIT 10;
-- 23: Month-over-month revenue with LAG
WITH m AS (SELECT DATE_FORMAT(InvoiceDate,'%Y-%m-01') month_start,SUM(LineRevenue) revenue FROM valid_sales GROUP BY month_start) SELECT month_start,revenue,LAG(revenue) OVER(ORDER BY month_start) prior_month,revenue-LAG(revenue) OVER(ORDER BY month_start) change_amount FROM m ORDER BY month_start;
-- 24: Null and quality audit
SELECT COUNT(*) rows_total,SUM(CustomerID IS NULL) missing_customer,SUM(Description IS NULL) missing_description,SUM(Quantity<=0) nonpositive_quantity,SUM(UnitPrice<=0) nonpositive_price FROM retail_transactions;
-- 25: JOIN transaction lines to per-customer invoice counts and spend
WITH customer_orders AS (SELECT CustomerID,COUNT(DISTINCT InvoiceNo) order_count,SUM(LineRevenue) spend FROM retail_transactions WHERE CustomerID IS NOT NULL AND IsCancellation=0 AND Quantity>0 AND UnitPrice>0 GROUP BY CustomerID) SELECT t.CustomerID,t.order_count,t.spend FROM customer_orders t JOIN (SELECT DISTINCT CustomerID FROM retail_transactions WHERE CustomerID IS NOT NULL) ids ON ids.CustomerID=t.CustomerID ORDER BY t.spend DESC LIMIT 20;
-- 26: LEFT JOIN sales facts to country-level order summary (shows full matching country groups)
WITH country_orders AS (SELECT Country,COUNT(DISTINCT InvoiceNo) orders FROM retail_transactions WHERE IsCancellation=0 GROUP BY Country) SELECT c.Country,c.orders,COUNT(*) line_rows FROM country_orders c LEFT JOIN retail_transactions r ON r.Country=c.Country GROUP BY c.Country,c.orders ORDER BY c.orders DESC;
