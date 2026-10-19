"""
Price Snapshot and Temporal Observation Tracker
===============================================
Performs repeated observation snapshots across target categories at defined
intervals or on repeated runs, records price differences, discount shifts,
and inventory availability changes, and outputs price_snapshots.csv.
"""

import os
import sys
import time
import logging
from datetime import datetime
import pandas as pd
from scraper import BlinkitCatalogScraper, TARGET_CATEGORIES

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRICE_SNAPSHOTS_CSV = os.path.join(BASE_DIR, "price_snapshots.csv")
CLEANED_CATALOGUE_CSV = os.path.join(BASE_DIR, "cleaned_product_catalogue.csv")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("PriceSnapshotTracker")


def collect_snapshot(run_label: str = "Snapshot") -> pd.DataFrame:
    """Collect an actual real-time snapshot of products."""
    logger.info(f"Initiating {run_label} collection at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}...")
    scraper = BlinkitCatalogScraper()
    df = scraper.run_pipeline(TARGET_CATEGORIES)
    return df


def record_snapshots(num_snapshots: int = 2, delay_seconds: int = 15):
    """
    Collect repeated observations across time to record genuine temporal behavior.
    Note: Immediate repeated runs capture short-term stability or micro-adjustments;
    future cron/scheduled runs accumulate longitudinal shifts.
    """
    snapshots = []
    
    # Check if price_snapshots.csv already exists
    if os.path.exists(PRICE_SNAPSHOTS_CSV):
        try:
            existing_df = pd.read_csv(PRICE_SNAPSHOTS_CSV)
            logger.info(f"Loaded {len(existing_df)} existing price snapshot records from disk.")
            snapshots.append(existing_df)
        except Exception as e:
            logger.warning(f"Could not load existing snapshots: {e}")

    # If cleaned catalogue exists from the first scrape, load it as T1
    if os.path.exists(CLEANED_CATALOGUE_CSV):
        t1_df = pd.read_csv(CLEANED_CATALOGUE_CSV)
        t1_df["observation_run"] = "T1_Initial_Observation"
        snapshots.append(t1_df)
    else:
        t1_df = collect_snapshot("T1_Initial_Observation")
        t1_df["observation_run"] = "T1_Initial_Observation"
        snapshots.append(t1_df)

    logger.info(f"Waiting {delay_seconds} seconds before collecting observation T2...")
    time.sleep(delay_seconds)

    # Collect T2 snapshot (focus on subset of high-turnover categories to respect server rate limits)
    t2_categories = TARGET_CATEGORIES[:6] # Dairy, Bakery, Beverages
    scraper_t2 = BlinkitCatalogScraper()
    t2_df = scraper_t2.run_pipeline(t2_categories)
    if not t2_df.empty:
        t2_df["observation_run"] = "T2_FollowUp_Observation"
        snapshots.append(t2_df)

    combined_df = pd.concat(snapshots, ignore_index=True)
    
    # Normalize and sort
    combined_df.sort_values(by=["source_product_id", "collection_timestamp"], inplace=True)
    combined_df.to_csv(PRICE_SNAPSHOTS_CSV, index=False)
    logger.info(f"Saved total {len(combined_df)} snapshot observations to: {PRICE_SNAPSHOTS_CSV}")

    # Perform Snapshot Analysis
    analyze_snapshots(combined_df)


def analyze_snapshots(df: pd.DataFrame):
    """Analyze price stability, discount consistency, and inventory across observation runs."""
    print("\n" + "="*70)
    print("PRICE SNAPSHOT ANALYSIS REPORT")
    print("="*70)
    
    # Group by product
    counts = df.groupby("source_product_id")["collection_timestamp"].nunique()
    repeated_prods = counts[counts > 1].index.tolist()
    print(f"Total Unique Products Tracked: {df['source_product_id'].nunique()}")
    print(f"Products with Repeated Observations: {len(repeated_prods)}")

    if len(repeated_prods) > 0:
        rep_df = df[df["source_product_id"].isin(repeated_prods)]
        
        # Check price differences
        price_stats = rep_df.groupby("source_product_id")["displayed_price"].agg(["min", "max", "std", "count"])
        price_changed = price_stats[price_stats["min"] != price_stats["max"]]
        print(f"Products with Price Differences between Runs: {len(price_changed)}")
        
        # Check inventory differences
        inv_stats = rep_df.groupby("source_product_id")["inventory"].agg(["min", "max", "std"])
        inv_changed = inv_stats[inv_stats["min"] != inv_stats["max"]]
        print(f"Products with Inventory Shifts between Runs: {len(inv_changed)}")

        print("\nCategory breakdown of repeated observation set:")
        print(rep_df.groupby("category")["source_product_id"].nunique())
    else:
        print("Note: Single observation snapshot recorded. Run schedule/cron required for longitudinal price dynamics.")
    print("="*70 + "\n")


if __name__ == "__main__":
    record_snapshots(delay_seconds=10)
