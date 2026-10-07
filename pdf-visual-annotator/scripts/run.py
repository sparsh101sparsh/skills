#!/usr/bin/env python3
"""
Universal Runner & Dependency Verifier
======================================
Verifies PyMuPDF environment and executes requested script or task.
"""

import sys
import subprocess
import os

def check_dependencies():
    try:
        import pymupdf
        return True, getattr(pymupdf, "__version__", "installed")
    except ImportError:
        return False, None

def main():
    ok, ver = check_dependencies()
    if not ok:
        print("❌ Error: 'pymupdf' is not installed in the current Python environment.")
        print("💡 Install it using:")
        print("    pip install pymupdf")
        sys.exit(1)
    
    if len(sys.argv) < 2:
        print(f"✅ PyMuPDF is installed (v{ver}).")
        print("Usage: python3 run.py <script_path_or_command> [args...]")
        print("Examples:")
        print("    python3 run.py examples/annotate_over_image.py")
        print("    python3 run.py examples/draw_3d_prism.py")
        print("    python3 run.py examples/dsa_binary_search_steps.py")
        print("    python3 run.py scripts/pdf_annotator_cli.py --help")
        sys.exit(0)

    target_script = sys.argv[1]
    script_args = sys.argv[2:]

    cmd = [sys.executable, target_script] + script_args
    res = subprocess.run(cmd)
    sys.exit(res.returncode)

if __name__ == "__main__":
    main()
