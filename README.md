# Sales Performance Analysis of a Retail Superstore

Data Analytics internship project - Codec Technologies Pvt. Ltd. (1-31 October 2026)

**Author:** Harsh, Raj Kumar Goel Institute of Technology, Ghaziabad (AKTU)

## Objective

Analyse four years of retail sales data to find which products, regions and customer
segments drive sales and profit, and where the business is losing money.

## Dataset

- Superstore Sales dataset: 8,399 order lines, 21 columns, January 2009 to December 2012
- Source: [github.com/curran/data](https://github.com/curran/data/tree/gh-pages/superstoreSales)
- File: `data/superstore_sales_raw.csv`

## Tools

Python (Pandas, Matplotlib), SQL, Excel

## How to run

```bash
pip install pandas matplotlib
python analysis.py data/superstore_sales_raw.csv superstore_clean.csv
python charts.py superstore_clean.csv charts
```

## Key findings

| KPI | Value |
| --- | --- |
| Total sales | $14.92 million |
| Total profit | $1.52 million |
| Profit margin | 10.2% |

1. Technology is the most profitable category (40.1% of sales, 14.8% margin).
2. Furniture earns only a 2.3% margin. Tables (-$99,063) and Bookcases (-$33,582) make losses.
3. West is the largest region ($3.60M) but has a below-average margin (8.3%).
4. Delivery Truck orders have a 4.3% margin, compared with 14.7% for Regular Air.
5. Margin falls from 12.4% at 0-2% discount to 7.5% at 9% or more.
6. December and January are the peak sales months; June is the weakest.

## Charts

![Monthly sales](charts/fig1_monthly_sales.png)
![Sales and profit by category](charts/fig2_category.png)
![Sales by region](charts/fig3_region.png)
![Profit by sub-category](charts/fig4_subcategory_profit.png)
