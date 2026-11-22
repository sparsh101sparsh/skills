"""
Unit test suite for Milestone M1: Core Architecture & Invariant Encoding in thenuke.
Verifies SKILL.md integrity, 12-section architecture, 6 dimensions, 0 Devanagari,
code fence parity, make_formula_box, natural section flow, and forbidden names QA.
"""

import re
from pathlib import Path
import pytest
from reportlab.platypus import Paragraph, KeepTogether, Table, Spacer, PageBreak
from reportlab.lib.colors import HexColor

from scripts.diagramming.reportlab_engine import ReferenceManualBuilder, latex_to_reportlab_html, compute_table_col_widths
from scripts.qa.qa_audit_engine import run_pass2_textual


def test_skill_md_structure_and_frontmatter():
    """Verify that SKILL.md exists, has valid YAML frontmatter, 12 sections, and 6 dimensions."""
    skill_path = Path("/Users/iamsparsh00321/.gemini/config/skills/thenuke/SKILL.md")
    assert skill_path.exists(), "SKILL.md must exist at the expected path."
    text = skill_path.read_text(encoding="utf-8")

    # Frontmatter check
    assert text.startswith("---"), "SKILL.md must start with YAML frontmatter delimiter."
    parts = text.split("---", 2)
    assert len(parts) >= 3, "Frontmatter must have opening and closing delimiters."
    frontmatter = parts[1]
    assert "name: thenuke" in frontmatter
    assert "version: 3.0.0" in frontmatter
    assert "@issparsh" in frontmatter

    # 12 Sections check
    for sec in range(1, 13):
        pattern = rf"## {sec}\. "
        match = re.search(pattern, text)
        assert match, f"Section {sec} missing from SKILL.md!"

    # 6 Dimensions check
    dimensions = [
        "Zero Synthetic Fluff & Lecture Parity Protocol (Dimension 1)",
        "Full-Stream Vision & Scene-Change OCR Specification (Dimension 2)",
        "ReportLab Typography & Layout Engine Contract (Dimension 3)",
        "Pre-Flight Syntax & Parity Verification Gates (Dimension 4)",
        "Provenance & Exact Lecture Manifest Standards (Dimension 5)",
        "Core Non-Negotiables & Author Branding (Dimension 6)",
    ]
    for dim in dimensions:
        assert dim in text, f"Dimension '{dim}' not found in SKILL.md!"


def test_skill_md_zero_devanagari_and_code_fence_parity():
    """Verify 0 Devanagari characters and balanced code fences in SKILL.md."""
    skill_path = Path("/Users/iamsparsh00321/.gemini/config/skills/thenuke/SKILL.md")
    text = skill_path.read_text(encoding="utf-8")

    # Zero Devanagari invariant
    deva_regex = re.compile(r"[\u0900-\u097F\uA8E0-\uA8FF\u1CD0-\u1CFF\U00011B00-\U00011B5F]")
    deva_hits = list(deva_regex.finditer(text))
    assert len(deva_hits) == 0, f"Found {len(deva_hits)} Devanagari characters in SKILL.md!"

    # Code fence parity
    fences = [line for line in text.splitlines() if line.strip().startswith("```")]
    assert len(fences) % 2 == 0, f"Unbalanced code fences in SKILL.md: total count {len(fences)} is odd."

    # Check required invariant strings
    assert "Prepared by @issparsh" in text
    assert "5-Token / 7-Shade Monochrome Palette" in text
    assert "make_formula_box" in text
    assert "latex_to_reportlab_html" in text
    assert "select='gt(scene,0.015)+eq(n,0)',fps=0.33" in text
    assert "stripTypeScriptTypes" in text
    assert "ast.parse" in text


def test_make_formula_box_flowable(tmp_path):
    """Verify that ReferenceManualBuilder.make_formula_box generates a KeepTogether formula card."""
    engine = ReferenceManualBuilder(output_path=tmp_path / "test.pdf", branding="Prepared by @issparsh")
    box = engine.make_formula_box(r"\frac{a+b}{2} \le \sqrt{ab}")
    assert isinstance(box, KeepTogether), "make_formula_box must return a KeepTogether flowable."
    elements = box._content
    assert len(elements) == 3
    assert isinstance(elements[0], Spacer)
    assert isinstance(elements[1], Table)
    assert isinstance(elements[2], Spacer)


def test_natural_section_flow_no_double_pagebreak(tmp_path):
    """Verify that # PART followed by # MODULE 01 does not emit double PageBreak."""
    engine = ReferenceManualBuilder(output_path=tmp_path / "test.pdf", branding="Prepared by @issparsh")
    md_content = """# Title
## Syllabus
1. Part I

# PART I — CORE ARCHITECTURE
# MODULE 01: Systems Runtime
Here is the narrative body text of section 1.
"""
    story = engine.parse_markdown_to_flowables(md_content)
    page_break_count = sum(1 for e in story if isinstance(e, PageBreak))
    # Cover to Syllabus (1), Syllabus to Content (1), PART I starts fresh page (1)
    # But MODULE 01 must NOT trigger an additional PageBreak immediately after PART I
    assert page_break_count <= 3, f"Expected <= 3 PageBreaks, got {page_break_count} (unwanted blank divider page)"


