---
name: thenuke
description: >
  thenuke is an authoritative multi-modal documentation and engineering reference manual
  engine that ingests video lectures (YouTube), web documentation, and competitive programming
  problems, synthesizing 100% lecture-grounded, production-grade reference manuals in Roman-alphabet
  Hinglish (zero Devanagari) with authentic vector typography, monochrome aesthetics, and
  author branding (@issparsh with the official vector X logo).
version: 3.0.0
authors:
  - "@issparsh"
  - "@sumitsingh097"
tags:
  - documentation
  - reference-manual
  - reportlab
  - roman-hinglish
  - zero-devanagari
  - machine-vision-ocr
  - apple-silicon-ocr
  - scene-change-detection
  - zero-synthetic-fluff
  - lecture-parity
  - latex-math
  - competitive-programming
  - monochrome-palette
  - vector-diagrams
  - multi-agent
---

# thenuke — Multi-Modal Documentation & Engineering Reference Engine

> Koi bhi resource lo — YouTube playlist, web docs, local PDF, competitive programming problems — aur ek production-grade
> engineering reference manual banao in Roman Hinglish. Zero Devanagari characters. Always.

---

## 1. Quick Start & Execution Pipelines

### Command Line Interface (`thenuke_cli.py`)

```bash
# 🚀 Multi-Agent Autonomous Pipeline (Recommended):
# Coordinates Architect, Researcher, Writer, Diagrammer, and Reviewer agents
python thenuke_cli.py multi-agent --topic Git --output ~/Downloads/Git_Complete_Reference_Manual.pdf

# Interactive /grill-me Clarification Interview Mode:
python thenuke_cli.py multi-agent --topic Git --interactive

# Full Ingestion + Multi-Agent Pipeline:
python thenuke_cli.py run \
  "https://www.youtube.com/playlist?list=PLlasXeu85E9cQ32gLCvAvr9vNaUccPVNP" \
  "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide" \
  "/Users/yourname/Downloads/JS_Notes.pdf"

# 🏆 Competitive Programming Problem Reference Manual:
# Inspect/fetch problem statement with full math and samples:
python thenuke_cli.py fetch-problem "https://www.codechef.com/problems/FLOW001"
python thenuke_cli.py fetch-problem "https://www.hackerrank.com/challenges/simple-array-sum/problem"
python thenuke_cli.py fetch-problem "https://www.geeksforgeeks.org/problems/missing-number-in-array1416/1"
python thenuke_cli.py fetch-problem "https://www.interviewbit.com/problems/max-sum-contiguous-subarray/"

# Full compilation to production-grade PDF:
python thenuke_cli.py run "https://codeforces.com/problemset/problem/1915/C" --preset senior_architect_faang --skip-cleanup

# 📚 Canonical Git Reference Manual Compiler:
python thenuke_cli.py compile-git --output output/Git_Reference_Manual.pdf

# 📝 Grounded Extractive Notes Synthesizer (from arbitrary ingested sources):
python thenuke_cli.py ingest-notes "https://youtu.be/..." --topic "Modern Distributed Systems" --output output/Notes.pdf

# 📐 Academic Mathematical Explanation & Typesetting:
python thenuke_cli.py explain-math conditional-probability --output output/Conditional_Probability.pdf

# Individual Pipeline Stages:
python thenuke_cli.py ingest "https://youtube.com/..." # Fast path: subtitles only (use --download-video for full streams)
python thenuke_cli.py grill --preset senior_architect_faang
python thenuke_cli.py synthesize
python thenuke_cli.py compile output/thenuke_manual_*.md --branding "Prepared by @issparsh"
python thenuke_cli.py qa output/thenuke_manual_*.pdf --profile auto --report output/qa_report.json
python thenuke_cli.py clean
```

### Installation

```bash
# Editable install with core runtime dependencies:
pip install -e .

# Or install from pinned requirements:
pip install -r requirements.txt

# Optional capability extras:
pip install -e ".[cp]"          # Competitive programming tools (online-judge-tools)
pip install -e ".[whisper]"     # Local audio transcription fallback (faster-whisper)
pip install -e ".[dev]"         # Test suite runner & dev tools (pytest)
pip install -e ".[cp,whisper,dev]" # All optional extras
```

### Seven Core Pipeline Stages

| Stage | Subsystem | Description | Primary Operational Artifacts |
| :--- | :--- | :--- | :--- |
| **1. Ingest** | `scripts/ingestion/` | Multi-source crawler: Subtitles fast-path, scene-change video extraction, Apple Silicon Neural OCR, web scraper, CP fetchers. | `nuke_ingestion_corpus.json`, `full_stream_ocr_results.json` |
| **2. Grill** | `scripts/grilling/` | Interactive user interview (`/grill-me`): Depth levels, visual thresholds, audience profile. | `grilling_profile.json` |
| **3. Multi-Agent** | `scripts/multi_agent/` | Autonomous team: Architect, Researcher, Writer, Diagrammer, Reviewer. | `thenuke_manual_*.md`, evidence spans |
| **4. Vector Engine** | `scripts/diagramming/` | Native ReportLab Drawing vectors (DAGs, Memory Heaps, Call Stacks, ASTs). | Rendered PDF flowables, PNG fallback cache |
| **5. PDF Compiler** | `reportlab_engine.py` | Two-pass ISO A4 Platypus compiler: Natural section flow, formula cards, dynamic table budgeting. | Publication-grade ISO A4 PDF |
| **6. 6-Gate QA** | `scripts/qa/` + Verifiers | Automated gates: File integrity, 0 Devanagari, 0 forbidden names, AST syntax, code fence parity, 150 DPI raster QA. | `qa_report.json`, terminal gate reports |
| **7. Cleanup** | `thenuke_cli.py clean` | Post-clearance permanent wipe of scratch video frames, demuxed audio, and raw HTML. | Empty scratch workspaces |

### System Data Flow Architecture

