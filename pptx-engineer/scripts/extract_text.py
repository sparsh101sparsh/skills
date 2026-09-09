#!/usr/bin/env python3
"""
extract_text.py - Extract full text in presentation order from a .pptx or unpacked directory.

Usage:
    python extract_text.py <presentation.pptx or unpacked_dir>
"""
import sys
import os
import zipfile
import xml.etree.ElementTree as ET

A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"

def get_ordered_slides(target):
    is_zip = zipfile.is_zipfile(target) if os.path.isfile(target) else False
    zf = zipfile.ZipFile(target, 'r') if is_zip else None
    
    def read_xml(rel_path):
        if zf:
            try:
                data = zf.read(rel_path)
                return ET.fromstring(data)
            except KeyError:
                return None
        else:
            full_path = os.path.join(target, rel_path)
            if os.path.exists(full_path):
                return ET.parse(full_path).getroot()
            return None

    pres_root = read_xml("ppt/presentation.xml")
    rels_root = read_xml("ppt/_rels/presentation.xml.rels")
    
    if pres_root is None or rels_root is None:
        return []

    # Map rId -> target slide path
    r_map = {}
    for rel in rels_root.findall(f"{{{PKG_REL_NS}}}Relationship"):
        r_id = rel.get("Id")
        r_target = rel.get("Target")
        r_type = rel.get("Type")
        if "slide" in r_type.lower():
            if not r_target.startswith("ppt/"):
                r_target = "ppt/" + r_target.lstrip("/")
            r_map[r_id] = r_target

    ordered_slides = []
    sld_id_lst = pres_root.find(f"{{{P_NS}}}sldIdLst")
    if sld_id_lst is not None:
        for sld_id in sld_id_lst.findall(f"{{{P_NS}}}sldId"):
            rid = sld_id.get(f"{{{R_NS}}}id") or sld_id.get("id")
            if rid in r_map:
                ordered_slides.append((sld_id.get("id"), rid, r_map[rid]))

    if zf:
        zf.close()
    return ordered_slides

def extract_text(target):
    is_zip = zipfile.is_zipfile(target) if os.path.isfile(target) else False
    zf = zipfile.ZipFile(target, 'r') if is_zip else None

    def read_slide_root(slide_path):
        if zf:
            return ET.fromstring(zf.read(slide_path))
        else:
            return ET.parse(os.path.join(target, slide_path)).getroot()

    ordered = get_ordered_slides(target)
    if not ordered:
        print(f"No ordered slides found in '{target}'.", file=sys.stderr)
        return

    for idx, (sid, rid, slide_path) in enumerate(ordered, 1):
        slide_name = os.path.basename(slide_path)
        print(f"\n<!-- Slide number: {idx} (ID: {sid} | rId: {rid} | {slide_name}) -->")
        try:
            root = read_slide_root(slide_path)
        except Exception as e:
            print(f"[Error reading slide XML: {e}]")
            continue

        sp_tree = root.find(f".//{{{P_NS}}}spTree")
        if sp_tree is None:
            continue

        for sp in sp_tree.iter(f"{{{P_NS}}}sp"):
            # Shape name
            cNvPr = sp.find(f".//{{{P_NS}}}cNvPr")
            sp_name = cNvPr.get("name", "Shape") if cNvPr is not None else "Shape"
            sp_id = cNvPr.get("id", "") if cNvPr is not None else ""

            txBody = sp.find(f"{{{P_NS}}}txBody")
            if txBody is None:
                continue

            shape_lines = []
            for p in txBody.findall(f"{{{A_NS}}}p"):
                runs = p.findall(f"{{{A_NS}}}r")
                p_text = "".join(r.findtext(f"{{{A_NS}}}t", default="") for r in runs)
                # Also check direct <a:t>
                if not p_text:
                    p_text = "".join(t.text for t in p.findall(f".//{{{A_NS}}}t") if t.text)
                p_text = p_text.strip()
                if p_text:
                    shape_lines.append(p_text)

            if shape_lines:
                print(f"\n[Shape: {sp_name} (ID: {sp_id})]")
                for line in shape_lines:
                    print(f"  {line}")

    if zf:
        zf.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    extract_text(sys.argv[1])
