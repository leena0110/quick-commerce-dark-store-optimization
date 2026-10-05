# Dataset Documentation
## Quick-Commerce Dark Store Inventory & Bundling Optimization

Course: **23CSE452 — Business Analytics Capstone Project** | Review 1

---

## Quick Reference — Review 1 Rubric Mapping

| Rubric Requirement | Section in this Document |
|---|---|
| Source and collection method | §3 Data Generation Method |
| Dataset size | §6 Dataset Size |
| Key variables | §7 Variable Dictionary |
| Prediction target | §9 Prediction Target |
| Collection period and limitations | §5 Simulation Period · §13 Known Limitations |
| Dataset documentation | This document |
| Small data sample | §17 Sample Records |

---

## 1. Project Title
**Quick-Commerce Dark Store Inventory & Bundling Optimization**

---

## 2. Purpose
This dataset supports the investigation of two connected business problems in quick-commerce:
1. **Inventory/Demand Prediction** (Review 1): Predict daily product demand to support demand-informed inventory planning
2. **Product Bundling via Association Rules** (Review 2): Discover frequently co-purchased products to support product bundling recommendations

---

## 3. Data Generation Method
The dataset is **entirely synthetic**, generated using Python with the NumPy and Pandas libraries.

**Why Synthetic Data?**
- Real quick-commerce transaction data is proprietary and confidential (Blinkit, Zepto, Swiggy Instamart do not release operational data)
- The course prohibits pre-built datasets from Kaggle, UCI, GitHub, or similar repositories
- Synthetic generation provides full control over data assumptions and enables reproducibility

**Generation Script:** `src/data_generation.py`

**Random Seed:** 42 (ensures exact reproducibility)

---

## 4. Synthetic Data Assumptions

### 4.1 Business Context
- 8 dark stores operating in a metro city (Bangalore), each serving a local zone
- ~5,000 unique customers place orders across stores
- ~180 base orders per day across all stores

### 4.2 Product Catalogue
- **58 products** across **9 categories**: Dairy, Bakery, Beverages, Snacks, Fruits & Vegetables, Staples, Personal Care, Household, Instant & Frozen
- Each product has a defined demand level (high/medium/low) and time-of-day demand weights
- Prices are in Indian Rupees (INR), reflecting realistic quick-commerce pricing

### 4.3 Temporal Demand Patterns
- **Hourly patterns**: Morning peak (7–9 AM), lunch prep (11 AM–1 PM), evening/dinner peak (6–9 PM), minimal late-night demand
- **Day-of-week patterns**: Friday is ~5% above baseline (pre-weekend), Saturday +20%, Sunday +15%
- **Monthly/seasonal patterns**: Summer months (May-Jun) slightly higher; festive buildup (Aug-Sep) adds ~10-15%

### 4.4 Product Co-Purchase Relationships
Co-purchase rules are embedded to create realistic baskets for future Association Rule Mining:
| Anchor Product | Companion Product | Co-purchase Probability |
|---|---|---|
| Milk (1L) | Bread (White) | 40% |
| Bread (White) | Butter (100g) | 35% |
| Chips (Large) | Soft Drink (500ml) | 45% |
| Pasta (500g) | Pasta Sauce | 55% |
| Onion (1kg) | Tomato (500g) | 45% |
| Rice (1kg) | Dal/Lentils (500g) | 35% |
| ... | ... | ... |

These probabilities control the likelihood of adding a companion product when the anchor is already in the basket. The final co-purchase patterns emerge naturally from the data and must be discovered analytically.

### 4.5 Basket Size
Orders contain 1–6 products, with distribution weighted toward 2–4 items (realistic for quick-commerce).

### 4.6 Data Quality Issues (Intentional)
To demonstrate realistic data cleaning, minor quality issues were introduced:
- ~1.5% missing delivery distances (GPS/sensor failures)
- ~0.8% missing discount data
- ~0.3% missing payment types
- ~0.5% duplicate records (system retry/double-entry)
- ~0.2% outlier quantities (data entry errors with qty 10–20)
- 5 negative prices (system errors)

---

## 5. Simulation Period
**April 1, 2026 – September 30, 2026** (183 days / ~6 months)

---

## 6. Dataset Size

| Metric | Value |
|---|---:|
| Total raw transaction records | 106,398 |
| Total cleaned transaction records | 105,872 |
| Complete daily product-store combinations | 84,912 |
| Final modelling observations | 78,416 |
| Unique orders | ~34,700 |
| Unique products | 58 |
| Unique customers | 4,994 |
| Dark stores | 8 |
| Raw columns | 15 |
| Engineered features | 18 |

### Daily Store-Product Panel

For demand modelling, the transaction-level data was aggregated into a complete daily product-store panel.

The complete panel contains:

**183 days × 8 dark stores × 58 products = 84,912 observations**