```
[Multi-Modal Sources]
   ├── YouTube Video Lectures / Playlists  ──► Subtitles Fast-Path (1-2s) OR Scene-Change Extraction (0.33 fps)
   ├── Web URLs & API Specs                ──► Headless Crawler & Markdown Extractors
   ├── Competitive Programming Problems    ──► Official Platform APIs & oj-api
   └── Local Course Archives (/Volumes/...) ──► ffmpeg Hardware Decoder + Apple Vision Neural Engine OCR
              │
              ▼
[R1: Grounded Evidence Ingestion]
   ├── Audio Transcripts (Timestamped Cues)
   ├── Machine Vision OCR Frames (Timestamp Synchronized: |t_audio - t_ocr| <= 30s)
   └── CorpusIndexer ──► EvidenceSpans (Zero Synthetic Fluff, Native Primitives Only)
              │
              ▼
[R2: Grilling & Curriculum Architectural Scoping]
   ├── Level: foundations | resource_parity | senior_architect
   ├── Visual: strict_need_based | balanced | diagram_dense
   └── Audience: faang_interview | production_engineering | academic
              │
              ▼
[R3: Synthesis & Verification Engine]
   ├── 100% Roman-alphabet Hinglish (0 Devanagari characters)
   ├── 0 Forbidden Instructor/Channel Names
   ├── Seamless Flowable Hierarchy (# PART + # MODULE 01 on same page; zero blank divider pages)
   ├── Code Block Parity & AST Validation (Node.js stripTypeScriptTypes & CPython ast.parse)
   └── Formula Cards Flowables (latex_to_reportlab_html + make_formula_box)
              │
              ▼
[R4: Publication-Grade ReportLab Compiler]
   ├── Two-Pass NumberedCanvas (Exact Page Counts, Running Headers & Footers)
   ├── Dynamic Content-Weighted Table Column Budgeting (Clamped to 48-85 pt floors)
   ├── Courier Type-1 Font Emoji Sanitization (WinAnsi bounds) & Max 50-Line Code Splitting
   └── Official Vector Twitter/X Glyph (12-vertex + 4-vertex polygons) + "Prepared by @issparsh"
              │
              ▼
[R5: Multi-Gate Automated Pre-Flight Suite (Gates 1-6)]
   ├── Gate 1: Deliverables Integrity & File Size
   ├── Gate 2: Language & Forbidden Names Invariants
   ├── Gate 3: Executable AST Validation (Python & TypeScript)
   ├── Gate 4: Code Fence Parity Balance Audit
   ├── Gate 5: Diagram Registry & 2x PNG Cache Audit
   └── Gate 6: 150 DPI Page-by-Page Visual Raster QA
              │
              ▼
[R6: Publication Release & Secure Cleanup]
   ├── Output Manual: output/<Title>_The_Master_Reference_Manual.pdf & .md
   ├── Master Resources Manifest: output/Master_Resources_Manifest.pdf (Exact 1-Page ISO A4)
   └── Scratch Wipe: Removal of downloaded MP4s, temporary JPEGs, and demuxed audio
```

---

## 2. 🔒 Core Non-Negotiables & Author Branding (Dimension 6)

Under all circumstances, every manual, document, script, and PDF generated by `thenuke` must strictly comply with the following zero-tolerance invariants. Any violation halts publication immediately.

### Invariant 1: Strictly 100% Roman Hinglish — Zero Devanagari Characters
- **Rule:** Every single character across markdown sources, code blocks, diagram labels, and compiled PDF text layers must belong to the Roman/Latin alphabet (`a-z, A-Z, 0-9`, standard punctuation).
- **Zero Devanagari Tolerance:** Not a single Devanagari character (`[\u0900-\u097F]`) is permitted anywhere in the deliverable.
- **Enforcement Regex:**
  ```python
  DEVANAGARI_REGEX = re.compile(
      r"[\u0900-\u097F\uA8E0-\uA8FF\u1CD0-\u1CFF\U00011B00-\U00011B5F]"
  )
  assert len(list(DEVANAGARI_REGEX.finditer(content))) == 0
  ```
- **Dual-Register Cadence:**
  - *Pedagogical Bridges (Spoken Roman Hinglish):* `"Technically bolo toh..."`, `"Sabse pehle memory layout samjho..."`, `"Gotcha ye hai ki..."`, `"Under the hood yahan pointer swap ho raha hai..."`
  - *Technical Rigor (Formal English):* `Call Stack`, `Memory Heap`, `Lexical Environment Record`, `Epoll Event Demultiplexer`, `Double-Entry Ledger`.

### Invariant 2: Strictly 0 Forbidden Instructor/Channel Names
- **Rule:** Under zero circumstances may instructor names or YouTube channel names appear in manual prose, code comments, diagram annotations, or PDF text layers.
- **Banned Names List:**
  `sriniously`, `chai aur code`, `sheryians`, `hitesh`, `harsh`, `harry`, `dsthakurrawat`.
- **Enforcement Regex (Case-Insensitive):**
  ```python
  FORBIDDEN_NAME_PATTERNS = [
      (re.compile(r"\bsriniously\b", re.IGNORECASE), "sriniously"),
      (re.compile(r"\bchai\s+aur\s+code\b", re.IGNORECASE), "chai aur code"),
      (re.compile(r"\bsheryians\b", re.IGNORECASE), "sheryians"),
      (re.compile(r"\bhitesh\b", re.IGNORECASE), "hitesh"),
      (re.compile(r"\bharsh\b", re.IGNORECASE), "harsh"),
      (re.compile(r"\bharry\b", re.IGNORECASE), "harry"),
      (re.compile(r"\bdsthakurrawat\b", re.IGNORECASE), "dsthakurrawat"),
  ]
  for pattern, label in FORBIDDEN_NAME_PATTERNS:
      assert not pattern.search(content), f"Found forbidden name '{label}'"
  ```

