#!/usr/bin/env python3
"""
Example: Multi-Page Step-by-Step DSA Binary Search Visualizer
=============================================================
Demonstrates programmatically generating a sequential multi-page PDF deck
visualizing the execution steps of the Binary Search algorithm.
"""

import os
import sys

# Add scripts directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from pdf_annotator_engine import DSAVisualizer


def main():
    output_pdf = "dsa_binary_search_output.pdf"
    print("🚀 Generating Step-by-Step Binary Search Visualization PDF...")

    arr = [3, 7, 11, 15, 23, 34, 45, 58, 69, 82, 95]
    target = 45

    steps = [
        {
            "description": f"Target = {target}. Initial Search Space: [0..10]. Compute Mid = (0 + 10) // 2 = 5.",
            "array": arr,
            "active": list(range(11)),
            "compared": [5],
            "pointers": {"low": 0, "mid": 5, "high": 10},
            "note": f"arr[mid] = {arr[5]} < {target}. Discard left partition [0..5] and update Low = mid + 1 = 6.",
        },
        {
            "description": f"Search Space updated to [6..10]. Compute Mid = (6 + 10) // 2 = 8.",
            "array": arr,
            "active": list(range(6, 11)),
            "compared": [8],
            "pointers": {"low": 6, "mid": 8, "high": 10},
            "note": f"arr[mid] = {arr[8]} > {target}. Discard right partition [8..10] and update High = mid - 1 = 7.",
        },
        {
            "description": f"Search Space updated to [6..7]. Compute Mid = (6 + 7) // 2 = 6.",
            "array": arr,
            "active": [6, 7],
            "sorted": [6],
            "pointers": {"low": 6, "mid": 6, "high": 7},
            "note": f"arr[mid] = {arr[6]} == {target}! Value located at Index 6 in exactly 3 comparison steps.",
        },
    ]

    DSAVisualizer.create_algorithm_slide_deck(
        output_pdf=output_pdf,
        title="Binary Search Algorithm Visualizer",
        steps=steps,
        slide_w=900,
        slide_h=480,
    )

    print(f"✅ Generated: {output_pdf} (3-page execution sequence)")


if __name__ == "__main__":
    main()
