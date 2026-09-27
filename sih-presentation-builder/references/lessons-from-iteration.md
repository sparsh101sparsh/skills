# Lessons From Iteration: SIH Presentation Engineering Retrospective

## 1. Overview and Retrospective Context

This retrospective documents the iterative development of presentation decks for the Smart India Hackathon (SIH), specifically based on the live engineering and design cycles for **Problem Statement ID: SIH26188** (Ministry of Home Affairs / Sashastra Seema Bal — "ThirdEye-SSB: Air-Gapped Multimodal AI and Forensic Identity Screening System"), alongside comparative analysis of 50 official winning decks (including *Team Lumora / Kartikay*, *Storm Surge SIH25042*, *Udaan PS25150*, *Arize / CoalWorks SIH1645*, and *Mindsmiths / EcoPick PS25266*).

The objective of this retrospective is not to present abstract presentation advice. It records the specific friction points, visual rendering failures, content mismatches, and iterative corrections that occurred between the user and the AI agent, extracting the permanent rules required to produce competition-winning decks on the first attempt.

---

## 2. Iterative Reconstruction: Prompt-by-Prompt Evolution

The following analysis traces the key stages of interaction across the deck construction process.

### Stage 1: Winning Deck Research & Reverse Engineering
* **User Request:** Search for, verify, and download 50 latest SIH winner presentation decks (specifically 2024–2025 winners like Team Lumora). Analyze them frame-by-frame and extract their design language and master prompts.
* **AI Output:** Initially performed generic web searches and summarized high-level advice ("make slides clean, use icons"). 
* **User Correction:** *"download the images in this linkedin post... can you review each image you downloaded and observe every detail and make a prompt for each slide diagram focused less content act like sih ppt expert for each slide create a master prompt /goal"*.
* **AI Revision:** Extracted the core anatomical formula of winning decks:
  1. 80% diagram/visual, 20% high-impact telegraphic text (max 6–8 words per bullet point).
  2. Slide 2 as a dual-cluster infographic: Problem hub with 5–6 radial problem nodes on the left, paired directly with 5–6 capability solution badges on the right.
  3. Slide 3 as a numbered end-to-end pipeline with explicit offline/no-internet fallback paths, data payload labels, and trust boundaries.
  4. Slide 4 as a paired challenge-versus-mitigation matrix.
  5. Slide 5 as a 4-step stakeholder journey process ribbon with quantified Indian baseline metrics.
  6. Slide 6 as TAM/SAM/SOM concentric circles paired with peer-reviewed academic and statutory citations.
* **Final Lesson:** Never write slide copy before establishing the dominant visual container. Every slide must be designed around one defensible diagram.

### Stage 2: Slide 2 Rebrand and Visual Asset Migration
* **User Request:** Re-content and recolor "Lumora Slide 2" into "ThirdEye-SSB" for SIH26188 using `new.pptx` as the reference layout.
* **AI Output:** Produced a modified PPTX file where text was swapped, but the visual rendering was severely degraded:
  - The script inserted random leaf watermarks, giant tree icons, and decorative background graphics.
  - Colors were shifted to arbitrary golden and greenish hues instead of maintaining Lumora's clean navy/blue brand palette.
  - Text strings overlapped icons, and icons overlapped background containers.
  - The device mockup displayed a generic, futuristic tablet that had zero relationship to frontline border outposts.
* **User Correction:** *"its not of reference template level compare each element you will see its like our one has so many rendering issues also font design is not same too and what is this device does it even make sense? no is... pick elements (like arrows, icons diagram structure jo broken h, background gradient, background element) from new.pptx to better design it... also so many overlapping issues and remove the leaves make sure all the arrows are properly visible every box is properly visible every background is properly visible every icon is in size"*.
* **AI Revision:** Rebuilt the slide using `rebuild_slide2.py`:
  1. Purged all 17 extraneous leaf and tree watermarks (`image1.png` to `image33.png`).
  2. Standardized color palette to Deep Navy (`#0F2044`), Slate Blue (`#2563EB`), and Cool Neutral (`#F8FAFC`).
  3. Replaced the generic device mockup with a ruggedized Android field smartphone (MIL-STD-810H).
  4. Adjusted text box padding and bounding boxes to guarantee zero overlap with icon glyphs.
* **Final Lesson:** AI models default to decorative clutter ("AI slop") when attempting to look visual. Decorative flourishes must be actively stripped. Visual elements must have direct operational meaning to the problem statement.

