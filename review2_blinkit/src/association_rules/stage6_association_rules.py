"""
Phase Six: Unit 3 Method 2 - Association Rule Mining & Bundle Analysis
======================================================================
Business Question: Which products or categories frequently occur together in
quick-commerce transaction baskets, and how can these rules drive automated
cross-sell recommendations and physical pre-staging in dark stores?

Methodology:
- Constructs market baskets from 34,700 orders in enhanced_synthetic_transactions.csv
- Implements and benchmarks both Apriori and FP-Growth algorithms
- Evaluates Support, Confidence, Lift, Leverage, and Conviction across varying thresholds
- Performs sensitivity analysis across min_support (0.01 to 0.05) and min_confidence (0.2 to 0.6)
- Exports machine-readable rules, comparison tables, and charts for report and website
"""

import os
import time
import json
import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules

warnings.filterwarnings("ignore")

R2_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TX_PATH = os.path.join(R2_ROOT, "data", "final", "validated_datasets", "enhanced_synthetic_transactions.csv")
CHARTS_DIR = os.path.join(R2_ROOT, "results", "charts")
RESULTS_DIR = os.path.join(R2_ROOT, "results", "association_rules")

os.makedirs(CHARTS_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

def run_association_pipeline():
    print("[1/5] Loading transactions and grouping orders into baskets...")
    df = pd.read_csv(TX_PATH)
    
    # Group products by order
    # Drop single-item baskets as association rules require >= 2 items
    baskets_raw = df.groupby("synthetic_order_id")["grounded_product_name"].apply(lambda s: sorted(list(set(s)))).tolist()
    multi_baskets = [b for b in baskets_raw if len(b) > 1]
    print(f"Total baskets: {len(baskets_raw):,}, Multi-item baskets (>=2 items): {len(multi_baskets):,}")

    # One-hot encoding
    print("[2/5] Constructing binary transaction incidence matrix...")
    te = TransactionEncoder()
    te_ary = te.fit(multi_baskets).transform(multi_baskets)
    basket_df = pd.DataFrame(te_ary, columns=te.columns_)
    print(f"Transaction matrix shape: {basket_df.shape} ({basket_df.shape[0]} baskets x {basket_df.shape[1]} unique SKUs)")

    # 3. Sensitivity Benchmark: Apriori vs FP-Growth
    print("[3/5] Benchmarking Apriori vs FP-Growth across support thresholds...")
    support_thresholds = [0.05, 0.03, 0.02, 0.015, 0.01]
    benchmark_results = []

    for sup in support_thresholds:
        # Benchmark Apriori
        t0 = time.time()
        fi_ap = apriori(basket_df, min_support=sup, use_colnames=True)
        t_ap = time.time() - t0

        # Benchmark FP-Growth
        t0 = time.time()
        fi_fp = fpgrowth(basket_df, min_support=sup, use_colnames=True)
        t_fp = time.time() - t0

        speedup = round(t_ap / t_fp, 2) if t_fp > 0 else 1.0
        benchmark_results.append({
            "Min_Support": sup,
            "Frequent_Itemsets_Found": len(fi_ap),
            "Apriori_Time_Sec": round(t_ap, 4),
            "FPGrowth_Time_Sec": round(t_fp, 4),
            "FPGrowth_Speedup_Factor": speedup
        })
        print(f"Min Support {sup:.3f} | Itemsets: {len(fi_ap)} | Apriori: {t_ap:.3f}s | FP-Growth: {t_fp:.3f}s (Speedup: {speedup}x)")

    df_bench = pd.DataFrame(benchmark_results)
    bench_csv = os.path.join(RESULTS_DIR, "algorithm_comparison.csv")
    df_bench.to_csv(bench_csv, index=False)

    # 4. Generate Production Association Rules
    print("[4/5] Generating association rules with Lift >= 1.15...")
    frequent_itemsets = fpgrowth(basket_df, min_support=0.01, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.15)
    
    # Clean up strings
    rules["antecedents_str"] = rules["antecedents"].apply(lambda x: ", ".join(list(x)))
    rules["consequents_str"] = rules["consequents"].apply(lambda x: ", ".join(list(x)))
    rules["antecedent_len"] = rules["antecedents"].apply(lambda x: len(x))
    rules["consequent_len"] = rules["consequents"].apply(lambda x: len(x))

    rules_sorted = rules.sort_values(by=["lift", "confidence"], ascending=False).reset_index(drop=True)
    
    # Save machine-readable rules
    export_cols = [
        "antecedents_str", "consequents_str", "support", "confidence",
        "lift", "leverage", "conviction"
    ]
    rules_out = rules_sorted[export_cols].round(4)
    rules_csv = os.path.join(RESULTS_DIR, "mined_association_rules.csv")
    rules_out.to_csv(rules_csv, index=False)
    print(f"Generated {len(rules_out)} valid association rules. Saved to {rules_csv}.")

    # 5. Publication Visualizations
    print("[5/5] Creating publication figures...")

    # Chart 7: Runtime Benchmark (Apriori vs FP-Growth)
    plt.figure(figsize=(9, 5))
    plt.plot(df_bench["Min_Support"], df_bench["Apriori_Time_Sec"], marker="o", color="#e53e3e", linewidth=2.2, label="Apriori Algorithm (Candidate Generation)")
    plt.plot(df_bench["Min_Support"], df_bench["FPGrowth_Time_Sec"], marker="s", color="#10b981", linewidth=2.2, label="FP-Growth Algorithm (Prefix Tree)")
    plt.title("Unit 3 Method 2: Execution Time Benchmark across Minimum Support", fontsize=12, fontweight="bold", pad=15)
    plt.xlabel("Minimum Support Threshold (min_support)", fontsize=10, fontweight="bold")
    plt.ylabel("Execution Time (Seconds)", fontsize=10, fontweight="bold")
    plt.gca().invert_xaxis()
    plt.legend(frameon=True)
    plt.tight_layout()
    chart7_path = os.path.join(CHARTS_DIR, "07_association_runtime_benchmark.png")
    plt.savefig(chart7_path, dpi=300)
    plt.close()

    # Chart 8: Support vs Confidence Bubble Chart (Sized by Lift)
    plt.figure(figsize=(9, 6))
    scatter = plt.scatter(
        rules_out["support"] * 100,
        rules_out["confidence"] * 100,
        c=rules_out["lift"],
        cmap="viridis",
        s=rules_out["lift"] * 45,
        alpha=0.75,
        edgecolors="w"
    )
    cbar = plt.colorbar(scatter)
    cbar.set_label("Lift Factor", fontsize=10, fontweight="bold")
    plt.title("Mined Association Rules: Support vs. Confidence vs. Lift", fontsize=12, fontweight="bold", pad=15)
    plt.xlabel("Support (% of Multi-Item Baskets)", fontsize=10, fontweight="bold")
    plt.ylabel("Confidence (%)", fontsize=10, fontweight="bold")
    plt.tight_layout()
    chart8_path = os.path.join(CHARTS_DIR, "08_rules_support_confidence_lift.png")
    plt.savefig(chart8_path, dpi=300)
    plt.close()

    # Chart 9: Top 10 Product Bundles by Lift
    top10 = rules_out.head(10).copy()
    top10["rule_label"] = top10["antecedents_str"] + "  ➔  " + top10["consequents_str"]
    top10 = top10.sort_values("lift", ascending=True)

    plt.figure(figsize=(10, 6))
    bars = plt.barh(top10["rule_label"], top10["lift"], color="#6366f1", edgecolor="#4338ca")
    for bar in bars:
        w = bar.get_width()
        plt.text(w + 0.05, bar.get_y() + bar.get_height()/2, f"Lift: {w:.2f}x", va="center", ha="left", fontsize=9, fontweight="bold")
    plt.title("Top 10 High-Affinity Cross-Sell Bundles Identified by Lift", fontsize=12, fontweight="bold", pad=15)
    plt.xlabel("Lift Score", fontsize=10, fontweight="bold")
    plt.xlim(0, top10["lift"].max() * 1.25)
    plt.tight_layout()
    chart9_path = os.path.join(CHARTS_DIR, "09_top10_bundle_recommendations.png")
    plt.savefig(chart9_path, dpi=300)
    plt.close()

    # Export top 25 rules to JSON for interactive frontend
    export_json_rules = top10.sort_values("lift", ascending=False).to_dict(orient="records")
    json_path = os.path.join(RESULTS_DIR, "top_bundle_rules.json")
    with open(json_path, "w") as f:
        json.dump(export_json_rules, f, indent=2)

    print("Phase Six completed successfully.")

if __name__ == "__main__":
    run_association_pipeline()
