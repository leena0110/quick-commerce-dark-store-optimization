# Quick-Commerce Dark Store Inventory & Bundling Optimization

## 23CSE452 — Business Analytics Capstone Project

---

## Project Overview

This project focuses on two connected business problems in quick-commerce platforms such as Blinkit, Zepto, and Swiggy Instamart:

1. **Inventory / Demand Prediction (Review 1)**  
   Predict daily product demand at the dark-store level to support demand-informed inventory planning.

2. **Product Bundling (Review 2)**  
   Identify products that are frequently purchased together using Association Rule Mining and extend demand forecasting using Time-Series Analysis.

---

## Review 1 — Data Analysis and Predictive Modelling

Review 1 focuses on predicting daily SKU-level demand using historical transaction data.

The analysis follows this workflow:

```text
Synthetic Transaction Data
        ↓
Data Cleaning
        ↓
Exploratory Data Analysis
        ↓
Daily SKU-Store Demand
        ↓
Feature Engineering
        ↓
Chronological Train-Test Split
        ↓
Regression Models
        ↓
Model Evaluation
        ↓
Business Findings
```

The complete analysis is available in:

`notebooks/review1_analysis.ipynb`

---

## Project Structure

```text
BA_Project/
│
├── data/
│   ├── raw/
│   │   ├── darkstore_transactions.csv
│   │   └── product_catalogue.csv
│   │
│   └── processed/
│       ├── darkstore_transactions_cleaned.csv
│       └── daily_demand_features.csv
│
├── documentation/
│   └── dataset_documentation.md
│
├── notebooks/
│   └── review1_analysis.ipynb
│
├── outputs/
│   ├── figures/
│   ├── metrics/
│   └── tables/
│
├── src/
│   └── data_generation.py
│
└── README.md
```

---

## Dataset

The project uses a **synthetic dataset generated using Python** for academic purposes.

### Dataset Summary

| Attribute | Details |
|---|---|
| **Raw transaction records** | 106,398 |
| **Cleaned records** | 105,872 |
| **Unique orders** | ~34,700 |
| **Products** | 58 |
| **Categories** | 9 |
| **Dark stores** | 8 |
| **Collection period** | April 1 – September 30, 2026 |
| **Duration** | 183 days |

The raw transaction data contains variables such as:

| Variable | Description |
|---|---|
| `Order_ID` | Unique order identifier |
| `Timestamp` | Transaction date and time |
| `Customer_ID` | Customer identifier |
| `Dark_Store_ID` | Dark store identifier |
| `Product_ID` | Product identifier |
| `Product_Name` | Product name |
| `Product_Category` | Product category |
| `Quantity` | Number of units purchased |
| `Unit_Price` | Price per unit |
| `Discount_Pct` | Discount percentage |
| `Delivery_Distance_km` | Delivery distance in kilometres |
| `Payment_Type` | Payment method used |

Detailed dataset information is available in:

`documentation/dataset_documentation.md`

---

## Data Cleaning and Preprocessing

The raw transaction data was checked for:

- Duplicate records
- Invalid or negative prices
- Unusually high quantities
- Missing values

### After Preprocessing

| Metric | Result |
|---|---:|
| **Original records** | 106,398 |
| **Cleaned records** | 105,872 |
| **Duplicate rows removed** | 526 |

Additional preprocessing steps included:

- Missing values were handled using appropriate imputation methods.
- Invalid price values were corrected.
- Unusually high quantity values were handled.

The detailed preprocessing steps and evidence are available in the Review 1 notebook.

---

## Exploratory Data Analysis

The exploratory analysis was performed to understand demand patterns across time, product categories, and stores.

### Key EDA Findings

#### 1. Peak-Hour Demand

**52.2% of units** were concentrated in the identified morning and evening peak periods.

This indicates that demand is not evenly distributed throughout the day and that inventory availability should account for peak-hour demand.

#### 2. Category Demand

**Fruits & Vegetables** and **Dairy** were the highest-volume product categories.

These categories therefore represent important areas for demand-informed inventory planning.

#### 3. Weekend Demand

Average weekend demand was **23.1% higher** than weekday demand.

This suggests that inventory planning should account for differences between weekday and weekend demand patterns.

### EDA Visualizations

The generated EDA visualizations are available in:

`outputs/figures/`

Key visualizations include:

- `01_hourly_demand.png` — Hourly demand pattern
- `02_category_demand.png` — Category-wise demand
- `03_weekday_vs_weekend.png` — Weekday vs weekend demand
- `04_top_products.png` — Top products by demand
- `05_daily_trend.png` — Daily demand trend
- `06_demand_heatmap.png` — Demand heatmap
- `07_store_demand.png` — Store-level demand

---

## Feature Engineering

The transaction-level data was transformed into daily SKU-store demand records.

### Prediction Target

**`Daily_Quantity`**

This represents the total number of units of a specific product sold at a specific dark store on a specific day.

### Features Used