### Stage 3: Connector Geometry and Alignment Precision
* **User Request:** Review the rendered visual output of Slide 2 and Slide 3.
* **AI Output:** Slide rendered with straight lines that failed to connect to component cards, small arrowheads that were clipped by bounding boxes, and unbordered pill badges.
* **User Correction:** *"one final render is more needed the arrows are not properly aligned the solution ke piche wala background noticable nai h and the icons are overlapping the text and one arrow is not even connected to the smartphone just this krna h... just fix these arrows make the smaller arrows bent and make it bigger their head point is not rendered properly render it properly and ye 100%offline wala pr kuch bordering nai h woh shi krdo"*.
* **AI Revision:** Refined shape XML and drawing scripts:
  1. Replaced broken straight connectors with orthogonal bent connectors (`type="bentConnector3"`).
  2. Enlarged arrowhead geometry (`w="med" len="lg"` in DrawingML) so arrowheads were unmistakably visible at slide scale.
  3. Added explicit 1.5pt solid borders to the offline capability pill badges.
  4. Anchored connectors to exact coordinate attachment points on the smartphone mockup.
* **Final Lesson:** Arrow routing and connector visibility communicate system architecture. A broken, floating, or clipped arrow signals an unverified technical concept to a technical judge.

### Stage 4: Palette Discipline and Stroke Weight
* **User Request:** Build and rebrand Slide 3 (Technical Architecture).
* **AI Output:** Introduced heavy 3pt golden lines and multi-colored boxes to highlight different tech modules.
* **User Correction:** *"instead of using golden colour can you use the same colour language team lumora used and give me the slide 3 ppt single slide only... the lines are so thick and the arrows are not properly visible"*.
* **AI Revision:** Restored the strict navy/slate palette, set connection lines to 1.25pt crisp strokes, and eliminated conflicting accent hues.
* **Final Lesson:** Maintain a unified 3-color palette across the entire deck. Color should indicate semantic meaning (e.g., green for passing verification, amber for human review, red for security tripwires), not decoration.

### Stage 5: Icon Semantics, Clutter Removal, and Role Clarity
* **User Request:** Fix Slide 5 (Impacts and Benefits).
* **AI Output:** Selected aggressive, menacing security badge icons; left text backgrounds improperly sized; used confusing operational jargon ("BOP officers").
* **User Correction:** *"fix slide 5 here fix the last icon and the colour should be like the reference here... let these icons be in black... ye icon thoda better bna do yr it looks menacingly... remove all the leaf icons... the circles have not been rendered properly render them asap and the text background doesnt cover it fix it too... whats bop officers"*.
* **AI Revision:**
  1. Replaced aggressive icons with standard, neutral outlined glyphs rendered in uniform black (`#1E293B`).
  2. Fixed circle rendering geometry and expanded container fill rectangles to completely encapsulate multi-line text strings.
  3. Stripped decorative leaf graphics.
  4. Clarified domain terminology: defined "Border Outpost (BOP) field personnel" with specific role context rather than bare acronyms.
* **Final Lesson:** Icons must be neutral, professional, and visually quiet. Outlined monochrome glyphs outperform complex colored illustrations. Every institutional acronym must be grounded in real-world personnel roles.

### Stage 6: Plain-Text Portal Submission Safety & Jargon Purging
* **User Request:** Prepare the textual idea description and abstract summary corresponding to the deck for the official portal.
* **AI Output:** Generated markdown containing formatted tables (`|`), mathematical LaTeX dollar signs (`$`), em-dashes (`—`), banking terminology ("KYC"), military buzzwords ("sentry", "jawan"), and exaggerated processing times ("10 seconds").
* **User Correction:**
  - *"dont make table wagera udar sirf plain text submit krskte"*
  - *"idea description m hm problem kyu explain krrha h"*
  - *"our system does rely on human evaluaiton wdym"*
  - *"stop using words like sentry wagera"*
  - *"wtf is kyc dont use this term use something simpler"*
  - *"10 seconds is an overeggeration better not put these things here"*
  - *"dont make it like an article 1.1 wagera comeon"*
  - *"use /humanizer to write the filles again... make every word sound amazing like unnhe padh kr maja aana chaiye"*
* **AI Revision:**
  1. Stripped all Markdown tables and LaTeX formatting, converting data into structured bullet hierarchies readable on any government submission portal.
  2. Refocused the idea description entirely on the technical solution, mechanics, and operational deployment.
  3. Replaced "KYC" with "online identity verification tools" and "automated airport gates".
  4. Replaced "sentry/jawan" with official terms: "inspecting officer", "field personnel", "SSB personnel".
  5. Corrected exaggerated claims: replaced "10 seconds" with verifiable edge inference latency ("1.18 seconds") and realistic operational queue descriptions.
  6. Positioned the system as an explainable decision-support copilot featuring an Amber review tier (30–69) that explicitly empowers human officers to resolve natural aging and card wear.
* **Final Lesson:** Competition evaluators reject buzzwords from mismatched domains (e.g., "KYC" on an international border) and exaggerated claims. Text must be humanized, technically grounded, and structured for the submission medium.

---

## 3. Repeated Mistakes Database

