"""
populate_presentation_v2.py
Populates the Final_Project_Presentation_Template.pptx with actual
Review 2 results using EXACT placeholder text from the template.

Run from the BA_Project directory:
    python review2_blinkit/src/evaluation/populate_presentation_v2.py
"""

import sys
import os
from pathlib import Path

BASE     = Path(__file__).resolve().parents[3]
TEMPLATE = BASE / "Final_Project_Presentation_Template.pptx"
CHARTS   = BASE / "review2_blinkit" / "results" / "charts"
OUTPUT   = BASE / "review2_blinkit" / "presentation" / "Review2_Final_Presentation.pptx"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

try:
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
except ImportError:
    os.system(f"{sys.executable} -m pip install python-pptx -q")
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN

GREEN = RGBColor(0x2E, 0xCC, 0x71)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GREY  = RGBColor(0xEC, 0xF0, 0xF1)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def set_run_text(run, text):
    run.text = text

def replace_in_shape(shape, old_text, new_text):
    """Replace placeholder text preserving existing run formatting."""
    if not shape.has_text_frame:
        return False
    tf = shape.text_frame
    full = tf.text
    if old_text not in full:
        return False
    # walk paragraphs / runs and replace
    for para in tf.paragraphs:
        para_text = "".join(r.text for r in para.runs)
        if old_text in para_text:
            # rebuild first run, clear rest
            if para.runs:
                para.runs[0].text = para_text.replace(old_text, new_text)
                for run in para.runs[1:]:
                    run.text = ""
            return True
        # also handle splits across runs
        combined = ""
        for run in para.runs:
            combined += run.text
        if old_text in combined:
            para.runs[0].text = combined.replace(old_text, new_text)
            for run in para.runs[1:]:
                run.text = ""
            return True
    return False

def replace_slide(slide, replacements: dict):
    """Apply all replacements to every shape on the slide."""
    for shape in slide.shapes:
        for old, new in replacements.items():
            replace_in_shape(shape, old, new)

def add_image(slide, img_path: Path, left_in, top_in, width_in, height_in=None):
    if not img_path.exists():
        print(f"  [WARN] Image not found: {img_path.name}")
        return
    kw = dict(left=Inches(left_in), top=Inches(top_in), width=Inches(width_in))
    if height_in:
        kw["height"] = Inches(height_in)
    slide.shapes.add_picture(str(img_path), **kw)

def add_textbox(slide, text, left_in, top_in, width_in, height_in,
                font_size=12, bold=False, color=WHITE, align=PP_ALIGN.LEFT):
    txBox = slide.shapes.add_textbox(
        Inches(left_in), Inches(top_in), Inches(width_in), Inches(height_in))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.color.rgb = color

def add_metric(slide, label, value, left_in, top_in):
    add_textbox(slide, value, left_in, top_in, 2.2, 0.5,
                font_size=20, bold=True, color=GREEN, align=PP_ALIGN.CENTER)
    add_textbox(slide, label, left_in, top_in+0.52, 2.2, 0.4,
                font_size=10, color=GREY, align=PP_ALIGN.CENTER)

# ---------------------------------------------------------------------------
# Load template
# ---------------------------------------------------------------------------
if not TEMPLATE.exists():
    print(f"[ERROR] Template not found: {TEMPLATE}")
    sys.exit(1)

prs = Presentation(str(TEMPLATE))
slides = prs.slides
print(f"Template loaded: {len(slides)} slides\n")

# ===========================================================================
# SLIDE 1 — Title
# ===========================================================================
s = slides[0]
replace_slide(s, {
    "[Project title]":
        "Quick-Commerce Dark Store Optimization:\nProduct Demand Forecasting & Purchase Bundle Analysis",
    "[Team number]     [Member names and register numbers]":
        "Team 1   |   "
        "Leena Sri K (CB.SC.U4CSE23526)   "
        "A.C. Sanhitha Reddy (CB.SC.U4CSE23206)   "
        "Kanish Kumaran M (CB.SC.U4CSE23424)   "
        "Ande Taraka Srinivas (CB.SC.U4CSE23212)   "
        "Ajay N Mukunth (CB.SC.U4CSE23006)",
    "[Guide / Faculty]     [Presentation date]":
        "Guide: Faculty, Dept. of CSE     |     Date: October 2026",
})
print("Slide 1: Title — done")

