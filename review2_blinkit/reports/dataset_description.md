# Dataset Description: Real Blinkit Catalogue & Grounded Transactions

**Project:** Quick-Commerce Product Demand Forecasting and Purchase Bundle Analysis  
**Course:** 23CSE452 — Business Analytics Capstone (Review 2)  
**Team 4:** Leena Sri K, A.C. Sanhitha Reddy, Kanish Kumaran M, Ande Taraka Srinivas, Ajay N Mukunth  

---

## 1. Executive Summary of Datasets

Review 2 integrates empirical e-grocery catalog observations from Blinkit with a grounded synthetic transaction log:

1. **Observed Blinkit Product Catalogue (`cleaned_product_catalogue.csv`):**
   - **Total Verified Products:** 609 unique items across 9 core grocery departments.
   - **Distinct Brands:** 150 brands (including Amul, Mother Dairy, Harvest Gold, Haldiram's, McCain, Dabur, Vim, Surf Excel).
   - **Price Range:** ₹10.00 to ₹2948.00 (Mean: ₹216.79).
   - **MRP Ceiling:** Mean MRP is ₹255.19, with an average observed promotional discount of 13.10%.
   - **Provenance:** Direct live HTML scraping from Blinkit's server endpoints under ethical throttling guidelines.

2. **Temporal Price Snapshots (`price_snapshots.csv`):**
   - **Total Observations:** 850 records covering 609 distinct products across multiple passes.
   - **Purpose:** Documenting intra-day and cross-run price stickiness vs. discount changes.

3. **Grounded Synthetic Transactions (`enhanced_synthetic_transactions.csv`):**
   - **Total Transactions:** 106,398 line items across 34,700 distinct consumer baskets.
   - **Simulation Horizon:** 183 operating days (2026-04-01 to 2026-09-30).
   - **Dark Store Facilities:** 8 localized fulfillment hubs (`DS_001` to `DS_008`).
   - **Customer Population:** 4,994 unique synthetic customer profiles.
   - **Mean Basket Value:** ₹270.99.

---

## 2. Category Distribution of Real Scraped Catalogue

| Category | Product Count | Share (%) | Mean Selling Price (INR) | Mean MRP (INR) | Mean Discount (%) |
|:---|:---|:---|:---|:---|:---|
| **Bakery** | 70 | 11.5% | ₹129.77 | ₹134.51 | 2.4% |
| **Beverages** | 88 | 14.4% | ₹161.09 | ₹182.42 | 10.7% |
| **Dairy** | 83 | 13.6% | ₹377.58 | ₹404.05 | 4.1% |
| **Fruits & Vegetables** | 68 | 11.2% | ₹78.56 | ₹96.71 | 18.1% |
| **Household** | 100 | 16.4% | ₹250.69 | ₹314.16 | 18.8% |
| **Instant & Frozen** | 61 | 10.0% | ₹204.38 | ₹239.67 | 14.6% |
| **Personal Care** | 37 | 6.1% | ₹369.92 | ₹450.73 | 18.2% |
| **Snacks** | 67 | 11.0% | ₹139.06 | ₹156.63 | 11.2% |
| **Staples** | 35 | 5.7% | ₹329.91 | ₹474.97 | 31.3% |

---

## 3. Data Dictionary Summary

All columns across raw and processed datasets have been fully documented in `reports/data_dictionary.csv`.
Key identifiers include:
- `source_product_id`: Permanent platform primary key from Blinkit.
- `synthetic_order_id`: Unique identifier for each simulated checkout basket (`ORD_XXXXXX`).
- `grounded_unit_price`: Real observed selling price directly scraped from Blinkit.
- `data_origin`: Explicit audit label (`grounded_synthetic`) guaranteeing transparency.
