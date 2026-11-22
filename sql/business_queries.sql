-- SQLite: open data/processed/retail.db
SELECT * FROM kpis;
SELECT Month, ROUND(SUM(Revenue),2) AS gross_sales, COUNT(DISTINCT InvoiceNo) AS invoices FROM sales GROUP BY Month ORDER BY Month;
SELECT StockCode, SUM(Quantity) AS units, ROUND(SUM(Revenue),2) AS revenue FROM sales GROUP BY StockCode ORDER BY revenue DESC LIMIT 10;
SELECT Country, ROUND(SUM(Revenue),2) AS revenue FROM sales GROUP BY Country ORDER BY revenue DESC;
WITH customer_orders AS (SELECT CustomerID, COUNT(DISTINCT InvoiceNo) AS orders FROM sales WHERE CustomerID IS NOT NULL GROUP BY CustomerID) SELECT ROUND(100.0*AVG(CASE WHEN orders>1 THEN 1.0 ELSE 0.0 END),2) AS repeat_rate FROM customer_orders;
WITH m AS (SELECT Month,SUM(Revenue) AS revenue FROM sales GROUP BY Month), prev AS (SELECT *, LAG(revenue) OVER(ORDER BY Month) AS previous FROM m) SELECT *, ROUND(100.0*(revenue-previous)/NULLIF(previous,0),2) AS growth_pct FROM prev;
SELECT Segment,COUNT(*) AS customers,ROUND(SUM(Monetary),2) AS gross_sales FROM rfm GROUP BY Segment ORDER BY customers DESC;
WITH s AS (SELECT Month,SUM(Revenue) AS gross FROM sales GROUP BY Month), r AS (SELECT Month,-SUM(Revenue) AS returns FROM returns GROUP BY Month), months AS (SELECT Month FROM s UNION SELECT Month FROM r) SELECT months.Month, COALESCE(gross,0) AS gross, COALESCE(returns,0) AS returns, COALESCE(gross,0)-COALESCE(returns,0) AS net FROM months LEFT JOIN s USING(Month) LEFT JOIN r USING(Month) ORDER BY months.Month;
