# Data Validation Report

**Project:** Quick-Commerce Product Demand Forecasting and Purchase Bundle Analysis  
**Audit Date:** 2026-10-18 01:47:00 IST  
**Auditor:** Automated Capstone Data Pipeline Auditor  
**Primary Datasets Validated:**
1. `raw_product_observations.csv`
2. `cleaned_product_catalogue.csv`
3. `price_snapshots.csv`
4. `enhanced_synthetic_transactions.csv`

---

## 1. Quality Audit Summary

| Dataset | Record Count | Distinct Products | Null Value Pct | Duplicate Keys | Integrity Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `raw_product_observations.csv` | 744 rows | 609 unique IDs | 0.0% in primary fields | Handled (135 multi-listing duplicates preserved) | **PASSED** |
| `cleaned_product_catalogue.csv` | 609 rows | 609 unique IDs | 0.0% in mandatory fields | 0 duplicates (Primary Key enforced) | **PASSED** |
| `price_snapshots.csv` | 850 rows | 609 unique IDs | 0.0% in key price fields | 241 multi-run snapshot pairs | **PASSED** |
| `enhanced_synthetic_transactions.csv` | 106,398 rows | 58 mapped products | 0.0% in pricing/keys | 0 duplicate order-item conflicts | **PASSED** |

---

## 2. Real Product Catalogue Validation (`cleaned_product_catalogue.csv`)

### 2.1 Schema & Field Population
- **Field Completeness:**
  - `source_product_id`: 100% complete, string identifiers matching Blinkit backend entities.
  - `product_name`: 100% complete, genuine Indian retail titles (e.g. *Amul Taaza Toned Milk*, *Harvest Gold White Bread*, *Fortune Sunlite Refined Sunflower Oil*).
  - `brand`: 100% complete; unbranded items (such as loose farm produce) are explicitly standardized as `"Generic / Unbranded"`.
  - `displayed_price`: 100% complete. Range: ₹10.00 to ₹799.00; Mean: ₹104.30.
  - `original_price` (MRP): 100% complete. Validated `original_price >= displayed_price` across all records.
  - `discount_pct`: Validated within bounds `[0.0%, 65.0%]`. Mean discount on promotional grocery items: 8.4%.
  - `availability_status`: 100% complete.

### 2.2 Category Breakdown
The 609 scraped real products span the entire operational spectrum of Indian dark stores:
- **Household Cleaners:** 100 items (16.4%)
- **Beverages & Juices:** 88 items (14.4%)
- **Dairy Products:** 83 items (13.6%)
- **Bakery & Breads:** 70 items (11.5%)
- **Fresh Fruits & Vegetables:** 68 items (11.2%)
- **Snacks & Namkeen:** 67 items (11.0%)
- **Instant & Frozen Foods:** 61 items (10.0%)
- **Personal Care:** 37 items (6.1%)
- **Staples & Dry Fruits:** 35 items (5.7%)

---

## 3. Grounded Synthetic Transactions Validation (`enhanced_synthetic_transactions.csv`)

### 3.1 Structural Consistency with Baseline
- **Order Count:** Exactly 34,700 unique synthetic orders preserved.
- **Line Item Count:** Exactly 106,398 transaction line items preserved.
- **Temporal Horizon:** Exactly 183 simulated operating days (2026-04-01 to 2026-09-30).
- **Dark Store Coverage:** All 8 simulated dark stores (`DS_001` through `DS_008`) maintained.

### 3.2 Value Recalculation Check
- **Formula Verification:**
  - `Line_Total = (Quantity * Grounded_Unit_Price) - Discount_Amount`
  - Recomputed and passed with 0.00 discrepancy.
- **Order Basket Value:**
  - Recalculated as the sum of line totals per order ID.
  - 100% of order totals match the sum of their constituent transaction lines.

### 3.3 Provenance & Data Origin Labels
- 100% of rows contain `data_origin = "grounded_synthetic"`
- 100% of rows contain `generation_rule_version = "v2.0_blinkit_grounded"`
- 100% of rows contain direct references to `source_product_id` and `source_price_observation_timestamp`.

---

## 4. Academic Integrity & Methodological Transparency

1. **Simulation Boundaries:** Transaction dates, basket compositions, and customer order volumes remain simulated models generated to satisfy faculty research objectives. They are **not** customer proprietary purchase records.
2. **Grounding Mechanism:** Unit prices, pack sizes, product names, brands, and category tags are **genuine empirical observations** scraped directly from Blinkit's public retail interface on 2026-10-18.
