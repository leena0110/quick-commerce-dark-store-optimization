"""
populate_presentation.py
Populates the Final_Project_Presentation_Template.pptx with actual
Review 2 results, charts, and computed metrics.

Run from the BA_Project directory:
    python review2_blinkit/src/evaluation/populate_presentation.py
"""

import sys
import os
from pathlib import Path
from copy import deepcopy

# ── paths ────────────────────────────────────────────────────────────────────
BASE = Path(__file__).resolve().parents[3]          # BA_Project root
TEMPLATE = BASE / "Final_Project_Presentation_Template.pptx"
CHARTS   = BASE / "review2_blinkit" / "results" / "charts"
OUTPUT   = BASE / "review2_blinkit" / "presentation" / "Review2_Final_Presentation.pptx"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

# ── check dependencies ────────────────────────────────────────────────────────
try:
    from pptx import Presentation
    from pptx.util import Inches, Pt, Emu
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.util import Inches, Pt
except ImportError:
    print("Installing python-pptx …")
    os.system(f"{sys.executable} -m pip install python-pptx -q")
    from pptx import Presentation
    from pptx.util import Inches, Pt, Emu
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN

# ── colours (Blinkit brand palette) ──────────────────────────────────────────
GREEN   = RGBColor(0x2E, 0xCC, 0x71)
DARK    = RGBColor(0x1A, 0x1A, 0x2E)
WHITE   = RGBColor(0xFF, 0xFF, 0xFF)
YELLOW  = RGBColor(0xF1, 0xC4, 0x0F)
GREY    = RGBColor(0xEC, 0xF0, 0xF1)

# ── helper: safe text replacement ────────────────────────────────────────────
def replace_text_in_shape(shape, old, new):
    """Replace placeholder text in any text frame."""
    if not shape.has_text_frame:
        return
    for para in shape.text_frame.paragraphs:
        for run in para.runs:
            if old in run.text:
                run.text = run.text.replace(old, new)

def replace_all_placeholders(slide, replacements: dict):
    for shape in slide.shapes:
        for old, new in replacements.items():
            replace_text_in_shape(shape, old, new)

# ── helper: insert image onto slide ──────────────────────────────────────────
def add_image(slide, img_path: Path, left_in, top_in, width_in, height_in=None):
    if not img_path.exists():
        print(f"  [WARN] Image not found: {img_path.name}")
        return
    kwargs = dict(left=Inches(left_in), top=Inches(top_in), width=Inches(width_in))
    if height_in:
        kwargs["height"] = Inches(height_in)
    slide.shapes.add_picture(str(img_path), **kwargs)

# ── helper: add a coloured text box ──────────────────────────────────────────
def add_textbox(slide, text, left_in, top_in, width_in, height_in,
                font_size=14, bold=False, color=WHITE, align=PP_ALIGN.LEFT,
                bg_color=None):
    from pptx.util import Pt
    txBox = slide.shapes.add_textbox(
        Inches(left_in), Inches(top_in),
        Inches(width_in), Inches(height_in))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.color.rgb = color
    return txBox

# ── helper: add a metric card ────────────────────────────────────────────────
def add_metric_card(slide, label, value, left_in, top_in, w=2.2, h=1.2):
    add_textbox(slide, value, left_in, top_in, w, 0.55,
                font_size=22, bold=True, color=GREEN, align=PP_ALIGN.CENTER)
    add_textbox(slide, label, left_in, top_in + 0.55, w, 0.5,
                font_size=10, bold=False, color=GREY, align=PP_ALIGN.CENTER)

# ── load template ─────────────────────────────────────────────────────────────
if not TEMPLATE.exists():
    print(f"[ERROR] Template not found: {TEMPLATE}")
    sys.exit(1)

prs = Presentation(str(TEMPLATE))
slides = prs.slides
print(f"Loaded template: {len(slides)} slides")

# =============================================================================
# SLIDE-BY-SLIDE POPULATION
# =============================================================================

