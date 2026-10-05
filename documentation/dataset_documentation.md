# Dataset Documentation
## Quick-Commerce Dark Store Inventory & Bundling Optimization

---

## 1. Project Title
**Quick-Commerce Dark Store Inventory & Bundling Optimization**

Course: 23CSE452 — Business Analytics Capstone Project

---

## 2. Purpose
This dataset supports the investigation of two connected business problems in quick-commerce:
1. **Inventory/Demand Prediction** (Review 1): Predict future product demand to reduce stockout risk
2. **Product Bundling via Association Rules** (Review 2): Discover frequently co-purchased products to increase Average Order Value (AOV)

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
|---|---|
| Total raw transaction records | 106,398 |
| Total cleaned transaction records | 105,872 |
| Aggregated daily product-store observations | 78,416 |
| Unique orders | 34,700 |
| Unique products | 58 |
| Unique customers | 4,994 |
| Dark stores | 8 |
| Raw columns | 15 |
| Engineered feature count | 18 |

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
**Daily_Quantity**: The total quantity of a specific product ordered at a specific dark store on a given day.

This is a **regression** target used for demand prediction.

---

## 10. Missing Value Handling
| Column | Missing Count | % Missing | Handling Method | Justification |
|---|---|---|---|---|
| Delivery_Distance_km | ~1,593 | ~1.5% | Imputed with store-level median | GPS failures are store-specific |
| Discount_Pct | ~852 | ~0.8% | Imputed with 0 | Missing discount likely means no discount |
| Discount_Amount | ~852 | ~0.8% | Imputed with 0 | Consistent with Discount_Pct handling |
| Payment_Type | ~318 | ~0.3% | Imputed with mode (UPI) | System glitch; most common payment used |

---

## 11. Outlier Handling
| Issue | Count | Method | Justification |
|---|---|---|---|
| Quantity > 5 | ~212 | Capped at 5 | Quick-commerce single-item orders rarely exceed 5 units |
| Negative prices | 5 | Converted to absolute value | Clearly system errors (no product has a negative price) |
| Duplicate rows | ~526 | Removed | System retry/double-entry artifacts |

---

## 12. Known Limitations
1. **Synthetic data**: Does not capture the full complexity of real-world consumer behavior
2. **No external factors**: Does not include weather, local events, promotions, or competitor activity
3. **Simplified geography**: Delivery distances are simulated, not based on real maps
4. **Static pricing**: Prices do not change over the simulation period (no dynamic pricing)
5. **No returns/cancellations**: The dataset only includes completed transactions
6. **No supply-side constraints**: Assumes unlimited product availability (no actual stockouts simulated)
7. **Homogeneous customer behavior**: Customer segments are not explicitly modeled

---

## 13. Ethical & Privacy Statement
- This dataset is **100% synthetic** — it does not contain any real customer data
- No personal information, names, addresses, or behavioral data from real individuals was used
- This is NOT proprietary data from Blinkit, Zepto, Swiggy Instamart, or any real company
- The dataset was generated solely for academic purposes as part of a capstone project
- All analysis results apply only to this synthetic dataset and should not be generalized as real-world findings

---

## 14. Reproducibility Instructions

### Requirements
```
Python 3.10+
pandas >= 2.0
numpy >= 1.24
scikit-learn >= 1.2
xgboost >= 1.7
matplotlib >= 3.7
seaborn >= 0.12
```

### Steps to Reproduce
```bash
# 1. Generate the synthetic dataset
python src/data_generation.py

# 2. Run the complete analysis pipeline
python run_analysis.py

# 3. Generate the Jupyter notebook
python generate_notebook.py
```

The random seed (42) is set in all scripts to ensure exact reproducibility.

---

## 15. Files
| File | Location | Description |
|---|---|---|
| Raw dataset | `data/raw/darkstore_transactions.csv` | Original generated dataset with data quality issues |
| Product catalogue | `data/raw/product_catalogue.csv` | Master list of 58 products with attributes |
| Cleaned dataset | `data/processed/darkstore_transactions_cleaned.csv` | Dataset after cleaning |
| Feature dataset | `data/processed/daily_demand_features.csv` | Aggregated daily demand with engineered features |
