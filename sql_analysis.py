import sqlite3, pandas as pd
df = pd.read_csv("cleaned_sales_dataset.csv")
con = sqlite3.connect("sales.db")
# Normalised tables so multi-table JOINs are meaningful
df[["Customer_ID","Customer_Name","Age","Gender","City","Age_Group"]].drop_duplicates(["Customer_ID","Customer_Name"]).to_sql("customers", con, if_exists="replace", index=False)
df[["Product","Category"]].drop_duplicates().to_sql("products", con, if_exists="replace", index=False)
df[["Order_ID","Order_Date","Customer_ID","Customer_Name","Product","Quantity","Unit_Price","Total_Sales","Order_Month","Order_Quarter"]].to_sql("orders", con, if_exists="replace", index=False)

Q = [
("Q1. What are the top 5 products by revenue?",
"""SELECT o.Product, p.Category, COUNT(*) AS orders, SUM(o.Quantity) AS units,
       ROUND(SUM(o.Total_Sales),2) AS revenue
FROM orders o JOIN products p ON o.Product = p.Product
GROUP BY o.Product, p.Category
ORDER BY revenue DESC LIMIT 5;"""),
("Q2. What is the monthly revenue and order trend?",
"""SELECT strftime('%Y-%m', Order_Date) AS month, COUNT(*) AS orders,
       ROUND(SUM(Total_Sales),2) AS revenue, ROUND(AVG(Total_Sales),2) AS avg_order_value
FROM orders GROUP BY month ORDER BY month;"""),
("Q3. Which cities generate the most revenue, and what is the average order value per city?",
"""SELECT c.City, COUNT(*) AS orders, ROUND(SUM(o.Total_Sales),2) AS revenue,
       ROUND(AVG(o.Total_Sales),2) AS avg_order_value
FROM orders o JOIN customers c ON o.Customer_ID = c.Customer_ID AND o.Customer_Name = c.Customer_Name
GROUP BY c.City ORDER BY revenue DESC;"""),
("Q4. Which category earns the most revenue in each city? (top category per city)",
"""WITH city_cat AS (
  SELECT c.City, p.Category, ROUND(SUM(o.Total_Sales),2) AS revenue
  FROM orders o JOIN customers c ON o.Customer_ID = c.Customer_ID AND o.Customer_Name = c.Customer_Name
                JOIN products p ON o.Product = p.Product
  GROUP BY c.City, p.Category),
ranked AS (SELECT *, RANK() OVER (PARTITION BY City ORDER BY revenue DESC) AS rnk FROM city_cat)
SELECT City, Category, revenue FROM ranked WHERE rnk = 1 ORDER BY revenue DESC;"""),
("Q5. Which age group spends the most?",
"""SELECT c.Age_Group, COUNT(*) AS orders, ROUND(SUM(o.Total_Sales),2) AS revenue,
       ROUND(AVG(o.Total_Sales),2) AS avg_order_value
FROM orders o JOIN customers c ON o.Customer_ID = c.Customer_ID AND o.Customer_Name = c.Customer_Name
GROUP BY c.Age_Group ORDER BY c.Age_Group;"""),
("Q6. How does revenue split by gender and category?",
"""SELECT c.Gender, p.Category, COUNT(*) AS orders, ROUND(SUM(o.Total_Sales),2) AS revenue
FROM orders o JOIN customers c ON o.Customer_ID = c.Customer_ID AND o.Customer_Name = c.Customer_Name
              JOIN products p ON o.Product = p.Product
GROUP BY c.Gender, p.Category ORDER BY c.Gender, revenue DESC;"""),
("Q7. Which 2025 quarter performed best, and what is each quarter's share of 2025 revenue?",
"""SELECT Order_Quarter, COUNT(*) AS orders, ROUND(SUM(Total_Sales),2) AS revenue,
       ROUND(100.0*SUM(Total_Sales)/(SELECT SUM(Total_Sales) FROM orders WHERE Order_Date < '2026-01-01'),1) AS pct_of_total
FROM orders WHERE Order_Date < '2026-01-01'
GROUP BY Order_Quarter ORDER BY Order_Quarter;"""),
]
sql_out, md = [], ["# SQL Queries with Results\n", "Note: the dataset has 5 orders dated 1 Jan 2026; Q7 uses 2025 orders only. Joins use Customer_ID + Customer_Name because some Customer_IDs are reused (flagged in Task 1).\n", "Database: `sales.db` (SQLite) with tables `customers`, `products`, `orders` built from the cleaned dataset (Task 1).\n"]
for title, q in Q:
    r = pd.read_sql_query(q, con)
    sql_out.append(f"-- {title}\n{q}\n")
    md += [f"## {title}\n", "```sql", q, "```\n", r.to_markdown(index=False), "\n"]
    print("=====", title); print(r.to_string(index=False))
open("sql_queries.sql","w").write("\n".join(sql_out))
open("sql_queries_with_results.md","w").write("\n".join(md))