Days with no recorded sales were explicitly represented with `Daily_Quantity = 0`.

The first 14 days were then excluded from modelling because the lag and rolling features require sufficient historical observations. This resulted in **78,416 final modelling observations**.

---

## 7. Variable Dictionary

| # | Variable | Type | Description |
|---|---|---|---|
| 1 | `Order_ID` | String | Unique identifier for each order (e.g., ORD_000001) |
| 2 | `Timestamp` | Datetime | Date and time when the order was placed |
| 3 | `Customer_ID` | String | Unique identifier for each customer (e.g., CUST_0001) |
| 4 | `Dark_Store_ID` | String | Identifier for the dark store fulfilling the order (DS_001 to DS_008) |
| 5 | `Product_ID` | String | Unique identifier for each product (e.g., P001) |
| 6 | `Product_Name` | String | Human-readable product name |
| 7 | `Product_Category` | String | Product category (Dairy, Bakery, Beverages, Snacks, Fruits & Vegetables, Staples, Personal Care, Household, Instant & Frozen) |
| 8 | `Quantity` | Integer | Number of units of the product in this order line |
| 9 | `Unit_Price` | Float | Price per unit in INR |
| 10 | `Discount_Pct` | Float | Discount percentage applied (0–30%) |
| 11 | `Discount_Amount` | Float | Absolute discount amount in INR |
| 12 | `Line_Total` | Float | Total amount for this line item after discount |
| 13 | `Payment_Type` | String | Payment method (UPI, Credit Card, Debit Card, Cash on Delivery, Wallet) |
| 14 | `Delivery_Distance_km` | Float | Distance from dark store to delivery location in kilometers |
| 15 | `Order_Value` | Float | Total value of the complete order (sum of all line items) |

---

## 8. Data Types

| Variable | Python/Pandas Type |
|---|---|
| Order_ID | object (string) |
| Timestamp | datetime64[ns] |
| Customer_ID | object (string) |
| Dark_Store_ID | object (string) |
| Product_ID | object (string) |
| Product_Name | object (string) |
| Product_Category | object (string) |
| Quantity | int64 |
| Unit_Price | int64/float64 |
| Discount_Pct | float64 |
| Discount_Amount | float64 |
| Line_Total | float64 |
| Payment_Type | object (string) |
| Delivery_Distance_km | float64 |
| Order_Value | float64 |

---

## 9. Prediction Target
**`Daily_Quantity`**: The total number of units of a specific product sold at a specific dark store on a specific calendar day.

This is a **regression** target used for demand prediction.

---

## 10. Feature Engineering

For Review 1, the cleaned transaction-level data was transformed into daily product-store observations and 18 leakage-safe features were created.

### Calendar Features

- `Day_of_Week`
- `Day_of_Month`
- `Month`
- `Is_Weekend`
- `Week_of_Year`

### Product and Category Features

- `Unit_Price`
- `Product_Hist_Avg_Demand`
- `Category_Hist_Avg_Demand`

### Demand Lag Features

- `Demand_Lag_1d`
- `Demand_Lag_2d`
- `Demand_Lag_3d`
- `Demand_Lag_7d`

### Rolling Demand Features

- `Demand_Roll_Mean_3d`
- `Demand_Roll_Mean_7d`
- `Demand_Roll_Mean_14d`
- `Demand_Roll_Std_7d`

### Store Activity Features

- `Store_Orders_Lag_1d`
- `Store_Orders_Roll_Mean_7d`

Historical and lag-based features were constructed using information available before the prediction date to avoid data leakage.

## 11. Missing Value Handling

| Column | Handling Method | Justification |
|---|---|---|
| `Delivery_Distance_km` | Imputed using store-level median | Delivery distance can vary by store, so store-level median preserves local distance characteristics |
| `Discount_Pct` | Missing values replaced with 0 | Represents no discount when discount information is missing |
| `Payment_Type` | Imputed using the mode | Used to retain records affected by missing payment information |
| Derived financial fields | Recalculated after cleaning | Ensures financial values remain consistent with the cleaned transaction attributes |

---

## 12. Outlier Handling
| Issue | Count | Method | Justification |
|---|---|---|---|
| Quantity > 5 | — | Capped at 5 | Extremely high quantities were treated as potential data-entry anomalies |
| Negative prices | 5 | Converted to absolute value | Clearly system errors (no product has a negative price) |
| Duplicate rows | ~526 | Removed | System retry/double-entry artifacts |

---

## 13. Known Limitations
1. **Synthetic data**: Does not capture the full complexity of real-world consumer behavior
2. **No external factors**: Does not include weather, local events, promotions, or competitor activity
3. **Simplified geography**: Delivery distances are simulated, not based on real maps
4. **Static pricing**: Prices do not change over the simulation period (no dynamic pricing)
5. **No returns/cancellations**: The dataset only includes completed transactions
6. **No supply-side constraints**: Product availability and actual stockouts are not represented in the dataset.
7. **Homogeneous customer behavior**: Customer segments are not explicitly modeled

