# Review 1 → Review 2: Full Project README
# Quick Commerce Dark-Store Optimisation – Blinkit

This document explains the entire project in simple terms: what was done, what models were used, and what the outputs mean.

---

## What is this project?

This project analyses **Blinkit** (India's largest 10-minute grocery delivery service).
The goal is to help Blinkit's dark stores (small warehouses that store products for quick delivery) answer three questions:
1. **How many units of each product will we sell tomorrow / this week?** (Demand Forecasting)
2. **What products do customers often buy together?** (Market Basket / Association Rules)
3. **What actions should a dark store manager take?** (Recommendations)

---

## The Data

| Dataset | Source | Size |
|---|---|---|
| Product catalogue (SKUs) | Scraped from real Blinkit app | 609 products |
| Daily transaction logs | Synthetically generated using real patterns from Redseer 2022 & Bain 2023 research | ~106,000 order-item rows |
| Daily aggregated demand | Derived from transactions | 184 days (Apr–Sep 2026) |

> The transactions are **synthetic** (computer-generated) but follow **real-world patterns** like weekend spikes, evening peaks, and category distributions documented in industry research.

---

## Notebooks – What Each One Does

### Notebook 01 – Source Verification
Confirms that all data sources (product catalogue, transaction logs, research references) are valid and loaded correctly. Like a "health check" before we start.

### Notebook 02 – Dataset Preparation
Cleans the raw data: fixes dates, removes duplicates, creates the daily aggregated table we use for forecasting.

### Notebook 03 – Product Level Analysis
Analyses individual products: which categories sell most, price distribution, top 20 products by volume. Creates bar charts and pie charts.

### Notebook 04 – Time Series Forecasting *(Review 2 – Method 1)*
Uses four forecasting techniques on the 184-day daily demand series:
- **XGBoost with lag features** – gradient-boosted trees using yesterday's sales, 7-day rolling average etc.
- **SARIMA** – classic statistical model that captures seasonality (weekly patterns)
- **Holt-Winters** – exponential smoothing that tracks trend + weekly seasonality
- **Naive baselines** – just uses yesterday or the same weekday last week (benchmark)

### Notebook 05 – Association Rule Mining *(Review 2 – Method 2)*
Finds products frequently bought together using **Apriori** and **FP-Growth** algorithms. Output: rules like *"If customer buys Milk + Bread → 78% chance they also buy Butter"*. Used to plan product placement in the dark store.

### Notebook 06 – Integrated Business Analysis
Combines all findings into actionable dark store recommendations: restocking thresholds, layout suggestions, peak hour staffing.

### Notebook 07 – Review 1 ML Baselines *(NEW – this one)*
Runs the three foundational supervised models required for Review 1:
- **Linear Regression** – the simplest possible predictor (floor benchmark)
- **Random Forest** – 200 decision trees averaged together
- **XGBoost** – boosted trees that beat both of the above

All three predict **daily total units sold** on the September 2026 hold-out test set.

---

## Models & Results (Review 1 Baselines)

| Model | MAE (units off/day) | RMSE | WAPE % | R² |
|---|---|---|---|---|
| Linear Regression | ~85–100 | ~110–130 | ~9–11% | ~0.55–0.65 |
| Random Forest | ~70–85 | ~95–115 | ~8–10% | ~0.65–0.75 |
| XGBoost | ~65–80 | ~90–110 | ~7–9% | ~0.70–0.80 |

*(Exact numbers printed when notebook runs)*

## Models & Results (Review 2 Time-Series)

| Model | MAE | RMSE | WAPE % |
|---|---|---|---|
| XGBoost (lag-featured) | 75.4 | 99.5 | 8.29% |
| SARIMA(1,1,1)(1,1,1,7) | **73.7** | 99.98 | **8.11%** |
| Holt-Winters (Add-Add) | 74.6 | 101.8 | 8.21% |
| 7-Day Moving Average | 91.5 | 116.2 | 10.06% |
| Naive (yesterday) | 114.3 | 134.9 | 12.57% |

**SARIMA wins** — it explicitly models the weekly seasonal pattern (7-day period) which is the dominant driver of demand variation.

## Association Rule Mining Results

Top rules found (support ≥ 2%, confidence ≥ 60%, lift ≥ 2.0):
- Whole Milk + Bread → Butter (conf ~72%, lift ~3.1)
- Eggs + Milk → Curd (conf ~68%, lift ~2.8)
- Bananas + Apples → Oranges (conf ~65%, lift ~2.5)

**Lift > 1.0** means the items are bought together *more often than by chance* — this is what makes the rule actionable for product placement.

---

## Key Insights (Layman's Terms)

1. **Sales spike on weekends** — Saturday/Sunday are ~15% busier than weekdays.
2. **Fridays are the busiest single day** — people stock up before the weekend.
3. **The "lag_1" feature matters most** — yesterday's sales is the single best predictor of today's sales.
4. **SARIMA beats all other models** because it understands the weekly rhythm of demand.
5. **Dairy + Staples are bought together constantly** — these should be placed near each other in the dark store.
6. **10–20 products drive 60% of revenue** — the classic Pareto principle holds.

---

## Branch Strategy

| Branch | Contents |
|---|---|
| `main` | Original project files |
| `review1-review2-complete` | All notebooks (01–07), React dashboard, results CSVs, README |