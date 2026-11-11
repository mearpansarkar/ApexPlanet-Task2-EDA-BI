# SQL Queries with Results

Note: the dataset has 5 orders dated 1 Jan 2026; Q7 uses 2025 orders only. Joins use Customer_ID + Customer_Name because some Customer_IDs are reused (flagged in Task 1).

Database: `sales.db` (SQLite) with tables `customers`, `products`, `orders` built from the cleaned dataset (Task 1).

## Q1. What are the top 5 products by revenue?

```sql
SELECT o.Product, p.Category, COUNT(*) AS orders, SUM(o.Quantity) AS units,
       ROUND(SUM(o.Total_Sales),2) AS revenue
FROM orders o JOIN products p ON o.Product = p.Product
GROUP BY o.Product, p.Category
ORDER BY revenue DESC LIMIT 5;
```

| Product   | Category    |   orders |   units |     revenue |
|:----------|:------------|---------:|--------:|------------:|
| Laptop    | Electronics |      170 |     970 | 2.5443e+07  |
| Mobile    | Electronics |      184 |    1008 | 2.53356e+07 |
| Book      | Education   |      178 |     977 | 2.50317e+07 |
| Rice      | Grocery     |      153 |     826 | 2.22317e+07 |
| Chair     | Furniture   |      159 |     855 | 2.15216e+07 |


## Q2. What is the monthly revenue and order trend?

```sql
SELECT strftime('%Y-%m', Order_Date) AS month, COUNT(*) AS orders,
       ROUND(SUM(Total_Sales),2) AS revenue, ROUND(AVG(Total_Sales),2) AS avg_order_value
FROM orders GROUP BY month ORDER BY month;
```

| month   |   orders |          revenue |   avg_order_value |
|:--------|---------:|-----------------:|------------------:|
| 2025-01 |       76 |      1.00962e+07 |            132845 |
| 2025-02 |       86 |      1.15112e+07 |            133851 |
| 2025-03 |       89 |      1.30599e+07 |            146740 |
| 2025-04 |       80 |      1.22227e+07 |            152784 |
| 2025-05 |       85 |      1.09847e+07 |            129232 |
| 2025-06 |       83 |      1.29123e+07 |            155570 |
| 2025-07 |       83 |      1.17462e+07 |            141521 |
| 2025-08 |       75 |      9.44847e+06 |            125980 |
| 2025-09 |       79 |      9.1799e+06  |            116201 |
| 2025-10 |       84 |      1.25009e+07 |            148821 |
| 2025-11 |       77 |      1.26276e+07 |            163995 |
| 2025-12 |       98 |      1.22999e+07 |            125509 |
| 2026-01 |        5 | 809390           |            161878 |


## Q3. Which cities generate the most revenue, and what is the average order value per city?

```sql
SELECT c.City, COUNT(*) AS orders, ROUND(SUM(o.Total_Sales),2) AS revenue,
       ROUND(AVG(o.Total_Sales),2) AS avg_order_value
FROM orders o JOIN customers c ON o.Customer_ID = c.Customer_ID AND o.Customer_Name = c.Customer_Name
GROUP BY c.City ORDER BY revenue DESC;
```

| City      |   orders |     revenue |   avg_order_value |
|:----------|---------:|------------:|------------------:|
| Patna     |      135 | 1.9286e+07  |            142859 |
| Kolkata   |      133 | 1.88843e+07 |            141988 |
| Bengaluru |      122 | 1.87736e+07 |            153882 |
| Mumbai    |      131 | 1.87571e+07 |            143184 |
| Hyderabad |      125 | 1.71668e+07 |            137334 |
| Delhi     |      125 | 1.60971e+07 |            128777 |
| Pune      |       99 | 1.45132e+07 |            146598 |
| Gaya      |      117 | 1.43809e+07 |            122913 |
| Unknown   |       13 | 1.54062e+06 |            118509 |


## Q4. Which category earns the most revenue in each city? (top category per city)

