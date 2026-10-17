"""
Multi-Metric Basket Affinity & Cross-Category Correlation Engine
================================================================

Course: 23CSE452 - Business Analytics Capstone Project
Component: Review 2 Unit 3 Method 2 Preparation
Author: Ande Taraka Srinivas (CB.SC.U4CSE23212)

This module provides advanced null-invariant co-occurrence metrics for quick-commerce
baskets. While standard support-confidence can be heavily skewed by ultra-frequent SKUs
(such as Milk or Curd), null-invariant measures (Kulczynski and Cosine) provide
unbiased cross-selling signals.

Metrics Implemented:
1. Support, Confidence, and Lift.
2. Kulczynski measure: Kulc(A, B) = 0.5 * (P(A|B) + P(B|A)).
3. Imbalance Ratio (IR) to assess basket asymmetry.
4. Cosine similarity for transaction vectors.
5. Cross-category transition affinity matrix.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Set, Any
import math
import json
import os


class BasketAffinityAnalyzer:
    """
    Evaluates multi-item transaction records and computes null-invariant association metrics.
    """
    
    def __init__(self, min_support: float = 0.015, min_lift: float = 1.15):
        self.min_support = min_support
        self.min_lift = min_lift

    def compute_null_invariant_metrics(
        self,
        supp_a: float,
        supp_b: float,
        supp_ab: float
    ) -> Dict[str, float]:
        """
        Computes Lift, Kulczynski, Imbalance Ratio (IR), and Cosine similarity.
        """
        conf_a_to_b = (supp_ab / supp_a) if supp_a > 0 else 0.0
        conf_b_to_a = (supp_ab / supp_b) if supp_b > 0 else 0.0
        
        expected_joint = supp_a * supp_b
        lift = (supp_ab / expected_joint) if expected_joint > 0 else 0.0
        
        # Kulczynski measure (average conditional probability)
        kulc = 0.5 * (conf_a_to_b + conf_b_to_a)
        
        # Imbalance Ratio: |supp(A) - supp(B)| / (supp(A) + supp(B) - supp(AB))
        union_supp = supp_a + supp_b - supp_ab
        ir = (abs(supp_a - supp_b) / union_supp) if union_supp > 0 else 0.0
        
        # Cosine similarity
        cosine = (supp_ab / math.sqrt(supp_a * supp_b)) if (supp_a > 0 and supp_b > 0) else 0.0
        
        return {
            "confidence_A_to_B": round(conf_a_to_b, 4),
            "confidence_B_to_A": round(conf_b_to_a, 4),
            "lift": round(lift, 3),
            "kulczynski": round(kulc, 4),
            "imbalance_ratio": round(ir, 4),
            "cosine_similarity": round(cosine, 4)
        }

    def evaluate_bundle_economics(
        self,
        item_a_price: float,
        item_a_margin_pct: float,
        item_b_price: float,
        item_b_margin_pct: float,
        bundle_discount_pct: float = 0.08,
        incremental_lift_pct: float = 0.25
    ) -> Dict[str, float]:
        """
        Models the profit feasibility of promoting product bundles.
        """
        individual_total_rev = item_a_price + item_b_price
        individual_gross_profit = (item_a_price * item_a_margin_pct) + (item_b_price * item_b_margin_pct)
        
        bundle_price = individual_total_rev * (1.0 - bundle_discount_pct)
        bundle_gross_profit = bundle_price - (
            item_a_price * (1.0 - item_a_margin_pct) + item_b_price * (1.0 - item_b_margin_pct)
        )
        
        # Incremental gross margin contribution under sales lift
        net_profit_delta = (bundle_gross_profit * (1.0 + incremental_lift_pct)) - individual_gross_profit
        
        return {
            "individual_revenue": round(individual_total_rev, 2),
            "bundle_price": round(bundle_price, 2),
            "bundle_discount_pct": round(bundle_discount_pct * 100.0, 1),
            "individual_margin_pct": round((individual_gross_profit / individual_total_rev) * 100.0, 2),
            "bundle_margin_pct": round((bundle_gross_profit / bundle_price) * 100.0, 2),
            "net_profit_delta_per_bundle": round(net_profit_delta, 2),
            "is_economically_viable": net_profit_delta > 0
        }


if __name__ == "__main__":
    print("Testing BasketAffinityAnalyzer...")
    analyzer = BasketAffinityAnalyzer()
    
    # Milk + Bread test case
    metrics = analyzer.compute_null_invariant_metrics(supp_a=0.18, supp_b=0.12, supp_ab=0.065)
    print("Milk + Bread Metrics:", json.dumps(metrics, indent=2))
    
    # Bundle economics test
    econ = analyzer.evaluate_bundle_economics(
        item_a_price=65.0, item_a_margin_pct=0.12,  # Milk
        item_b_price=45.0, item_b_margin_pct=0.22,  # Bread
        bundle_discount_pct=0.08
    )
    print("Bundle Economics:", json.dumps(econ, indent=2))