### Invariant 3: Official Vector Author Branding & 𝕏 Glyph
- **Primary Branding String:** `Prepared by @issparsh`
- **Dual-Author Variant (where configured):** `Prepared by @issparsh @sumitsingh097`
- **Location:** Rendered on 100% of non-cover footers (strictly suppressed on the cover page).
- **Authentic Vector Twitter/𝕏 Geometry:**
  Never use Unicode character `𝕏` (U+1D54F) in ReportLab text strings; it does not exist in Type-1 PostScript Helvetica/Courier fonts and causes font encoding crashes or tofu replacement boxes. The logo must be drawn programmatically onto the canvas using exact vector polygon coordinates:
  ```python
  def draw_twitter_x_logo(canvas, x: float, y: float, size: float = 7.5):
      canvas.saveState()
      canvas.setFillColor(HexColor("#222222"))
      canvas.setStrokeColor(HexColor("#222222"))
      scale = size / 24.0

      # Primary Polygon: 12 vertices (thick arm and outer facets)
      poly1 = [
          (18.244, 2.25), (21.552, 2.25), (14.325, 10.51), (22.827, 21.75),
          (16.170, 21.75), (10.956, 14.933), (4.990, 21.75), (1.680, 21.75),
          (9.410, 12.915), (1.254, 2.25), (8.080, 2.25), (12.793, 8.481),
      ]
      # Crossing Polygon: 4 vertices (thin crossing arm)
      poly2 = [
          (17.083, 19.770), (18.916, 19.770), (7.084, 4.126), (5.117, 4.126),
      ]

      p = canvas.beginPath()
      p.moveTo(x + poly1[0][0] * scale, y + size - poly1[0][1] * scale)
      for px, py in poly1[1:]:
          p.lineTo(x + px * scale, y + size - py * scale)
      p.close()

      p.moveTo(x + poly2[0][0] * scale, y + size - poly2[0][1] * scale)
      for px, py in poly2[1:]:
          p.lineTo(x + px * scale, y + size - py * scale)
      p.close()

      canvas.drawPath(p, fill=1, stroke=0)
      canvas.restoreState()
  ```

### Invariant 4: Strict 5-Token / 7-Shade Monochrome Palette
All manuals adhere strictly to a publication monochrome aesthetic. Color accents (red, green, blue) are forbidden unless rendering syntax highlighting in code listings:

| Token Name | Hex Value | Typographic & Architectural Role |
| :--- | :--- | :--- |
| `COLOR_BLACK` | `#000000` | Cover titles, major `# PART` openers, table header bold text, heavy horizontal rules (1.2–1.5 pt). |
| `COLOR_CHARCOAL` | `#222222` | Body prose font, section headers (`## `, `### `), table header backgrounds, vector 𝕏 logo fill. |
| `COLOR_DARK_GREY` | `#444444` | Chapter horizontal dividing rules (0.75 pt), callout border accents, code listing text. |
| `COLOR_MUTED` | `#666666` | Running headers, running footers, page count indicators ("Page X of Y"), metadata labels. |
| `COLOR_HAIRLINE` | `#CCCCCC` | Running header/footer dividing rules (0.5 pt), table grids, formula card borders, callout boxes. |
| `COLOR_BG_CARD` | `#F8F8F8` / `#F5F5F5` | Centered formula card backgrounds (`make_formula_box`), callout backgrounds, alternating table rows. |
| `COLOR_WHITE` | `#FFFFFF` | Document canvas, primary table cell backgrounds, white table header text. |

### Invariant 5: 100% Executable AST Validation
Every code listing in a reference manual must be syntactically valid and executable. No incomplete pseudocode, invalid tokens, or unclosed syntax brackets:
- **Python Code Listings:** Must pass CPython `ast.parse(source, mode="exec")`. REPL prompts (`>>> `) are parsed via `doctest.DocTestParser()`. Top-level `await` statements are automatically wrapped in `async def __verify_wrapper():` to validate async syntax.
- **TypeScript Code Listings:** Must pass Node.js V8 `stripTypeScriptTypes(code)`. (Standard TypeScript constructor parameter properties and enums are explicitly permitted).

---

## 3. 🚫 Zero Synthetic Fluff & Lecture Parity Protocol (Dimension 1)

### 1. The Grounding Invariant
- **100% Authentic Grounding:** Every conceptual model, code pattern, algorithm, interface, class, and architectural diagram in a reference manual MUST originate directly from the source video lectures, companion slide decks, or extracted OCR code frames.
- **Zero Page-Count Quota Padding:**
  - Page count is strictly an emergent property of the lecture's authentic informational density.
  - Never add synthetic boilerplate, imaginary enterprise patterns, or unmentioned third-party libraries simply to reach an arbitrary page count.
  - User trajectory mandate: *"who said there is requirement for any page count dumb fking ass also remove all synthetic conteent"* (Step 4360).

### 2. Forbidden Synthetic Fluff Blacklist
In any curriculum where the instructor taught native language primitives (e.g. native TypeScript types, native CPython runtime, native Node.js HTTP/fs), the manual MUST contain ONLY native primitives.
Introducing unmentioned enterprise frameworks to artificially inflate complexity is strictly forbidden:

```python
SYNTHETIC_FLUFF_TERMS = [
    "Kafka",
    "Redis",
    "Zod",
    "InMemoryCrudRepository",
    "ProductionRedisClusterManager",
    "DistributedLockRegistry",
    "ExtendedApplicationRequest",
    "mediaReducer",
    "DeepReadonly",
]
```

- ❌ **BANNED in courses where unmentioned:**
  - Message queues: Kafka, RabbitMQ, BullMQ.
  - Caching layers: Redis, Memcached (unless explicitly taught in Backend systems).
  - Validation libraries: Zod, Joi, Yup.
  - Containerization / Cloud: Docker, Kubernetes, AWS S3 (unless part of the source syllabus).
  - Synthetic enterprise mock patterns: `InMemoryCrudRepository<T>`, `ProductionRedisClusterManager`, `DistributedLockRegistry`.
  - Academic textbook filler: "Fallacies of Distributed Computing", academic IoC containers, Saga/2PC distributed transactions in practical introductory courses.
- ✅ **PERMITTED ONLY:** Technologies, classes, and libraries explicitly demonstrated in the lecture videos and audio transcripts.

### 3. Anti-Toy-Code with Authentic Grounding
- **Definition:** "Anti-toy-code" means avoiding meaningless `foo`, `bar`, `baz`, `test123` identifiers in favor of the **authentic domain models used by the instructor** (e.g. `Sellable<T>` from TypeScript Domination; `PyObject` from CPython internals; `ApiError`/`ApiResponse` from Backend series).
- It does NOT mean inventing fictitious microservice architectures that were never taught.

---

## 4. 👁️ Full-Stream Vision & Scene-Change OCR Specification (Dimension 2)

### 1. High-Frequency Scene-Change Detection
Programming tutorials feature rapid code modifications, interactive terminal execution, and dynamic slide animations. Naive static sampling (e.g. 1 frame every 60s) misses over 90% of live code changes.
The pipeline evaluates high-frequency scene transitions across the entire video stream:

