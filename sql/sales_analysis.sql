
-- E-commerce Revenue Intelligence Dashboard
-- SQL analysis queries

-- Query 1: View the first 10 records
SELECT *
FROM cleaned_retail
LIMIT 10;

-- Query 2: Count total records
SELECT COUNT(*) AS total_records
FROM cleaned_retail;

-- Query 3: Calculate total revenue
SELECT SUM(Quantity * UnitPrice) AS total_revenue
FROM cleaned_retail;

-- Query 4: Count unique customers
SELECT COUNT(DISTINCT CustomerID) AS unique_customers
FROM cleaned_retail;

-- Query 5: Find the top 10 products by revenue
SELECT
    Description,
    SUM(Quantity * UnitPrice) AS revenue
FROM cleaned_retail
GROUP BY Description
ORDER BY revenue DESC
LIMIT 10;
