# Dataset Quality and Validation Summary

**Project:** Quick-Commerce Product Demand Forecasting and Purchase Bundle Analysis  
**Audit Standard:** Review 2 Academic & Technical Integrity Verification  
**Evaluation Date:** 2026-10-18  

---

## 1. Data Integrity Verification Matrix

| Validation Test | Criterion / Rule | Observed Result | Status |
|:---|:---|:---|:---|
| **Primary Key Uniqueness** | `source_product_id` in cleaned catalogue must be unique | Exactly 609 unique IDs out of 609 rows (0 duplicate IDs) | **PASSED** |
| **MRP Ceiling Invariance** | `original_price >= displayed_price` | 0 violations across all catalogue rows | **PASSED** |
| **Non-Negative Pricing** | `displayed_price > 0` | Min price is ₹10.00 (> 0) | **PASSED** |
| **Discount Bounds** | `0% <= discount_pct <= 100%` | Bounded within [0.0%, 65.0%] | **PASSED** |
| **Inventory Validity** | `inventory >= 0` | Valid non-negative integers | **PASSED** |
| **Transaction Order Integrity** | Every line item belongs to a valid order | Exactly 106,398 line items mapped to 34,700 orders | **PASSED** |
| **Temporal Range Check** | Continuous 6-month simulation | 2026-04-01 to 2026-09-30 (183 full operating days) | **PASSED** |
| **Cross-Table Referential Integrity** | All transaction products map to catalogue | 100% of synthetic products map to verified Blinkit items | **PASSED** |

---

## 2. Missing Value Audit

- Mandatory catalogue fields (`source_product_id`, `product_name`, `category`, `displayed_price`, `original_price`): **0% missing (0 nulls)**.
- Unbranded farm produce (`Fruits & Vegetables`): Formally imputed as `"Generic / Unbranded"` to preserve truth in advertising.
- Rating field: Present on 85.2% of items with active consumer reviews; unrated items left as null to avoid synthetic bias.

---

## 3. Provenance and Academic Ethics Compliance

- **No Artificial Web Traffic:** Web scraping was throttled with exponential backoffs and robots.txt inspection.
- **No Fictional Pricing:** 100% of prices in the catalogue originate directly from live Blinkit listings.
- **Synthetic Distinction:** All simulated transaction records are explicitly tagged `data_origin="grounded_synthetic"` and `generation_rule_version="v2.0_blinkit_grounded"`.
