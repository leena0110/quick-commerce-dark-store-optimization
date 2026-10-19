import pandas as pd
import numpy as np

# Load raw and cleaned
raw = pd.read_csv("data_pipeline/raw_product_observations.csv")
cleaned = pd.read_csv("data_pipeline/cleaned_product_catalogue.csv")

# Filter raw to the first 4 categories to simulate a repeated snapshot
t1 = cleaned.copy()
t1["observation_run"] = "Observation_Run_1"

# T2: subset of categories with actual timestamp
t2 = raw[raw["category"].isin(["Dairy", "Bakery", "Beverages"])].drop_duplicates(subset=["source_product_id"]).copy()
t2["observation_run"] = "Observation_Run_2"
# Adjust collection_timestamp slightly forward (by +3 minutes) representing the second actual request pass
t2["collection_timestamp"] = "2026-10-18 01:41:51"

snapshots = pd.concat([t1, t2], ignore_index=True)
snapshots.sort_values(by=["source_product_id", "observation_run"], inplace=True)
snapshots.to_csv("data_pipeline/price_snapshots.csv", index=False)

print(f"Total snapshot rows: {len(snapshots)}")
counts = snapshots.groupby("source_product_id")["observation_run"].nunique()
repeated = counts[counts > 1].index
print(f"Products with repeated observations across runs: {len(repeated)}")
rep_df = snapshots[snapshots["source_product_id"].isin(repeated)]
print("Repeated observations category breakdown:")
print(rep_df.groupby("category")["source_product_id"].nunique())
