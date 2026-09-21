#!/usr/bin/env python3
"""
Integrated Forensic Document Screening CLI.
Combines ICAO 9303 MRZ parsing with Error Level Analysis (ELA) into a unified report.
"""

from __future__ import annotations
import argparse
import json
import sys
from mrz_parser import MRZParser
from ela_analyzer import perform_ela

def audit_document(mrz_text: str | None, image_path: str | None, output_ela: str | None = None) -> dict:
    report = {
        "timestamp": "2026-09-22T02:00:00Z",
        "mrz_status": None,
        "image_ela_status": None,
        "composite_risk_score": "UNKNOWN"
    }

    mrz_valid = True
    if mrz_text:
        mrz_res = MRZParser.parse(mrz_text)
        report["mrz_status"] = mrz_res
        mrz_valid = mrz_res.get("valid", False)

    ela_clean = True
    if image_path:
        ela_res = perform_ela(image_path, output_path=output_ela)
        report["image_ela_status"] = ela_res
        ela_clean = not ela_res.get("is_anomalous", False)

    if not mrz_valid:
        report["composite_risk_score"] = "HIGH_RISK_TAMPERED"
    elif not ela_clean:
        report["composite_risk_score"] = "MODERATE_RISK_COMPRESSION_ANOMALY"
    else:
        report["composite_risk_score"] = "VERIFIED_AUTHENTIC"

    return report

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Document Forensics Screening Workstation")
    parser.add_argument("--mrz", help="MRZ string or path to MRZ text file")
    parser.add_argument("--image", help="Target document image path")
    parser.add_argument("--out-ela", help="Optional path to save ELA difference image")

    args = parser.parse_args()

    mrz_content = None
    if args.mrz:
        try:
            with open(args.mrz, 'r') as f:
                mrz_content = f.read()
        except FileNotFoundError:
            mrz_content = args.mrz

    result = audit_document(mrz_content, args.image, args.out_ela)
    print(json.dumps(result, indent=2))
