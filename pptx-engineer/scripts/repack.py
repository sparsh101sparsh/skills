#!/usr/bin/env python3
"""
repack.py - Safely repack an unpacked directory into a .pptx file.

Usage:
    python repack.py <unpacked_dir> <output.pptx>
"""
import sys
import os
import zipfile

def repack(unpacked_dir, output_pptx):
    if not os.path.exists(unpacked_dir) or not os.path.isdir(unpacked_dir):
        print(f"Error: Directory '{unpacked_dir}' does not exist.", file=sys.stderr)
        sys.exit(1)
        
    output_pptx = os.path.abspath(output_pptx)
    if os.path.exists(output_pptx):
        os.remove(output_pptx)
        
    # Check essential parts
    content_types = os.path.join(unpacked_dir, "[Content_Types].xml")
    if not os.path.exists(content_types):
        print(f"Error: '{unpacked_dir}' does not look like an unpacked PPTX (missing [Content_Types].xml).", file=sys.stderr)
        sys.exit(1)
        
    count = 0
    with zipfile.ZipFile(output_pptx, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(unpacked_dir):
            for file in files:
                if (file.startswith('.') and not file.endswith('.rels')) or file.endswith('.tmp') or file.endswith('.stale'):
                    continue
                full_path = os.path.join(root, file)
                # Don't accidentally include the output file if placed inside
                if os.path.abspath(full_path) == output_pptx:
                    continue
                rel_path = os.path.relpath(full_path, unpacked_dir)
                zf.write(full_path, rel_path)
                count += 1
                
    print(f"Successfully repacked {count} items from '{unpacked_dir}' -> '{output_pptx}'")
    return output_pptx

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    repack(sys.argv[1], sys.argv[2])
