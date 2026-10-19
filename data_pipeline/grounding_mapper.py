"""
Grounding and Mapping Engine
============================
Bridges original 58 synthetic products to real observed quick-commerce products
scraped from Blinkit, preserving original behavioral transaction signatures while
grounding prices, pack sizes, brands, and real product identities.
"""

import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJ_ROOT = os.path.dirname(BASE_DIR)
ORIG_CATALOGUE_PATH = os.path.join(PROJ_ROOT, "data", "raw", "product_catalogue.csv")
REAL_CATALOGUE_PATH = os.path.join(BASE_DIR, "cleaned_product_catalogue.csv")
MAPPING_CSV_PATH = os.path.join(BASE_DIR, "product_mapping.csv")

def create_grounded_mapping():
    orig_cat = pd.read_csv(ORIG_CATALOGUE_PATH)
    real_cat = pd.read_csv(REAL_CATALOGUE_PATH)
    
    print(f"Original synthetic products: {len(orig_cat)}")
    print(f"Real scraped products: {len(real_cat)}")

    # For each of the 58 original products, find the most representative real product
    # Match criteria: same category, matching keywords in product name, closest price
    mappings = []

    for _, row in orig_cat.iterrows():
        p_id = row['Product_ID']
        p_name = row['Product_Name']
        p_cat = row['Product_Category']
        p_price = row['Unit_Price']
        
        # Filter real catalog by category
        cat_matches = real_cat[real_cat['category'].str.lower() == p_cat.lower()]
        
        # If no direct category match, search in entire catalog
        search_pool = cat_matches if not cat_matches.empty else real_cat
        
        # Keyword extraction from original product name (e.g. 'Milk', 'Bread', 'Curd', 'Chips')
        kw = p_name.split('(')[0].strip().lower()
        # Clean specific words
        kw_root = kw.split()[0] if len(kw.split()) > 0 else kw
        
        # Substring search
        kw_matches = search_pool[search_pool['product_name'].str.lower().str.contains(kw_root, regex=False)]
        
        if not kw_matches.empty:
            # Select item with price closest to original synthetic price
            kw_matches = kw_matches.copy()
            kw_matches['price_diff'] = (kw_matches['displayed_price'] - p_price).abs()
            best_match = kw_matches.sort_values(by='price_diff').iloc[0]
            match_type = "High Confidence (Keyword + Category)"
        else:
            # Fallback to closest price in category
            cat_pool = cat_matches if not cat_matches.empty else real_cat
            cat_pool = cat_pool.copy()
            cat_pool['price_diff'] = (cat_pool['displayed_price'] - p_price).abs()
            best_match = cat_pool.sort_values(by='price_diff').iloc[0]
            match_type = "Category Nearest Price Fallback"
            
        mappings.append({
            "synthetic_product_id": p_id,
            "original_synthetic_name": p_name,
            "original_category": p_cat,
            "original_synthetic_price": p_price,
            "grounded_source_product_id": best_match['source_product_id'],
            "grounded_real_product_name": best_match['product_name'],
            "grounded_brand": best_match['brand'],
            "grounded_pack_size": best_match['pack_size'],
            "grounded_unit": best_match['unit'],
            "grounded_real_displayed_price": best_match['displayed_price'],
            "grounded_real_original_price": best_match['original_price'],
            "grounded_real_discount_pct": best_match['discount_pct'],
            "source_price_observation_timestamp": best_match['collection_timestamp'],
            "mapping_method": match_type
        })

    mapping_df = pd.DataFrame(mappings)
    mapping_df.to_csv(MAPPING_CSV_PATH, index=False)
    print(f"Saved product grounding mapping ({len(mapping_df)} entries) to: {MAPPING_CSV_PATH}")
    
    print("\nSample Grounded Mappings:")
    for _, r in mapping_df.head(10).iterrows():
        print(f"[{r['synthetic_product_id']}] {r['original_synthetic_name']} (Rs {r['original_synthetic_price']}) --> {r['grounded_real_product_name']} by {r['grounded_brand']} (Rs {r['grounded_real_displayed_price']})")

if __name__ == "__main__":
    create_grounded_mapping()
