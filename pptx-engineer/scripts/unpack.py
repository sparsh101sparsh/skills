#!/usr/bin/env python3
"""
unpack.py - Safely unpack a .pptx file into a working directory.

Usage:
    python unpack.py <presentation.pptx> [output_directory]
"""
import sys
import os
import zipfile
import shutil

def unpack(pptx_path, out_dir=None):
    if not os.path.exists(pptx_path):
        print(f"Error: File '{pptx_path}' does not exist.", file=sys.stderr)
        sys.exit(1)
        
    if not zipfile.is_zipfile(pptx_path):
        print(f"Error: '{pptx_path}' is not a valid zip / pptx file.", file=sys.stderr)
        sys.exit(1)
        
    if out_dir is None:
        base = os.path.splitext(os.path.basename(pptx_path))[0]
        out_dir = f"unpacked_{base}"
        
    if os.path.exists(out_dir):
        print(f"Warning: Output directory '{out_dir}' already exists. Overwriting...", file=sys.stderr)
        shutil.rmtree(out_dir)
        
    os.makedirs(out_dir, exist_ok=True)
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        zf.extractall(out_dir)
        
    print(f"Successfully unpacked '{pptx_path}' -> '{out_dir}'")
    return out_dir

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    pptx = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else None
    unpack(pptx, out)