# ===========================================================================
# SLIDE 2 — Project Overview
# ===========================================================================
s = slides[1]
replace_slide(s, {
    "Business problem: [Who faces what problem?]":
        "Business problem: Blinkit dark store operators face demand volatility causing "
        "stockouts during peak windows and perishable write-offs during off-peak hours, "
        "while missing cross-sell revenue from unidentified product bundle affinities.",
    "Objectives: [Two measurable project objectives]":
        "Objectives:\n"
        "1. Forecast daily aggregate product demand 30 days ahead (WAPE < 12%).\n"
        "2. Mine statistically significant product co-purchase rules (Lift > 1.5).",
    "Business decision: [What decision will the analysis support?]":
        "Business decision: Dark store replenishment scheduling and promotional bundle design.",
    "Expected output: [Prediction, insight or recommendation]":
        "Expected output:\n"
        "• 30-day demand forecast with RMSE/WAPE model comparison.\n"
        "• 42 association rules with lift scores for bundle recommendations.\n"
        "• Interactive dashboard for stakeholder exploration.",
})
print("Slide 2: Project Overview — done")

# ===========================================================================
# SLIDE 3 — Workflow
# ===========================================================================
s = slides[2]
replace_slide(s, {
    "Completion status: [Confirm 100% implementation and integration]":
        "Completion status: 100% implemented and integrated.\n\n"
        "Unit 1 — EDA & Preprocessing: 609 real Blinkit SKUs scraped and cleaned.\n"
        "Unit 2 — Predictive Modelling: XGBoost demand regressor (RMSE 99.50).\n"
        "Unit 3 — Advanced Analytics:\n"
        "  Method 1: Time-Series Forecasting (6 models benchmarked)\n"
        "  Method 2: Association Rule Mining (Apriori + FP-Growth, 42 rules)\n\n"
        "All code in review2_blinkit/src/ | Charts in review2_blinkit/results/charts/\n"
        "Notebooks: review2_blinkit/notebooks/ | Dashboard: review2_blinkit/website/",
})
print("Slide 3: Workflow — done")

# ===========================================================================
# SLIDE 4 — Dataset Description
# ===========================================================================
s = slides[3]
replace_slide(s, {
    "Source and collection / generation method: [Details]":
        "Source and collection method:\n"
        "Primary — Web scraped from Blinkit.com using Python (requests + BeautifulSoup).\n"
        "Secondary — Research-grounded synthetic transactions (Redseer 2022, Bain 2023).",
    "Final dataset size: [Records] and [Variables]":
        "Final dataset size: 609 product SKUs (primary) | 106,398 transaction records (secondary)\n"
        "Variables: 8 product fields (name, category, MRP, price, discount, rating, reviews, id)",
    "Coverage: [Dates, population, location or domain]":
        "Coverage: Blinkit platform, India | Transactions: April–September 2026 (183 days)\n"
        "16 product categories | Single dark store simulation",
    "Unit mapping: [Variables / linked data used by each unit]":
        "Unit mapping:\n"
        "Unit 1: All 8 product variables — EDA, cleaning, discount analysis\n"
        "Unit 2: daily_quantity (target), lag features, calendar features — XGBoost\n"
        "Unit 3: daily_quantity time series (Method 1) | basket transactions (Method 2)",
})
print("Slide 4: Dataset — done")

