"""Superstore Sales Performance Analysis - data cleaning and EDA."""
import sys
import pandas as pd

path = sys.argv[1]
df = pd.read_csv(path, encoding="latin1")
print("Raw shape:", df.shape)

# ---------- Data cleaning ----------
print("Duplicate rows:", df.duplicated().sum())
df = df.drop_duplicates()
print("Missing values:\n", df.isna().sum()[df.isna().sum() > 0])
df["Product Base Margin"] = df["Product Base Margin"].fillna(df["Product Base Margin"].median())
df["Order Date"] = pd.to_datetime(df["Order Date"], format="%m/%d/%Y")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="%m/%d/%Y")
df["Year"] = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.month
df["Ship Days"] = (df["Ship Date"] - df["Order Date"]).dt.days
print("Date range:", df["Order Date"].min().date(), "to", df["Order Date"].max().date())
print("Orders:", df["Order ID"].nunique(), "Customers:", df["Customer Name"].nunique(),
      "Products:", df["Product Name"].nunique())

# ---------- KPIs ----------
sales, profit = df["Sales"].sum(), df["Profit"].sum()
print(f"\nTotal sales: {sales:,.0f}  Total profit: {profit:,.0f}  Margin: {profit/sales*100:.1f}%")
print(f"Total quantity: {df['Order Quantity'].sum():,}  Avg discount: {df['Discount'].mean()*100:.1f}%")
print(f"Avg ship days: {df['Ship Days'].mean():.1f}")


def summary(col):
    g = df.groupby(col).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Orders=("Order ID", "nunique"))
    g["Sales %"] = g["Sales"] / sales * 100
    g["Margin %"] = g["Profit"] / g["Sales"] * 100
    return g.sort_values("Sales", ascending=False).round(1)


pd.set_option("display.width", 200)
for col in ["Year", "Product Category", "Region", "Customer Segment", "Ship Mode", "Order Priority"]:
    print(f"\n=== By {col} ===\n", summary(col))

sub = summary("Product Sub-Category")
print("\n=== Top 5 sub-categories by sales ===\n", sub.head(5))
print("\n=== Loss-making sub-categories ===\n", sub[sub["Profit"] < 0].sort_values("Profit"))

m = df.groupby("Month")["Sales"].sum()
print("\n=== Sales by month (all years) ===\n", m.round(0))

prod = df.groupby("Product Name")["Sales"].sum().sort_values(ascending=False)
print("\n=== Top 5 products ===\n", prod.head(5).round(0))

# Discount vs profit
df["Discount band"] = pd.cut(df["Discount"], [-0.01, 0.02, 0.05, 0.08, 0.25],
                             labels=["0-2%", "3-5%", "6-8%", "9%+"])
print("\n=== Margin by discount band ===\n",
      df.groupby("Discount band", observed=True).apply(
          lambda x: pd.Series({"Rows": len(x), "Margin %": x["Profit"].sum() / x["Sales"].sum() * 100})).round(1))
print("\nCorrelation discount-profit:", round(df["Discount"].corr(df["Profit"]), 3))
print("Loss-making rows:", (df["Profit"] < 0).sum(), f"({(df['Profit'] < 0).mean()*100:.1f}%)")

df.to_csv(sys.argv[2], index=False)
