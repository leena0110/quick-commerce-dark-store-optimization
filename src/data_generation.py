"""
Synthetic Data Generation for Quick-Commerce Dark Store Inventory Optimization
==============================================================================

This script generates a realistic synthetic dataset of quick-commerce transactions.
It simulates orders placed across multiple dark stores over a 6-month period
(April 2026 – September 2026).

WHY SYNTHETIC DATA:
- The faculty prohibits using pre-built datasets (Kaggle, UCI, GitHub, etc.)
- Real quick-commerce data is proprietary and not publicly available
- Synthetic generation allows us to control and document all assumptions
- The process is fully reproducible with fixed random seeds

ASSUMPTIONS:
1. 8 dark stores operating in a metro city, each serving a local zone
2. Customers order 1-6 products per order; basket size follows realistic patterns
3. Demand peaks occur in mornings (7-9 AM) and evenings (6-9 PM)
4. Weekend demand is ~20% higher than weekday demand
5. Product co-purchase relationships are embedded via basket generation rules
6. Prices are realistic Indian rupee values for quick-commerce products
7. Discounts range 0-30%, applied more frequently during evenings and weekends
8. Each dark store has slightly different demand characteristics
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os
import warnings
warnings.filterwarnings('ignore')

# ==============================================================================
# CONFIGURATION
# ==============================================================================
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

# Simulation period: 6 months
START_DATE = datetime(2026, 4, 1)
END_DATE = datetime(2026, 9, 30)
NUM_DAYS = (END_DATE - START_DATE).days + 1  # 183 days

# Scale
NUM_DARK_STORES = 8
NUM_CUSTOMERS = 5000
ORDERS_PER_DAY_BASE = 180  # base orders per day across all stores

# Output path
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "raw")

# ==============================================================================
# PRODUCT CATALOGUE
# ==============================================================================

PRODUCT_CATALOGUE = {
    # Category: [(Product_Name, Unit_Price, Demand_Level, Morning_Weight, Evening_Weight)]
    # Demand_Level: 'high', 'medium', 'low'
    # Morning/Evening weights control time-of-day demand (higher = more demand at that time)
    
    "Dairy": [
        ("Milk (1L)", 65, "high", 1.8, 1.4),
        ("Curd (400g)", 40, "high", 1.5, 1.2),
        ("Paneer (200g)", 90, "medium", 1.0, 1.5),
        ("Butter (100g)", 55, "medium", 1.4, 0.8),
        ("Cheese Slices", 120, "medium", 1.0, 1.0),
        ("Yogurt (200ml)", 35, "low", 1.3, 0.9),
        ("Cream (200ml)", 60, "low", 0.7, 1.2),
    ],
    "Bakery": [
        ("Bread (White)", 45, "high", 1.9, 1.0),
        ("Bread (Brown)", 55, "medium", 1.7, 0.9),
        ("Pav (6pcs)", 30, "medium", 1.2, 1.4),
        ("Cake (Slice)", 80, "low", 0.6, 1.3),
        ("Cookies Pack", 50, "medium", 0.8, 1.1),
        ("Bun (4pcs)", 35, "medium", 1.5, 0.9),
    ],
    "Beverages": [
        ("Soft Drink (500ml)", 40, "high", 0.6, 1.7),
        ("Juice (1L)", 95, "medium", 1.3, 1.0),
        ("Mineral Water (1L)", 25, "high", 1.0, 1.0),
        ("Cold Coffee (200ml)", 50, "medium", 0.9, 1.4),
        ("Energy Drink", 110, "low", 0.5, 1.5),
        ("Buttermilk (200ml)", 25, "medium", 1.4, 0.8),
        ("Tea Bags (25pcs)", 150, "medium", 1.6, 0.7),
    ],
    "Snacks": [
        ("Chips (Large)", 50, "high", 0.5, 1.8),
        ("Namkeen Mix", 45, "medium", 0.6, 1.6),
        ("Biscuits", 30, "high", 1.0, 1.2),
        ("Popcorn", 60, "low", 0.4, 1.7),
        ("Makhana (Fox Nuts)", 120, "low", 0.8, 1.3),
        ("Dry Fruits Mix", 250, "low", 0.9, 1.0),
    ],
    "Fruits & Vegetables": [
        ("Banana (6pcs)", 40, "high", 1.6, 1.0),
        ("Onion (1kg)", 35, "high", 1.2, 1.3),
        ("Tomato (500g)", 25, "high", 1.3, 1.2),
        ("Potato (1kg)", 30, "high", 1.1, 1.2),
        ("Apple (4pcs)", 160, "medium", 1.4, 0.8),
        ("Lemon (6pcs)", 20, "medium", 1.0, 1.0),
        ("Spinach (Bunch)", 25, "medium", 1.3, 1.4),
        ("Capsicum (2pcs)", 40, "low", 1.0, 1.3),
    ],
    "Staples": [
        ("Rice (1kg)", 70, "high", 0.9, 1.3),
        ("Atta/Flour (1kg)", 50, "medium", 0.8, 1.1),
        ("Sugar (500g)", 25, "medium", 1.0, 0.9),
        ("Salt (1kg)", 20, "low", 1.0, 1.0),
        ("Cooking Oil (1L)", 140, "medium", 0.9, 1.2),
        ("Dal/Lentils (500g)", 75, "medium", 0.8, 1.3),
    ],
    "Personal Care": [
        ("Soap (3pcs)", 120, "medium", 0.8, 1.0),
        ("Shampoo (200ml)", 180, "low", 0.7, 1.1),
        ("Toothpaste", 95, "medium", 1.2, 0.8),
        ("Face Wash", 150, "low", 0.9, 1.0),
        ("Hand Sanitizer", 80, "low", 1.0, 1.0),
        ("Tissue Paper", 50, "medium", 1.0, 1.0),
    ],
    "Household": [
        ("Detergent (500g)", 110, "medium", 0.7, 1.0),
        ("Dish Soap (500ml)", 60, "medium", 0.8, 1.0),
        ("Floor Cleaner (500ml)", 90, "low", 0.9, 0.8),
        ("Garbage Bags", 70, "low", 1.0, 0.9),
        ("Sponge/Scrubber", 30, "low", 0.8, 0.9),
    ],
    "Instant & Frozen": [
        ("Instant Noodles (4pk)", 80, "high", 0.7, 1.6),
        ("Frozen Peas (200g)", 50, "low", 0.8, 1.2),
        ("Pasta (500g)", 75, "medium", 0.6, 1.5),
        ("Pasta Sauce", 110, "medium", 0.6, 1.5),
        ("Ready-to-Eat Meal", 120, "medium", 0.5, 1.6),
        ("Frozen Paratha (5pcs)", 90, "medium", 1.4, 1.0),
    ],
}

# ==============================================================================
# CO-PURCHASE RELATIONSHIP MATRIX
# ==============================================================================
# These define which products tend to appear together in the same basket.
# Each rule: (anchor_product, companion_product, probability_of_adding_companion)

CO_PURCHASE_RULES = [
    ("Milk (1L)", "Bread (White)", 0.40),
    ("Milk (1L)", "Bread (Brown)", 0.15),
    ("Milk (1L)", "Curd (400g)", 0.20),
    ("Bread (White)", "Eggs" , 0.30),  # We'll add Eggs separately
    ("Bread (White)", "Butter (100g)", 0.35),
    ("Bread (Brown)", "Butter (100g)", 0.25),
    ("Chips (Large)", "Soft Drink (500ml)", 0.45),
    ("Namkeen Mix", "Soft Drink (500ml)", 0.25),
    ("Pasta (500g)", "Pasta Sauce", 0.55),
    ("Instant Noodles (4pk)", "Soft Drink (500ml)", 0.25),
    ("Instant Noodles (4pk)", "Chips (Large)", 0.20),
    ("Rice (1kg)", "Dal/Lentils (500g)", 0.35),
    ("Rice (1kg)", "Cooking Oil (1L)", 0.20),
    ("Onion (1kg)", "Tomato (500g)", 0.45),
    ("Onion (1kg)", "Potato (1kg)", 0.30),
    ("Tomato (500g)", "Potato (1kg)", 0.25),
    ("Banana (6pcs)", "Milk (1L)", 0.20),
    ("Banana (6pcs)", "Curd (400g)", 0.15),
    ("Biscuits", "Milk (1L)", 0.20),
    ("Biscuits", "Tea Bags (25pcs)", 0.15),
    ("Cold Coffee (200ml)", "Cookies Pack", 0.20),
    ("Soap (3pcs)", "Shampoo (200ml)", 0.30),
    ("Toothpaste", "Soap (3pcs)", 0.15),
    ("Detergent (500g)", "Dish Soap (500ml)", 0.30),
    ("Frozen Paratha (5pcs)", "Curd (400g)", 0.30),
    ("Frozen Paratha (5pcs)", "Butter (100g)", 0.20),
    ("Ready-to-Eat Meal", "Mineral Water (1L)", 0.20),
    ("Atta/Flour (1kg)", "Cooking Oil (1L)", 0.20),
    ("Atta/Flour (1kg)", "Sugar (500g)", 0.15),
    ("Apple (4pcs)", "Banana (6pcs)", 0.25),
    ("Spinach (Bunch)", "Paneer (200g)", 0.25),
    ("Popcorn", "Soft Drink (500ml)", 0.30),
    ("Energy Drink", "Chips (Large)", 0.20),
]

# Add Eggs to the catalogue (was referenced in co-purchase rules)
PRODUCT_CATALOGUE["Dairy"].append(("Eggs (6pcs)", 55, "high", 1.7, 1.0))

# ==============================================================================
# DARK STORES
# ==============================================================================

DARK_STORES = {
    "DS_001": {"name": "Store-Koramangala", "demand_multiplier": 1.20, "area_type": "urban_core"},
    "DS_002": {"name": "Store-Indiranagar", "demand_multiplier": 1.15, "area_type": "urban_core"},
    "DS_003": {"name": "Store-HSR_Layout", "demand_multiplier": 1.10, "area_type": "suburban"},
    "DS_004": {"name": "Store-Whitefield", "demand_multiplier": 0.95, "area_type": "suburban"},
    "DS_005": {"name": "Store-Jayanagar", "demand_multiplier": 1.05, "area_type": "urban_core"},
    "DS_006": {"name": "Store-MG_Road", "demand_multiplier": 1.00, "area_type": "urban_core"},
    "DS_007": {"name": "Store-Electronic_City", "demand_multiplier": 0.85, "area_type": "tech_park"},
    "DS_008": {"name": "Store-Marathahalli", "demand_multiplier": 0.90, "area_type": "suburban"},
}

PAYMENT_TYPES = ["UPI", "Credit Card", "Debit Card", "Cash on Delivery", "Wallet"]
PAYMENT_WEIGHTS = [0.45, 0.15, 0.10, 0.15, 0.15]

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def build_product_lookup():
    """Build a flat list of all products with their attributes."""
    products = []
    pid = 1
    for category, items in PRODUCT_CATALOGUE.items():
        for name, price, demand_level, morning_w, evening_w in items:
            products.append({
                "Product_ID": f"P{pid:03d}",
                "Product_Name": name,
                "Product_Category": category,
                "Unit_Price": price,
                "Demand_Level": demand_level,
                "Morning_Weight": morning_w,
                "Evening_Weight": evening_w,
            })
            pid += 1
    return pd.DataFrame(products)


def get_demand_weight(demand_level):
    """Convert demand level to a sampling weight."""
    return {"high": 3.0, "medium": 1.5, "low": 0.5}[demand_level]


def get_hour_multiplier(hour):
    """
    Simulate realistic quick-commerce hourly demand patterns.
    Peaks: 7-9 AM (breakfast rush), 11 AM-1 PM (lunch prep), 6-9 PM (evening/dinner).
    Low: 12 AM - 6 AM.
    """
    hourly_pattern = {
        0: 0.05, 1: 0.02, 2: 0.01, 3: 0.01, 4: 0.01, 5: 0.03,
        6: 0.15, 7: 0.60, 8: 0.85, 9: 0.70, 10: 0.50, 11: 0.65,
        12: 0.75, 13: 0.60, 14: 0.40, 15: 0.35, 16: 0.45, 17: 0.55,
        18: 0.80, 19: 1.00, 20: 0.90, 21: 0.70, 22: 0.40, 23: 0.15,
    }
    return hourly_pattern.get(hour, 0.3)


def get_day_multiplier(day_of_week):
    """
    Day-of-week demand multiplier.
    0=Monday ... 6=Sunday. Weekends are higher.
    """
    daily_pattern = {
        0: 0.90,  # Monday
        1: 0.85,  # Tuesday (lowest weekday)
        2: 0.90,  # Wednesday
        3: 0.95,  # Thursday
        4: 1.05,  # Friday (pre-weekend)
        5: 1.20,  # Saturday
        6: 1.15,  # Sunday
    }
    return daily_pattern.get(day_of_week, 1.0)


def get_monthly_multiplier(month):
    """
    Monthly/seasonal variation.
    Summer months (Apr-Jun) have higher beverage demand.
    Festive season (Aug-Sep) has overall higher demand.
    """
    monthly = {
        4: 1.00,  # April
        5: 1.05,  # May (summer)
        6: 1.08,  # June (peak summer)
        7: 0.95,  # July (monsoon, slightly lower)
        8: 1.10,  # August (festive buildup)
        9: 1.15,  # September (festive season)
    }
    return monthly.get(month, 1.0)


def generate_basket(product_df, hour, is_weekend, month, rng):
    """
    Generate a realistic product basket for a single order.
    
    Steps:
    1. Determine basket size (1-6 products, weighted towards 2-4)
    2. Select an anchor product based on demand level and time-of-day weights
    3. Apply co-purchase rules to add companion products
    4. Fill remaining slots with category-appropriate random products
    5. Assign realistic quantities and discounts
    """
    # Basket size: skewed towards 2-4 items
    basket_sizes = [1, 2, 3, 4, 5, 6]
    basket_weights = [0.12, 0.25, 0.28, 0.20, 0.10, 0.05]
    basket_size = rng.choice(basket_sizes, p=basket_weights)
    
    # Calculate time-of-day product weights
    if 6 <= hour <= 10:
        time_weights = product_df["Morning_Weight"].values
    elif 17 <= hour <= 22:
        time_weights = product_df["Evening_Weight"].values
    else:
        time_weights = np.ones(len(product_df))
    
    # Combine demand level weight and time-of-day weight
    demand_weights = product_df["Demand_Level"].map(get_demand_weight).values
    combined_weights = demand_weights * time_weights
    combined_weights = combined_weights / combined_weights.sum()
    
    # Select anchor product
    anchor_idx = rng.choice(len(product_df), p=combined_weights)
    anchor_product = product_df.iloc[anchor_idx]["Product_Name"]
    selected_indices = {anchor_idx}
    
    # Apply co-purchase rules
    name_to_idx = {row["Product_Name"]: idx for idx, row in product_df.iterrows()}
    
    for anchor, companion, prob in CO_PURCHASE_RULES:
        if anchor == anchor_product and companion in name_to_idx:
            if rng.random() < prob and len(selected_indices) < basket_size:
                selected_indices.add(name_to_idx[companion])
    
    # Also check reverse co-purchase (companion → anchor)
    for anchor, companion, prob in CO_PURCHASE_RULES:
        if companion == anchor_product and anchor in name_to_idx:
            if rng.random() < (prob * 0.6) and len(selected_indices) < basket_size:
                selected_indices.add(name_to_idx[anchor])
    
    # Fill remaining slots with weighted random selection
    remaining = basket_size - len(selected_indices)
    if remaining > 0:
        available_mask = np.ones(len(product_df), dtype=bool)
        for idx in selected_indices:
            available_mask[idx] = False
        available_weights = combined_weights * available_mask
        if available_weights.sum() > 0:
            available_weights = available_weights / available_weights.sum()
            extra_indices = rng.choice(
                len(product_df), size=min(remaining, available_mask.sum()),
                replace=False, p=available_weights
            )
            selected_indices.update(extra_indices.tolist())
    
    # Build basket items
    basket_items = []
    for idx in selected_indices:
        product = product_df.iloc[idx]
        
        # Quantity: most products bought in qty 1-2, some staples up to 3
        if product["Product_Category"] in ["Staples", "Dairy", "Fruits & Vegetables"]:
            qty = rng.choice([1, 1, 1, 2, 2, 3])
        else:
            qty = rng.choice([1, 1, 1, 1, 2])
        
        # Discount: more discounts on evenings and weekends
        discount_prob = 0.15
        if is_weekend:
            discount_prob += 0.10
        if 17 <= hour <= 22:
            discount_prob += 0.05
        
        if rng.random() < discount_prob:
            discount_pct = rng.choice([5, 10, 10, 15, 15, 20, 25, 30],
                                       p=[0.15, 0.25, 0.25, 0.15, 0.10, 0.05, 0.03, 0.02])
        else:
            discount_pct = 0
        
        basket_items.append({
            "Product_ID": product["Product_ID"],
            "Product_Name": product["Product_Name"],
            "Product_Category": product["Product_Category"],
            "Quantity": qty,
            "Unit_Price": product["Unit_Price"],
            "Discount_Pct": discount_pct,
        })
    
    return basket_items


def generate_timestamp(date, hour, rng):
    """Generate a realistic timestamp within the given hour."""
    minute = rng.integers(0, 60)
    second = rng.integers(0, 60)
    return date.replace(hour=hour, minute=int(minute), second=int(second))


# ==============================================================================
# MAIN DATA GENERATION
# ==============================================================================

def generate_dataset():
    """Generate the complete synthetic transaction dataset."""
    print("=" * 70)
    print("SYNTHETIC DATA GENERATION")
    print("Quick-Commerce Dark Store Inventory Optimization")
    print("=" * 70)
    
    rng = np.random.default_rng(RANDOM_SEED)
    product_df = build_product_lookup()
    
    print(f"\nProduct catalogue: {len(product_df)} products across {len(PRODUCT_CATALOGUE)} categories")
    print(f"Simulation period: {START_DATE.strftime('%Y-%m-%d')} to {END_DATE.strftime('%Y-%m-%d')} ({NUM_DAYS} days)")
    print(f"Dark stores: {NUM_DARK_STORES}")
    print(f"Customer pool: {NUM_CUSTOMERS}")
    
    all_records = []
    order_counter = 0
    
    # Generate date range
    dates = [START_DATE + timedelta(days=d) for d in range(NUM_DAYS)]
    
    for day_idx, current_date in enumerate(dates):
        if day_idx % 30 == 0:
            print(f"  Generating: {current_date.strftime('%Y-%m')}")
        
        day_of_week = current_date.weekday()
        is_weekend = day_of_week >= 5
        month = current_date.month
        
        # Calculate daily order count with variability
        day_mult = get_day_multiplier(day_of_week)
        month_mult = get_monthly_multiplier(month)
        daily_orders = int(ORDERS_PER_DAY_BASE * day_mult * month_mult)
        daily_orders += int(rng.normal(0, daily_orders * 0.08))  # Add noise
        daily_orders = max(daily_orders, 50)
        
        # Distribute orders across hours based on hourly pattern
        hours = list(range(24))
        hour_weights = [get_hour_multiplier(h) for h in hours]
        hour_weights = np.array(hour_weights)
        hour_weights = hour_weights / hour_weights.sum()
        
        order_hours = rng.choice(hours, size=daily_orders, p=hour_weights)
        
        for order_hour in order_hours:
            order_counter += 1
            order_id = f"ORD_{order_counter:06d}"
            
            # Select dark store (weighted by demand multiplier)
            store_ids = list(DARK_STORES.keys())
            store_multipliers = [DARK_STORES[s]["demand_multiplier"] for s in store_ids]
            store_probs = np.array(store_multipliers) / sum(store_multipliers)
            store_id = rng.choice(store_ids, p=store_probs)
            
            # Select customer
            customer_id = f"CUST_{rng.integers(1, NUM_CUSTOMERS + 1):04d}"
            
            # Generate timestamp
            timestamp = generate_timestamp(current_date, int(order_hour), rng)
            
            # Generate basket
            basket = generate_basket(product_df, int(order_hour), is_weekend, month, rng)
            
            # Payment type
            payment = rng.choice(PAYMENT_TYPES, p=PAYMENT_WEIGHTS)
            
            # Delivery distance (km) — depends on area type
            area_type = DARK_STORES[store_id]["area_type"]
            if area_type == "urban_core":
                delivery_dist = round(rng.exponential(1.5) + 0.5, 1)
            elif area_type == "tech_park":
                delivery_dist = round(rng.exponential(2.0) + 0.8, 1)
            else:
                delivery_dist = round(rng.exponential(2.5) + 1.0, 1)
            delivery_dist = min(delivery_dist, 8.0)  # Cap at 8 km
            
            for item in basket:
                line_total = item["Quantity"] * item["Unit_Price"]
                discount_amount = round(line_total * item["Discount_Pct"] / 100, 2)
                
                record = {
                    "Order_ID": order_id,
                    "Timestamp": timestamp,
                    "Customer_ID": customer_id,
                    "Dark_Store_ID": store_id,
                    "Product_ID": item["Product_ID"],
                    "Product_Name": item["Product_Name"],
                    "Product_Category": item["Product_Category"],
                    "Quantity": item["Quantity"],
                    "Unit_Price": item["Unit_Price"],
                    "Discount_Pct": item["Discount_Pct"],
                    "Discount_Amount": discount_amount,
                    "Line_Total": round(line_total - discount_amount, 2),
                    "Payment_Type": payment,
                    "Delivery_Distance_km": delivery_dist,
                }
                all_records.append(record)
    
    df = pd.DataFrame(all_records)
    
    # ===========================================================================
    # INTRODUCE REALISTIC DATA QUALITY ISSUES (for data cleaning demonstration)
    # ===========================================================================
    print("\nIntroducing realistic data quality issues...")
    
    n = len(df)
    
    # 1. Missing values (~1-2% in select columns)
    # Some orders missing delivery distance (sensor/GPS issue)
    missing_dist_idx = rng.choice(n, size=int(n * 0.015), replace=False)
    df.loc[missing_dist_idx, "Delivery_Distance_km"] = np.nan
    
    # Some missing discount info
    missing_disc_idx = rng.choice(n, size=int(n * 0.008), replace=False)
    df.loc[missing_disc_idx, "Discount_Pct"] = np.nan
    df.loc[missing_disc_idx, "Discount_Amount"] = np.nan
    
    # A few missing payment types (system glitch)
    missing_pay_idx = rng.choice(n, size=int(n * 0.003), replace=False)
    df.loc[missing_pay_idx, "Payment_Type"] = np.nan
    
    # 2. Duplicate records (~0.5% — simulates double-entry from system retry)
    n_dup = int(n * 0.005)
    dup_idx = rng.choice(n, size=n_dup, replace=False)
    duplicates = df.iloc[dup_idx].copy()
    df = pd.concat([df, duplicates], ignore_index=True)
    
    # 3. A few outlier quantities (data entry errors — qty like 10, 15, 20)
    outlier_qty_idx = rng.choice(len(df), size=int(len(df) * 0.002), replace=False)
    df.loc[outlier_qty_idx, "Quantity"] = rng.choice([10, 12, 15, 20], size=len(outlier_qty_idx))
    
    # 4. A few negative prices (system error)
    neg_price_idx = rng.choice(len(df), size=5, replace=False)
    df.loc[neg_price_idx, "Unit_Price"] = -df.loc[neg_price_idx, "Unit_Price"]
    
    # Recalculate Line_Total where Quantity was changed to outlier
    for idx in outlier_qty_idx:
        row = df.loc[idx]
        if pd.notna(row["Discount_Pct"]):
            lt = row["Quantity"] * abs(row["Unit_Price"])
            da = round(lt * row["Discount_Pct"] / 100, 2)
            df.loc[idx, "Line_Total"] = round(lt - da, 2)
            df.loc[idx, "Discount_Amount"] = da
    
    # Shuffle to mix duplicates in
    df = df.sample(frac=1, random_state=RANDOM_SEED).reset_index(drop=True)
    
    # ===========================================================================
    # CALCULATE ORDER_VALUE (sum of Line_Total per order)
    # ===========================================================================
    order_values = df.groupby("Order_ID")["Line_Total"].sum().reset_index()
    order_values.columns = ["Order_ID", "Order_Value"]
    df = df.merge(order_values, on="Order_ID", how="left")
    
    # ===========================================================================
    # SAVE
    # ===========================================================================
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, "darkstore_transactions.csv")
    df.to_csv(output_path, index=False)
    
    # Also save the product catalogue
    product_df.to_csv(os.path.join(OUTPUT_DIR, "product_catalogue.csv"), index=False)
    
    # ===========================================================================
    # SUMMARY STATISTICS
    # ===========================================================================
    print(f"\n{'=' * 70}")
    print("DATASET GENERATION COMPLETE")
    print(f"{'=' * 70}")
    print(f"Total transaction-product records: {len(df):,}")
    print(f"Unique orders: {df['Order_ID'].nunique():,}")
    print(f"Unique products: {df['Product_ID'].nunique()}")
    print(f"Unique customers: {df['Customer_ID'].nunique():,}")
    print(f"Date range: {df['Timestamp'].min()} to {df['Timestamp'].max()}")
    print(f"Columns: {list(df.columns)}")
    print(f"\nMissing values:")
    for col in df.columns:
        miss = df[col].isna().sum()
        if miss > 0:
            print(f"  {col}: {miss} ({miss/len(df)*100:.2f}%)")
    print(f"\nDuplicate rows: {df.duplicated().sum()}")
    print(f"\nSaved to: {output_path}")
    print(f"Product catalogue saved to: {os.path.join(OUTPUT_DIR, 'product_catalogue.csv')}")
    
    return df


if __name__ == "__main__":
    df = generate_dataset()
    print("\n\nSample records:")
    print(df.head(10).to_string())