---

## 14. Ethical & Privacy Statement
- This dataset is **100% synthetic** — it does not contain any real customer data
- No personal information, names, addresses, or behavioral data from real individuals was used
- This is NOT proprietary data from Blinkit, Zepto, Swiggy Instamart, or any real company
- The dataset was generated solely for academic purposes as part of a capstone project
- All analysis results apply only to this synthetic dataset and should not be generalized as real-world findings

---

## 15. Reproducibility Instructions

### Requirements

```text
Python 3.10+
pandas
numpy
scikit-learn
xgboost
matplotlib
seaborn
jupyter
```

### Steps to Reproduce

1. Generate the synthetic dataset:

python src/data_generation.py

2. Open the Review 1 analysis notebook:

notebooks/review1_analysis.ipynb

Run the notebook cells sequentially to reproduce the Review 1 preprocessing, feature engineering, modelling and evaluation.

The random seed (42) is set in all scripts to ensure exact reproducibility.

---

## 16. Files

| File | Location | Description |
|---|---|---|
| Raw transaction dataset | `data/raw/darkstore_transactions.csv` | Original synthetic transaction dataset |
| Product catalogue | `data/raw/product_catalogue.csv` | Master list of 58 products and product attributes |
| Cleaned dataset | `data/processed/darkstore_transactions_cleaned.csv` | Transaction dataset after preprocessing |
| Feature dataset | `data/processed/daily_demand_features.csv` | Daily demand data with engineered features |
| Dataset documentation | `documentation/dataset_documentation.md` | Dataset generation, variables, preprocessing and limitations |
| Review 1 notebook | `notebooks/review1_analysis.ipynb` | Complete Review 1 analysis and predictive modelling |
| Data generation script | `src/data_generation.py` | Python script used to generate the synthetic dataset |

---

## 17. Sample Records

The table below shows 5 representative rows from the raw transaction dataset (`data/raw/darkstore_transactions.csv`). These are actual records from the generated file — no values have been modified.

| Order_ID | Timestamp | Customer_ID | Dark_Store_ID | Product_ID | Product_Name | Product_Category | Qty | Unit_Price (₹) | Discount_Pct | Line_Total (₹) | Payment_Type | Delivery_Dist (km) | Order_Value (₹) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ORD_017803 | 2026-07-05 20:35:49 | CUST_4293 | DS_001 | P011 | Pav (6pcs) | Bakery | 1 | 30 | 0.0 | 30.0 | Credit Card | — | 200.0 |
| ORD_033614 | 2026-09-25 23:01:05 | CUST_2898 | DS_001 | P031 | Potato (1kg) | Fruits & Vegetables | 1 | 30 | 15.0 | 25.5 | UPI | 2.3 | 325.5 |
| ORD_032323 | 2026-09-19 22:08:39 | CUST_4760 | DS_002 | P029 | Onion (1kg) | Fruits & Vegetables | 1 | 35 | 0.0 | 35.0 | Cash on Delivery | 1.7 | 420.0 |
| ORD_017309 | 2026-07-02 11:56:21 | CUST_4405 | DS_007 | P049 | Dish Soap (500ml) | Household | 1 | 60 | 0.0 | 60.0 | Credit Card | 0.8 | 520.0 |
| ORD_006185 | 2026-05-04 09:01:20 | CUST_0166 | DS_003 | P002 | Curd (400g) | Dairy | 1 | 40 | 0.0 | 40.0 | Wallet | 1.6 | 235.0 |

> **Note:** The `Delivery_Distance_km` column shows `—` where the value is missing in the raw data. Missing delivery distances (~1.5% of records) were imputed with store-level medians during preprocessing (see §11).

### Product Catalogue Sample

The product catalogue (`data/raw/product_catalogue.csv`) defines the 58 products and their demand properties. A sample of 5 rows is shown below.

| Product_ID | Product_Name | Category | Unit_Price (₹) | Demand_Level | Morning_Weight | Evening_Weight |
|---|---|---|---|---|---|---|
| P001 | Milk (1L) | Dairy | 65 | high | 1.8 | 1.4 |
| P009 | Bread (White) | Bakery | 45 | high | 1.9 | 1.0 |
| P015 | Soft Drink (500ml) | Beverages | 40 | high | 0.6 | 1.7 |
| P029 | Onion (1kg) | Fruits & Vegetables | 35 | high | 1.0 | 1.2 |
| P049 | Dish Soap (500ml) | Household | 60 | medium | 0.9 | 1.1 |

`Morning_Weight` and `Evening_Weight` are multipliers applied during data generation to model time-of-day demand patterns.