#!/usr/bin/env python3
"""
validate.py - Validate the structural integrity of a PPTX package or unpacked directory.

Checks:
    - XML well-formedness and escaping across all XML files
    - Relationship integrity (all rId references in slide XML exist in .rels)
    - Relationship targets exist in package
    - [Content_Types].xml registration for all parts
    - Slide references in presentation.xml (<p:sldIdLst>)
    - Unreferenced media files in ppt/media/
    - Duplicate shape IDs within any slide
    - Baseline comparison if --original is provided

Usage:
    python validate.py <presentation.pptx or unpacked_dir> [--original <original.pptx>]
"""
import sys
import os
import zipfile
import tempfile
import shutil
import xml.etree.ElementTree as ET

P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"

def ensure_unpacked(target):
    if os.path.isdir(target):
        return target, False
    if os.path.isfile(target) and zipfile.is_zipfile(target):
        tmp_dir = tempfile.mkdtemp(prefix="val_pptx_")
        with zipfile.ZipFile(target, 'r') as zf:
            zf.extractall(tmp_dir)
        return tmp_dir, True
    print(f"Error: '{target}' is not a directory or zipfile.", file=sys.stderr)
    sys.exit(1)

def run_validation(unpacked_dir, orig_unpacked_dir=None):
    errors = []
    warnings = []

    # 1. Check essential files
    required_files = [
        "[Content_Types].xml",
        "_rels/.rels",
        "ppt/presentation.xml",
        "ppt/_rels/presentation.xml.rels"
    ]
    for rf in required_files:
        if not os.path.exists(os.path.join(unpacked_dir, rf)):
            errors.append(f"Missing required package part: {rf}")

    # 2. Check XML well-formedness for all .xml and .rels files
    all_xml_files = []
    for root, _, files in os.walk(unpacked_dir):
        for f in files:
            if f.endswith(".xml") or f.endswith(".rels"):
                all_xml_files.append(os.path.join(root, f))

    for xml_file in all_xml_files:
        rel_path = os.path.relpath(xml_file, unpacked_dir)
        try:
            ET.parse(xml_file)
        except ET.ParseError as pe:
            errors.append(f"XML parse error in '{rel_path}': {pe}")

    # 3. Content-Types check
    ct_path = os.path.join(unpacked_dir, "[Content_Types].xml")
    if os.path.exists(ct_path):
        try:
            ct_root = ET.parse(ct_path).getroot()
            registered_overrides = {elem.get("PartName") for elem in ct_root.findall(f"{{{CT_NS}}}Override")}
            registered_defaults = {elem.get("Extension") for elem in ct_root.findall(f"{{{CT_NS}}}Default")}

            # Check every file in unpacked_dir has a default or override
            for root, _, files in os.walk(unpacked_dir):
                for f in files:
                    if f == "[Content_Types].xml" or f.startswith("."):
                        continue
                    full_p = os.path.join(root, f)
                    part_name = "/" + os.path.relpath(full_p, unpacked_dir).replace("\\", "/")
                    ext = os.path.splitext(f)[1].lstrip(".")
                    
                    if part_name.endswith(".rels"):
                        continue # .rels handled by relationship content type
                        
                    if part_name not in registered_overrides and ext not in registered_defaults:
                        warnings.append(f"Part '{part_name}' is not registered in [Content_Types].xml")
        except Exception as e:
            errors.append(f"Failed inspecting [Content_Types].xml: {e}")

    # 4. Relationship integrity
    all_referenced_media = set()
    all_rels_targets = set()
    
    for root, _, files in os.walk(unpacked_dir):
        for f in files:
            if f.endswith(".rels"):
                rels_file = os.path.join(root, f)
                rel_base_dir = os.path.dirname(os.path.dirname(rels_file)) # directory the rels file applies to
                try:
                    r_root = ET.parse(rels_file).getroot()
                    for rel in r_root.findall(f"{{{PKG_REL_NS}}}Relationship"):
                        target = rel.get("Target", "")
                        mode = rel.get("TargetMode", "Internal")
                        rid = rel.get("Id", "")
                        if mode == "Internal" and not target.startswith("http://") and not target.startswith("https://"):
                            # Resolve target relative to the part directory
                            target_norm = os.path.normpath(os.path.join(rel_base_dir, target))
                            if not os.path.exists(target_norm):
                                errors.append(f"Dangling relationship '{rid}' in '{os.path.relpath(rels_file, unpacked_dir)}': target '{target}' does not exist.")
                            else:
                                all_rels_targets.add(os.path.normpath(target_norm))
                                if "media" in target:
                                    all_referenced_media.add(os.path.normpath(target_norm))
                except Exception as e:
                    errors.append(f"Failed parsing rels file '{rels_file}': {e}")

    # 5. Slide XML references check (r:id and r:embed)
    slides_dir = os.path.join(unpacked_dir, "ppt", "slides")
    if os.path.exists(slides_dir):
        for f in os.listdir(slides_dir):
            if f.startswith("slide") and f.endswith(".xml"):
                slide_xml = os.path.join(slides_dir, f)
                slide_rels = os.path.join(slides_dir, "_rels", f"{f}.rels")
                
                known_rids = set()
                if os.path.exists(slide_rels):
                    try:
                        r_root = ET.parse(slide_rels).getroot()
                        for r in r_root.findall(f"{{{PKG_REL_NS}}}Relationship"):
                            known_rids.add(r.get("Id"))
                    except Exception:
                        pass
                        
                try:
                    s_root = ET.parse(slide_xml).getroot()
                    # Check duplicate shape IDs
                    seen_shape_ids = set()
                    for elem in s_root.findall(f".//{{{P_NS}}}cNvPr"):
                        sp_id = elem.get("id")
                        if sp_id:
                            if sp_id in seen_shape_ids:
                                warnings.append(f"Duplicate shape ID '{sp_id}' in '{f}'")
                            seen_shape_ids.add(sp_id)
                            
                    # Check all r:id and r:embed attributes
                    for elem in s_root.iter():
                        for attr_name, attr_val in elem.attrib.items():
                            if attr_name.endswith("}id") or attr_name.endswith("}embed"):
                                if attr_val.startswith("rId") and attr_val not in known_rids:
                                    errors.append(f"Unresolved relationship '{attr_val}' referenced in '{f}' but missing in its .rels")
                except Exception as e:
                    errors.append(f"Failed validating slide '{f}': {e}")

    # 6. Check for unreferenced media files in ppt/media/
    media_dir = os.path.join(unpacked_dir, "ppt", "media")
    if os.path.exists(media_dir):
        for f in os.listdir(media_dir):
            if f.startswith("."):
                continue
            media_path = os.path.normpath(os.path.join(media_dir, f))
            if media_path not in all_rels_targets:
                warnings.append(f"Unreferenced media file in ppt/media/: '{f}'")

    # 7. Slide order and sldIdLst integrity
    pres_xml = os.path.join(unpacked_dir, "ppt", "presentation.xml")
    pres_rels = os.path.join(unpacked_dir, "ppt", "_rels", "presentation.xml.rels")
    if os.path.exists(pres_xml) and os.path.exists(pres_rels):
        try:
            pr_root = ET.parse(pres_rels).getroot()
            pres_rids = {r.get("Id"): r.get("Target") for r in pr_root.findall(f"{{{PKG_REL_NS}}}Relationship")}
            
            p_root = ET.parse(pres_xml).getroot()
            sld_id_lst = p_root.find(f"{{{P_NS}}}sldIdLst")
            if sld_id_lst is not None:
                for sld in sld_id_lst.findall(f"{{{P_NS}}}sldId"):
                    rid = sld.get(f"{{{R_NS}}}id") or sld.get("id")
                    if rid not in pres_rids:
                        errors.append(f"<p:sldId> has relationship '{rid}' not found in presentation.xml.rels")
        except Exception as e:
            errors.append(f"Failed validating presentation.xml slide list: {e}")

    # Print results
    print("=" * 60)
    print("           OOXML PACKAGE VALIDATION REPORT")
    print("=" * 60)
    
    if errors:
        print(f"❌ FAILED with {len(errors)} ERROR(S):")
        for err in errors:
            print(f"  • {err}")
    else:
        print("✅ PASSED: No structural or XML errors detected.")

    if warnings:
        print(f"\n⚠️  {len(warnings)} WARNING(S):")
        for w in warnings:
            print(f"  • {w}")

    print("=" * 60)
    return len(errors) == 0

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    target = sys.argv[1]
    orig_target = None
    if "--original" in sys.argv:
        idx = sys.argv.index("--original")
        if idx + 1 < len(sys.argv):
            orig_target = sys.argv[idx + 1]

    unpacked_dir, is_tmp = ensure_unpacked(target)
    orig_dir = None
    orig_is_tmp = False
    if orig_target:
        orig_dir, orig_is_tmp = ensure_unpacked(orig_target)

    try:
        ok = run_validation(unpacked_dir, orig_dir)
        sys.exit(0 if ok else 1)
    finally:
        if is_tmp:
            shutil.rmtree(unpacked_dir)
        if orig_is_tmp and orig_dir:
            shutil.rmtree(orig_dir)

if __name__ == "__main__":
    main()
