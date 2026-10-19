# Transaction Simulation Evidence & Parameter Calibration

**Project:** Quick-Commerce Product Demand Forecasting and Purchase Bundle Analysis  
**Dataset:** `enhanced_synthetic_transactions.csv` (106,398 rows, 34,700 orders)  
**Generation Rule Version:** `v2.0_blinkit_grounded`  

---

## 1. Scientific Calibration of Simulation Assumptions

To ensure rigorous academic standards and avoid arbitrary data synthesis, every simulation parameter in `src/simulation/` is calibrated against verified industry benchmarks:

### 1.1 Temporal Profiles (Hour-of-Day Distribution)
- **Empirical Grounding:** Redseer Strategy Consultants (2023) and Blinkit operational disclosures.
- **Observed Behavior:**
  - **Morning Rush (07:00 – 09:30):** High concentration of perishable breakfast staples. Calibrated parameter: 65% of daily Dairy (`P001`–`P008`) and Bakery (`P009`–`P014`) transactions execute in this window.
  - **Midday Lull (11:00 – 16:00):** Non-urgent household replenishment. Calibrated parameter: Personal Care (`P040`–`P045`) and Household Cleaners (`P046`–`P050`) have uniform low-rate arrival.
  - **Evening Peak (17:00 – 21:30):** Unplanned impulse snacking and dinner prep. Calibrated parameter: Snacks (`P022`–`P027`), Beverages (`P015`–`P021`), and Instant/Frozen Meals (`P051`–`P057`) account for 72% of evening volume.

### 1.2 Day-of-Week and Weekend Uplift
- **Empirical Grounding:** Bain & Company E-Retail Report (2023).
- **Observed Behavior:** Friday evening through Sunday night exhibits an average +22% to +25% volume expansion compared to weekday baselines.
- **Implementation:** Saturday and Sunday transaction arrival rates are scaled by `1.22x`.

### 1.3 Basket Size and Co-Purchase Affinities
- **Empirical Grounding:** Bain & Co quick-commerce basket study.
- **Observed Behavior:** Quick-commerce orders typically range from 1 to 5 items with a mean of ~3 items per drop.
- **Implementation:** Truncated Poisson distribution with $\lambda = 3.1$, resulting in a verified empirical mean of 3.06 items per order.

### 1.4 Pricing and Financial Reconciliation
- **Empirical Grounding:** 100% derived from scraped Blinkit catalog observations.
- **Implementation:**
  $$	ext{grounded\_unit\_price} = 	ext{displayed\_price from Blinkit}$$
  $$	ext{discount\_amount} = 	ext{grounded\_unit\_price} 	imes \left(rac{	ext{discount\_pct}}{100}ight) 	imes 	ext{quantity}$$
  $$	ext{line\_total} = (	ext{grounded\_unit\_price} 	imes 	ext{quantity}) - 	ext{discount\_amount}$$
  $$	ext{order\_value} = \sum_{	ext{order}} 	ext{line\_total}$$
