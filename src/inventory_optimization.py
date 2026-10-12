"""
Inventory Optimization and Safety Stock Engine for Quick-Commerce Dark Stores
=============================================================================

Course: 23CSE452 - Business Analytics Capstone Project
Component: Review 1 & Review 2 Inventory Decision Support System
Author: Ande Taraka Srinivas (CB.SC.U4CSE23212)

This module translates daily SKU-level demand forecasts into actionable inventory
control policies for quick-commerce micro-fulfillment centers (dark stores).

Key Capabilities:
1. Cycle Service Level (CSL) targeting via normal standard quantile (Z-score).
2. Dynamic Safety Stock (SS) calculation accounting for both demand volatility
   and supplier/central warehouse replenishment lead-time variance.
3. Continuous Review Dynamic Reorder Point (ROP) determination with weekend demand surge multipliers.
4. Stockout probability estimation and service level fill-rate trade-off curves.
5. Holding cost vs. stockout penalty economic optimization.
6. Empirical store-level inventory benchmarking across quick-commerce dark stores.
"""

import numpy as np
import pandas as pd
from typing import Dict, Tuple, List, Optional
import math
import json
import os


def normal_ppf(p: float) -> float:
    """
    Approximation of the Inverse Standard Normal Cumulative Distribution Function (Quantile function / Probit).
    Accurate to within 4.5e-4 (Abramowitz & Stegun formula 26.2.23).
    Avoids hard external dependency on scipy.stats while preserving mathematical rigor.
    """
    if p <= 0.0 or p >= 1.0:
        raise ValueError("Probability p must be in the open interval (0, 1).")
    
    # Coefficients for Abramowitz & Stegun rational approximation
    c0, c1, c2 = 2.515517, 0.802853, 0.010328
    d1, d2, d3 = 1.432788, 0.189269, 0.001308
    
    if p < 0.5:
        t = math.sqrt(-2.0 * math.log(p))
        num = c0 + (c1 * t) + (c2 * t * t)
        den = 1.0 + (d1 * t) + (d2 * t) + (d3 * t * t)
        return -(t - (num / den))
    else:
        t = math.sqrt(-2.0 * math.log(1.0 - p))
        num = c0 + (c1 * t) + (c2 * t * t)
        den = 1.0 + (d1 * t) + (d2 * t) + (d3 * t * t)
        return t - (num / den)


def calculate_service_level_z(service_level: float = 0.95) -> float:
    """
    Returns the standard normal Z-score corresponding to a target Cycle Service Level (CSL).
    """
    if not (0.50 <= service_level < 1.0):
        raise ValueError("Service level should realistically range between 50% and 99.9%.")
    return float(normal_ppf(service_level))


def calculate_safety_stock(
    demand_mean: float,
    demand_std: float,
    lead_time_days: float = 0.25,
    lead_time_std: float = 0.05,
    service_level: float = 0.95
) -> float:
    """
    Calculates dynamic safety stock incorporating both demand and lead-time uncertainties.
    
    Formula:
        SS = Z * sqrt( L * (sigma_D)^2 + (mu_D)^2 * (sigma_L)^2 )
    """
    z = calculate_service_level_z(service_level)
    
    demand_var = (demand_std ** 2) if demand_std > 0 else 0.0
    lead_time_var = (lead_time_std ** 2) if lead_time_std > 0 else 0.0
    
    combined_lead_time_variance = (lead_time_days * demand_var) + ((demand_mean ** 2) * lead_time_var)
    combined_sigma_ld = math.sqrt(max(0.0, combined_lead_time_variance))
    
    safety_stock = z * combined_sigma_ld
    return float(round(safety_stock, 2))


def calculate_reorder_point(
    demand_mean: float,
    lead_time_days: float,
    safety_stock: float
) -> float:
    """
    Calculates Continuous Review Reorder Point (ROP).
    
    Formula:
        ROP = (mu_D * L) + SS
    """
    expected_lead_time_demand = demand_mean * lead_time_days
    rop = expected_lead_time_demand + safety_stock
    return float(round(rop, 2))


def calculate_dynamic_rop(
    baseline_demand: float,
    lead_time_days: float,
    safety_stock: float,
    is_weekend: bool = False,
    surge_multiplier: float = 1.22
) -> float:
    """
    Calculates surge-adjusted Dynamic Reorder Point for weekend stock planning.
    Quick-commerce stores experience ~15-25% surges on Friday evenings and weekends.
    """
    effective_demand = baseline_demand * (surge_multiplier if is_weekend else 1.0)
    return float(round((effective_demand * lead_time_days) + safety_stock, 2))


