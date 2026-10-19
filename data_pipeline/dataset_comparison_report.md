# Dataset Comparison Report: Original Synthetic vs. Real-Data-Grounded Dataset

**Project Title:** Quick-Commerce Product Demand Forecasting and Purchase Bundle Analysis  
**Date:** 2026-10-18  
**Scope:** Comparative evaluation of original baseline synthetic data against real observed retail observations and grounded synthetic transactions.

---

## 1. Overview of Evaluated Datasets

To satisfy academic requirements, this comparison evaluates three distinct datasets:

1. **Original Synthetic Dataset:** Generated in Review 1 (`data/raw/darkstore_transactions.csv` & `data/raw/product_catalogue.csv`) featuring 58 idealized synthetic products and 106,398 simulated transaction lines.
2. **Real-World Scraped Dataset:** Freshly scraped from Blinkit (`data_pipeline/cleaned_product_catalogue.csv`) containing 609 genuine product observations across 9 retail categories with real MRPs, discounts, brands, and pack sizes.
3. **Enhanced Grounded Synthetic Dataset:** (`data_pipeline/enhanced_synthetic_transactions.csv`) containing 106,398 transaction lines mapped to authentic Blinkit products with recalculated unit economics and transparent provenance metadata.

---

## 2. PART A: Comparison of Genuinely Observed Product Attributes

Part A evaluates **only real empirical data attributes** collected from the platform versus the initial theoretical assumptions.

| Dimension | Original Synthetic Catalogue | Real Scraped Catalogue (Blinkit) | Grounded 58 Product Subset | Evaluation & Impact |
| :--- | :--- | :--- | :--- | :--- |
| **Product Count** | 58 items | **609 items** | 58 items | Scraped catalogue expands product breadth by 10.5x, capturing real variant diversity. |
| **Category Breadth** | 9 categories | 9 categories | 9 categories | Category taxonomy matches 100% with Indian quick-commerce assortments. |
| **Brand Presence** | 0% (Abstract names: e.g. "Milk (1L)") | **100% Genuine Brands** | **100% Genuine Brands** | Real brands (Amul, Mother Dairy, Harvest Gold, Yakult, Dabur, Fortune) replace placeholders. |
| **Price Mean (INR)** | ₹74.40 | **₹104.30** | **₹76.60** | Baseline assumed prices were slightly lower than live market rates across premium packaged goods. |
| **Price Std Dev (INR)** | ₹49.10 | **₹96.80** | **₹51.20** | Scraped retail catalog exhibits higher variance due to gourmet and imported SKUs. |
| **Price Range** | ₹20.00 – ₹250.00 | **₹10.00 – ₹799.00** | **₹20.00 – ₹245.00** | High-end household and imported snack items in real data reach up to ₹799. |
| **Discounting Pattern** | Theoretical flat rules (0-30%) | **Genuine Market Discounts** | **Real Grounded Discounts** | Real catalogue displays 0% on fresh essentials (milk) and up to 45% on packaged snacks/detergents. |
| **Pack Size & Units** | Hardcoded in name string | **Explicitly Structured** | **Explicitly Structured** | Standardized `pack_size` (float) and `unit` (ml, g, kg, pcs) extracted cleanly. |

### Visualizations Referenced:
- `dataset_comparison_charts/01_price_distribution_comparison.png` — Demonstrates that while original synthetic prices formed discrete artificial peaks, real prices exhibit a smooth log-normal distribution common to consumer retail.
- `dataset_comparison_charts/02_category_price_boxplot.png` — Highlights category-level price variation, showing higher dispersion in real Beverages and Household cleaners compared to original conservative assumptions.
- `dataset_comparison_charts/03_category_product_counts.png` — Illustrates catalog depth across the 9 primary quick-commerce departments.

---

## 3. PART B: Comparison of Simulated Transaction Characteristics

Part B evaluates **simulated operational and behavioral characteristics**.

> **Methodological Clarification:**  
> The enhanced transactions are **grounded in real observed catalogue attributes**, but the basket timings, order frequencies, customer identities, and quantities remain **simulated models**. They should **never** be cited as real proprietary consumer order histories.

| Metric | Original Synthetic Transactions | Enhanced Grounded Transactions | Difference Analysis |
| :--- | :--- | :--- | :--- |
| **Total Order Count** | 34,700 orders | 34,700 orders | Identical (order structure preserved for direct comparative benchmarking). |
| **Total Transaction Lines** | 106,398 lines | 106,398 lines | Identical (basket item counts preserved). |
| **Mean Basket Size** | 3.07 items/order | 3.07 items/order | Preserved simulation parameter (1 to 6 items). |
| **Mean Order Value** | **₹262.92** | **₹270.99** | **+3.07% shift** (₹8.07 increase per basket due to live market pricing adjustments). |
| **Total Simulated Revenue** | ₹9,123,280.00 | **₹9,403,246.50** | Real catalogue pricing yields a more realistic revenue baseline for 8 dark stores over 6 months. |
| **Line Item Quantity** | 1 to 4 units (Mean: 1.48) | 1 to 4 units (Mean: 1.48) | Preserved. Most grocery transactions involve single-unit purchases. |
| **Temporal Profile** | Dual diurnal peaks | Dual diurnal peaks | 7-9 AM morning rush (milk/bread) and 6-9 PM evening rush (snacks/dinner essentials). |
| **Weekend Surge** | +20% higher order volume | +20% higher order volume | Preserved simulation parameter reflecting quick-commerce weekend spikes. |
| **Provenance Tracking** | None (Unlabelled synthetic) | **Full Explicit Metadata** | Every transaction line explicitly tagged with source ID, timestamp, and rule version. |

### Visualizations Referenced:
- `dataset_comparison_charts/04_order_value_distribution.png` — Displays the slight rightward shift in order basket value resulting from real-world product price grounding.
- `dataset_comparison_charts/05_quantity_distribution.png` — Confirms that item quantity distributions remain identical between baseline and enhanced models.
- `dataset_comparison_charts/06_hourly_order_profile.png` — Visualizes the 24-hour demand velocity curves, highlighting morning and evening peak hours.
- `dataset_comparison_charts/07_category_revenue_comparison.png` — Compares category revenue contributions, showing increased realistic contributions from Dairy and Bakery.

---

## 4. Key Analytical Insights for Capstone Faculty Presentation

1. **Why Real Grounding Matters:**
   - Synthetic models built on arbitrary prices risk misestimating revenue, holding costs, and bundle affinity margins.
   - Grounding synthetic dark store transactions in real Blinkit catalogue observations ensures that unit economic evaluations, safety stock costs, and inventory replenishment models reflect current Indian retail conditions.
2. **Bundle Analysis Implications:**
   - In Review 1, bundle association rules paired generic items like `"Milk (1L)"` + `"Bread (White)"`.
   - In the grounded dataset, bundle algorithms analyze authentic commercial pairs like *Mother Dairy Cow Milk* with *English Oven Milk Bread*, making dark store cross-merchandising recommendations actionable.
3. **Academic Defensibility:**
   - By distinguishing genuine observed retail data (Part A) from simulated transaction mechanics (Part B), the project maintains scientific rigor without misleading faculty or inventing non-existent purchase histories.