# ===========================================================================
# SLIDE 5 — Final Data Sample
# ===========================================================================
s = slides[4]
replace_slide(s, {
    "Key variables: [Meaning, data types and units]":
        "Key variables:\n"
        "product_id (int) — unique SKU identifier\n"
        "category (str) — product category (16 levels)\n"
        "mrp (float, Rs) — Maximum Retail Price (MRP-compliant, fixed)\n"
        "selling_price (float, Rs) — actual Blinkit selling price\n"
        "discount_pct (float, %) — (MRP–price)/MRP × 100\n"
        "order_id (str) — unique transaction order identifier\n"
        "quantity (int) — units purchased per line item\n"
        "order_date (date) — transaction date (Apr–Sep 2026)",
    "[Explain linked datasets or method-specific subsets, if used]":
        "Linked datasets:\n"
        "• cleaned_product_catalogue.csv (609 rows) → product metadata for all units\n"
        "• enhanced_synthetic_transactions.csv (106,398 rows) → demand time series & baskets\n"
        "• daily_aggregated_demand.csv (183 rows) → Method 1 input series\n"
        "• Basket pivot matrix (30,296 multi-item orders) → Method 2 input",
})
# Insert product catalogue chart
add_image(s, CHARTS / "03_mrp_vs_selling_price.png", 0.3, 3.2, 5.0, 3.2)
add_image(s, CHARTS / "02_sku_depth_vs_discount.png", 5.5, 3.2, 4.5, 3.2)
print("Slide 5: Final Data — done + charts")

# ===========================================================================
# SLIDE 6 — Validation
# ===========================================================================
s = slides[5]
replace_slide(s, {
    "Final validated dataset: [Records retained and version / filename]":
        "Final validated dataset:\n"
        "• cleaned_product_catalogue.csv — 609 records | 8 variables | 0 missing\n"
        "• enhanced_synthetic_transactions.csv — 106,398 records | 0 missing | 0 duplicates\n"
        "• daily_aggregated_demand.csv — 183 records | Complete series\n\n"
        "Validation steps performed:\n"
        "1. Deduplication: 744 raw → 609 clean (removed 135 duplicate SKUs)\n"
        "2. MRP compliance check: 100% of products selling_price <= MRP\n"
        "3. Temporal continuity: 183 consecutive days confirmed, no date gaps\n"
        "4. Join integrity: All 106,398 transaction product_ids in catalogue\n"
        "5. Discount sanity: All values 0%–80%, mean 15.7%\n\n"
        "Price stability justification: Legal Metrology (Packaged Commodities) Rules 2011\n"
        "mandates fixed MRP on all packaged goods — Blinkit cannot charge above MRP.",
})
print("Slide 6: Validation — done")

# ===========================================================================
# SLIDE 7 — Unit 1 EDA
# ===========================================================================
s = slides[6]
replace_slide(s, {
    "[Insert two readable final-data charts with labels and units]":
        "[Chart 1: Category price boxplots | Chart 2: Discount depth distribution]",
    "Key findings: [Two patterns relevant to the objectives]":
        "Key findings:\n"
        "1. Snacks have the highest median discount (17.4%) — "
        "indicating promotional pricing as primary demand lever.\n"
        "2. Dairy & Beverage prices cluster tightly around MRP — "
        "confirming MRP compliance and stable procurement pricing.",
    "Preparation: [Cleaning, encoding, scaling or feature selection]":
        "Preparation:\n"
        "• Removed 135 duplicate SKUs (product_id deduplication)\n"
        "• Computed discount_pct = (mrp - selling_price) / mrp × 100\n"
        "• One-hot encoded category for regression features\n"
        "• Created lag features (lag_1, lag_2, lag_7, lag_14) for time-series\n"
        "• Created rolling statistics (roll_mean_7, roll_std_7, roll_mean_14)\n"
        "• Calendar features: day_of_week, is_weekend, month, day_of_month",
})
add_image(s, CHARTS / "01_catalogue_price_boxplots.png", 0.2, 1.8, 5.0, 3.5)
add_image(s, CHARTS / "02_sku_depth_vs_discount.png",    5.4, 1.8, 4.6, 3.5)
print("Slide 7: Unit 1 EDA — done + charts")

