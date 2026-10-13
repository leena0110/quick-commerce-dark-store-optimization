"""
Dark Store Spatial Layout & Picker Path Distance Optimization
=============================================================

Course: 23CSE452 - Business Analytics Capstone Project
Component: Review 1 & Review 2 Operational Optimization Engine
Author: Ande Taraka Srinivas (CB.SC.U4CSE23212)

This module models the internal physical topology of a quick-commerce dark store.
It optimizes SKU shelf placement (Golden Zone allocation) and picker travel distance
to ensure order assembly meets the 10-minute dispatch SLA.

Key Principles:
1. Golden Zone Allocation: Fast-moving items (high daily pick frequency) are placed
   at eye/waist level (Shelf Levels 2 & 3) close to the staging/dispatch counter.
2. Heavy/Bulky items (e.g. Atta, Oil, Beverages) are assigned to lower shelf levels
   for picker ergonomics and safety.
3. Multi-item basket routing simulation: S-shape / serpentine picker routing through aisles.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
import math
import os


class DarkStoreSpatialOptimizer:
    """
    Simulates dark store layout and optimizes product shelf binning and pick trajectories.
    """
    
    def __init__(
        self,
        num_aisles: int = 6,
        bays_per_aisle: int = 10,
        shelf_levels: int = 4,
        aisle_width_meters: float = 2.0,
        bay_length_meters: float = 1.2
    ):
        self.num_aisles = num_aisles
        self.bays_per_aisle = bays_per_aisle
        self.shelf_levels = shelf_levels
        self.aisle_width = aisle_width_meters
        self.bay_length = bay_length_meters
        self.packing_counter_coord = (0.0, 0.0)  # Front corner dispatch staging area

    def get_bin_coordinates(self, aisle: int, bay: int) -> Tuple[float, float]:
        """
        Maps (aisle, bay) indices to physical 2D coordinates in meters.
        """
        x = (aisle - 1) * self.aisle_width
        y = (bay - 1) * self.bay_length
        return (x, y)

    def calculate_manhattan_distance(self, p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
        """
        Manhattan walking distance for warehouse aisle movement.
        """
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def assign_skus_to_zones(self, sku_velocity_df: pd.DataFrame) -> pd.DataFrame:
        """
        Assigns SKUs to layout bins based on sales velocity and category ergonomics.
        
        Zones:
        - Zone A (Golden Zone): Aisles 1-2, Bays 1-5, Levels 2-3 (Closest to dispatch)
        - Zone B (Secondary Velocity): Aisles 2-4, Levels 1-4
        - Zone C (Slow/Bulk): Aisles 5-6, Levels 1 & 4
        """
        df = sku_velocity_df.sort_values(by='pick_frequency', ascending=False).reset_index(drop=True)
        
        allocations = []
        total_bins = self.num_aisles * self.bays_per_aisle * self.shelf_levels
        
        aisle = 1
        bay = 1
        level = 2  # Start with Golden Zone level
        
        for idx, row in df.iterrows():
            product_id = row['Product_ID']
            product_name = row.get('Product_Name', f"Product_{product_id}")
            category = row.get('Product_Category', 'General')
            velocity = row['pick_frequency']
            
            # Bulky categories override: always place on bottom level (Level 1)
            is_bulky = category in ['Staples', 'Beverages', 'Home Care']
            assigned_level = 1 if is_bulky else level
            
            # Zone classification
            if aisle <= 2 and bay <= 5 and assigned_level in [2, 3]:
                zone = 'Zone A (Golden Zone)'
            elif aisle <= 4:
                zone = 'Zone B (Standard Flow)'
            else:
                zone = 'Zone C (Slow/Bulk)'
                
            coord = self.get_bin_coordinates(aisle, bay)
            dist_to_dispatch = self.calculate_manhattan_distance(self.packing_counter_coord, coord)
            
            allocations.append({
                'Product_ID': product_id,
                'Product_Name': product_name,
                'Product_Category': category,
                'Pick_Velocity_Rank': idx + 1,
                'Daily_Pick_Frequency': round(float(velocity), 1),
                'Assigned_Zone': zone,
                'Aisle': aisle,
                'Bay': bay,
                'Shelf_Level': assigned_level,
                'Distance_To_Packing_Meters': round(dist_to_dispatch, 2)
            })
            
            # Increment layout slot
            bay += 1
            if bay > self.bays_per_aisle:
                bay = 1
                aisle += 1
                if aisle > self.num_aisles:
                    aisle = 1
                    level = 3 if level == 2 else (1 if level == 3 else 4)
                    
        return pd.DataFrame(allocations)

    def simulate_order_pick_path(
        self,
        order_sku_list: List[str],
        shelf_allocation_df: pd.DataFrame
    ) -> Dict[str, float]:
        """
        Simulates the picker trajectory for a multi-item order using S-shape traversal.
        """
        sku_lookup = shelf_allocation_df.set_index('Product_ID')
        item_coords = []
        
        for sku in order_sku_list:
            if sku in sku_lookup.index:
                row = sku_lookup.loc[sku]
                if isinstance(row, pd.DataFrame):
                    row = row.iloc[0]
                coord = self.get_bin_coordinates(int(row['Aisle']), int(row['Bay']))
                item_coords.append(coord)
                
        if not item_coords:
            return {"total_distance_meters": 0.0, "estimated_pick_time_seconds": 0.0}
            
        # Sort items primarily by Aisle, then by Bay for serpentine picking
        sorted_coords = sorted(item_coords, key=lambda c: (c[0], c[1]))
        
        total_distance = self.calculate_manhattan_distance(self.packing_counter_coord, sorted_coords[0])
        current = sorted_coords[0]
        
        for nxt in sorted_coords[1:]:
            total_distance += self.calculate_manhattan_distance(current, nxt)
            current = nxt
            
        # Return to packing counter
        total_distance += self.calculate_manhattan_distance(current, self.packing_counter_coord)
        
        # Human picker parameters: walking speed 1.2 m/s, item search/grab 12 seconds
        walking_time = total_distance / 1.2
        grab_time = len(order_sku_list) * 12.0
        total_time = walking_time + grab_time
        
        return {
            "total_distance_meters": round(total_distance, 2),
            "estimated_pick_time_seconds": round(total_time, 1),
            "items_picked": len(order_sku_list)
        }


if __name__ == "__main__":
    print("Testing DarkStoreSpatialOptimizer...")
    optimizer = DarkStoreSpatialOptimizer()
    sample_skus = pd.DataFrame({
        'Product_ID': [f'P{i:03d}' for i in range(1, 21)],
        'Product_Name': [f'Sample Item {i}' for i in range(1, 21)],
        'Product_Category': ['Dairy', 'Snacks', 'Produce', 'Beverages'] * 5,
        'pick_frequency': np.linspace(150, 10, 20)
    })
    alloc_df = optimizer.assign_skus_to_zones(sample_skus)
    print("Sample Shelf Allocation:")
    print(alloc_df.head())