```sql
WITH city_cat AS (
  SELECT c.City, p.Category, ROUND(SUM(o.Total_Sales),2) AS revenue
  FROM orders o JOIN customers c ON o.Customer_ID = c.Customer_ID AND o.Customer_Name = c.Customer_Name
                JOIN products p ON o.Product = p.Product
  GROUP BY c.City, p.Category),
ranked AS (SELECT *, RANK() OVER (PARTITION BY City ORDER BY revenue DESC) AS rnk FROM city_cat)
SELECT City, Category, revenue FROM ranked WHERE rnk = 1 ORDER BY revenue DESC;
```

| City      | Category    |          revenue |
|:----------|:------------|-----------------:|
| Kolkata   | Electronics |      7.6802e+06  |
| Mumbai    | Electronics |      7.60986e+06 |
| Patna     | Electronics |      6.49912e+06 |
| Bengaluru | Electronics |      6.13855e+06 |
| Delhi     | Electronics |      6.03257e+06 |
| Pune      | Electronics |      5.98661e+06 |
| Hyderabad | Electronics |      5.63263e+06 |
| Gaya      | Electronics |      4.7832e+06  |
| Unknown   | Furniture   | 617547           |


## Q5. Which age group spends the most?

```sql
SELECT c.Age_Group, COUNT(*) AS orders, ROUND(SUM(o.Total_Sales),2) AS revenue,
       ROUND(AVG(o.Total_Sales),2) AS avg_order_value
FROM orders o JOIN customers c ON o.Customer_ID = c.Customer_ID AND o.Customer_Name = c.Customer_Name
GROUP BY c.Age_Group ORDER BY c.Age_Group;
```

| Age_Group   |   orders |     revenue |   avg_order_value |
|:------------|---------:|------------:|------------------:|
| 18-25       |      158 | 2.22841e+07 |            141039 |
| 26-35       |      219 | 2.96323e+07 |            135307 |
| 36-45       |      223 | 3.15332e+07 |            141405 |
| 46-55       |      202 | 2.82165e+07 |            139686 |
| 56-65       |      198 | 2.77333e+07 |            140067 |


## Q6. How does revenue split by gender and category?

```sql
SELECT c.Gender, p.Category, COUNT(*) AS orders, ROUND(SUM(o.Total_Sales),2) AS revenue
FROM orders o JOIN customers c ON o.Customer_ID = c.Customer_ID AND o.Customer_Name = c.Customer_Name
              JOIN products p ON o.Product = p.Product
GROUP BY c.Gender, p.Category ORDER BY c.Gender, revenue DESC;
```

| Gender   | Category    |   orders |     revenue |
|:---------|:------------|---------:|------------:|
| Female   | Electronics |      158 | 2.26255e+07 |
| Female   | Education   |       96 | 1.28444e+07 |
| Female   | Fashion     |       89 | 1.15453e+07 |
| Female   | Furniture   |       74 | 1.00868e+07 |
| Female   | Grocery     |       72 | 9.83382e+06 |
| Male     | Electronics |      196 | 2.81531e+07 |
| Male     | Grocery     |       81 | 1.23979e+07 |
| Male     | Education   |       82 | 1.21873e+07 |
| Male     | Furniture   |       85 | 1.14347e+07 |
| Male     | Fashion     |       67 | 8.29057e+06 |


## Q7. Which 2025 quarter performed best, and what is each quarter's share of 2025 revenue?

```sql
SELECT Order_Quarter, COUNT(*) AS orders, ROUND(SUM(Total_Sales),2) AS revenue,
       ROUND(100.0*SUM(Total_Sales)/(SELECT SUM(Total_Sales) FROM orders WHERE Order_Date < '2026-01-01'),1) AS pct_of_total
FROM orders WHERE Order_Date < '2026-01-01'
GROUP BY Order_Quarter ORDER BY Order_Quarter;
```

| Order_Quarter   |   orders |     revenue |   pct_of_total |
|:----------------|---------:|------------:|---------------:|
| Q1              |      251 | 3.46673e+07 |           25   |
| Q2              |      248 | 3.61197e+07 |           26.1 |
| Q3              |      237 | 3.03746e+07 |           21.9 |
| Q4              |      259 | 3.74285e+07 |           27   |