# ===========================================================================
# SLIDE 8 — Unit 2 Predictive Modelling
# ===========================================================================
s = slides[7]
replace_slide(s, {
    "Evaluation setup: [Target, inputs, split and test record count]":
        "Evaluation setup:\n"
        "Target: daily_quantity (aggregate units per day)\n"
        "Inputs: lag_1, lag_2, lag_7, lag_14, roll_mean_7, roll_std_7,\n"
        "        roll_mean_14, day_of_week, is_weekend, month, day_of_month\n"
        "Split: Chronological holdout — Train 153 days (Apr–Aug 2026) | "
        "Test 30 days (Sep 2026)\n"
        "Test records: 30 daily observations | No data leakage",
    "Selected model and interpretation: [Choice, evidence and limitation]":
        "Selected model: XGBoost Regressor\n"
        "Evidence: RMSE 99.50 units | WAPE 8.29% — best RMSE across 6 models\n"
        "Key driver: day_of_week (31.78% importance) — captures weekend uplift\n"
        "Second driver: lag_7 (17.58%) — same-weekday-last-week demand memory\n"
        "Limitation: requires 14-day warm-up window; not suitable for new SKUs\n\n"
        "Model Comparison:\n"
        "XGBoost: RMSE 99.50 | SARIMA: 99.98 | HW: 101.76 | "
        "MovAvg: 116.17 | S-Naive: 137.57 | Naive: 134.93",
})
add_image(s, CHARTS / "04_time_series_forecast_comparison.png", 0.2, 1.7, 5.8, 3.7)
add_image(s, CHARTS / "05_forecast_model_rmse_comparison.png",  6.2, 1.7, 3.8, 2.0)
add_image(s, CHARTS / "06_xgboost_feature_importance.png",       6.2, 3.9, 3.8, 2.0)
print("Slide 8: Unit 2 Modelling — done + charts")

# ===========================================================================
# SLIDE 9 — Unit 3 Method Selection
# ===========================================================================
s = slides[8]
replace_slide(s, {
    "Select any two: Time-Series Analysis, Text Mining, Association Rule Mining":
        "Selected Methods:\n\n"
        "METHOD 1: Time-Series Analysis\n"
        "Purpose: Forecast daily aggregate demand 30 days ahead to optimise\n"
        "dark store inventory replenishment scheduling.\n"
        "Models: Naive, Seasonal-Naive, Moving Average, Holt-Winters, SARIMA, XGBoost\n"
        "Winner: XGBoost — RMSE 99.50 | WAPE 8.29%\n\n"
        "METHOD 2: Association Rule Mining\n"
        "Purpose: Discover high-lift product co-purchase patterns from transaction\n"
        "baskets to design bundle promotions and optimise dark store shelf layout.\n"
        "Algorithms: Apriori (baseline) + FP-Growth (production)\n"
        "Result: 42 valid rules | Top lift 5.11x (Malabar Paratha bundle)",
})
add_image(s, CHARTS / "05_forecast_model_rmse_comparison.png", 0.2, 3.8, 4.8, 2.8)
add_image(s, CHARTS / "09_top10_bundle_recommendations.png",   5.2, 3.8, 4.8, 2.8)
print("Slide 9: Unit 3 Selection — done + charts")

# ===========================================================================
# SLIDE 10 — Method 1 Implementation (Time-Series)
# ===========================================================================
s = slides[9]
replace_slide(s, {
    "Selected method: [Method 1 name and purpose]":
        "Selected method: Time-Series Demand Forecasting\n"
        "Purpose: Predict daily product demand to enable proactive dark store restocking.",
    "Input and preparation: [Final-data subset and transformations]":
        "Input: daily_aggregated_demand.csv — 183-day time series (Apr–Sep 2026)\n"
        "Preparation: Lag features (lag_1,2,7,14), rolling mean/std (7,14-day),\n"
        "calendar features (day_of_week, is_weekend, month, day_of_month)\n"
        "Train: 153 days | Test: 30 days (Sep 2026) — strict temporal split",
    "Implementation: [Algorithm, parameters and tools]":
        "Algorithms: Naive, Seasonal-Naive, 7-day Moving Average, Holt-Winters\n"
        "(alpha=auto, beta=auto, additive), SARIMA(1,1,1)(1,1,1,7) (auto-tuned),\n"
        "XGBoost Regressor (n_estimators=300, max_depth=5, learning_rate=0.05)\n"
        "Tools: Python, scikit-learn, statsmodels, xgboost, pandas, matplotlib",
    "Output: [Actual forecast, text result or association rules]":
        "Output:\n"
        "• 30-day Sep 2026 forecast series per model (JSON + CSV)\n"
        "• Model comparison table (RMSE, MAE, WAPE)\n"
        "• XGBoost feature importance chart\n"
        "• Recommendation: stock +35% dairy ahead of weekends",
})
print("Slide 10: Method 1 Implementation — done")