- **Hardware Acceleration:** Uses Apple Silicon VideoToolbox (`-hwaccel videotoolbox`) on macOS, or NVDEC/VA-API on Linux.
- **FFmpeg Scene-Change Filter:**
  ```bash
  ffmpeg -hwaccel videotoolbox -y -i "{video_path}" \
    -vf "select='gt(scene,0.015)+eq(n,0)',fps=0.33" \
    -fps_mode vfr -q:v 2 -threads 4 \
    "{output_dir}/scene_%04d.jpg"
  ```
- **Frame Density Standard:** Multi-hour courses evaluate thousands of frames on local or external storage (`/Volumes/issparsh/`):
  - TypeScript Track (8.6 hours): 7,734 evaluated frames (4,667 active code frames).
  - Python & GenAI (8.0 hours): 6,240 evaluated frames (3,890 active code frames).
  - Backend Master (35.0 hours): 36,000+ evaluated frames (2,343 active code frames).

### 2. Apple Silicon Neural Engine OCR Pipeline
On macOS, machine vision OCR runs locally on the Apple Neural Engine via `Vision.framework` (`VNRecognizeTextRequest`) using PyObjC:
- **Accuracy Levels:**
  - `VNRequestTextRecognitionLevelAccurate`: Used for deep code inspection and intricate math typesetting (~0.3s/frame).
  - `VNRequestTextRecognitionLevelFast`: Used for real-time high-throughput stream scanning (~18–25 fps, 5–7 minutes for an entire 8-hour course).
- **Configuration:** `usesLanguageCorrection = True`, recognition languages `["en-US"]`.
- **Producer-Consumer Streaming Architecture:** FFmpeg decodes scene frames in the background while the Vision OCR worker processes them concurrently as they land on disk, checkpointing progress incrementally to JSON.

### 3. Chronological Transcript-Timeline Synchronization
Dumping OCR frames into disconnected JSON arrays destroys pedagogical context. Every active code frame MUST be mapped 1-to-1 against audio transcript cues based on chronological timestamp windows:
- **Temporal Alignment Window:** $|t_{transcript} - t_{ocr}| \le 15\text{s}$–$30\text{s}$.
- **Standard OCR Database Schema (`full_stream_ocr_results.json`):**
  ```json
  [
    {
      "video_id": "ts_domination_part1",
      "timestamp_seconds": 1845.2,
      "timestamp_formatted": "00:30:45",
      "frame_path": "frames/scene_0512.jpg",
      "ocr_text": "interface Sellable<T> {\n  title: string;\n  price: number;\n  metadata: T;\n}",
      "active_code": true,
      "transcript_sync_cue": "Ab yahan par hum Sellable interface define kar rahe hain jisme generic T metadata hold karega..."
    }
  ]
  ```
- **Duplicate Frame Decimation:** If consecutive scene frames have identical OCR text (`difflib.SequenceMatcher.ratio() >= 0.85`), redundant frames are decimated, preserving only true code state transitions and periodic 60s anchor keyframes.

### 4. Ingestion Invariants & Honest Communication
- **Subtitles-First Priority (Fast Path):**
  - Always attempt subtitle extraction first using `--skip-download` (`hi-orig,hi,en,en.*,hi.*`). Subtitles download in 1–2 seconds with zero video bandwidth consumption.
  - **CRITICAL INVARIANT:** NEVER invoke or claim Whisper processing when native YouTube subtitles are available. Whisper is strictly a fallback for videos with zero caption tracks.
- **Zero-Pretense Communication:**
  - State processing reality in plain language without deflection:
    *"Subtitles downloaded in 2 seconds. Video is 140 min (~1.4 GB). Downloading video stream in background for visual frame extraction..."*
  - NEVER claim that visual frame analysis was performed if frames were not extracted.

---

## 5. 📐 ReportLab Typography & Layout Engine Contract (Dimension 3)

### 1. Natural Section Flow & Zero Blank Divider Pages
- **The Divider Page Anti-Pattern:**
  Forcing unconditional `PageBreak()` on both `# PART` and `# MODULE` results in `# PART I` being placed alone on Page 4 with 95% blank space, followed by an immediate pagebreak to `# MODULE 01` on Page 5.
- **The Natural Flow Contract:**
  1. `# PART ...` initiates a new page via `add_page_break()`, rendering the Part title in `PhaseHeader` style (15 pt Helvetica-Bold) followed by a heavy dividing rule (`1.2 pt COLOR_BLACK`).
  2. `# MODULE ...` (or `## Chapter ...`) flows **IMMEDIATELY beneath `# PART` on the exact same page** with a `Spacer(1, 14)` and `ChapterHeader` style (12 pt Helvetica-Bold), followed immediately by Section 1.1, body narrative, and code listings.
  3. **Zero Blank Divider Pages:** Under zero circumstances may a page contain only a Part heading and whitespace.
- **Idempotent PageBreak Helper:**
  ```python
  def add_page_break(self, story: List[Any]) -> None:
      for elem in reversed(story):
          if isinstance(elem, PageBreak):
              return  # Already breaking page; do not duplicate
          if (
              isinstance(elem, SectionTracker)
              or isinstance(elem, HRFlowable)
              or (isinstance(elem, Spacer) and elem.height <= 10)
          ):
              continue
          break
      story.append(PageBreak())
  ```
- **Dangling Rule Suppression:** Suppress markdown `---` rules if the next immediate heading is a `# PART` or `# MODULE` to prevent orphan hairlines.

### 2. LaTeX Math Engine & Centered Formula Card Architecture
ReportLab's `Paragraph` flowable parses only limited XML tags (`<b>`, `<i>`, `<sub>`, `<sup>`). It crashes on raw LaTeX delimiters (`$`, `$$`) and macros (`\frac`, `\sqrt`).

