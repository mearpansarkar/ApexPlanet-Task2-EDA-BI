# Task 2: Exploratory Data Analysis & Business Intelligence

**Dataset:** cleaned sales data from Task 1 (1,000 orders, 12 original + 12 engineered columns). Revenue is in INR (assumed).
**Tools:** Python (pandas, seaborn, matplotlib), SQLite, Excel.

## 1. Headline numbers
| Metric | Value |
|---|---|
| Total revenue | 139.4 million |
| Orders | 1,000 |
| Average order value | 139,399 |
| Units sold | 5,435 |
| Period | 1 Jan 2025 to 1 Jan 2026 (5 orders fall on 1 Jan 2026) |

## 2. Descriptive statistics (univariate)
| Variable | Mean | Median | Std | Min | Max | Skew |
|---|---|---|---|---|---|---|
| Age | 41.4 | 41 | 13.7 | 18 | 65 | 0.04 |
| Quantity | 5.4 | 5 | 2.8 | 1 | 10 | 0.06 |
| Unit_Price | 25,487 | 25,399 | 14,179 | 146 | 49,998 | -0.03 |
| Total_Sales | 139,399 | 108,594 | 114,100 | 437 | 493,678 | 0.99 |

![Histograms](charts/01_histograms.png)

- Age, Quantity and Unit_Price are close to evenly spread (skew near 0).
- **Total_Sales is right-skewed** (mean 139k vs median 109k): the top 25% of orders bring in about 55% of revenue.

**Categorical mix:** Male 51.1% / Female 48.9%. Electronics is 35.4% of orders; the other four categories are 15 to 18% each. Patna, Kolkata and Mumbai are the largest cities by order count; Pune is smallest (9.9%) apart from 13 orders with unknown city.

![Orders by category, city, gender](charts/02_orders_by_category_city_gender.png)
![Revenue by category](charts/03_revenue_by_category.png)

## 3. Trends over time
![Monthly revenue](charts/04_monthly_revenue.png)

- Revenue peaked in **March (13.1M)** and was lowest in **September (9.2M)**, with a clear Aug-Sep dip.
- **Q4 is the best quarter (37.4M, 27.0%)** and Q3 the weakest (30.4M, 21.9%).
- December has the most orders (98) but a low average order value (125.5k), so volume rose while basket value fell.

## 4. Multivariate analysis
![Correlation heatmap](charts/07_correlation_heatmap.png)

| Pair | Correlation |
|---|---|
| Total_Sales vs Unit_Price | 0.69 |
| Total_Sales vs Quantity | 0.65 |
| Age vs anything | about 0.00 |

Total_Sales depends on price and quantity (expected, since it is their product). **Age has no linear relationship with spending.**

![Price vs sales](charts/05_scatter_price_sales.png)
![Age vs sales](charts/06_scatter_age_sales.png)
![City x category](charts/08_heatmap_city_category.png)
![Age group x category](charts/09_heatmap_age_category.png)
![Pair plot](charts/11_pairplot.png)

## 5. Key insights
1. **Electronics drives the business**: 50.8M, or 36.4% of revenue (Laptop 25.4M, Mobile 25.3M). It is the top category in every known city, which is also a concentration risk.
2. **Top products:** Laptop, Mobile and Book are the top three by revenue (25.4M, 25.3M, 25.0M); Chair is last (21.5M).
3. **Cities:** Patna (19.3M), Kolkata (18.9M) and Bengaluru (18.8M) lead. Bengaluru has the highest average order value (153.9k); **Gaya is lowest on both revenue (14.4M) and average order value (122.9k)**.
4. **Customers aged 36-45 spend the most** (31.5M). The 18-25 group spends least (22.3M) mainly because it has the fewest orders (158), not smaller baskets: average order value is similar across all age groups (135k to 141k).
5. **Gender:** male customers generate slightly more revenue (72.5M vs 66.9M) with a similar basket size; Electronics is the top category for both.
6. **Seasonality:** a mid-year dip (Aug-Sep) followed by a strong Q4 suggests running promotions before September.

## 6. Data limitations to keep in mind
- Unit prices do not differ meaningfully by product (e.g. Rice averages about 26k, similar to Laptop), so the data appears synthetic. Product rankings are driven by how many orders and units were sold, not by price differences.
- 20 ages were imputed with the median; 13 orders have an unknown city.
- Some Customer_IDs are reused for different names, so customer-level (repeat purchase) analysis is not reliable. SQL joins use Customer_ID + Customer_Name.

## 7. SQL and dashboard
- Seven business questions answered in SQL (joins, aggregation, window function): see `sql_queries_with_results.md` and `sql_queries.sql`.
- Static dashboard mock-up with proposed KPIs: `ApexPlanet_Task2_Dashboard_Mockup.xlsx`.