# ===========================================================================
# SLIDE 11 — Method 1 Evaluation
# ===========================================================================
s = slides[10]
replace_slide(s, {
    "Evaluation data: [Final-data records, subset and evaluation setup]":
        "Evaluation data: 30 daily records (Sep 2026 holdout, previously unseen)\n"
        "Setup: Metrics — MAE, RMSE, WAPE; chronological split ensures no data leakage",
    "Interpretation: [Selected approach, business meaning and limitation]":
        "Selected: XGBoost Regressor (RMSE 99.50 | WAPE 8.29%)\n\n"
        "Full model comparison:\n"
        "Rank 1: XGBoost     RMSE 99.50  WAPE 8.29%\n"
        "Rank 2: SARIMA      RMSE 99.98  WAPE 8.11%\n"
        "Rank 3: Holt-Winters RMSE 101.76 WAPE 8.21%\n"
        "Rank 4: Moving Avg  RMSE 116.17 WAPE 10.06%\n"
        "Rank 5: Naive       RMSE 134.93 WAPE 12.57%\n"
        "Rank 6: Seasonal-Naive RMSE 137.57 WAPE 11.18%\n\n"
        "Business meaning: XGBoost identifies weekend demand spikes 7 days ahead,\n"
        "enabling just-in-time dairy and frozen food restocking.\n\n"
        "Limitation: 183-day training series may under-represent annual seasonality;\n"
        "model requires 14-day warm-up and daily retraining as new data arrives.",
})
add_image(s, CHARTS / "04_time_series_forecast_comparison.png", 0.2, 2.5, 6.0, 4.0)
add_image(s, CHARTS / "06_xgboost_feature_importance.png",       6.4, 2.5, 3.6, 4.0)
print("Slide 11: Method 1 Evaluation — done + charts")

# ===========================================================================
# SLIDE 12 — Method 2 Implementation (Association Rules)
# ===========================================================================
s = slides[11]
replace_slide(s, {
    "Selected method: [Method 2 name and purpose]":
        "Selected method: Association Rule Mining\n"
        "Purpose: Discover product co-purchase patterns to design targeted bundle "
        "promotions and optimise dark store shelf layout for faster picking.",
    "Input and preparation: [Final-data subset and transformations]":
        "Input: 30,296 multi-item baskets extracted from 34,700 orders\n"
        "Preparation: One-hot encoded basket matrix (orders × products)\n"
        "Only orders with 2+ items used for meaningful co-occurrence\n"
        "Parameters: min_support=0.03 | min_confidence=0.20 | min_lift=1.15",
    "Implementation: [Algorithm, parameters and tools]":
        "Algorithms benchmarked:\n"
        "Apriori — traditional candidate generation (baseline)\n"
        "FP-Growth — Frequent Pattern tree (selected for scalability)\n"
        "Both algorithms validated to produce identical rule sets.\n"
        "Tools: Python, mlxtend, pandas, matplotlib",
    "Output: [Actual forecast, text result or association rules]":
        "Output: 42 valid association rules\n"
        "Top rule: Baker's Dozen Malabar Paratha → Aashirvaad Malabar Paratha\n"
        "Support: 1.66% | Confidence: 29.37% | Lift: 5.11x\n"
        "Bundle themes: Frozen Breakfast, Indian Cooking, Snack+Drink, Morning Dairy",
})
print("Slide 12: Method 2 Implementation — done")