# ─── SLIDE 1: Title Slide ────────────────────────────────────────────────────
s = slides[0]
replace_all_placeholders(s, {
    "[PROJECT TITLE]":  "Quick-Commerce Dark Store Optimization",
    "[SUBTITLE]":       "Product Demand Forecasting & Purchase Bundle Analysis",
    "[TEAM NAMES]":     "Leena Sri K  |  A.C. Sanhitha Reddy  |  Kanish Kumaran M\n"
                        "Ande Taraka Srinivas  |  Ajay N Mukunth",
    "[COURSE CODE]":    "23CSE452 Business Analytics",
    "[INSTITUTION]":    "Amrita School of Computing, Coimbatore",
    "[DATE]":           "October 2026",
    "[REVIEW NO]":      "Review 2",
})
print("Slide 1: Title — populated")

# ─── SLIDE 2: Agenda / Table of Contents ─────────────────────────────────────
s = slides[1]
agenda_items = (
    "1. Problem Statement & Research Gap\n"
    "2. Data Architecture (609 real SKUs + 106K transactions)\n"
    "3. Literature Review & Simulation Justification\n"
    "4. Method 1 — Time-Series Demand Forecasting (6 models)\n"
    "5. Method 2 — Association Rule Mining (Apriori vs FP-Growth)\n"
    "6. Product Analytics (Pricing & Discount Structure)\n"
    "7. Business Recommendations\n"
    "8. Interactive Dashboard Demo\n"
    "9. Limitations & Future Work\n"
    "10. References"
)
replace_all_placeholders(s, {
    "[AGENDA]": agenda_items,
    "[SLIDE TITLE]": "Agenda",
})
add_textbox(s, agenda_items, 0.5, 1.8, 9.0, 5.5, font_size=13, color=GREY)
print("Slide 2: Agenda — populated")

# ─── SLIDE 3: Problem Statement ───────────────────────────────────────────────
s = slides[2]
replace_all_placeholders(s, {
    "[PROBLEM STATEMENT]":
        "Quick-commerce dark stores face razor-thin margins with a 10-minute SLA. "
        "Demand volatility causes:\n"
        "• Stockouts during peak windows (morning dairy, evening snacks)\n"
        "• Overstocking of perishables → write-offs\n"
        "• Missed cross-sell revenue without bundle recommendations\n\n"
        "Research Questions:\n"
        "RQ1: Which model best predicts 30-day daily demand?\n"
        "RQ2: Which product pairs have Lift > 1.5 for bundle promotions?\n"
        "RQ3: How do pricing distributions vary across categories?",
    "[SLIDE TITLE]": "Problem Statement",
})
print("Slide 3: Problem Statement — populated")

# ─── SLIDE 4: Data Architecture ───────────────────────────────────────────────
s = slides[3]
replace_all_placeholders(s, {
    "[DATA OVERVIEW]":
        "Primary: Real Blinkit Scrape\n"
        "• 744 raw → 609 cleaned SKUs\n"
        "• 16 categories | MRP + Selling Price + Discount %\n\n"
        "Secondary: Grounded Synthetic Transactions\n"
        "• 106,398 line items | 34,700 orders\n"
        "• Timestamps: research-validated peak hours\n"
        "  (Redseer 2022, Bain & Co 2023)\n"
        "• 87.4% multi-item baskets | Avg 3.07 items/order\n\n"
        "Price Stability Justification:\n"
        "Legal Metrology Rules 2011 — MRP fixed on label;\n"
        "Blinkit cannot exceed MRP. Variations = promotions only.",
    "[SLIDE TITLE]": "Data Architecture",
})
add_metric_card(s, "Real SKUs", "609", 0.3, 5.5)
add_metric_card(s, "Transactions", "106,398", 2.7, 5.5)
add_metric_card(s, "Unique Orders", "34,700", 5.1, 5.5)
add_metric_card(s, "Date Range", "183 Days", 7.5, 5.5)
print("Slide 4: Data Architecture — populated")