def test_qa_audit_flags_forbidden_names(tmp_path):
    """Verify that qa_audit_engine flags forbidden instructor/channel names."""
    test_md = tmp_path / "test_forbidden.md"
    test_md.write_text(
        "# Test Document\n\nPrepared by @issparsh\n\nIn this lecture by hitesh we learn JavaScript.",
        encoding="utf-8",
    )
    res = run_pass2_textual(test_md, profile="general")
    assert not res.passed, "Document containing forbidden instructor name must fail QA Pass 2."
    forbidden_violations = [v for v in res.rendering_violations if "Forbidden name" in v]
    assert len(forbidden_violations) >= 1, "Expected forbidden name violation to be detected."


def test_math_parser_nested_fractions_and_formatting():
    """Verify that latex_to_reportlab_html handles nested fractions and inner formatting without losing division operators."""
    # Test 1: Fraction with bold formatting inside denominator
    res1 = latex_to_reportlab_html(r"\frac{a}{\mathbf{b}}")
    assert "/" in res1 and "<b>b</b>" in res1, f"Expected fraction with <b>b</b>, got {res1}"

    # Test 2: Nested fractions
    res2 = latex_to_reportlab_html(r"\frac{\frac{a}{b}}{c}")
    assert "/" in res2 and "c" in res2 and "b" in res2, f"Expected nested fractions, got {res2}"

    # Test 3: Fraction with text descriptions in numerator and denominator
    res3 = latex_to_reportlab_html(r"\frac{\text{loss}}{\text{total}}")
    assert "/" in res3 and "loss" in res3 and "total" in res3, f"Expected '(loss / total)', got {res3}"

    # Test 4: Nested fraction with square roots and bold operators
    res4 = latex_to_reportlab_html(r"\frac{\sqrt{x}}{\mathbf{W} + \mathbf{b}}")
    assert "/" in res4 and "&radic;" in res4 and "<b>W</b>" in res4 and "<b>b</b>" in res4, f"Expected formatted fraction, got {res4}"


def test_math_parser_underscore_shielding():
    """Verify that escaped underscores in identifiers are shielded from subscript mangling."""
    # Test 1: Programmatic identifier with escaped underscore
    res1 = latex_to_reportlab_html(r"\text{batch\_size}")
    assert res1 == "batch_size", f"Expected 'batch_size', got {res1}"

    # Test 2: Compound identifier with multiple underscores
    res2 = latex_to_reportlab_html(r"\text{PyObject\_Hash\_Values}")
    assert res2 == "PyObject_Hash_Values", f"Expected 'PyObject_Hash_Values', got {res2}"

    # Test 3: True subscript syntax must still work as subscripts (with font sizing)
    res3 = latex_to_reportlab_html(r"x_{total}")
    assert "<sub>" in res3 and "total" in res3, f"Expected subscript in {res3}"

    res4 = latex_to_reportlab_html(r"x_i")
    assert "<sub>" in res4 and "i" in res4, f"Expected subscript in {res4}"


def test_tier2_table_budgeting_floor_protection():
    """Verify that Tier 2 dynamic table budgeting with water-filling protects minimum column floors."""
    content_width = 475.0

    # Test 1: 7-column highly asymmetric table where Column 0 dominates
    weights_7col = [1000, 12, 12, 12, 12, 12, 12]
    widths_7col = compute_table_col_widths(7, weights_7col, content_width=content_width)
    assert len(widths_7col) == 7
    # For num_cols >= 5, min_w is 48.0 pt
    for col_idx, w in enumerate(widths_7col):
        assert w >= 48.0, f"Column {col_idx} width {w} violates minimum floor 48.0 pt in 7-col table!"
    assert abs(sum(widths_7col) - content_width) < 0.1, f"Total width {sum(widths_7col)} != {content_width}"
    # Clamped narrow columns should be exactly 48.0 pt
    for c in range(1, 7):
        assert widths_7col[c] == 48.0
    assert widths_7col[0] == 187.0

    # Test 2: 4-column asymmetric table (min_w is 60.0 pt)
    weights_4col = [500, 10, 10, 10]
    widths_4col = compute_table_col_widths(4, weights_4col, content_width=content_width)
    assert len(widths_4col) == 4
    for col_idx, w in enumerate(widths_4col):
        assert w >= 60.0, f"Column {col_idx} width {w} violates minimum floor 60.0 pt in 4-col table!"
    assert abs(sum(widths_4col) - content_width) < 0.1, f"Total width {sum(widths_4col)} != {content_width}"

    # Test 3: 3-column asymmetric table (min_w is 85.0 pt)
    weights_3col = [300, 5, 5]
    widths_3col = compute_table_col_widths(3, weights_3col, content_width=content_width)
    assert len(widths_3col) == 3
    for col_idx, w in enumerate(widths_3col):
        assert w >= 85.0, f"Column {col_idx} width {w} violates minimum floor 85.0 pt in 3-col table!"
    assert abs(sum(widths_3col) - content_width) < 0.1, f"Total width {sum(widths_3col)} != {content_width}"