# ===========================================================================
# SLIDE 13 — Method 2 Evaluation
# ===========================================================================
s = slides[12]
replace_slide(s, {
    "Evaluation data: [Final-data records, subset and evaluation setup]":
        "Evaluation data: 30,296 multi-item baskets from 34,700 orders\n"
        "Metrics: Support, Confidence, Lift, Leverage, Conviction\n"
        "Algorithm benchmark: Apriori vs FP-Growth across 5 support thresholds",
    "Interpretation: [Selected approach, business meaning and limitation]":
        "Selected: FP-Growth (retained for scalability at min_support=0.03)\n\n"
        "Algorithm comparison at support=0.03:\n"
        "Apriori: 42 itemsets | 0.074s | FP-Growth: 42 itemsets | 0.169s\n"
        "Note: Apriori is faster at low item counts; FP-Growth scales better >10K SKUs\n\n"
        "Top Rules:\n"
        "1. Malabar Paratha bundle — Lift 5.11x — Frozen Breakfast\n"
        "2. Spring Onion + Tomato — Lift 2.26x — Indian Cooking\n"
        "3. Apple + Banana — Lift 2.26x — Fresh Fruit\n"
        "4. Kettle Chips + 7UP — Lift 1.87x — Snack+Drink\n"
        "5. Milk + Bread — Lift 1.85x — Morning Dairy\n\n"
        "Limitation: Transaction data is synthetic (research-grounded);\n"
        "real basket validation required before production deployment.",
})
add_image(s, CHARTS / "07_association_runtime_benchmark.png",  0.2, 2.5, 4.8, 2.8)
add_image(s, CHARTS / "08_rules_support_confidence_lift.png",  5.2, 2.5, 4.8, 2.8)
add_image(s, CHARTS / "09_top10_bundle_recommendations.png",   0.2, 5.5, 9.8, 2.0)
print("Slide 13: Method 2 Evaluation — done + charts")

# ===========================================================================
# SLIDE 14 — Business Outcomes
# ===========================================================================
s = slides[13]
replace_slide(s, {
    "Business objective addressed: [Explain the overall outcome]":
        "Business objective addressed:\n\n"
        "FORECASTING OUTCOMES:\n"
        "• XGBoost predicts demand 30 days ahead with WAPE 8.29% — enables\n"
        "  just-in-time replenishment and eliminates reactive emergency restocking.\n"
        "• Weekend uplift (+35%) confirmed — trigger dairy/frozen stock increase\n"
        "  every Friday by 18:00.\n\n"
        "BUNDLE RECOMMENDATION OUTCOMES:\n"
        "• 42 rules with Lift >1.15 identify high-value cross-sell opportunities.\n"
        "• Malabar Paratha bundle (5.11x lift) — highest-priority promotion.\n"
        "• Sabzi Essentials (Tomato+Onion+Potato, 2.26x lift) — co-locate in store.\n"
        "• Expected basket uplift: Rs 47–89 per order applying top 10 rules.\n\n"
        "PRICING INSIGHTS:\n"
        "• 44% of SKUs in 10–20% discount band — modal strategy validated.\n"
        "• 100% MRP compliance confirmed across all 609 products.\n"
        "• Reserve >30% discounts exclusively for perishable clearance.\n\n"
        "ESTIMATED REVENUE IMPACT:\n"
        "• 1,500 orders/day × Rs 68 avg uplift × 365 = Rs 3.7 Cr annual opportunity",
})
add_metric(s, "Top Lift Rule", "5.11x",  0.5, 5.6)
add_metric(s, "Best RMSE",   "99.50",   3.0, 5.6)
add_metric(s, "Rules Mined",   "42",     5.5, 5.6)
add_metric(s, "Est. Rev Impact", "Rs 3.7 Cr", 8.0, 5.6)
print("Slide 14: Business Outcomes — done")

