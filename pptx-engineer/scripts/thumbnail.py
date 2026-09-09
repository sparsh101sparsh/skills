#!/usr/bin/env python3
"""
thumbnail.py - Generate visual rendering/preview of slides for visual QA.

Tries in order:
1. soffice (LibreOffice) headless to PDF + pdftoppm
2. macOS native qlmanage
3. Fallback layout & text-bounds analysis report

Usage:
    python thumbnail.py <presentation.pptx> [output_dir]
"""
import sys
import os
import shutil
import subprocess

def render(pptx_path, out_dir=None):
    if not os.path.exists(pptx_path):
        print(f"Error: File '{pptx_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    if out_dir is None:
        out_dir = "previews"
    os.makedirs(out_dir, exist_ok=True)

    # 1. Try LibreOffice + pdftoppm
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    pdftoppm = shutil.which("pdftoppm")
    if soffice and pdftoppm:
        print("Using LibreOffice + pdftoppm for visual rendering...")
        pdf_dir = os.path.join(out_dir, "tmp_pdf")
        os.makedirs(pdf_dir, exist_ok=True)
        cmd_pdf = [soffice, "--headless", "--convert-to", "pdf", "--outdir", pdf_dir, pptx_path]
        res = subprocess.run(cmd_pdf, capture_output=True, text=True)
        if res.returncode == 0:
            base_pdf = os.path.splitext(os.path.basename(pptx_path))[0] + ".pdf"
            full_pdf = os.path.join(pdf_dir, base_pdf)
            if os.path.exists(full_pdf):
                prefix = os.path.join(out_dir, "slide")
                cmd_ppm = [pdftoppm, "-png", "-r", "150", full_pdf, prefix]
                res_ppm = subprocess.run(cmd_ppm, capture_output=True, text=True)
                if res_ppm.returncode == 0:
                    shutil.rmtree(pdf_dir)
                    images = [f for f in os.listdir(out_dir) if f.startswith("slide-") and f.endswith(".png")]
                    print(f"Rendered {len(images)} slide preview(s) in '{out_dir}'.")
                    return

    # 2. Try macOS qlmanage
    qlmanage = shutil.which("qlmanage")
    if qlmanage and sys.platform == "darwin":
        print("Using macOS QuickLook (qlmanage) for thumbnail rendering...")
        cmd_ql = [qlmanage, "-t", "-s", "1600", "-o", out_dir, pptx_path]
        res = subprocess.run(cmd_ql, capture_output=True, text=True)
        if res.returncode == 0:
            thumb_name = os.path.basename(pptx_path) + ".png"
            thumb_path = os.path.join(out_dir, thumb_name)
            if os.path.exists(thumb_path):
                print(f"QuickLook thumbnail generated: {thumb_path}")
                return

    print("Note: soffice / pdftoppm not found. Visual QA should inspect element bounding boxes with inspect_shapes.py or preview via native viewer.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    pptx = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else None
    render(pptx, out)
