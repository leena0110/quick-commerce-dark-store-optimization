"""
Comprehensive Dataset Comparison and Validation Analysis
==========================================================
Generates statistical comparisons and visualizations between:
1. Original Synthetic Dataset (data/raw/darkstore_transactions.csv & product_catalogue.csv)
2. Real Scraped Product Catalogue (data_pipeline/cleaned_product_catalogue.csv)
3. Enhanced Grounded Synthetic Dataset (data_pipeline/enhanced_synthetic_transactions.csv)

Outputs charts in data_pipeline/dataset_comparison_charts/ and generates validation metrics.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 150

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJ_ROOT = os.path.dirname(BASE_DIR)
CHARTS_DIR = os.path.join(BASE_DIR, "dataset_comparison_charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

# File paths
ORIG_CAT_PATH = os.path.join(PROJ_ROOT, "data", "raw", "product_catalogue.csv")
ORIG_TX_PATH = os.path.join(PROJ_ROOT, "data", "raw", "darkstore_transactions.csv")
REAL_CAT_PATH = os.path.join(BASE_DIR, "cleaned_product_catalogue.csv")
ENHANCED_TX_PATH = os.path.join(BASE_DIR, "enhanced_synthetic_transactions.csv")
MAPPING_PATH = os.path.join(BASE_DIR, "product_mapping.csv")

def run_comparison():
    print("Loading datasets for comparison...")
    orig_cat = pd.read_csv(ORIG_CAT_PATH)
    orig_tx = pd.read_csv(ORIG_TX_PATH)
    real_cat = pd.read_csv(REAL_CAT_PATH)
    enhanced_tx = pd.read_csv(ENHANCED_TX_PATH)
    mapping = pd.read_csv(MAPPING_PATH)

    print(f"Loaded: Orig Cat ({len(orig_cat)}), Real Cat ({len(real_cat)}), Orig Tx ({len(orig_tx)}), Enhanced Tx ({len(enhanced_tx)})")

    # =========================================================================
    # PART A: CATALOGUE & PRICE COMPARISON
    # =========================================================================
    
    # 1. Price Distribution Comparison (KDE & Histogram)
    plt.figure(figsize=(10, 5))
    sns.kdeplot(orig_cat['Unit_Price'], label=f"Original Synthetic Catalogue (N={len(orig_cat)})", color="#3498db", fill=True, alpha=0.3, bw_adjust=0.8)
    sns.kdeplot(real_cat['displayed_price'], label=f"Real Scraped Blinkit Catalogue (N={len(real_cat)})", color="#2ecc71", fill=True, alpha=0.3, bw_adjust=0.8)
    sns.kdeplot(mapping['grounded_real_displayed_price'], label=f"Grounded 58 Product Subset (N={len(mapping)})", color="#e74c3c", linestyle="--")
    plt.title("Product Price Density Distribution: Synthetic vs. Real vs. Grounded", fontsize=14, fontweight='bold', pad=12)
    plt.xlabel("Price (INR / ₹)", fontsize=11)
    plt.ylabel("Density", fontsize=11)
    plt.xlim(0, 500)
    plt.legend(frameon=True)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "01_price_distribution_comparison.png"))
    plt.close()
    print("Saved 01_price_distribution_comparison.png")

    # 2. Category-Level Price Range (Boxplot)
    plt.figure(figsize=(12, 6))
    # Combine original and real catalogue into tidy dataframe
    tidy_orig = orig_cat[['Product_Category', 'Unit_Price']].copy()
    tidy_orig.columns = ['Category', 'Price']
    tidy_orig['Source'] = 'Original Synthetic'
    
    tidy_real = real_cat[['category', 'displayed_price']].copy()
    tidy_real.columns = ['Category', 'Price']
    tidy_real['Source'] = 'Real Blinkit'
    
    # Filter common categories
    common_cats = tidy_orig['Category'].unique()
    tidy_combined = pd.concat([tidy_orig, tidy_real[tidy_real['Category'].isin(common_cats)]], ignore_index=True)
    
    sns.boxplot(data=tidy_combined, x='Category', y='Price', hue='Source', palette=['#3498db', '#2ecc71'], showmeans=True, meanprops={"marker":"o","markerfacecolor":"white", "markeredgecolor":"black"})
    plt.title("Category-Level Price Comparison: Original Synthetic vs. Real Blinkit Observations", fontsize=14, fontweight='bold', pad=12)
    plt.xlabel("Product Category", fontsize=11)
    plt.ylabel("Observed / Unit Price (INR)", fontsize=11)
    plt.xticks(rotation=25, ha='right')
    plt.ylim(0, 400)
    plt.legend(title="Data Source", frameon=True)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "02_category_price_boxplot.png"))
    plt.close()
    print("Saved 02_category_price_boxplot.png")

    # 3. Product Count by Category Comparison
    plt.figure(figsize=(10, 5))
    cat_counts_orig = orig_cat['Product_Category'].value_counts()
    cat_counts_real = real_cat['category'].value_counts()
    cat_df = pd.DataFrame({'Original Synthetic': cat_counts_orig, 'Real Blinkit (Scraped)': cat_counts_real}).fillna(0)
    
    cat_df.plot(kind='bar', figsize=(11, 5), color=['#3498db', '#2ecc71'], width=0.7)
    plt.title("Catalogue Depth: Product Count by Category", fontsize=14, fontweight='bold', pad=12)
    plt.xlabel("Category", fontsize=11)
    plt.ylabel("Number of Distinct Products", fontsize=11)
    plt.xticks(rotation=30, ha='right')
    plt.legend(frameon=True)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "03_category_product_counts.png"))
    plt.close()
    print("Saved 03_category_product_counts.png")

    # =========================================================================
    # PART B: SIMULATED TRANSACTION CHARACTERISTICS COMPARISON
    # =========================================================================

    # 4. Order Value Distribution Comparison
    plt.figure(figsize=(10, 5))
    orig_order_vals = orig_tx.groupby('Order_ID')['Line_Total'].sum()
    enh_order_vals = enhanced_tx.groupby('synthetic_order_id')['line_total'].sum()

    sns.kdeplot(orig_order_vals, label=f"Original Synthetic (Mean: ₹{orig_order_vals.mean():.1f})", color="#e67e22", fill=True, alpha=0.3)
    sns.kdeplot(enh_order_vals, label=f"Grounded Synthetic (Mean: ₹{enh_order_vals.mean():.1f})", color="#9b59b6", fill=True, alpha=0.3)
    plt.title("Simulated Order Basket Value Distribution: Original vs. Grounded", fontsize=14, fontweight='bold', pad=12)
    plt.xlabel("Total Order Basket Value (INR)", fontsize=11)
    plt.ylabel("Density", fontsize=11)
    plt.xlim(0, 1000)
    plt.legend(frameon=True)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "04_order_value_distribution.png"))
    plt.close()
    print("Saved 04_order_value_distribution.png")

    # 5. Quantity Distribution per Line Item
    plt.figure(figsize=(8, 4))
    qty_comp = pd.DataFrame({
        'Original Synthetic': orig_tx['Quantity'].value_counts(normalize=True).sort_index(),
        'Grounded Synthetic': enhanced_tx['quantity'].value_counts(normalize=True).sort_index()
    })
    qty_comp.plot(kind='bar', color=['#e67e22', '#9b59b6'], width=0.6, figsize=(8, 4))
    plt.title("Line Item Quantity Distribution Comparison", fontsize=13, fontweight='bold', pad=12)
    plt.xlabel("Units Purchased per Line Item", fontsize=10)
    plt.ylabel("Proportion of Transactions", fontsize=10)
    plt.xticks(rotation=0)
    plt.legend(frameon=True)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "05_quantity_distribution.png"))
    plt.close()
    print("Saved 05_quantity_distribution.png")

    # 6. Hourly Transaction Velocity Pattern
    plt.figure(figsize=(11, 5))
    orig_tx['hour'] = pd.to_datetime(orig_tx['Timestamp']).dt.hour
    enhanced_tx['hour'] = pd.to_datetime(enhanced_tx['synthetic_transaction_timestamp']).dt.hour
    
    orig_hourly = orig_tx.groupby('hour')['Order_ID'].nunique()
    enh_hourly = enhanced_tx.groupby('hour')['synthetic_order_id'].nunique()
    
    plt.plot(orig_hourly.index, orig_hourly.values, marker='o', color='#e67e22', label='Original Synthetic Demand Curve', linewidth=2)
    plt.plot(enh_hourly.index, enh_hourly.values, marker='s', linestyle='--', color='#9b59b6', label='Grounded Synthetic Demand Curve', linewidth=2)
    plt.title("Simulated Hourly Demand Profile Across 24 Hours", fontsize=14, fontweight='bold', pad=12)
    plt.xlabel("Hour of Day (0 - 23)", fontsize=11)
    plt.ylabel("Unique Orders Completed", fontsize=11)
    plt.xticks(range(0, 24))
    plt.axvspan(7, 9, color='gold', alpha=0.15, label='Morning Rush (7-9 AM)')
    plt.axvspan(18, 21, color='lightblue', alpha=0.15, label='Evening Rush (6-9 PM)')
    plt.legend(frameon=True)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "06_hourly_order_profile.png"))
    plt.close()
    print("Saved 06_hourly_order_profile.png")

    # 7. Category Revenue Contribution
    plt.figure(figsize=(10, 5))
    orig_rev = orig_tx.groupby('Product_Category')['Line_Total'].sum()
    enh_rev = enhanced_tx.groupby('product_category')['line_total'].sum()
    rev_df = pd.DataFrame({'Original Synthetic Revenue': orig_rev, 'Grounded Synthetic Revenue': enh_rev})
    rev_df.plot(kind='bar', figsize=(11, 5), color=['#e67e22', '#9b59b6'], width=0.7)
    plt.title("Simulated Category Revenue Contribution (INR)", fontsize=14, fontweight='bold', pad=12)
    plt.xlabel("Product Category", fontsize=11)
    plt.ylabel("Total Revenue (₹)", fontsize=11)
    plt.xticks(rotation=25, ha='right')
    plt.legend(frameon=True)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "07_category_revenue_comparison.png"))
    plt.close()
    print("Saved 07_category_revenue_comparison.png")

    print("\nAll 7 comparison charts generated successfully!")

if __name__ == "__main__":
    run_comparison()