- **In-Text Math Parser (`latex_to_reportlab_html`):**
  1. *Delimiter Stripping:* Strips leading/trailing `$$` or `$`.
  2. *Escaped Token Shielding:* Protects `\_` as `@@UNDERSCORE@@` to prevent false subscript matching on programmatic identifiers (e.g. `batch_size`, `PyObject_Hash`). Protects `\%`, `\{`, `\}`.
  3. *Balanced-Brace Fraction Parsing:*
     Recursively converts `\frac{num}{den}` $\to$ `(num / den)` using a depth-tracking state machine that correctly handles arbitrary nested braces.
  4. *Balanced-Brace Square Root Parsing:*
     Converts `\sqrt{inner}` $\to$ `√(inner)`.
  5. *Balanced-Brace Superscripts & Subscripts:*
     Converts `^{...}` $\to$ `<sup>...</sup>` and `_{...}` $\to$ `<sub>...</sub>`.
  6. *Unicode Operator Mapping:*
     `\sum` $\to$ `∑`, `\prod` $\to$ `∏`, `\approx` $\to$ `≈`, `\times` $\to$ `×`, `\cdot` $\to$ `·`, `\implies` $\to$ `⇒` (U+21D2 renders cleanly in Helvetica; U+27F9 fails), `\in` $\to$ `∈`, `\notin` $\to$ `∉`, `\le` $\to$ `≤`, `\ge` $\to$ `≥`, `\to` $\to$ `→`, `\infty` $\to$ `∞`.
  7. *Restoration & Entity Escaping:* Restores `@@UNDERSCORE@@` to `_`, escapes unmanaged `<` to `&lt;` and `&` to `&amp;`.

- **Dedicated Formula Card Flowable (`make_formula_box`):**
  Block mathematical expressions (`$$ ... $$`) must be rendered as isolated, centered formula cards:
  ```python
  def make_formula_box(self, math_content: str) -> Flowable:
      clean_html = latex_to_reportlab_html(math_content)
      p = safe_paragraph(
          f"<b>{clean_html}</b>", self.styles.get("Formula", self.styles["Body"])
      )
      table = Table([[p]], colWidths=[CONTENT_WIDTH])
      table.setStyle(
          TableStyle([
              ("BACKGROUND", (0, 0), (-1, -1), HexColor("#F8F8F8")),
              ("BOX", (0, 0), (-1, -1), 0.5, HexColor("#CCCCCC")),
              ("TOPPADDING", (0, 0), (-1, -1), 5.0),
              ("BOTTOMPADDING", (0, 0), (-1, -1), 5.0),
              ("LEFTPADDING", (0, 0), (-1, -1), 12.0),
              ("RIGHTPADDING", (0, 0), (-1, -1), 12.0),
              ("ALIGN", (0, 0), (-1, -1), "CENTER"),
          ])
      )
      return KeepTogether([Spacer(1, 2.5), table, Spacer(1, 3.5)])
  ```

### 3. Dynamic Content-Weighted Table Column Budgeting
Uniform table column widths (`CONTENT_WIDTH / N`) cause catastrophic rendering errors: narrow status columns get too much space while descriptive columns get squeezed into single-word vertical wraps.

- **2-Tier Table Budgeting Algorithm:**
  1. *Tier 1: Explicit Domain Profiles:* Use exact point budgets for canonical tables (e.g. 5-col syllabus table: `[52.0, 104.0, 68.0, 106.0, 145.0] pt`).
  2. *Tier 2: Content-Weighted Dynamic Budgeting (Iterative Floor Clamping / Water-Filling):*
     ```python
     col_weights = [max(12, len(header_row[c].strip())) for c in range(num_cols)]
     for r in data_rows:
         for c in range(min(num_cols, len(r))):
             col_weights[c] = max(col_weights[c], len(r[c].strip()))

     # Minimum width floor clamping prevents single-word vertical wrapping
     min_w = 48.0 if num_cols >= 5 else (60.0 if num_cols >= 4 else 85.0)
     min_w = min(min_w, CONTENT_WIDTH / num_cols)

     # Iterative floor clamping (water-filling): protect clamped columns from downward scaling
     raw_widths = [0.0] * num_cols
     fixed_cols = set()
     while True:
         unfixed_cols = [c for c in range(num_cols) if c not in fixed_cols]
         if not unfixed_cols:
             break
         unfixed_weight = sum(col_weights[c] for c in unfixed_cols) or 1.0
         avail_width = max(0.0, CONTENT_WIDTH - sum(raw_widths[c] for c in fixed_cols))
         newly_clamped = False
         for c in unfixed_cols:
             w = (col_weights[c] / unfixed_weight) * avail_width
             if w < min_w:
                 raw_widths[c] = min_w
                 fixed_cols.add(c)
                 newly_clamped = True
         if not newly_clamped:
             for c in unfixed_cols:
                 raw_widths[c] = (col_weights[c] / unfixed_weight) * avail_width
             break

     col_widths = [round(w, 2) for w in raw_widths]
     ```
- **Table Cell Typography:**
  - Header Row: `TableCellHead` (Helvetica-Bold 8.0 pt, `#FFFFFF` on `#222222` background).
  - Code Cells: `TableCellCode` (Courier 7.2 pt, leading 9.5 pt, `#000000`).
  - Prose Cells: `TableCellBody` (Helvetica 7.8 pt, leading 10.5 pt, `#222222`).
  - Alternating rows striped with `#F8F8F8`. Multi-page tables set `repeatRows = 1`. Short tables ($\le 10$ rows) wrapped in `KeepTogether`.

### 4. Code Block Splitting & Courier Type-1 Font Sanitization
- **Max 50-Line Splitting:** Long code blocks exceeding 36–50 lines must be split via `split_code_block` into `Part 1 of N`, `Part 2 of N` with `KeepTogether` on each part to eliminate massive white voids.
- **Line Wrapping:** Lines exceeding 72–88 characters must be cleanly wrapped via `wrap_code_text` preserving indentation.
- **Courier Type-1 Font Emoji Sanitization:**
  ReportLab's core Type-1 fonts (Helvetica, Courier) are bound to PostScript `WinAnsiEncoding` (single-byte 256-glyph table). Multi-byte UTF-8 emojis cause `UnicodeEncodeError` or corrupt into tofu (`'I'` or `\ufffd`).
  All emojis are stripped or converted to ASCII tags before PDF compilation:
  - `🎬` $\to$ `[VIDEO]` (or ASCII string in code)
  - `🚀` $\to$ `[LAUNCH]`
  - `💡` $\to$ `[NOTE]`
  - `⚠️` $\to$ `[WARNING]`
  - `✅` $\to$ `[OK]`
  - `❌` $\to$ `[FAIL]`
