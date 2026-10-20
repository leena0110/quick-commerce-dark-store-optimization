# Team Contributions and Project Module Ownership

**Course:** 23CSE452 — Business Analytics Capstone Project  
**Institution:** Amrita School of Computing, Coimbatore  
**Team 4:**
- **Leena Sri K** (CB.SC.U4CSE23526)
- **A.C. Sanhitha Reddy** (CB.SC.U4CSE23206)
- **Kanish Kumaran M** (CB.SC.U4CSE23424)
- **Ande Taraka Srinivas** (CB.SC.U4CSE23212)
- **Ajay N Mukunth** (CB.SC.U4CSE23006)

---

## Technical Work Breakdown Structure (WBS)

### 1. Ande Taraka Srinivas (CB.SC.U4CSE23212)
- **Inventory Safety Stock Optimization Engine (`src/inventory_optimization.py`):**
  - Formulated continuous-review dynamic safety stock equations accounting for stochastic supplier lead times ($L \pm \sigma_L$).
  - Implemented normal quantile approximation ($Z$-scores) and target Cycle Service Level ($CSL$) evaluation (90%, 95%, 99%).
  - Developed Weekend Dynamic Reorder Point ($ROP$) module handling 15–25% demand surges.
  - Achieved **79.97% reduction in stockouts** across 8 dark stores (evaluated in `outputs/metrics/inventory_stockout_benchmarks.json`).
- **Dark Store Spatial Layout & Picker Path Optimization (`src/spatial_store_layout.py`):**
  - Designed the 3D warehouse layout model (Zones A, B, C; Aisles 1–6, Bays 1–10, Shelf Levels 1–4).
  - Implemented Golden Zone binning for top-velocity SKUs and Manhattan serpentine routing heuristics.
  - Reduced average picker travel distance per order by **34.2%** (assembly time from 215s down to 142s).
- **Cross-Validation & Hyperparameter Tuning Pipeline (`src/model_tuning.py`):**
  - Engineered 5-fold Expanding Window Forward-Chaining Time-Series Split to prevent lookahead leakage.
  - Tuned Random Forest and XGBoost regressors, reducing WAPE to 7.74% on holdout folds.
- **Null-Invariant Basket Affinity & Bundle Margin Scoring (`src/basket_affinity.py`):**
  - Implemented Kulczynski, Cosine similarity, and Imbalance Ratio ($IR$) for grocery baskets.
  - Formulated bundle margin feasibility formulas to ensure promotional discounts preserve profitability.
- **Rubric Compliance & Defense Harness (`src/evaluation_rubric_check.py`):**
  - Developed automated audit harness verifying 100% compliance with Amrita evaluation criteria.

---

### 2. A.C. Sanhitha Reddy (CB.SC.U4CSE23206)
- Data scraping pipeline for live Blinkit product observations (`data_pipeline/scraper.py`).
- Unit 3 Method 1 — Time-Series Forecasting (`stage5_time_series.py`, SARIMA, Holt-Winters, XGBoost lag models).
- Unit 3 Method 2 — Association Rule Mining (`stage6_association_rules.py`, Apriori & FP-Growth).
- Interactive React + Vite decision dashboard (`review2_blinkit/dashboard/`).
- Review 2 Final Presentation slides synthesis (`Review2_Final_Presentation.pptx`).

---

### 3. Leena Sri K (CB.SC.U4CSE23526)
- Review 1 synthetic transaction generation (`src/data_generation.py`).
- Review 1 exploratory data analysis & baseline regression notebook (`notebooks/review1_analysis.ipynb`).
- Dataset documentation and data dictionary creation (`documentation/dataset_documentation.md`).
- Initial model baseline benchmarks (Linear Regression, Random Forest).

---

### 4. Kanish Kumaran M (CB.SC.U4CSE23424) & Ajay N Mukunth (CB.SC.U4CSE23006)
- Literature review compilation and research gap matrix (`review2_blinkit/research/`).
- Simulation evidence gathering and benchmark verification against industry publications (Redseer, Bain & Co).
- Presentation formatting and visual asset preparation.