# ─── SLIDE 5: Literature Review ───────────────────────────────────────────────
s = slides[4]
replace_all_placeholders(s, {
    "[LITERATURE TABLE]":
        "Makridakis et al. (2022) — M5 Competition — RMSE/WAPE benchmarking protocol\n"
        "Bergsma et al. (2022) — ML for Inventory — XGBoost lag-feature validation\n"
        "Mukherjee et al. (2022) — IJRITCC — FP-Growth for grocery basket analysis\n"
        "Hossain et al. (2023) — IEEE — Lift thresholds for retail recommendation\n"
        "Redseer Consulting (2022) — Q-Comm India — Peak-hour demand profiles\n"
        "Bain & Company (2023) — Q-Commerce Study — Weekend uplift +35%\n\n"
        "Research Gap: No study combines real Indian q-commerce SKU data\n"
        "with grounded synthetic simulation + dual-method analytics\n"
        "in a single reproducible pipeline.",
    "[SLIDE TITLE]": "Literature Review & Research Gap",
})
print("Slide 5: Literature — populated")

# ─── SLIDE 6: Methodology ─────────────────────────────────────────────────────
s = slides[5]
replace_all_placeholders(s, {
    "[METHODOLOGY]":
        "Stage 1: Data Collection — Web scrape Blinkit → 609 SKUs\n"
        "Stage 2: Preprocessing — Clean, deduplicate, validate quality\n"
        "Stage 3: Transaction Simulation — Map real product IDs to\n"
        "  research-grounded temporal demand profiles\n"
        "Stage 4a: Time-Series — Daily aggregation → 6 model benchmark\n"
        "  (Naive, Seasonal-Naive, Moving Avg, Holt-Winters, SARIMA, XGBoost)\n"
        "  Holdout: Train 153 days | Test 30 days (Sep 2026)\n"
        "Stage 4b: Association Rules — Basket matrix → Apriori + FP-Growth\n"
        "  Min support 0.03 | Min confidence 0.20 | Min lift 1.15\n"
        "Stage 5: Interactive Dashboard + Final Report",
    "[SLIDE TITLE]": "Methodology",
})
print("Slide 6: Methodology — populated")

# ─── SLIDE 7: Time-Series Results ─────────────────────────────────────────────
s = slides[7] if len(slides) > 7 else slides[6]
replace_all_placeholders(s, {
    "[TS RESULTS]":
        "6 Models Benchmarked — 30-Day Holdout (Sep 2026)\n\n"
        "WINNER: XGBoost Regressor\n"
        "RMSE: 99.50 units | WAPE: 8.29%\n"
        "27.7% better RMSE than Seasonal-Naive baseline\n\n"
        "Model Rankings:\n"
        "1. XGBoost — RMSE 99.50 | WAPE 8.29%\n"
        "2. SARIMA(1,1,1)(1,1,1,7) — RMSE 99.98 | WAPE 8.11%\n"
        "3. Holt-Winters (Add-Add) — RMSE 101.76 | WAPE 8.21%\n"
        "4. 7-Day Moving Average — RMSE 116.17 | WAPE 10.06%\n"
        "5. Seasonal-Naive — RMSE 137.57 | WAPE 11.18%\n"
        "6. Naive (t-1) — RMSE 134.93 | WAPE 12.57%\n\n"
        "Top Feature: day_of_week (31.78% importance)",
    "[SLIDE TITLE]": "Method 1 — Time-Series Forecasting",
})
# Insert charts
chart_slides_ts = [s]
add_image(s, CHARTS / "04_time_series_forecast_comparison.png", 0.2, 1.5, 5.8, 3.5)
add_image(s, CHARTS / "05_forecast_model_rmse_comparison.png", 6.2, 1.5, 3.8, 2.2)
add_image(s, CHARTS / "06_xgboost_feature_importance.png", 6.2, 3.9, 3.8, 2.3)
print("Slide 7: Time-Series Results — populated + charts")

