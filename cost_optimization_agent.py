import pandas as pd

# =========================================================
# COST OPTIMIZATION AGENT
# =========================================================

DATA_PATH = "data/cost_data.csv"

df = pd.read_csv(DATA_PATH)

print("COST OPTIMIZATION AGENT")
print("=======================")

# ---------------------------------------------------------
# DATA PREPARATION
# ---------------------------------------------------------

df["report_date"] = pd.to_datetime(
    df["report_date"],
    errors="coerce"
)

df["amount"] = pd.to_numeric(
    df["amount"],
    errors="coerce"
)

df = df.dropna(
    subset=["amount", "report_date"]
)

print(f"\nTotal Cost Records: {len(df):,}")

# ---------------------------------------------------------
# TOTAL COST ANALYSIS
# ---------------------------------------------------------

total_cost = df["amount"].sum()

average_cost = df["amount"].mean()

highest_cost = df["amount"].max()

lowest_cost = df["amount"].min()

print("\nCOST SUMMARY")
print("------------")

print(f"Total Facility Cost : {total_cost:,.2f}")
print(f"Average Cost        : {average_cost:,.2f}")
print(f"Highest Cost        : {highest_cost:,.2f}")
print(f"Lowest Cost         : {lowest_cost:,.2f}")

# ---------------------------------------------------------
# CATEGORY-WISE COST ANALYSIS
# ---------------------------------------------------------

category_analysis = (
    df.groupby("category")
    .agg(
        Total_Cost=("amount", "sum"),
        Average_Cost=("amount", "mean"),
        Number_of_Records=("amount", "count")
    )
    .reset_index()
)

category_analysis = category_analysis.sort_values(
    by="Total_Cost",
    ascending=False
)

print("\nCATEGORY-WISE COST ANALYSIS")
print("---------------------------")

print(
    category_analysis.to_string(index=False)
)

# ---------------------------------------------------------
# MONTHLY COST ANALYSIS
# ---------------------------------------------------------

df["month"] = df["report_date"].dt.to_period("M").astype(str)

monthly_cost = (
    df.groupby("month")["amount"]
    .sum()
    .reset_index()
)

monthly_cost = monthly_cost.sort_values("month")

print("\nMONTHLY COST ANALYSIS")
print("---------------------")

print(
    monthly_cost.to_string(index=False)
)

# ---------------------------------------------------------
# HIGHEST COST CATEGORY
# ---------------------------------------------------------

highest_cost_category = category_analysis.iloc[0]["category"]

highest_category_amount = category_analysis.iloc[0]["Total_Cost"]

print("\nCOST OPTIMIZATION INSIGHTS")
print("--------------------------")

print(
    f"Highest-cost category: "
    f"{highest_cost_category}"
)

print(
    f"Cost in highest category: "
    f"{highest_category_amount:,.2f}"
)

# ---------------------------------------------------------
# COST RISK DETECTION
# ---------------------------------------------------------

category_share = (
    highest_category_amount / total_cost
) * 100

print(
    f"Highest-cost category represents "
    f"{category_share:.2f}% of total facility cost."
)

if category_share >= 40:

    print(
        "🔴 HIGH COST CONCENTRATION: "
        "A major portion of facility cost is concentrated "
        "in one category."
    )

elif category_share >= 20:

    print(
        "🟠 MEDIUM COST CONCENTRATION: "
        "A significant portion of facility cost is "
        "concentrated in one category."
    )

else:

    print(
        "🟢 LOW COST CONCENTRATION: "
        "Facility costs are distributed across categories."
    )

# ---------------------------------------------------------
# AI COST RECOMMENDATIONS
# ---------------------------------------------------------

print("\nAI COST OPTIMIZATION RECOMMENDATIONS")
print("------------------------------------")

if category_share >= 40:

    print(
        f"1. Review {highest_cost_category} expenses "
        "to identify major cost-saving opportunities."
    )

elif category_share >= 20:

    print(
        f"1. Monitor {highest_cost_category} expenses "
        "and identify possible optimization opportunities."
    )

else:

    print(
        "1. Continue monitoring all facility cost categories."
    )

print(
    "2. Compare monthly cost trends to identify "
    "unusual increases in facility expenses."
)

print(
    "3. Prioritize high-cost maintenance and "
    "facility activities for optimization."
)

print(
    "4. Use energy consumption information from "
    "the Energy Agent to identify energy-related savings."
)

print(
    "5. Use Maintenance Agent results to identify "
    "equipment-related cost reduction opportunities."
)

print(
    "6. Combine occupancy insights with facility costs "
    "to identify opportunities for better space utilization."
)

print(
    "7. Continuously monitor facility expenses and "
    "generate alerts for significant cost increases."
)

print("\nCost Optimization Agent completed successfully.")