### Category A: Content & Framing Failures
1. **The Problem Statement Echo:** Rehashing the official problem statement for multiple paragraphs instead of jumping immediately into the solution architecture and novelty.
2. **Domain-Blind Buzzword Dumping:** Using corporate SaaS or fintech terms ("KYC", "customer onboarding", "growth hacking") in defense, healthcare, or agricultural problem statements.
3. **The Omniscient Black-Box Claim:** Claiming "100% automated AI detection with zero errors" instead of a realistic human-in-the-loop copilot with an explainable review tier.
4. **Exaggerated Time & Accuracy Claims:** Inventing unrealistic metrics (e.g., "detects fake IDs in 5 milliseconds with 99.99% accuracy") without specifying the hardware benchmark, dataset, or test conditions.
5. **Treating Slides Like Documentation:** Pasting dense technical paragraphs or academic paper abstracts directly into slide body blocks.

### Category B: Visual & Layout Failures
1. **The Card Matrix Trap:** Defaulting to 4 to 6 identical rounded rectangles filled with text, resulting in a monotonous dashboard appearance.
2. **Decorative AI Clutter ("AI Slop"):** Adding random leaves, trees, geometric floating bubbles, or abstract circuit board vectors that carry zero semantic meaning.
3. **Broken Connector Geometry:** Using straight connector lines that overlap text, fail to touch component edges, or have invisible/clipped arrowheads.
4. **Container Overflow & Text Clipping:** Bounding boxes that truncate text, text that spills outside pill badges, and inconsistent margins across cards.
5. **Color Palette Disarray:** Mixing conflicting accent colors (gold, purple, orange, neon green) instead of maintaining a disciplined 3-color brand system.
6. **Inconsistent Icon Visual Weight:** Mixing flat monochrome glyphs with 3D glossy icons, colored illustrations, and menacing/aggressive iconography.
7. **Phantom Hardware Mockups:** Showing futuristic, imaginary tablets or glass holographic displays instead of actual field equipment (e.g., rugged IP68 smartphones, industrial fanless mini PCs).

### Category C: SIH-Specific & Compliance Failures
1. **Altering the Official 6-Slide Template:** Adding unnecessary slides or altering mandatory headings, risking disqualification during automated screening.
2. **The Missing Offline Fallback:** Proposing a cloud-only, high-bandwidth architecture for a problem statement located in rural, underground, forest, or border regions.
3. **The Unverifiable Impact Claim:** Using generic slogans ("empowers millions of citizens") without citing baseline numbers from official ministry annual reports.
4. **Missing Statutory & Regulatory Anchors:** Overlooking mandatory Indian laws and standards (DPDP Act 2023, BIS standards, CERT-In guidelines, Section 65B of the Indian Evidence Act).
5. **Zero Proof-of-Work Links:** Failing to include verifiable repository links, 60-second prototype video walkthroughs, and interactive deployment links.

---

## 4. Extracted Design System & Principles

### Visual Philosophy
* **80/20 Rule:** 80% of slide area must be dedicated to structural diagrams, comparative infographics, or visual evidence. Text is restricted to 20% telegraphic copy.
* **Telegraphic Copy:** Maximum 6 to 8 words per bullet point. Eliminate conversational filler, staging, and introductory fluff.
* **Numbers Beat Adjectives:** Replace "extremely fast, highly accurate neural model" with "GhostFaceNet-v2 (512-D) inference in 35ms on edge CPU".
* **Visual Anchor Requirement:** Every slide must have a dominant focal anchor (a central hub, a numbered pipeline, a comparison matrix, or an annotated device UI).

### Color Architecture
* **Primary Background:** Crisp White (`#FFFFFF`) or Ultra-Light Slate (`#F8FAFC`).
* **Primary Deep Tone:** Deep Institutional Navy (`#0F2044` / `#0A192F`) for headers, container borders, and structural nodes.
* **Technical Accent:** High-Contrast Blue (`#2563EB` / `#1D4ED8`) for active pipeline stages, primary CTA pills, and flow arrows.
* **Semantic Status Colors:**
  - Green (`#16A34A`): Validated, passed checksum, authentic.
  - Amber (`#D97706`): Human evaluation tier, natural aging, card wear, secondary inspection.
  - Red (`#DC2626`): Deterministic security tripwire, spoof attack, forgery alert.

### Information Flow Hierarchy
1. **Slide Header:** Official SIH Logo (left), Title & PS ID (center), Category Tag (right).
2. **Top-Level Banner / One-Liner:** Immediate 1-sentence product thesis or milestone statement.
3. **Core Visual Engine:** Dominant diagram or flowchart occupying 60–70% of vertical slide space.
4. **Bottom Evidence Bar:** 3 to 4 quantified proof metrics, USPs, or tech-stack categorizations.