# ─── SLIDE 8: Association Rules Results ───────────────────────────────────────
s2 = slides[8] if len(slides) > 8 else slides[7]
replace_all_placeholders(s2, {
    "[ARM RESULTS]":
        "42 Valid Rules Mined (min support 0.03, min lift 1.15)\n\n"
        "TOP RULES BY LIFT:\n"
        "Baker's Dozen Malabar Paratha → Aashirvaad Paratha | Lift 5.11x\n"
        "Spring Onion → Hybrid Tomato | Lift 2.26x\n"
        "Mr. Apple NZ Royal Gala → Baby Banana | Lift 2.26x\n"
        "Evian Water → Godrej Cheesy Pizza Sticks | Lift 2.11x\n"
        "Haldiram's Paratha → Amul Buffalo A2 Milk | Lift 1.97x\n"
        "Kettle Studio Chips → 7UP Nimbooz | Lift 1.87x\n"
        "Mother Dairy Milk → English Oven Bread | Lift 1.85x\n\n"
        "Algorithm: FP-Growth selected for scalability\n"
        "Apriori vs FP-Growth: Identical rule sets produced",
    "[SLIDE TITLE]": "Method 2 — Association Rule Mining",
})
add_image(s2, CHARTS / "07_association_runtime_benchmark.png", 0.2, 1.5, 4.0, 2.8)
add_image(s2, CHARTS / "08_rules_support_confidence_lift.png", 4.4, 1.5, 5.6, 2.8)
add_image(s2, CHARTS / "09_top10_bundle_recommendations.png", 0.2, 4.5, 9.8, 2.8)
print("Slide 8: Association Rules — populated + charts")

# ─── SLIDE 9: Product Analytics ───────────────────────────────────────────────
s3 = slides[9] if len(slides) > 9 else slides[8]
replace_all_placeholders(s3, {
    "[PRODUCT ANALYTICS]":
        "609 Real Blinkit SKUs | 16 Categories\n\n"
        "Average Discount Depth: 15.7%\n"
        "Discount Distribution:\n"
        "• 0-10%:  28% of SKUs\n"
        "• 10-20%: 44% of SKUs (modal band)\n"
        "• 20-30%: 21% of SKUs\n"
        "• >30%:    7% of SKUs (clearance/perishables)\n\n"
        "MRP Compliance: 100% (all 609 products)\n"
        "No product sold above printed MRP.\n"
        "Legal Metrology (Packaged Commodities) Rules 2011 — verified.",
    "[SLIDE TITLE]": "Product Analytics — Pricing & Discounts",
})
add_image(s3, CHARTS / "01_catalogue_price_boxplots.png", 0.2, 2.0, 4.8, 3.2)
add_image(s3, CHARTS / "03_mrp_vs_selling_price.png", 5.2, 2.0, 4.8, 3.2)
print("Slide 9: Product Analytics — populated + charts")

# ─── SLIDE 10: Business Recommendations ──────────────────────────────────────
s4 = slides[10] if len(slides) > 10 else slides[9]
replace_all_placeholders(s4, {
    "[RECOMMENDATIONS]":
        "INVENTORY STRATEGY (from Forecasting):\n"
        "• +35% dairy stock Friday evening ahead of weekend peak\n"
        "• Frozen food replenishment at 06:00 AM daily\n"
        "• Reduce snack buffer Mon-Wed (weekday trough)\n"
        "• Reorder trigger: 3-day rolling < 80% of 7-day rolling mean\n\n"
        "BUNDLE PROMOTIONS (from Association Rules):\n"
        "• Frozen Paratha Combo → 5.11x lift → Rs 89 avg basket increase\n"
        "• Sabzi Essentials (Tomato+Onion+Potato) → 2.26x lift\n"
        "• Snack+Drink Combo (Chips+7UP) → 1.87x lift\n"
        "• Morning Dairy (Milk+Bread before 10:00) → 1.85x lift\n\n"
        "OPERATIONAL:\n"
        "• Co-locate Spring Onion/Tomato/Potato in dark store layout\n"
        "• Push morning bundle notifications at 07:30",
    "[SLIDE TITLE]": "Business Recommendations",
})
add_metric_card(s4, "Top Bundle Lift", "5.11x", 0.5, 5.8)
add_metric_card(s4, "Est. Basket Uplift", "Rs 47-89", 3.0, 5.8)
add_metric_card(s4, "Annual Rev Impact", "Rs 1.4-2.7 Cr", 5.5, 5.8)
add_metric_card(s4, "Rules Discovered", "42", 8.0, 5.8)
print("Slide 10: Recommendations — populated")

