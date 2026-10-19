# Research Gap Statement

**Project:** Quick-Commerce Product Demand Forecasting and Purchase Bundle Analysis  
**Focus Area:** Hyperlocal Quick-Commerce Dark Store Operations  

---

## 1. Context and Prior Work

Existing literature in retail analytics typically bifurcates into two isolated streams:
1. **Isolated Demand Forecasting:** Studies such as the M5 Competition (Makridakis et al., 2022) focus extensively on store-level or SKU-level unit demand forecasting using point-of-sale time series from traditional supermarkets and hypermarkets. However, these models presume daily or weekly replenishment schedules and do not account for micro-fulfillment centers (dark stores) with 10–15 minute delivery promises and ultra-compact inventory footprint.
2. **Isolated Market Basket Analysis:** Studies in association rule mining (Mukherjee et al., 2023; Hossain et al., 2019) focus on finding co-occurring itemsets in static transaction logs to optimize shelf placement or promotional coupons. These studies rarely link frequent itemset bundles to day-ahead stock replenishment models.

---

## 2. The Identified Research Gap

**There is an absence of an integrated, reproducible decision-support workflow tailored to quick-commerce dark stores that synthesizes:**
1. **Empirical real-world catalogue and pricing intelligence** (grounded in actual live SKU availability, brand competition, and legal MRP constraints);
2. **Short-horizon SKU demand forecasting** (Unit 3 Method 1) using comparative statistical and machine learning models evaluated on chronological holdout periods; and
3. **Association rule mining** (Unit 3 Method 2) using Apriori and FP-Growth to identify high-affinity bundles.

---

## 3. Capstone Project Contribution

This project addresses this gap by:
- Grounding all product attributes, prices, and pack sizes in 609 genuine Blinkit catalog items across 9 core grocery categories.
- Modeling demand across 8 Bangalore dark-store facilities over a 183-day operating horizon.
- Establishing a closed-loop business decision rule: using time-series forecasts to determine replenishment buffer stocks, while simultaneously utilizing association rules (e.g., Bread + Butter, Pasta + Sauce) to build automated cross-sell bundles in the consumer app and pre-stage physical picking locations inside the dark store.
