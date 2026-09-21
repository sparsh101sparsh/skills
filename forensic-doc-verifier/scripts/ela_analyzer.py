#!/usr/bin/env python3
"""
Error Level Analysis (ELA) Forensic Engine.
Analyzes JPEG re-compression error differentials to detect digital image tampering,
cloned text, and spliced boundaries.
"""

from __future__ import annotations
import argparse
import io
import json
import sys
from typing import Dict, Any, Optional

try:
    from PIL import Image, ImageChops, ImageEnhance, ImageStat
except ImportError:
    Image = None

def perform_ela(
    image_path: str,
    output_path: Optional[str] = None,
    quality: int = 90,
    scale: float = 15.0
) -> Dict[str, Any]:
    """
    Perform Error Level Analysis on an image.
    
    Args:
        image_path: Path to target document image.
        output_path: Optional path to save visual ELA difference map.
        quality: Standardized JPEG recompression quality factor (default 90).
        scale: Amplification factor to highlight error discrepancies.
    """
    if Image is None:
        return {
            "success": False,
            "error": "Pillow (PIL) is not installed. Install via `pip install Pillow`."
        }

    try:
        orig = Image.open(image_path).convert('RGB')
    except Exception as e:
        return {"success": False, "error": f"Failed to open image: {e}"}

    # Re-compress to in-memory JPEG at designated quality
    buffer = io.BytesIO()
    orig.save(buffer, 'JPEG', quality=quality)
    buffer.seek(0)
    recompressed = Image.open(buffer)

    # Compute per-pixel absolute difference
    diff = ImageChops.difference(orig, recompressed)

    # Statistical evaluation of difference
    stat = ImageStat.Stat(diff)
    mean_error = sum(stat.mean) / len(stat.mean)
    rms_error = sum(stat.rms) / len(stat.rms)
    extrema = diff.getextrema()
    max_error = max([ex[1] for ex in extrema])

    # Amplified visualization for inspection
    enhancer = ImageEnhance.Brightness(diff)
    ela_amplified = enhancer.enhance(scale)

    if output_path:
        ela_amplified.save(output_path, 'JPEG', quality=95)

    # Anomalous heuristic evaluation:
    # High variance or extreme localized peaks indicate spliced text/elements
    is_anomalous = (rms_error - mean_error) > 4.5 or max_error > 85

    return {
        "success": True,
        "metrics": {
            "mean_error": round(mean_error, 4),
            "rms_error": round(rms_error, 4),
            "max_error": max_error,
            "error_variance": round(rms_error - mean_error, 4)
        },
        "is_anomalous": is_anomalous,
        "verdict": "SUSPECT_TAMPERING" if is_anomalous else "CONSISTENT_COMPRESSION",
        "output_saved": output_path if output_path else None
    }

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Error Level Analysis (ELA) Document Tamper Engine")
    parser.add_argument("image", help="Target document image path")
    parser.add_argument("-o", "--output", help="Path to save visual ELA output image")
    parser.add_argument("-q", "--quality", type=int, default=90, help="Re-compression quality (default: 90)")
    parser.add_argument("-s", "--scale", type=float, default=15.0, help="Amplification scale (default: 15.0)")

    args = parser.parse_args()
    result = perform_ela(args.image, args.output, args.quality, args.scale)
    print(json.dumps(result, indent=2))
    sys.exit(0 if not result.get("is_anomalous") else 1)