| Feature Group | Description |
|---|---|
| **Calendar features** | Day, week, month, and related time-based information |
| **Historical product demand** | Previous demand information for the product |
| **Historical category demand** | Previous demand information for the product category |
| **Demand lag features** | Previous-day and historical demand values |
| **Rolling demand averages** | Moving averages of historical demand |
| **Rolling demand variability** | Rolling standard deviation of demand |
| **Store-level activity** | Historical order activity at the store level |

Features were constructed using information available **before the prediction date** to avoid data leakage.

---

## Predictive Modelling

The prediction task is a **regression problem**.

Three models were compared:

1. **Linear Regression**
2. **Random Forest Regressor**
3. **XGBoost Regressor**

A chronological **80/20 train-test split** was used, with earlier observations used for training and later observations used for testing.

This approach was selected because the task involves predicting future demand from historical observations.

---

## Model Results

The models were evaluated using **R², MAE, MSE, and RMSE**.

| Model | R² | MAE | MSE | RMSE |
|---|---:|---:|---:|---:|
| Linear Regression | 0.3675 | 1.3456 | 3.3792 | 1.8383 |
| **Random Forest** | **0.3710** | **1.3322** | **3.3606** | **1.8332** |
| XGBoost | 0.3694 | 1.3336 | 3.3688 | 1.8354 |

### Best Model

**Random Forest Regressor**

| Metric | Result |
|---|---:|
| **R²** | **0.3710** |
| **MAE** | **1.3322 units** |
| **RMSE** | **1.8332 units** |

Random Forest achieved the best overall test performance among the three models, although the differences between the models were relatively small.

### Model Interpretation

The results indicate that all three models produced similar performance on the test data. Random Forest performed slightly better based on the combination of higher R² and lower MAE and RMSE.

The relatively close performance of the models suggests that the historical demand features were more influential than the choice between these three regression algorithms.

---

## Feature Importance

The most important features in the Random Forest model were:

| Rank | Feature | Importance |
|---:|---|---:|
| 1 | `Product_Hist_Avg_Demand` | 65.25% |
| 2 | `Category_Hist_Avg_Demand` | 5.82% |
| 3 | `Store_Orders_Roll_Mean_7d` | 4.28% |
| 4 | `Day_of_Week` | 3.03% |
| 5 | `Demand_Roll_Std_7d` | 2.99% |

**Key finding:** Historical product-level demand was the strongest predictor among the features used by the Random Forest model.

This indicates that previous demand for a product provides the strongest signal for estimating its future demand.

---

## Business Findings

Based on the Review 1 analysis, the following observations were identified:

- Demand varies considerably across different hours of the day.
- Morning and evening periods account for a significant share of total demand.
- Fruits & Vegetables and Dairy are among the highest-volume categories.
- Weekend demand is higher than weekday demand.
- Historical product demand is the most influential predictive feature.
- Random Forest produced the best overall performance among the three tested regression models.

These findings can support **demand-informed inventory planning** at the dark-store level.

---

## Review 2 Plan

Review 2 will extend the project using the transaction-level data.

### Time-Series Analysis

Demand forecasting methods such as:

- **ARIMA / SARIMA**
- **Prophet**

will be explored for demand forecasting.

The objective is to analyse demand trends and forecast future demand over time.

### Association Rule Mining

Association Rule Mining will be used to identify frequently co-purchased products and support product bundling recommendations.

The analysis will focus on relationships between products purchased within the same order.

The transaction-level dataset preserves the required **order, product, and timestamp information** for these analyses.

---

## Outputs

The `outputs/` folder contains the results generated during the analysis.

### Figures

The `outputs/figures/` folder contains:

- EDA visualizations
- Model comparison plots
- Prediction vs actual plots
- Feature importance visualization

### Metrics

The `outputs/metrics/` folder contains:

- `business_interpretation.json`
- `cleaning_summary.json`
- `eda_findings.json`
- `model_results.json`

### Tables

The `outputs/tables/` folder contains:

- `feature_importance.csv`
- `model_comparison.csv`

---

## Data and Ethical Statement

This project uses **100% synthetic data** generated for academic purposes.

No real customer data, proprietary company data, or pre-built Kaggle, UCI, or GitHub datasets were used.

The findings therefore apply only to the synthetic dataset used in this academic project and should not be interpreted as direct findings about Blinkit, Zepto, or Swiggy Instamart.

The names of quick-commerce platforms are used only to provide business context for the academic problem.

---

## Project Files

| File / Folder | Purpose |
|---|---|
| `notebooks/review1_analysis.ipynb` | Review 1 analysis and modelling |
| `documentation/dataset_documentation.md` | Dataset generation and documentation |
| `data/raw/` | Raw synthetic datasets |
| `data/processed/` | Cleaned and processed datasets |
| `outputs/figures/` | EDA and model visualizations |
| `outputs/metrics/` | Analysis and model metrics |
| `outputs/tables/` | Result tables |
| `src/data_generation.py` | Synthetic data generation script |
| `README.md` | Project documentation |

---

## Academic Project

**Course:** 23CSE452 — Business Analytics

**Project:** Quick-Commerce Dark Store Inventory & Bundling Optimization