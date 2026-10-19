# Project Asset Inventory & Data Provenance Audit

**Project:** Quick-Commerce Product Demand Forecasting and Purchase Bundle Analysis  
**Course Code:** 23CSE452 — Business Analytics Capstone Project (Review 2)  
**Team 4 Members:**
- Leena Sri K (CB.SC.U4CSE23526)
- A.C. Sanhitha Reddy (CB.SC.U4CSE23206)
- Kanish Kumaran M (CB.SC.U4CSE23424)
- Ande Taraka Srinivas (CB.SC.U4CSE23212)
- Ajay N Mukunth (CB.SC.U4CSE23006)

**Audit Date:** 2026-10-18  
**Audit Scope:** Phase One repository inventory, authoritative documents, data assets, and protection boundaries.

---

## 1. Physical Asset Inventory Table

| Asset Name | Relative File Path | Size (KB) | Row Count | Column Count | Audit Status | Primary Role & Provenance |
|:---|:---|:---|:---|:---|:---|:---|
| **Raw Blinkit Observations** | `data_pipeline/raw_product_observations.csv` | 273.40 | 744 | 22 | `VERIFIED` | Scraped live catalog items with URLs, brand, price, inventory |
| **Cleaned Blinkit Catalogue** | `data_pipeline/cleaned_product_catalogue.csv` | 223.83 | 609 | 22 | `VERIFIED` | Deduplicated, standardized catalog with cleaned units, pack sizes and verified MRP |
| **Blinkit Price Snapshots** | `data_pipeline/price_snapshots.csv` | 321.06 | 850 | 23 | `VERIFIED` | Multi-run snapshot tracker recording prices across observation runs |
| **Product Mapping** | `data_pipeline/product_mapping.csv` | 9.46 | 58 | 14 | `VERIFIED` | Cross-walk mapping 58 simulated product classes to real Blinkit catalog items |
| **Enhanced Synthetic Transactions** | `data_pipeline/enhanced_synthetic_transactions.csv` | 23289.92 | 106,398 | 22 | `VERIFIED` | 106,398 transaction records grounded with genuine Blinkit items & prices |
| **Data Pipeline Dictionary** | `data_pipeline/data_dictionary.csv` | 6.92 | 60 | 6 | `VERIFIED` | Comprehensive column metadata, data types, and business constraints |
| **Original Synthetic Transactions (Raw)** | `data/raw/darkstore_transactions.csv` | 12118.44 | 106,398 | 15 | `VERIFIED` | Review 1 historical baseline transaction dataset |
| **Original Synthetic Transactions (Cleaned)** | `data/processed/darkstore_transactions_cleaned.csv` | 12068.36 | 105,872 | 15 | `VERIFIED` | Cleaned Review 1 transaction dataset with outlier filters |
| **Daily Demand Features (Original)** | `data/processed/daily_demand_features.csv` | 15754.88 | 78,416 | 24 | `VERIFIED` | Review 1 engineered time-series lag and rolling demand features |
| **Review 1 Analysis Notebook** | `notebooks/review1_analysis.ipynb` | 450.98 | N/A | N/A | `VERIFIED` | Original Review 1 exploratory data analysis & regression model notebook |
| **Review 1 Presentation Format** | `Review_1_Presentation_Format.pptx` | 36.14 | N/A | N/A | `VERIFIED` | Original 9-slide Review 1 slide deck |
| **Final Project Presentation Template** | `Final_Project_Presentation_Template.pptx` | 67.64 | N/A | N/A | `VERIFIED` | Official 17-slide Final Project PowerPoint template |
| **Review 2 Requirements and Rubrics** | `Review_2_Requirements_and_Rubrics .docx` | 28.77 | N/A | N/A | `VERIFIED` | Authoritative evaluation criteria, marking rubrics, and instructions |

---

## 2. Directory Protection Boundaries

To ensure strict compliance with project preservation requirements:
1. **Original Review 1 Project (`data/`, `notebooks/`, `outputs/`, `src/`):** **STRICTLY PRESERVED / READ-ONLY**. All existing baseline model results, historical features, and slide numbers remain completely intact.
2. **Existing Scraper & Pipeline (`data_pipeline/`):** **PRESERVED AS AUDIT LOG & REPRODUCIBLE ARTIFACTS**. Contains raw scraped Blinkit payloads, scraper logs, and intermediate mapping tables.
3. **Review 2 Workspace (`review2_blinkit/`):** **ACTIVE EXECUTION AREA**. All new Unit 3 time-series analysis, association rule mining, validation summaries, literature reviews, website frontend, final report, and the filled 17-slide PowerPoint presentation will reside exclusively within this directory.

---

## 3. Discrepancy & Verification Notes

- **Course Code Discrepancy:** The midterm examination papers in historical archives referenced `19CSE352`, whereas the official final presentation template specifies `23CSE452 Business Analytics`. The student cohort is 2023 batch CSE (`CB.SC.U4CSE23...`), verifying that **`23CSE452` is the authoritative course code**.
- **Faculty Requirement on Data Grounding:** The faculty panel rejected purely fictional data. The 609 verified real Blinkit products and 850 snapshot observations provide the empirical real-world grounding for both product-level analytics and the enhanced transaction dataset.
