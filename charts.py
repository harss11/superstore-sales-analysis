"""Charts for the Superstore Sales report."""
import sys
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

df = pd.read_csv(sys.argv[1], parse_dates=["Order Date"])
out = sys.argv[2]
plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.titleweight": "bold", "axes.titlesize": 13})
BLUE, GREEN, RED, GREY = "#2f6db5", "#3a9a5b", "#c94a3f", "#9aa0a6"

# Fig 5.1 Monthly sales trend
ms = df.set_index("Order Date")["Sales"].resample("MS").sum() / 1000
fig, ax = plt.subplots(figsize=(10, 4.2))
ax.plot(ms.index, ms.values, color=BLUE, lw=2)
ax.set_title("Figure 5.1: Monthly Sales, Jan 2009 - Dec 2012")
ax.set_ylabel("Sales (thousand $)")
ax.grid(axis="y", alpha=0.3)
fig.tight_layout(); fig.savefig(f"{out}/fig1_monthly_sales.png", dpi=160); plt.close(fig)

# Fig 5.2 Sales and profit by category
c = df.groupby("Product Category")[["Sales", "Profit"]].sum().sort_values("Sales", ascending=False) / 1e6
fig, ax = plt.subplots(figsize=(8, 4.2))
x = range(len(c)); w = 0.38
b1 = ax.bar([i - w/2 for i in x], c["Sales"], w, color=BLUE, label="Sales")
b2 = ax.bar([i + w/2 for i in x], c["Profit"], w, color=GREEN, label="Profit")
for bars in (b1, b2):
    for b in bars:
        ax.text(b.get_x() + b.get_width()/2, b.get_height() + 0.05, f"{b.get_height():.2f}", ha="center", fontsize=10)
ax.set_xticks(list(x)); ax.set_xticklabels(c.index)
ax.set_ylabel("Million $"); ax.legend(frameon=False)
ax.set_title("Figure 5.2: Sales and Profit by Product Category")
fig.tight_layout(); fig.savefig(f"{out}/fig2_category.png", dpi=160); plt.close(fig)

# Fig 5.3 Sales by region
r = (df.groupby("Region")["Sales"].sum().sort_values() / 1e6)
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.barh(r.index, r.values, color=BLUE)
for i, v in enumerate(r.values):
    ax.text(v + 0.03, i, f"{v:.2f}", va="center", fontsize=10)
ax.set_xlabel("Sales (million $)")
ax.set_title("Figure 5.3: Sales by Region")
fig.tight_layout(); fig.savefig(f"{out}/fig3_region.png", dpi=160); plt.close(fig)

# Fig 5.4 Profit by sub-category
s = (df.groupby("Product Sub-Category")["Profit"].sum().sort_values() / 1000)
fig, ax = plt.subplots(figsize=(9, 6.5))
ax.barh(s.index, s.values, color=[RED if v < 0 else GREEN for v in s.values])
ax.axvline(0, color=GREY, lw=1)
ax.set_xlabel("Profit (thousand $)")
ax.set_title("Figure 5.4: Profit by Product Sub-Category (red = loss)")
fig.tight_layout(); fig.savefig(f"{out}/fig4_subcategory_profit.png", dpi=160); plt.close(fig)
print("done")