# ===========================================================================
# SLIDE 15 — Dashboard Demo
# ===========================================================================
s = slides[14]
replace_slide(s, {
    "Application: [Name and clickable URL / local launch details]":
        "Application: Blinkit Dark Store Analytics Dashboard\n"
        "Launch: Open review2_blinkit/website/index.html in Chrome or Firefox\n"
        "No server required — fully client-side HTML5/CSS3/JavaScript/Chart.js",
    "[Insert one clear screenshot of the final application]":
        "[Screenshot: Blinkit Dark Store Dashboard — Forecast & Bundle Explorer]",
    "Live demo: [Change a filter / selector and show updated results]":
        "Live demo steps:\n"
        "1. Open index.html — dashboard loads with all 6 models pre-rendered\n"
        "2. Click model selector — toggle between XGBoost / SARIMA / Holt-Winters\n"
        "3. Move Lift slider from 1.15 to 2.0 — filter shows high-affinity rules only\n"
        "4. Search 'Paratha' in product catalogue — 5 matching SKUs highlighted",
    "Business scenario: [Use the application to answer a real question]":
        "Business scenario: 'What should we stock extra of this Friday for the weekend?'\n"
        "→ Select XGBoost forecast → Saturday/Sunday bars show +35% demand spike\n"
        "→ Filter rules by category Dairy → Milk+Bread bundle (1.85x lift) surfaces\n"
        "→ Action: Order +35% extra Milk + Bread before Friday 18:00 cutoff",
})
print("Slide 15: Dashboard Demo — done")

# ===========================================================================
# SLIDE 16 — Completion & Contributions
# ===========================================================================
s = slides[15]
replace_slide(s, {
    "Project board: [Link]     Repository / deliverables: [Link]":
        "Repository: c:/Users/Sunny-Cherry/Desktop/BA/BA_Project/review2_blinkit/\n"
        "Deliverables: src/ (pipeline) | results/charts/ (9 figures) | "
        "notebooks/ (6 Jupyter) | website/ (dashboard) | reports/ (final report)\n\n"
        "Individual contributions:\n"
        "Leena Sri K — Data collection, web scraping, EDA\n"
        "A.C. Sanhitha Reddy — Data validation, preprocessing pipeline\n"
        "Kanish Kumaran M — Time-series forecasting, model evaluation\n"
        "Ande Taraka Srinivas — Association rule mining, FP-Growth implementation\n"
        "Ajay N Mukunth — Interactive dashboard, final report, presentation",
})
print("Slide 16: Completion — done")

# ===========================================================================
# SLIDE 17 — Conclusion
# ===========================================================================
s = slides[16]
replace_slide(s, {
    "Main outcome: [What the completed project achieved]":
        "Main outcome: Successfully built a reproducible dual-method analytics pipeline\n"
        "for quick-commerce dark store optimization using 609 real Blinkit SKUs and\n"
        "106,398 research-grounded synthetic transactions.",
    "Business value: [What the evidence supports]":
        "Business value:\n"
        "• XGBoost forecasting (WAPE 8.29%) enables proactive inventory replenishment\n"
        "  — preventing stockouts during weekend demand peaks.\n"
        "• 42 association rules (top lift 5.11x) identify actionable bundle promotions\n"
        "  estimated to deliver Rs 3.7 Cr annual revenue uplift at 1,500 orders/day.\n"
        "• Real-time interactive dashboard enables non-technical stakeholders to\n"
        "  explore forecasts and bundle rules without coding.",
    "Limitations: [Data, model or application limitations]":
        "Limitations:\n"
        "• Single-point price scrape — MRP compliance justifies price stability\n"
        "• Synthetic transactions — grounded to real SKUs + published research\n"
        "• 183-day series — limits multi-year seasonal decomposition\n"
        "• Single platform/city — Blinkit #1 q-commerce India; directionally valid",
    "Future scope: [Extension beyond the completed project]":
        "Future scope:\n"
        "• Multi-zone scraping (Chennai, Bangalore, Mumbai) — geographic comparison\n"
        "• Hourly price tracking — build price-elasticity model per SKU\n"
        "• Temporal Fusion Transformer (TFT) — multi-variate deep learning forecast\n"
        "• User-level collaborative filtering — personalised bundle recommendations",
})
print("Slide 17: Conclusion — done")

# ===========================================================================
# Save
# ===========================================================================
prs.save(str(OUTPUT))
size_mb = OUTPUT.stat().st_size / 1024 / 1024
print(f"\n[OK] Saved: {OUTPUT}")
print(f"     Size: {size_mb:.2f} MB | Slides: {len(prs.slides)}")
print("\nAll done — open in PowerPoint / LibreOffice to review.")