- **Control Character Remediation:**
  Remediate unescaped Python string escapes: Formfeed `\x0c` $\to$ `\frac`, Bell `\x07` $\to$ `\approx`, literal tabs in math keywords $\to$ restore `\`. Zero null bytes (`\x00`) allowed.

### 5. Two-Pass Canvas Architecture (`PublicationCanvas`)
- **Page Geometry (ISO A4):** Width = 595.276 pt, Height = 841.890 pt. Standard margins: Left/Right = 60.14 pt, Top/Bottom = 54.0 pt $\implies$ `CONTENT_WIDTH = 475.0 pt`.
- **Pass 1:** Saves canvas state on each `showPage()` and records dynamic section titles.
- **Pass 2:** In `save()`, knows exact total pages `num_pages`:
  - Running Header: Hairline rule at $y = 799.89\text{ pt}$ (0.5 pt `#CCCCCC`), left title in Helvetica-Bold 6.5 pt `#666666`, right section in Helvetica 6.5 pt `#666666`.
  - Running Footer: Hairline rule at $y = 46.0\text{ pt}$ (0.5 pt `#CCCCCC`), left string `Page {pno} of {num_pages} • Monochrome Reference Edition`, right string `Prepared by @issparsh` preceded by authentic vector 𝕏 logo.
  - Cover page suppresses running headers and footers.

---

## 6. 🛡️ Pre-Flight Syntax & Parity Verification Gates (Dimension 4)

Before any manual is marked complete or released, it MUST pass 6 automated gates executed via independent verification scripts:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   PRE-FLIGHT MULTI-GATE PIPELINE                       │
└────────────────────────────────────────────────────────────────────────┘
                                    │
    [Gate 1: Deliverables Integrity & File Size]
    • Markdown manual exists (>25 KB, >250 lines)
    • Literal null bytes: raw_bytes.count(b"\x00") == 0
    • PDF exists, valid %PDF- header, size > 100 KB
                                    │
    [Gate 2: Strict Language & Forbidden Names Invariants]
    • Zero Devanagari characters ([\u0900-\u097F] == 0) in Markdown & PDF
    • Zero forbidden instructor names in Markdown & PDF
                                    │
    [Gate 3: Executable AST Syntax Validation]
    • Python: ast.parse(mode="exec") + doctest REPL + async wrapper
    • TypeScript: Node.js stripTypeScriptTypes(code)
    • Language Whitelist: 0 Python in TS manual, 0 TS in Python manual
                                    │
    [Gate 4: Code Fence Parity Balance Audit]
    • Code fence count % 2 == 0
    • Line-by-line state machine; reject unclosed fences at EOF
    • Detect fence inversion (markdown headers or tables inside code)
                                    │
    [Gate 5: Architecture Diagrams & Cache Audit]
    • Zero ASCII art boxes (+---, |---, ┌, └) in code listings
    • Every Mermaid diagram has a 2x resolution pre-compiled PNG in cache
                                    │
    [Gate 6: Dual-Pass 150 DPI Visual & Layout QA]
    • 150 DPI page-by-page rasterization via PyMuPDF
    • Bounding box overflow: x0 >= 50.0 pt, x1 <= 545.28 pt
    • Ghost blank page detection (0 body flowables)
    • Orphan header detection (headings in bottom 80 pt)
