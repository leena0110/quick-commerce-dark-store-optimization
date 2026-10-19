"""
Enhanced Grounded Synthetic Transaction Generator
===================================================
Generates the enhanced synthetic transaction dataset:
- Preserves original dataset order structure, customer distribution, and dark store operations
- Substitutes verified real-world product identities, brands, pack sizes, and prices
- Recomputes exact line totals, discounts, and order values based on genuine retail prices
- Annotates every single record with data_origin='grounded_synthetic', generation_rule_version='v2.0_blinkit_grounded',
  source_product_id, and source_price_observation_timestamp
- Outputs enhanced_synthetic_transactions.csv
"""

import os
import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("EnhancedDataGenerator")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJ_ROOT = os.path.dirname(BASE_DIR)
ORIG_TRANSACTIONS_PATH = os.path.join(PROJ_ROOT, "data", "raw", "darkstore_transactions.csv")
MAPPING_PATH = os.path.join(BASE_DIR, "product_mapping.csv")
ENHANCED_TRANSACTIONS_PATH = os.path.join(BASE_DIR, "enhanced_synthetic_transactions.csv")

def generate_enhanced_transactions():
    logger.info("Loading original synthetic transactions and product mapping...")
    orig_tx = pd.read_csv(ORIG_TRANSACTIONS_PATH)
    mapping = pd.read_csv(MAPPING_PATH)
    
    logger.info(f"Original transaction rows: {len(orig_tx):,}")
    
    # Merge mapping on Product_ID
    merged = pd.merge(
        orig_tx,
        mapping[[
            'synthetic_product_id', 
            'grounded_source_product_id', 
            'grounded_real_product_name', 
            'grounded_brand', 
            'grounded_pack_size', 
            'grounded_unit', 
            'grounded_real_displayed_price', 
            'grounded_real_original_price', 
            'grounded_real_discount_pct', 
            'source_price_observation_timestamp'
        ]],
        left_on='Product_ID',
        right_on='synthetic_product_id',
        how='left'
    )
    
    logger.info("Constructing enhanced schema with real grounded product fields...")
    
    # Calculate line totals grounded in real observed prices
    # We maintain the transaction's simulated discount percentage or calibrate to observed discount
    # Let's preserve transaction discount dynamics:
    # Use real displayed price as unit price
    merged['synthetic_unit_price'] = merged['grounded_real_displayed_price']
    
    # If transaction had a promotional discount, apply it, or use observed retail discount
    # To reflect real observed pricing structure:
    # Unit_Price = real displayed_price
    # Discount_Pct = real discount_pct combined with transaction promo
    merged['grounded_discount_pct'] = np.where(
        merged['Discount_Pct'] > 0,
        merged['Discount_Pct'],
        merged['grounded_real_discount_pct']
    )
    
    merged['grounded_discount_amount'] = (merged['synthetic_unit_price'] * (merged['grounded_discount_pct'] / 100.0) * merged['Quantity']).round(2)
    merged['grounded_line_total'] = ((merged['synthetic_unit_price'] * merged['Quantity']) - merged['grounded_discount_amount']).round(2)
    
    # Recompute order value per Order_ID
    order_totals = merged.groupby('Order_ID')['grounded_line_total'].transform('sum').round(2)
    merged['grounded_order_value'] = order_totals

    # Build clean output dataframe with explicit synthetic labelling
    enhanced_df = pd.DataFrame({
        "synthetic_order_id": merged["Order_ID"],
        "synthetic_transaction_timestamp": merged["Timestamp"],
        "synthetic_customer_id": merged["Customer_ID"],
        "synthetic_dark_store_id": merged["Dark_Store_ID"],
        "synthetic_product_id": merged["Product_ID"],
        "grounded_product_name": merged["grounded_real_product_name"],
        "product_category": merged["Product_Category"],
        "brand": merged["grounded_brand"],
        "pack_size": merged["grounded_pack_size"],
        "unit": merged["grounded_unit"],
        "quantity": merged["Quantity"],
        "grounded_unit_price": merged["synthetic_unit_price"],
        "discount_pct": merged["grounded_discount_pct"],
        "discount_amount": merged["grounded_discount_amount"],
        "line_total": merged["grounded_line_total"],
        "order_value": merged["grounded_order_value"],
        "payment_type": merged["Payment_Type"],
        "delivery_distance_km": merged["Delivery_Distance_km"],
        "source_product_id": merged["grounded_source_product_id"],
        "source_price_observation_timestamp": merged["source_price_observation_timestamp"],
        "data_origin": "grounded_synthetic",
        "generation_rule_version": "v2.0_blinkit_grounded"
    })

    enhanced_df.to_csv(ENHANCED_TRANSACTIONS_PATH, index=False)
    logger.info(f"Successfully generated {len(enhanced_df):,} enhanced synthetic transaction rows.")
    logger.info(f"Saved to: {ENHANCED_TRANSACTIONS_PATH}")

    # Print summary statistics
    print("\n" + "="*70)
    print("ENHANCED SYNTHETIC TRANSACTIONS SUMMARY")
    print("="*70)
    print(f"Total Transactions: {enhanced_df['synthetic_order_id'].nunique():,}")
    print(f"Total Transaction Lines: {len(enhanced_df):,}")
    print(f"Total Unique Products: {enhanced_df['synthetic_product_id'].nunique()}")
    print(f"Total Dark Stores: {enhanced_df['synthetic_dark_store_id'].nunique()}")
    print(f"Mean Order Value (Original): Rs {orig_tx.groupby('Order_ID')['Line_Total'].sum().mean():.2f}")
    print(f"Mean Order Value (Grounded): Rs {enhanced_df.groupby('synthetic_order_id')['line_total'].sum().mean():.2f}")
    print("="*70 + "\n")

if __name__ == "__main__":
    generate_enhanced_transactions()