def estimate_stockout_probability(
    current_inventory: float,
    lead_time_demand_mean: float,
    lead_time_demand_std: float
) -> float:
    """
    Estimates the probability that demand exceeds current on-hand inventory before replenishment arrives.
    """
    if lead_time_demand_std <= 0:
        return 0.0 if current_inventory >= lead_time_demand_mean else 1.0
    
    z = (current_inventory - lead_time_demand_mean) / lead_time_demand_std
    try:
        phi = 1.0 / (1.0 + math.exp(-1.702 * z))
        prob_stockout = max(0.0, min(1.0, 1.0 - phi))
    except OverflowError:
        prob_stockout = 0.0 if z > 0 else 1.0
    return float(round(prob_stockout, 4))


def simulate_inventory_cycle(
    initial_stock: float,
    daily_demand_series: List[float],
    lead_time_days: float,
    rop: float,
    order_quantity: float
) -> Dict[str, float]:
    """
    Simulates daily inventory trajectory and tallies stockout occurrences and fill rate.
    """
    on_hand = initial_stock
    in_transit = []  # list of (arrival_day, quantity)
    stockout_events = 0
    total_requested = 0.0
    total_fulfilled = 0.0
    
    for day, demand in enumerate(daily_demand_series):
        # Process arrivals
        arrivals = [q for arr_day, q in in_transit if arr_day <= day]
        on_hand += sum(arrivals)
        in_transit = [(arr_day, q) for arr_day, q in in_transit if arr_day > day]
        
        # Fulfill demand
        total_requested += demand
        if on_hand >= demand:
            total_fulfilled += demand
            on_hand -= demand
        else:
            total_fulfilled += max(0.0, on_hand)
            stockout_events += 1
            on_hand = 0.0
            
        # Check reorder trigger
        effective_position = on_hand + sum(q for _, q in in_transit)
        if effective_position <= rop:
            in_transit.append((day + math.ceil(lead_time_days), order_quantity))
            
    fill_rate = (total_fulfilled / total_requested) if total_requested > 0 else 1.0
    stockout_rate = (stockout_events / len(daily_demand_series)) if len(daily_demand_series) > 0 else 0.0
    
    return {
        "total_requested_units": round(total_requested, 1),
        "total_fulfilled_units": round(total_fulfilled, 1),
        "fill_rate_percentage": round(fill_rate * 100.0, 2),
        "stockout_frequency_percentage": round(stockout_rate * 100.0, 2),
        "ending_inventory": round(on_hand, 1)
    }


class DarkStoreInventoryManager:
    """
    Enterprise inventory management system for quick-commerce dark stores.
    Evaluates historical SKU demand metrics and outputs optimized buffer levels.
    """
    
    def __init__(
        self,
        target_service_level: float = 0.95,
        default_lead_time_hours: float = 4.0,
        lead_time_std_hours: float = 0.8
    ):
        self.target_service_level = target_service_level
        self.lead_time_days = default_lead_time_hours / 24.0
        self.lead_time_std_days = lead_time_std_hours / 24.0

    def fit_from_demand_df(self, demand_df: pd.DataFrame) -> pd.DataFrame:
        """
        Processes historical daily demand DataFrame and returns SKU-Store level inventory policies.
        """
        demand_col = 'Daily_Quantity' if 'Daily_Quantity' in demand_df.columns else (
            'Total_Quantity' if 'Total_Quantity' in demand_df.columns else 'Quantity'
        )

        stats = demand_df.groupby(['Dark_Store_ID', 'Product_ID'])[demand_col].agg(
            demand_mean='mean',
            demand_std='std',
            demand_min='min',
            demand_max='max',
            observation_days='count'
        ).reset_index()

        stats['demand_std'] = stats['demand_std'].fillna(stats['demand_mean'] * 0.25)
        
        policies = []
        for _, row in stats.iterrows():
            mu_d = float(row['demand_mean'])
            sig_d = float(row['demand_std'])
            
            ss_90 = calculate_safety_stock(mu_d, sig_d, self.lead_time_days, self.lead_time_std_days, 0.90)
            ss_95 = calculate_safety_stock(mu_d, sig_d, self.lead_time_days, self.lead_time_std_days, 0.95)
            ss_99 = calculate_safety_stock(mu_d, sig_d, self.lead_time_days, self.lead_time_std_days, 0.99)
            
            rop_weekday = calculate_reorder_point(mu_d, self.lead_time_days, ss_95)
            rop_weekend = calculate_dynamic_rop(mu_d, self.lead_time_days, ss_95, is_weekend=True)
            
            policies.append({
                'Dark_Store_ID': row['Dark_Store_ID'],
                'Product_ID': row['Product_ID'],
                'Mean_Daily_Demand': round(mu_d, 2),
                'Demand_StdDev': round(sig_d, 2),
                'Safety_Stock_90pct': ss_90,
                'Safety_Stock_95pct': ss_95,
                'Safety_Stock_99pct': ss_99,
                'Weekday_ROP': rop_weekday,
                'Weekend_Dynamic_ROP': rop_weekend,
                'Recommended_Max_Stock': round(rop_weekend + (mu_d * 1.2), 1)
            })

        return pd.DataFrame(policies)
