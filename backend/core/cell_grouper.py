"""
Cell Grouper — Groups detected dots into 2x3 Braille cells.
Braille cells consist of 6 dots arranged in 2 columns and 3 rows.
"""

import numpy as np
from typing import List, Tuple
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import ROW_TOLERANCE, COL_TOLERANCE, CELL_GAP_RATIO


def group_into_cells(boxes: List[List[float]], 
                    row_tolerance: int = ROW_TOLERANCE,
                    col_tolerance: int = COL_TOLERANCE) -> List[Tuple[int, ...]]:
    """
    Groups detected dot bounding boxes into Braille cells (2x3 arrangements).
    
    Args:
        boxes: List of [x1, y1, x2, y2] bounding boxes from detector
        row_tolerance: Pixels — dots within this Y-distance are considered in same row
        col_tolerance: Pixels — dots within this X-distance are considered in same column
    
    Returns:
        List of 6-tuples, each tuple representing a cell's dot pattern:
        (dot1, dot2, dot3, dot4, dot5, dot6)
        where dot_i ∈ {0, 1} indicating presence/absence
    """
    if not boxes or len(boxes) == 0:
        return []

    # Calculate centers of each box
    centers = []
    for x1, y1, x2, y2 in boxes:
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        centers.append((cx, cy))

    # Sort by Y first (top to bottom), then X (left to right)
    centers.sort(key=lambda p: (p[1], p[0]))

    # Cluster into rows
    rows = []
    current_row = [centers[0]]
    
    for i in range(1, len(centers)):
        # Check if this center belongs to current row
        if abs(centers[i][1] - centers[i-1][1]) <= row_tolerance:
            current_row.append(centers[i])
        else:
            rows.append(current_row)
            current_row = [centers[i]]
    
    if current_row:
        rows.append(current_row)

    # Sort each row by X coordinate (left to right)
    for row in rows:
        row.sort(key=lambda p: p[0])

    # Group columns (pair left and right columns into cells)
    cells = []
    
    for row in rows:
        for center in row:
            # Check if this is start of a new cell (left column)
            # or part of existing cell (right column)
            
            # Create cell if we have at least 1 dot per row
            if len(row) >= 2:
                # We have multiple dots; need to pair them
                # This is simplified; robust version would do proper clustering
                pass
    
    # Simplified approach: if we have 3+ rows of dots, treat as cells
    # Each group of 2-3 dots per row = 1 cell (or more)
    cells = []
    
    if len(rows) >= 3:
        # Match dots across 3 rows to form cells
        cells = _match_cells_from_rows(rows, col_tolerance)
    else:
        # Fewer than 3 rows; treat each dot as single-dot cell
        for row in rows:
            for center in row:
                cells.append((1, 0, 0, 0, 0, 0))  # placeholder
    
    return cells if cells else [(0, 0, 0, 0, 0, 0)]


def _match_cells_from_rows(rows: List[List[Tuple[float, float]]], 
                           col_tolerance: int = COL_TOLERANCE) -> List[Tuple[int, ...]]:
    """
    Match dots from 3 rows into cell columns.
    Expects: rows[0] = dots at y position for dots 1&4
             rows[1] = dots at y position for dots 2&5
             rows[2] = dots at y position for dots 3&6
    """
    if len(rows) < 3:
        return []
    
    # Ensure we have at least 3 rows
    row1_dots = rows[0] if len(rows) > 0 else []
    row2_dots = rows[1] if len(rows) > 1 else []
    row3_dots = rows[2] if len(rows) > 2 else []
    
    cells = []
    
    # Simple approach: pair dots by X proximity
    # For each column position, assign dots from each row
    
    all_x_positions = set()
    for dot in row1_dots + row2_dots + row3_dots:
        all_x_positions.add(dot[0])
    
    # Cluster X positions
    x_positions = sorted(all_x_positions)
    x_clusters = []
    current_cluster = [x_positions[0]] if x_positions else []
    
    for i in range(1, len(x_positions)):
        if x_positions[i] - x_positions[i-1] <= col_tolerance:
            current_cluster.append(x_positions[i])
        else:
            x_clusters.append(current_cluster)
            current_cluster = [x_positions[i]]
    
    if current_cluster:
        x_clusters.append(current_cluster)
    
    # For each X cluster, extract cell pattern
    for x_cluster in x_clusters:
        x_center = sum(x_cluster) / len(x_cluster)
        
        # Find dots near this X center in each row
        dot1 = 1 if any(abs(d[0] - x_center) <= col_tolerance for d in row1_dots) else 0
        dot2 = 1 if any(abs(d[0] - x_center) <= col_tolerance for d in row2_dots) else 0
        dot3 = 1 if any(abs(d[0] - x_center) <= col_tolerance for d in row3_dots) else 0
        
        # For left and right columns, we'd need additional logic here
        # For now, use placeholder for dots 4-6
        cell = (dot1, dot2, dot3, 0, 0, 0)
        cells.append(cell)
    
    return cells if cells else [(0, 0, 0, 0, 0, 0)]


def visualize_cells(cells: List[Tuple[int, ...]]):
    """
    Print Braille cells in visual format (for debugging).
    """
    for i, cell in enumerate(cells):
        d1, d2, d3, d4, d5, d6 = cell
        print(f"Cell {i}: [{d1}{d4}] [{d2}{d5}] [{d3}{d6}]")
