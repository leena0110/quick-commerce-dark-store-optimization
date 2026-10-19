# Quick-Commerce Product Demand Forecasting & Real Data Grounding Pipeline

**Capstone Project:** Quick-Commerce Product Demand Forecasting and Purchase Bundle Analysis  
**Repository Module:** `data_pipeline/`  
**Author / Team:** Business Analytics Capstone Cohort  
**Last Verified Execution:** 2026-10-18 01:47:00 IST  

---

## 1. Overview & Faculty Directive

This module implements a complete, reproducible web scraping and real-data-grounded synthetic transaction generation pipeline designed to address faculty requirements:
1. **Empirically investigate and verify** legitimate Indian quick-commerce and online grocery platforms.
2. **Collect genuine retail product observations** (names, categories, brands, pack sizes, selling prices, MRPs, discounts, and inventory availability).
3. **Capture repeated point-in-time price observations** across distinct collection runs.
4. **Construct an enhanced synthetic transaction dataset grounded in real retail observations**, preserving the original 6-month simulation structure while substituting authentic market prices and brands.
5. **Provide a rigorous comparative validation** separating observed catalogue attributes from simulated customer purchase behaviors.

---

## 2. Directory Structure

```text
BA_Project/
├── data/
│   ├── raw/
│   │   ├── darkstore_transactions.csv      # Original synthetic transaction baseline (PRESERVED)
│   │   └── product_catalogue.csv           # Original 58 synthetic products (PRESERVED)
│   └── processed/
├── data_pipeline/                          # NEW REPRODUCIBLE PIPELINE MODULE
│   ├── requirements.txt                    # Python environment dependencies
│   ├── scraper.py                          # Verified production scraper for Blinkit categories
│   ├── price_tracker.py                    # Repeated observation snapshot tracker
│   ├── grounding_mapper.py                 # Grounding engine linking original SKUs to real items
│   ├── enhanced_generator.py               # Grounded synthetic transaction generator
│   ├── generate_charts.py                  # Statistical chart generation engine
│   ├── raw_product_observations.csv        # 744 raw scraped observations
│   ├── cleaned_product_catalogue.csv       # 609 distinct cleaned & normalized products
│   ├── price_snapshots.csv                 # 850 temporal snapshot records across observation passes
│   ├── product_mapping.csv                 # Mapping table linking 58 SKUs to genuine Blinkit SKUs
│   ├── enhanced_synthetic_transactions.csv # 106,398 grounded transaction rows
│   ├── data_dictionary.csv                 # Comprehensive data dictionary for all outputs
│   ├── source_verification_report.md       # Empirical platform audit & robots.txt verification
│   ├── data_validation_report.md           # Dataset quality, completeness & integrity audit
│   ├── dataset_comparison_report.md        # Deep comparison (Part A: Observed vs. Part B: Simulated)
│   ├── dataset_comparison_charts/          # High-resolution statistical comparison charts
│   │   ├── 01_price_distribution_comparison.png
│   │   ├── 02_category_price_boxplot.png
│   │   ├── 03_category_product_counts.png
│   │   ├── 04_order_value_distribution.png
│   │   ├── 05_quantity_distribution.png
│   │   ├── 06_hourly_order_profile.png
│   │   └── 07_category_revenue_comparison.png
│   └── raw_payloads/                       # Provenance payload samples for faculty audit
└── README.md
```

---

## 3. How to Reproduce the Pipeline

Ensure dependencies are installed:
```bash
pip install -r data_pipeline/requirements.txt
```

### Step 1: Run the Verified Scraper
Scrapes live product categories from Blinkit adhering to `robots.txt` and rate limits:
```bash
python data_pipeline/scraper.py
```
*Outputs: `raw_product_observations.csv` and `cleaned_product_catalogue.csv`.*

### Step 2: Record Repeated Price Snapshots
Tracks price and availability shifts across observation runs:
```bash
python data_pipeline/price_tracker.py
```
*Outputs: `price_snapshots.csv`.*

### Step 3: Run the Product Grounding Mapper
Establishes the link between original synthetic IDs and real observed products:
```bash
python data_pipeline/grounding_mapper.py
```
*Outputs: `product_mapping.csv`.*

### Step 4: Generate the Grounded Synthetic Transactions
Generates the 106,398 enhanced transaction lines with recalculated unit economics:
```bash
python data_pipeline/enhanced_generator.py
```
*Outputs: `enhanced_synthetic_transactions.csv`.*

### Step 5: Generate Comparison Visualizations
Produces high-resolution analytical graphs comparing baseline vs. real vs. grounded datasets:
```bash
python data_pipeline/generate_charts.py
```
*Outputs charts in `data_pipeline/dataset_comparison_charts/`.*

---

## 4. Key Metrics Summary for Faculty Review

- **Verified Data Source:** Blinkit (Zomato Quick Commerce Platform)
- **Source URL:** `https://blinkit.com/` (Public Category listing paths `/cn/*` via `/sitemaps/categories.xml`)
- **Total Real Product Observations Scraped:** 744 raw records
- **Distinct Real Products in Cleaned Catalogue:** 609 unique products
- **Product Categories Covered:** 9 core quick-commerce departments (Household, Beverages, Dairy, Bakery, Fruits & Vegetables, Snacks, Instant & Frozen, Personal Care, Staples)
- **Repeated Price Snapshots Collected:** 850 observations across 2 actual request passes
- **Enhanced Grounded Synthetic Transactions:** 106,398 transaction lines across 34,700 orders and 8 dark stores
- **Original Dataset Integrity:** 100% preserved (`data/raw/darkstore_transactions.csv` remains untouched)
- **Academic Transparency:** All generated transaction lines explicitly declare `data_origin = "grounded_synthetic"` and reference their underlying `source_product_id` and observation timestamp.
