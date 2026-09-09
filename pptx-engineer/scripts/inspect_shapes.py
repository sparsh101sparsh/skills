#!/usr/bin/env python3
"""
inspect_shapes.py - Inspect shape IDs, positions, formatting, and relationships on a slide.

Usage:
    python inspect_shapes.py <unpacked_dir> [slide_num_or_filename]
"""
import sys
import os
import xml.etree.ElementTree as ET

A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"

EMU_PER_INCH = 914400.0
EMU_PER_PT = 12700.0

def load_rels(slide_rels_path):
    rel_map = {}
    if os.path.exists(slide_rels_path):
        root = ET.parse(slide_rels_path).getroot()
        for rel in root.findall(f"{{{PKG_REL_NS}}}Relationship"):
            rel_map[rel.get("Id")] = rel.get("Target")
    return rel_map

def inspect_slide(unpacked_dir, slide_filename):
    slide_path = os.path.join(unpacked_dir, "ppt", "slides", slide_filename)
    slide_rels_path = os.path.join(unpacked_dir, "ppt", "slides", "_rels", f"{slide_filename}.rels")

    if not os.path.exists(slide_path):
        print(f"Error: '{slide_path}' not found.", file=sys.stderr)
        return

    rel_map = load_rels(slide_rels_path)
    root = ET.parse(slide_path).getroot()

    print(f"=== INSPECTING: {slide_filename} ===")
    sp_tree = root.find(f".//{{{P_NS}}}spTree")
    if sp_tree is None:
        print("No spTree found.")
        return

    shape_idx = 0
    for elem in sp_tree:
        tag = elem.tag.split("}")[-1]
        if tag not in ("sp", "pic", "grpSp", "graphicFrame"):
            continue

        shape_idx += 1
        cNvPr = elem.find(f".//{{{P_NS}}}cNvPr")
        sp_id = cNvPr.get("id", "N/A") if cNvPr is not None else "N/A"
        sp_name = cNvPr.get("name", "N/A") if cNvPr is not None else "N/A"

        # Position and size
        xfrm = elem.find(f".//{{{A_NS}}}xfrm")
        pos_str = "Position: N/A"
        if xfrm is not None:
            off = xfrm.find(f"{{{A_NS}}}off")
            ext = xfrm.find(f"{{{A_NS}}}ext")
            if off is not None and ext is not None:
                x = int(off.get("x", 0))
                y = int(off.get("y", 0))
                cx = int(ext.get("cx", 0))
                cy = int(ext.get("cy", 0))
                x_in = x / EMU_PER_INCH
                y_in = y / EMU_PER_INCH
                cx_in = cx / EMU_PER_INCH
                cy_in = cy / EMU_PER_INCH
                pos_str = f"Pos: ({x} EMU / {x_in:.2f} in, {y} EMU / {y_in:.2f} in) | Size: ({cx}x{cy} EMU / {cx_in:.2f}x{cy_in:.2f} in)"

        print(f"\n[{shape_idx}] Type: <p:{tag}> | ID: {sp_id} | Name: {sp_name}")
        print(f"    {pos_str}")

        # Check for hyperlinks
        hlinks = elem.findall(f".//{{{A_NS}}}hlinkClick")
        for hl in hlinks:
            rid = hl.get(f"{{{R_NS}}}id")
            target = rel_map.get(rid, "UNKNOWN")
            print(f"    🔗 Hyperlink rId: {rid} -> Target: {target}")

        # Check for images
        blips = elem.findall(f".//{{{A_NS}}}blip")
        for blip in blips:
            rid = blip.get(f"{{{R_NS}}}embed")
            target = rel_map.get(rid, "UNKNOWN")
            print(f"    🖼️  Image rId: {rid} -> Target: {target}")

        # Check text
        txBody = elem.find(f"{{{P_NS}}}txBody")
        if txBody is not None:
            bodyPr = txBody.find(f"{{{A_NS}}}bodyPr")
            if bodyPr is not None:
                insets = []
                for ins in ("lIns", "tIns", "rIns", "bIns"):
                    val = bodyPr.get(ins)
                    if val is not None:
                        insets.append(f"{ins}: {int(val)/EMU_PER_PT:.1f}pt")
                if insets:
                    print(f"    Insets: {', '.join(insets)}")

            for p_idx, p in enumerate(txBody.findall(f"{{{A_NS}}}p")):
                pPr = p.find(f"{{{A_NS}}}pPr")
                indent_str = ""
                if pPr is not None:
                    marL = pPr.get("marL")
                    indent = pPr.get("indent")
                    if marL or indent:
                        indent_str = f" [marL: {marL}, indent: {indent}]"

                runs = p.findall(f"{{{A_NS}}}r")
                p_text = "".join(r.findtext(f"{{{A_NS}}}t", default="") for r in runs)
                if not p_text:
                    p_text = "".join(t.text for t in p.findall(f".//{{{A_NS}}}t") if t.text)
                p_text = p_text.strip()

                if p_text:
                    print(f"    P{p_idx+1}{indent_str}: {p_text[:90]}{'...' if len(p_text)>90 else ''}")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    unpacked = sys.argv[1]
    slide_arg = sys.argv[2] if len(sys.argv) > 2 else None

    if slide_arg:
        if not slide_arg.endswith(".xml"):
            if slide_arg.isdigit():
                slide_filename = f"slide{slide_arg}.xml"
            else:
                slide_filename = f"{slide_arg}.xml"
        else:
            slide_filename = slide_arg
        inspect_slide(unpacked, slide_filename)
    else:
        slides_dir = os.path.join(unpacked, "ppt", "slides")
        if not os.path.exists(slides_dir):
            print(f"Error: '{slides_dir}' not found.", file=sys.stderr)
            sys.exit(1)
        slide_files = sorted([f for f in os.listdir(slides_dir) if f.startswith("slide") and f.endswith(".xml")],
                             key=lambda x: int(''.join(filter(str.isdigit, x)) or 0))
        for sf in slide_files:
            inspect_slide(unpacked, sf)

if __name__ == "__main__":
    main()
