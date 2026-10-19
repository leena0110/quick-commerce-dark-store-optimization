"""
Phase Four: Real Product-Level Business Analytics (Blinkit Catalogue)
=====================================================================
Analyzes real scraped catalog items (609 products across 9 categories):
- Price and MRP distributions
- Discount percentages by category
- Unit pricing analysis
- Inventory and availability
- Price snapshot stability
Generates publication figures and outputs summary CSV/JSON for report & website.
"""

import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

R2_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CATALOG_PATH = os.path.join(R2_ROOT, "data", "processed", "product_catalogue", "cleaned_product_catalogue.csv")
SNAPSHOTS_PATH = os.path.join(R2_ROOT, "data", "processed", "product_catalogue", "price_snapshots.csv")
CHARTS_DIR = os.path.join(R2_ROOT, "results", "charts")
RESULTS_DIR = os.path.join(R2_ROOT, "results", "product_analytics")

os.makedirs(CHARTS_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

# Set clean aesthetic styling
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["axes.edgecolor"] = "#cccccc"
plt.rcParams["axes.linewidth"] = 0.8

def run_product_analytics():
    print("[1/5] Loading real Blinkit catalogue and snapshot records...")
    df = pd.read_csv(CATALOG_PATH)
    snap_df = pd.read_csv(SNAPSHOTS_PATH)
    print(f"Loaded {len(df)} catalogue items and {len(snap_df)} snapshot observations.")

    # 1. Category Summary Metrics
    print("[2/5] Computing category-level pricing, discounts, and ratings...")
    cat_stats = df.groupby("category").agg(
        Product_Count=("source_product_id", "count"),
        Mean_Selling_Price=("displayed_price", "mean"),
        Median_Selling_Price=("displayed_price", "median"),
        Std_Selling_Price=("displayed_price", "std"),
        Min_Price=("displayed_price", "min"),
        Max_Price=("displayed_price", "max"),
        Mean_MRP=("original_price", "mean"),
        Mean_Discount_Pct=("discount_pct", "mean"),
        Mean_Rating=("rating", "mean"),
        Mean_Inventory=("inventory", "mean")
    ).round(2).reset_index()

    cat_stats["Catalog_Share_Pct"] = (cat_stats["Product_Count"] / len(df) * 100).round(2)
    cat_stats_path = os.path.join(RESULTS_DIR, "category_summary_metrics.csv")
    cat_stats.to_csv(cat_stats_path, index=False)
    print(f"Saved category summary to {cat_stats_path}")

    # 2. Snapshot Stability Analysis
    print("[3/5] Evaluating repeated price snapshot stability...")
    prod_counts = snap_df.groupby("source_product_id")["collection_timestamp"].nunique()
    repeated_ids = prod_counts[prod_counts > 1].index
    rep_df = snap_df[snap_df["source_product_id"].isin(repeated_ids)]

    price_diffs = rep_df.groupby("source_product_id")["displayed_price"].agg(["min", "max"])
    price_diffs["diff"] = price_diffs["max"] - price_diffs["min"]
    prods_with_price_change = (price_diffs["diff"] > 0).sum()

    snapshot_report = {
        "total_snapshot_records": int(len(snap_df)),
        "unique_products_observed": int(snap_df["source_product_id"].nunique()),
        "products_with_repeated_passes": int(len(repeated_ids)),
        "products_with_price_shift": int(prods_with_price_change),
        "price_stickiness_rate": float(round((len(repeated_ids) - prods_with_price_change) / len(repeated_ids) * 100, 2)),
        "reason_for_stickiness": "Indian Legal Metrology (Packaged Commodities) Rules mandate fixed printed MRP; retailers maintain EDLP with discrete promotional calendar shifts."
    }
    with open(os.path.join(RESULTS_DIR, "price_stability_audit.json"), "w") as f:
        json.dump(snapshot_report, f, indent=2)

    # 3. High-Quality Publication Visualizations
    print("[4/5] Generating publication charts...")

    # Chart 1: Category Price Boxplots
    plt.figure(figsize=(10, 6))
    order = df.groupby("category")["displayed_price"].median().sort_values(ascending=False).index
    palette = sns.color_palette("mako", len(order))
    ax = sns.boxplot(x="category", y="displayed_price", data=df, order=order, palette=palette, fliersize=3)
    plt.xticks(rotation=35, ha="right", fontsize=10)
    plt.title("Blinkit Catalogue: Observed Price Distribution by Category", fontsize=13, fontweight="bold", pad=15)
    plt.xlabel("Category", fontsize=11, fontweight="bold")
    plt.ylabel("Selling Price (INR)", fontsize=11, fontweight="bold")
    plt.tight_layout()
    chart1_path = os.path.join(CHARTS_DIR, "01_catalogue_price_boxplots.png")
    plt.savefig(chart1_path, dpi=300)
    plt.close()

    # Chart 2: Category Product Counts & Mean Discount
    fig, ax1 = plt.subplots(figsize=(10, 5.5))
    ax2 = ax1.twinx()
    
    cat_sorted = cat_stats.sort_values(by="Product_Count", ascending=False)
    x = np.arange(len(cat_sorted))
    width = 0.4
    
    bars = ax1.bar(x - width/2, cat_sorted["Product_Count"], width, label="Product Count", color="#1a365d")
    line = ax2.plot(x + width/2, cat_sorted["Mean_Discount_Pct"], color="#e53e3e", marker="o", linewidth=2.5, label="Mean Discount (%)")
    
    ax1.set_xticks(x)
    ax1.set_xticklabels(cat_sorted["category"], rotation=35, ha="right", fontsize=10)
    ax1.set_ylabel("Number of Scraped SKUs", fontsize=11, fontweight="bold", color="#1a365d")
    ax2.set_ylabel("Average Promotional Discount (%)", fontsize=11, fontweight="bold", color="#e53e3e")
    ax1.set_title("Blinkit Category SKU Depth vs. Observed Promotional Discount", fontsize=13, fontweight="bold", pad=15)
    
    # Legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right")
    plt.tight_layout()
    chart2_path = os.path.join(CHARTS_DIR, "02_sku_depth_vs_discount.png")
    plt.savefig(chart2_path, dpi=300)
    plt.close()

    # Chart 3: Selling Price vs MRP Scatter
    plt.figure(figsize=(8, 6))
    sns.scatterplot(
        x="original_price", y="displayed_price", hue="category", data=df,
        palette="tab10", alpha=0.75, s=40
    )
    max_p = max(df["original_price"].max(), df["displayed_price"].max())
    plt.plot([0, max_p], [0, max_p], linestyle="--", color="gray", label="Price = MRP (0% Discount)")
    plt.title("Empirical Price vs. Maximum Retail Price (MRP) Dispersion", fontsize=13, fontweight="bold", pad=15)
    plt.xlabel("Maximum Retail Price - MRP (INR)", fontsize=11, fontweight="bold")
    plt.ylabel("Observed Selling Price (INR)", fontsize=11, fontweight="bold")
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=9)
    plt.tight_layout()
    chart3_path = os.path.join(CHARTS_DIR, "03_mrp_vs_selling_price.png")
    plt.savefig(chart3_path, dpi=300)
    plt.close()

    print("[5/5] Product analytics completed successfully.")

if __name__ == "__main__":
    run_product_analytics()