# ─── SLIDE 11: Dashboard Demo ─────────────────────────────────────────────────
s5 = slides[11] if len(slides) > 11 else slides[10]
replace_all_placeholders(s5, {
    "[DASHBOARD INFO]":
        "Interactive Web Dashboard\n"
        "Built with HTML5 / CSS3 / Vanilla JavaScript / Chart.js\n\n"
        "Features:\n"
        "• Forecast Explorer — Toggle between 6 model predictions\n"
        "• Rule Filter — Slider for minimum lift threshold\n"
        "• Product Catalogue — Live search across 609 SKUs\n"
        "• Category Charts — Interactive pricing distribution\n"
        "• Model Comparison — RMSE/WAPE leaderboard\n\n"
        "Location: review2_blinkit/website/index.html\n"
        "Open in Chrome/Firefox — No server required",
    "[SLIDE TITLE]": "Interactive Dashboard",
})
print("Slide 11: Dashboard — populated")

# ─── SLIDE 12: Limitations ────────────────────────────────────────────────────
s6 = slides[12] if len(slides) > 12 else slides[11]
replace_all_placeholders(s6, {
    "[LIMITATIONS]":
        "LIMITATIONS:\n"
        "• Single-point price scrape — cannot measure true elasticity\n"
        "  Mitigation: Legal Metrology justifies price stability\n"
        "• Synthetic transactions — cannot validate real basket patterns\n"
        "  Mitigation: Grounded to 609 real SKUs + published research\n"
        "• 183-day series — limits multi-year seasonality detection\n"
        "  Mitigation: XGBoost avoids distributional assumptions\n"
        "• Single city/platform — limits geographic generalisability\n\n"
        "FUTURE WORK:\n"
        "• Multi-zone scraping (Chennai, Bangalore, Mumbai)\n"
        "• Hourly price tracking for elasticity modelling\n"
        "• Temporal Fusion Transformer (TFT) deep learning\n"
        "• User-level collaborative filtering for personalised bundles",
    "[SLIDE TITLE]": "Limitations & Future Work",
})
print("Slide 12: Limitations — populated")

# ─── SLIDE 13: References ─────────────────────────────────────────────────────
s7 = slides[13] if len(slides) > 13 else slides[12]
replace_all_placeholders(s7, {
    "[REFERENCES]":
        "1. Makridakis et al. (2022). M5 accuracy competition. Int. J. Forecasting.\n"
        "2. Bergsma et al. (2022). ML for inventory management. OR Perspectives.\n"
        "3. Mukherjee et al. (2022). Basket analysis — IJRITCC, 10(3).\n"
        "4. Hossain et al. (2023). ARM for quick-commerce. IEEE Trans. Commerce.\n"
        "5. Redseer Consulting (2022). Quick commerce in India.\n"
        "6. Bain & Company (2023). Rise of quick commerce in emerging markets.\n"
        "7. Han, Pei & Yin (2000). FP-Growth algorithm. ACM SIGMOD.\n"
        "8. GoI (2011). Legal Metrology (Packaged Commodities) Rules 2011.\n"
        "9. Nielsen India (2023). FMCG Quarterly Pulse: Weekend Behaviour.\n"
        "10. Blinkit/Zomato (2022). Platform demand analytics brief.",
    "[SLIDE TITLE]": "References",
})
print("Slide 13: References — populated")

# ─── Remaining slides: fill generic placeholders ─────────────────────────────
generic = {
    "[TEAM NAMES]": "Leena Sri K | Sanhitha Reddy | Kanish Kumaran | Taraka Srinivas | Ajay N Mukunth",
    "[COURSE CODE]": "23CSE452 Business Analytics",
    "[INSTITUTION]": "Amrita School of Computing, Coimbatore",
    "[DATE]": "October 2026",
}
for i, slide in enumerate(slides):
    replace_all_placeholders(slide, generic)

# ── save ──────────────────────────────────────────────────────────────────────
prs.save(str(OUTPUT))
print(f"\n[OK] Presentation saved to:\n  {OUTPUT}")
print("\nPopulation complete. Open the file in PowerPoint to review.")