```

### Detailed Gate Audit Algorithms

1. **Code Fence Parity Balance Audit Algorithm (Gate 4):**
   ```python
   def audit_code_fence_parity(md_text: str) -> Tuple[bool, List[str]]:
       errors = []
       lines = md_text.splitlines()
       fence_count = 0
       in_code = False
       open_line = 0

       for idx, line in enumerate(lines, 1):
           stripped = line.strip()
           if stripped.startswith("```"):
               fence_count += 1
               if not in_code:
                   in_code = True
                   open_line = idx
               else:
                   in_code = False
           elif in_code:
               # Inversion detection: markdown headers or table delimiters inside code
               if re.match(r"^#{1,6}\s+", stripped) or re.match(r"^\|.*\|$", stripped):
                   errors.append(
                       f"Line {idx}: Suspected fence inversion — Markdown structure inside code opened at line {open_line}"
                   )

       if fence_count % 2 != 0:
           errors.append(f"Odd code fence count ({fence_count})! Unclosed code block opened at line {open_line}")
       if in_code:
           errors.append(f"Unclosed code fence at EOF opened at line {open_line}")

       return len(errors) == 0, errors
   ```

2. **Node.js V8 TypeScript AST Parsing (Gate 3):**
   ```javascript
   const fs = require('fs');
   const { stripTypeScriptTypes } = require('node:module');
   const code = fs.readFileSync(0, 'utf-8');
   try {
     stripTypeScriptTypes(code);
     process.exit(0);
   } catch (e) {
     if (e.message.includes('parameter property') || e.message.includes('TypeScript enum is not supported in strip-only mode')) {
       process.exit(0);
     }
     console.error(e.message);
     process.exit(1);
   }
   ```

3. **CPython AST Parsing (Gate 3):**
   ```python
   def verify_python_code_block(code_str: str) -> bool:
       try:
           ast.parse(code_str, mode="exec")
           return True
       except SyntaxError as e:
           if "outside async function" in str(e):
               wrapped = f"async def __verify_wrapper():\n" + textwrap.indent(code_str, "    ")
               ast.parse(wrapped, mode="exec")
               return True
           raise
   ```

4. **PyMuPDF 150 DPI Visual Raster QA (Gate 6):**
   ```python
   def audit_pdf_visual_layout(pdf_path: str) -> Tuple[bool, List[str]]:
       doc = pymupdf.open(pdf_path)
       errors = []
       for pno in range(len(doc)):
           page = doc[pno]
           # 150 DPI rasterization test
           pix = page.get_pixmap(matrix=pymupdf.Matrix(150 / 72, 150 / 72), colorspace=pymupdf.csGRAY)
           if pix.width == 0 or pix.height == 0:
               errors.append(f"Page {pno + 1}: Rasterization failure")

           # Ghost blank page check (exclude cover)
           if pno > 0:
               text_blocks = [b for b in page.get_text("blocks") if 50.0 <= b[1] <= 790.0]
               drawings = [d for d in page.get_drawings() if 50.0 <= d["rect"].y0 <= 790.0]
               if len(text_blocks) == 0 and len(drawings) == 0:
                   errors.append(f"Page {pno + 1}: Ghost blank page detected (zero body flowables)")

           # Orphan header check
           blocks = page.get_text("blocks")
           if blocks:
               last_b = blocks[-1]
               if last_b[3] > 740.0 and re.match(r"^(?:#{1,3}|PART|MODULE|CHAPTER)\s+", last_b[4].strip()):
                   errors.append(f"Page {pno + 1}: Orphan header stranded at page bottom")

       return len(errors) == 0, errors
   ```

---

## 7. 📋 Provenance & Exact Lecture Manifest Standards (Dimension 5)

Every multi-manual documentation release must generate a companion Master Resources Manifest in two formats:
1. Structured Markdown: `output/Master_Resources_Manifest.md`
2. Exact 1-Page ISO A4 PDF: `output/Master_Resources_Manifest.pdf`

### 1. Mandatory Exact Video Titles Invariant
- **Rule:** Under zero circumstances may provenance manifests use generic topic placeholders ("Foundations", "Backend Systems", "Runtime").
- **Citation Invariant:** Every row in Table 1 must quote the exact YouTube video title, duration, evaluated frame count, active code density, and architectural scope.

### 2. Four Canonical Provenance Tables
The manifest must contain exactly the following four tables:

#### Table 1: Primary Video Lecture Corpora & Exact Source Video Titles
Documents the primary video corpora, exact source lecture names, video durations, evaluated frame metrics, active code percentages, and architectural scope.

#### Table 2: Machine Vision OCR Catalogs & Extracted Frame Databases
Documents the machine vision OCR database artifact paths (`analysis/.../full_stream_ocr_results.json`), keyframe counts, vision engines (Apple Neural Engine vs VNRecognizeTextRequest), storage size on disk, and extracted code/architecture artifacts.

#### Table 3: Audio Transcription Corpora & Timing Alignment
Documents the curriculum domain, transcript storage corpus (`analysis/.../*_transcript.txt` and `.srt`), lecture file counts, total audio duration, sync granularity (exact timestamp cues / sentence-level sync), and transcription engines (Whisper Large-v3 & Auto-Captions).

#### Table 4: Toolchain, Layout Compilers & Automated Quality Assurance Suite
Documents the subsystem, component/engine, runtime version and platform, enforced quality invariants, and verification suites (`verify_*_manual.py`).

### 3. Exact 1-Page ISO A4 Layout Invariant
- Document geometry: `A4 = (595.28, 841.89) pt`.
- Margins: 36.0 pt left/right, 32.0 pt top/bottom $\implies$ `CONTENT_WIDTH = 523.28 pt`.
- Typographic budgeting: Table cell font size = 6.2 pt (leading 8.0 pt), header font size = 6.5 pt, padding = 1.8 pt.
- All 4 tables, running headers, and vector 𝕏 footers must fit onto **strictly ONE page without spillover to Page 2**.

---

## 8. 📐 Mathematical Typesetting Standards (Rules A through L)

Whenever `thenuke` generates mathematical explanations, reference manuals, or competitive programming solutions, it strictly enforces professional academic notation:

| Rule | Topic | Informal Plain-Text (BANNED) | Academic LaTeX Standard (MANDATORY) |
| :--- | :--- | :--- | :--- |
| **A** | **Fractions** | `a/b` | `\[ \frac{a}{b} \]` (Inline: `\(\frac{a}{b}\)` or compact `\(a/b\)` only when readability requires) |
| **B** | **Conditional Probability** | `P(A/B) = P(AB)/P(B)` | `\[ P(A \mid B) = \frac{P(A \cap B)}{P(B)}, \qquad P(B) > 0 \]` |
| **C** | **Subscripts** | `x1, x2, aij` | `\(x_1,\quad x_2,\quad a_{ij}\)` |
| **D** | **Superscripts & Powers** | `x^2, a^n` | `\[ x^2,\qquad a^n \]` |
| **E** | **Roots & Radicals** | `sqrt(x), sqrt(a+b)` | `\[ \sqrt{x},\qquad \sqrt{a+b} \]` |
| **F** | **Summations** | `sum(i=1 to n) xi` | `\[ \sum_{i=1}^{n} x_i \]` |
| **G** | **Integrals** | `integral f(x) dx` | `\[ \int f(x)\,dx \]` |
| **H** | **Limits** | `lim(x->0) f(x)` | `\[ \lim_{x \to 0} f(x) \]` |
| **I** | **Matrices** | ASCII tables or linear rows | `\[ A = \begin{bmatrix} a_{11} & a_{12} \\ a_{21} & a_{22} \end{bmatrix} \]` |
| **J** | **Sets & Logic** | `union, intersect, implies` | `\[ A \cup B,\quad A \cap B,\quad A \subseteq B,\quad A \Rightarrow B \]` |
| **K** | **Greek Letters** | `alpha, beta, theta` | `\(\alpha,\quad \beta,\quad \theta,\quad \lambda,\quad \mu,\quad \sigma\)` |
| **L** | **Multi-Step Derivations** | Unaligned multi-line text | `\[ \begin{aligned} x^2 - 5x + 6 &= 0 \\ (x-2)(x-3) &= 0 \\ x &= 2 \quad \text{or} \quad x = 3 \end{aligned} \]` |

- **Condition Preservation:** Typesetting must NEVER alter mathematical meaning. Preserve all boundary conditions (e.g. $P(B) > 0$). Distinguish conditional probability $P(A \mid B)$ from the ratio $\frac{P(A)}{P(B)}$.
- **No Guesswork on Ambiguities:** If an ingested formula is incomplete or ambiguous, flag it explicitly rather than silently fabricating missing terms.

---

## 9. 🏆 Multi-Platform Competitive Programming (CP) Ingestion Engine

`thenuke` provides a high-fidelity competitive programming problem ingestion engine across 7 major coding platforms:

| Platform | Ingestion Strategy | Extraction Pipeline & Capabilities |
| :--- | :--- | :--- |
| **Codeforces** | Official API + DOM Parser | Extracts tags, rating, statement with `$$$...$$$` LaTeX math, multiline `test-example-line` samples, `oj-api` fallback. |
| **LeetCode** | Official GraphQL API | Queries `question(titleSlug)` returning clean statement, topicTags, difficulty, hints, constraints, code stubs. |
| **AtCoder** | DOM Parser (`.lang-en`) | Extracts limits, `<var>...</var>` / `\(...\)` LaTeX math, constraints, sample inputs/outputs, Kenkoooo API fallback. |
| **CodeChef** | Official JSON API | Queries `api/contests/PRACTICE/problems/{code}`, extracts statement, constraints, input/output formats, `sampleTestCases`. |
| **HackerRank** | Official REST API | Queries `rest/contests/master/challenges/{slug}`, extracts native Markdown statement with LaTeX math (`$$t_{i+2} = ...$$`). |
| **GeeksforGeeks** | Next.js `__NEXT_DATA__` | Extracts `probData` with company tags (Amazon, Microsoft, Google), topic tags, formatted examples, constraints. |
| **InterviewBit** | Embedded `problemsData` | Extracts `meta.markdown_content` (description, constraints, input/output, example test cases), companies, hints. |

### Monospaced Sample Boxes (`:::sample`)
- Rendered as shaded 2-column tables with monospaced Courier font (`Input` vs `Output`) and optional editorial explanations.
- Leading whitespace and line breaks inside `<div class="test-example-line">` are strictly preserved (no line-collapsing bugs).

---

## 10. 👥 Multi-Agent Collaborative Architecture & Grilling Protocols

### 1. Autonomous Agent Roles
- **Architect Agent:** Reads evidence spans, establishes curriculum roadmap, partitions phases into parts, and calculates page budgets.
- **Researcher Agent:** Indexes audio transcripts and OCR databases, extracts code states, and filters out synthetic fluff.
- **Writer Agent:** Synthesizes high-density Roman Hinglish narrative prose, [MENTAL MODEL] callouts, and [ENGINEERING GOTCHA] cards.
- **Diagrammer Agent:** Compiles native ReportLab vector drawings and Mermaid architectural diagrams into 2x PNG caches.
- **Reviewer Agent:** Executes the 6-gate pre-flight verification pipeline and halts release upon any invariant violation.

### 2. Grilling Presets
The interactive interview mode (`/grill-me`) calibrates publication depth:

| Preset | Level of Detail | Visual Threshold | Audience Focus | Target Deliverable Profile |
| :--- | :--- | :--- | :--- | :--- |
| `foundations` | foundations | strict_need_based | academic_foundations | Concise reference, heavy math proofs |
| `resource_parity` | resource_parity | balanced | production_engineering | 100% lecture parity, real debugging |
| `senior_architect_faang` | senior_architect | diagram_dense | faang_interview | Systems internals, memory layouts |

### 3. Dynamic 100 Quotes Library
- Curated library of 100 foundational quotes from legendary computer scientists and philosophers (Alan Turing, Donald Knuth, Edsger Dijkstra, Richard Feynman, Grace Hopper, Claude Shannon, Marcus Aurelius, etc.).
- Tagged across 8 core domains (`systems`, `software_engineering`, `algorithms`, `debugging`, `curiosity`, `simplicity`, `learning`, `mastery`).
- Cover pages dynamically fetch quotes via `get_quote(topic=..., seed=...)` ensuring authoritative, contextual attribution.

---

## 11. ⚙️ Environment Requirements & Pytest Architecture

### Dependency Matrix

| Tool / Library | Verified Version | Subsystem & Operational Role |
| :--- | :--- | :--- |
| **Python** | 3.10+ (3.14 on M4) | Core runtime environment |
| **PyMuPDF** (`pymupdf`) | 1.24+ | PDF parsing, 150 DPI rasterization, bounding box layout QA |
| **reportlab** | 4.1+ (4.4.1 verified) | Two-pass ISO A4 Platypus PDF compilation engine |
| **Node.js** | 22.6+ (v22.14 verified) | TypeScript V8 AST parsing via `stripTypeScriptTypes` |
| **ffmpeg** | 7.0+ | VideoToolbox hardware-accelerated scene-change extraction |
| **online-judge-tools** | 11.5+ | CP problem fetching & sample testcase verification |
| **beautifulsoup4** | 4.15+ | Web crawler HTML cleaning and DOM extraction |
| **faster-whisper** | 1.2.1+ | Fallback neural speech-to-text (strictly when no captions exist) |
| **yt-dlp** | latest | YouTube audio demuxing & 720p stream downloading |
| **lxml** | 5.x | High-performance HTML parsing |

### Test Architecture

```bash
cd /Users/iamsparsh00321/.gemini/config/skills/thenuke
python3 -m pytest tests/ -q
```

- `tests/test_ingestion.py` — Multi-source crawler, subtitle parser, and corpus indexer.
- `tests/test_grilling.py` — Interactive intake and grilling presets.
- `tests/test_synthesis.py` — Synthesis engine: 0 Devanagari, callouts, and challenge drills.
- `tests/test_diagramming_and_qa.py` — Vector engine, palette verification, and QA audit engine.
- `tests/test_cp_ingestion.py` — Competitive programming ingestion across 7 platforms.
- `tests/test_rendering_invariants.py` — Escape artifact defense, math parity scoping, and XML resilience.
- `tests/test_mathematical_typesetting.py` — Rules A through L academic math acceptance tests.
- `tests/test_remediation_features.py` — Packaging, dependencies, and fixture integrity.
- `tests/e2e/` — End-to-end integration and multi-agent workload scenarios.

---

## 12. 🔒 Post-Clearance Artifact Security & Cleanup Policy

### 1. Git Repository Policy: ZERO PDF Binaries
- All `.gitignore` configurations enforce `*.pdf`, `output/`, and `scratch/`.
- PDFs are strictly distribution artifacts generated to `output/` or `~/Downloads/`.
- Git repositories store 100% clean, reproducible source code, vector drawing engines, test suites, and documentation.

### 2. Scratch Directory Cleanup
Once you verify and approve the final PDF release, run:
```bash
python thenuke_cli.py clean
```
This permanently deletes intermediate scratch files:
- `scratch/videos/` — Downloaded 720p MP4 files.
- `scratch/frames/` — Extracted video scene frames.
- `scratch/audio/` — Demuxed WAV audio files.
- `scratch/scrape_html/` — Raw scraped HTML pages.

> [!CAUTION]
> Cleanup is irreversible. Confirm that all verification gates pass and the final PDF is archived before executing cleanup.
