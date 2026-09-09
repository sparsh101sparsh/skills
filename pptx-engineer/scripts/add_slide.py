#!/usr/bin/env python3
"""
add_slide.py - Duplicate a slide in an unpacked presentation with complete relationship wiring.

Usage:
    python add_slide.py <unpacked_dir> <source_slide.xml> [--after <target_slide.xml>] [--before <target_slide.xml>]
"""
import sys
import os
import shutil
import xml.etree.ElementTree as ET

P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"

ET.register_namespace("p", P_NS)
ET.register_namespace("r", R_NS)
ET.register_namespace("rel", PKG_REL_NS)

def duplicate_slide(unpacked_dir, src_slide, after_slide=None, before_slide=None):
    slides_dir = os.path.join(unpacked_dir, "ppt", "slides")
    slides_rels_dir = os.path.join(slides_dir, "_rels")
    pres_xml = os.path.join(unpacked_dir, "ppt", "presentation.xml")
    pres_rels_xml = os.path.join(unpacked_dir, "ppt", "_rels", "presentation.xml.rels")
    ct_xml = os.path.join(unpacked_dir, "[Content_Types].xml")

    # Normalize filenames
    if not src_slide.endswith(".xml"):
        src_slide += ".xml"
    if after_slide and not after_slide.endswith(".xml"):
        after_slide += ".xml"
    if before_slide and not before_slide.endswith(".xml"):
        before_slide += ".xml"

    src_path = os.path.join(slides_dir, src_slide)
    if not os.path.exists(src_path):
        print(f"Error: Source slide '{src_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    # 1. Determine next available slide number
    existing_nums = []
    for f in os.listdir(slides_dir):
        if f.startswith("slide") and f.endswith(".xml"):
            num_str = f[5:-4]
            if num_str.isdigit():
                existing_nums.append(int(num_str))
    new_num = (max(existing_nums) + 1) if existing_nums else 1
    new_slide_name = f"slide{new_num}.xml"
    new_slide_path = os.path.join(slides_dir, new_slide_name)

    # 2. Copy slide XML and .rels
    shutil.copyfile(src_path, new_slide_path)
    src_rels = os.path.join(slides_rels_dir, f"{src_slide}.rels")
    new_rels = os.path.join(slides_rels_dir, f"{new_slide_name}.rels")
    if os.path.exists(src_rels):
        shutil.copyfile(src_rels, new_rels)

    # 3. Update [Content_Types].xml
    ct_tree = ET.parse(ct_xml)
    ct_root = ct_tree.getroot()
    part_name = f"/ppt/slides/{new_slide_name}"
    # Check if override already exists
    exists = any(elem.get("PartName") == part_name for elem in ct_root.findall(f"{{{CT_NS}}}Override"))
    if not exists:
        override = ET.SubElement(ct_root, f"{{{CT_NS}}}Override")
        override.set("PartName", part_name)
        override.set("ContentType", "application/vnd.openxmlformats-officedocument.presentationml.slide+xml")
        ct_tree.write(ct_xml, encoding="utf-8", xml_declaration=True)

    # 4. Update ppt/_rels/presentation.xml.rels
    pres_rels_tree = ET.parse(pres_rels_xml)
    pres_rels_root = pres_rels_tree.getroot()
    existing_rids = []
    for rel in pres_rels_root.findall(f"{{{PKG_REL_NS}}}Relationship"):
        rid = rel.get("Id", "")
        if rid.startswith("rId") and rid[3:].isdigit():
            existing_rids.append(int(rid[3:]))
    new_rid_num = (max(existing_rids) + 1) if existing_rids else 1
    new_rid = f"rId{new_rid_num}"

    rel_elem = ET.SubElement(pres_rels_root, f"{{{PKG_REL_NS}}}Relationship")
    rel_elem.set("Id", new_rid)
    rel_elem.set("Type", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide")
    rel_elem.set("Target", f"slides/{new_slide_name}")
    pres_rels_tree.write(pres_rels_xml, encoding="utf-8", xml_declaration=True)

    # 5. Update ppt/presentation.xml (<p:sldIdLst>)
    pres_tree = ET.parse(pres_xml)
    pres_root = pres_tree.getroot()
    sld_id_lst = pres_root.find(f"{{{P_NS}}}sldIdLst")
    if sld_id_lst is None:
        sld_id_lst = ET.SubElement(pres_root, f"{{{P_NS}}}sldIdLst")

    # Determine next available sldId id (typically 256+)
    existing_sids = []
    for s in sld_id_lst.findall(f"{{{P_NS}}}sldId"):
        sid = s.get("id")
        if sid and sid.isdigit():
            existing_sids.append(int(sid))
    new_sid = str((max(existing_sids) + 1) if existing_sids else 256)

    new_sld = ET.Element(f"{{{P_NS}}}sldId")
    new_sld.set("id", new_sid)
    new_sld.set(f"{{{R_NS}}}id", new_rid)

    # Build map of target -> element in sldIdLst
    # Need to know which rId maps to which target slide
    rid_to_target = {}
    for rel in pres_rels_root.findall(f"{{{PKG_REL_NS}}}Relationship"):
        rid_to_target[rel.get("Id")] = os.path.basename(rel.get("Target", ""))

    children = list(sld_id_lst)
    inserted = False

    target_filter = after_slide or before_slide
    if target_filter:
        for idx, child in enumerate(children):
            c_rid = child.get(f"{{{R_NS}}}id") or child.get("id")
            c_target = rid_to_target.get(c_rid, "")
            if c_target == target_filter:
                if after_slide:
                    sld_id_lst.insert(idx + 1, new_sld)
                else:
                    sld_id_lst.insert(idx, new_sld)
                inserted = True
                break

    if not inserted:
        sld_id_lst.append(new_sld)

    pres_tree.write(pres_xml, encoding="utf-8", xml_declaration=True)
    print(f"Created ppt/slides/{new_slide_name} from {src_slide} (Slide ID: {new_sid}, rId: {new_rid})")
    return new_slide_name

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    unpacked = sys.argv[1]
    src = sys.argv[2]
    after = None
    before = None

    i = 3
    while i < len(sys.argv):
        if sys.argv[i] == "--after" and i + 1 < len(sys.argv):
            after = sys.argv[i+1]
            i += 2
        elif sys.argv[i] == "--before" and i + 1 < len(sys.argv):
            before = sys.argv[i+1]
            i += 2
        else:
            i += 1

    duplicate_slide(unpacked, src, after_slide=after, before_slide=before)
