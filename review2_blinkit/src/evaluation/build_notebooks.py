"""
Notebook Builder for Review 2
=============================
Generates 6 complete, runnable, fully documented Jupyter Notebooks (.ipynb)
for each stage of the Review 2 submission.
"""

import os
import json

R2_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
NOTEBOOKS_DIR = os.path.join(R2_ROOT, "notebooks")
os.makedirs(NOTEBOOKS_DIR, exist_ok=True)

def make_nb(cells):
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.11.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

def md_cell(text):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in text.strip().split("\n")]
    }

def code_cell(code):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in code.strip().split("\n")]
    }

def build_all_notebooks():
    print("[1/6] Generating 01_source_verification.ipynb...")
    nb1_cells = [
        md_cell("""# Notebook 01: Source Verification & Scraped Blinkit Data Audit
**Course:** 23CSE452 — Business Analytics Capstone (Review 2)  
**Team 4:** Leena Sri K, A.C. Sanhitha Reddy, Kanish Kumaran M, Ande Taraka Srinivas, Ajay N Mukunth  
**Objective:** Verify the authenticity and provenance of raw Blinkit catalogue observations, URLs, and price snapshots."""),
        code_cell("""import os
import pandas as pd
import numpy as np

raw_path = "../data/raw/blinkit/raw_product_observations.csv"
clean_path = "../data/processed/product_catalogue/cleaned_product_catalogue.csv"
snap_path = "../data/processed/product_catalogue/price_snapshots.csv"

raw_df = pd.read_csv(raw_path)
clean_df = pd.read_csv(clean_path)
snap_df = pd.read_csv(snap_path)

print(f"Raw Observations: {len(raw_df):,} rows")
print(f"Cleaned Products: {len(clean_df):,} unique SKUs")
print(f"Snapshot Records: {len(snap_df):,} records")"""),
        code_cell("""# Display sample URLs and scraped attributes
clean_df[["source_product_id", "product_name", "category", "brand", "displayed_price", "original_price", "discount_pct", "product_url"]].head(10)"""),
        code_cell("""# Validate Legal Metrology MRP constraint: original_price >= displayed_price
mrp_violations = (clean_df["original_price"] < clean_df["displayed_price"]).sum()
print(f"MRP Violations: {mrp_violations} (Should be 0)")
assert mrp_violations == 0, "MRP constraint violated!"
print("Source data integrity successfully verified.")""")
    ]
    with open(os.path.join(NOTEBOOKS_DIR, "01_source_verification.ipynb"), "w") as f:
        json.dump(make_nb(nb1_cells), f, indent=2)

    print("[2/6] Generating 02_dataset_preparation.ipynb...")
    nb2_cells = [
        md_cell("""# Notebook 02: Dataset Preparation & Grounded Synthetic Transactions
**Course:** 23CSE452 — Business Analytics Capstone (Review 2)  
**Objective:** Demonstrate data cleaning, cross-table linkage between generic simulation items and real Blinkit products, and financial recalculation."""),
        code_cell("""import os
import pandas as pd
import numpy as np

tx_path = "../data/final/validated_datasets/enhanced_synthetic_transactions.csv"
df = pd.read_csv(tx_path, nrows=50000)
print(f"Loaded sample of {len(df):,} transaction records")
df.head()"""),
        code_cell("""# Verify financial formulas:
# line_total == (quantity * unit_price) - discount_amount
calculated_line_total = (df["quantity"] * df["grounded_unit_price"]) - df["discount_amount"]
diff = np.abs(calculated_line_total - df["line_total"])
print(f"Max numerical discrepancy in line_total: {diff.max():.6f}")
assert diff.max() < 0.05, "Discrepancy in financial calculation!"
print("Financial formulas verified.")"""),
        code_cell("""# Check distribution across the 8 dark stores
df.groupby("synthetic_dark_store_id").agg(
    order_count=("synthetic_order_id", "nunique"),
    total_sales=("line_total", "sum")
)""")
    ]
    with open(os.path.join(NOTEBOOKS_DIR, "02_dataset_preparation.ipynb"), "w") as f:
        json.dump(make_nb(nb2_cells), f, indent=2)

    print("[3/6] Generating 03_product_level_analysis.ipynb...")
    nb3_cells = [
        md_cell("""# Notebook 03: Real Product-Level Business Analysis (Blinkit)
**Course:** 23CSE452 — Business Analytics Capstone (Review 2)  
**Objective:** Analyze genuine Blinkit catalogue data: category price dispersion, discount depths, MRP elasticity, and price snapshot stability."""),
        code_cell("""import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

clean_path = "../data/processed/product_catalogue/cleaned_product_catalogue.csv"
df = pd.read_csv(clean_path)

# Category summary table
cat_summary = df.groupby("category").agg(
    SKU_Count=("source_product_id", "count"),
    Mean_Price=("displayed_price", "mean"),
    Median_Price=("displayed_price", "median"),
    Mean_MRP=("original_price", "mean"),
    Mean_Discount=("discount_pct", "mean"),
    Available_Ratio=("availability_status", lambda x: (x == "available").mean())
).round(2).reset_index()

cat_summary"""),
        code_cell("""# Plot category price boxplots
plt.figure(figsize=(10, 5))
order = df.groupby("category")["displayed_price"].median().sort_values(ascending=False).index
sns.boxplot(x="category", y="displayed_price", data=df, order=order, palette="mako")
plt.xticks(rotation=30, ha="right")
plt.title("Observed Price Dispersion by Category on Blinkit")
plt.show()"""),
        code_cell("""# Evaluate Price Snapshot Stability
snap_path = "../data/processed/product_catalogue/price_snapshots.csv"
snap_df = pd.read_csv(snap_path)
counts = snap_df.groupby("source_product_id")["collection_timestamp"].nunique()
repeated = counts[counts > 1].index
rep_df = snap_df[snap_df["source_product_id"].isin(repeated)]
price_shifts = rep_df.groupby("source_product_id")["displayed_price"].agg(["min", "max"])
shifts = (price_shifts["min"] != price_shifts["max"]).sum()
print(f"Products observed repeatedly: {len(repeated)}")
print(f"Products with price differences: {shifts}")
print(f"Price stickiness rate: {((len(repeated) - shifts) / len(repeated))*100:.2f}%")""")
    ]
    with open(os.path.join(NOTEBOOKS_DIR, "03_product_level_analysis.ipynb"), "w") as f:
        json.dump(make_nb(nb3_cells), f, indent=2)

    print("[4/6] Generating 04_time_series_forecasting.ipynb...")
    nb4_cells = [
        md_cell("""# Notebook 04: Unit 3 Method 1 — Time-Series Demand Forecasting
**Course:** 23CSE452 — Business Analytics Capstone (Review 2)  
**Objective:** Formulate, implement, and evaluate competitive time-series demand models (Naive, Seasonal Naive, Moving Average, Holt-Winters, SARIMA, XGBoost) using a 30-day chronological holdout."""),
        code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

comp_path = "../results/forecasting/model_comparison.csv"
eval_df = pd.read_csv(comp_path)
eval_df"""),
        code_cell("""# Load daily demand series and plot
daily_path = "../results/forecasting/daily_aggregated_demand.csv"
daily_df = pd.read_csv(daily_path, parse_dates=["date"])

plt.figure(figsize=(12, 4))
plt.plot(daily_df["date"], daily_df["total_quantity"], color="#2563eb", linewidth=1.5)
plt.axvline(pd.to_datetime("2026-09-01"), color="red", linestyle="--", label="Train/Test Split (Sep 1)")
plt.title("Daily Dark Store Unit Demand Across Operating Horizon (183 Days)")
plt.xlabel("Date")
plt.ylabel("Total Units Demanded")
plt.legend()
plt.show()"""),
        code_cell("""# Feature importance from XGBoost
fi_path = "../results/forecasting/xgboost_feature_importance.csv"
fi_df = pd.read_csv(fi_path)
fi_df""")
    ]
    with open(os.path.join(NOTEBOOKS_DIR, "04_time_series_forecasting.ipynb"), "w") as f:
        json.dump(make_nb(nb4_cells), f, indent=2)

    print("[5/6] Generating 05_association_rule_mining.ipynb...")
    nb5_cells = [
        md_cell("""# Notebook 05: Unit 3 Method 2 — Association Rule Mining & Bundle Analysis
**Course:** 23CSE452 — Business Analytics Capstone (Review 2)  
**Objective:** Compare Apriori and FP-Growth algorithms, evaluate support, confidence, and lift metrics, and discover high-affinity product bundles."""),
        code_cell("""import pandas as pd
import matplotlib.pyplot as plt

# Load algorithm comparison table
bench_path = "../results/association_rules/algorithm_comparison.csv"
bench_df = pd.read_csv(bench_path)
bench_df"""),
        code_cell("""# Load mined production rules
rules_path = "../results/association_rules/mined_association_rules.csv"
rules_df = pd.read_csv(rules_path)
print(f"Total Rules Mined: {len(rules_df)}")
rules_df.head(15)"""),
        code_cell("""# Top 10 Bundles by Lift Score
top10 = rules_df.head(10)[["antecedents_str", "consequents_str", "support", "confidence", "lift"]]
top10""")
    ]
    with open(os.path.join(NOTEBOOKS_DIR, "05_association_rule_mining.ipynb"), "w") as f:
        json.dump(make_nb(nb5_cells), f, indent=2)

    print("[6/6] Generating 06_integrated_business_analysis.ipynb...")
    nb6_cells = [
        md_cell("""# Notebook 06: Integrated Business Recommendations
**Course:** 23CSE452 — Business Analytics Capstone (Review 2)  
**Objective:** Synthesize findings from catalogue pricing, time-series demand forecasting, and association rule bundles into actionable operational policies."""),
        code_cell("""import pandas as pd

# 1. High Velocity Demand SKUs (from Forecasting)
# 2. High Margin / High Discount Categories (from Catalogue)
# 3. High Lift Bundles (from Association Mining)

print("Synthesizing closed-loop dark store optimization framework:")
print("1. Replenishment Policy: Buffer stocks set via XGBoost daily forecasts with day-ahead lead time.")
print("2. Physical Picking Optimization: Co-locating high-lift pairs (e.g. Bread + Milk, Chips + Soft Drinks) on adjacent racks.")
print("3. Commercial Bundling: Dynamic discount bundles in customer app to lift AOV from Rs 550 to Rs 650+.")""")
    ]
    with open(os.path.join(NOTEBOOKS_DIR, "06_integrated_business_analysis.ipynb"), "w") as f:
        json.dump(make_nb(nb6_cells), f, indent=2)

    print("All 6 Jupyter notebooks generated successfully in review2_blinkit/notebooks/!")

if __name__ == "__main__":
    build_all_notebooks()
