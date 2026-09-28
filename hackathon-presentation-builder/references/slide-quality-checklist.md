# Slide Quality Checklist: Multi-Dimensional Evaluation Matrix

This checklist provides an automated evaluation framework for vetting presentation slides built for the Smart India Hackathon and high-stakes technical competitions. Every slide must pass all criteria before being declared production-ready.

---

## 1. Narrative & Storytelling Audit

* [ ] **Single Purpose Test:** Does this slide communicate exactly one central message that can be summarized in a single sentence?
* [ ] **Forward Momentum:** Does this slide logically transition from the previous slide and set up the next one?
* [ ] **Omission Test:** If this slide were removed, would the core argument collapse? (If not, consolidate or eliminate it).
* [ ] **Immediate Value:** Can an evaluator understand what problem is being solved and how within the first 5 seconds of looking at the slide?

---

## 2. Content & Factual Grounding Audit

* [ ] **Telegraphic Density:** Are bullet points restricted to a maximum of 6 to 8 words?
* [ ] **Zero Text Walls:** Are there zero full narrative paragraphs in the body of the slide?
* [ ] **Jargon Sanity:** Is every acronym defined or immediately obvious to a domain evaluator? Are misplaced corporate buzzwords (e.g., "KYC", "synergy") completely eliminated?
* [ ] **Claim Defensibility:** Is every performance percentage, throughput metric, or latency claim backed by a named benchmark, dataset, or test condition?
* [ ] **Human-in-the-Loop Realism:** Does the slide avoid claiming impossible 100% autonomous accuracy? Is human operational command or review clearly preserved?

---

## 3. Visual & Diagrammatic Effectiveness

* [ ] **80/20 Visual Balance:** Does visual content (diagrams, flowcharts, architectures, comparison tables, UI crops) occupy at least 70–80% of the slide canvas?
* [ ] **Zero Decorative AI Slop:** Are there zero decorative cliparts, random leaf/tree watermarks, floating geometric bubbles, or generic stock illustrations?
* [ ] **Physical Hardware Fidelity:** If a device mockup is shown, does it represent real, field-grade hardware (e.g., rugged IP68 mobile, fanless edge PC) rather than a futuristic fantasy gadget?
* [ ] **Connector Integrity:**
  * Do all arrows start and terminate cleanly at component card boundaries without floating in empty space?
  * Are connectors routed orthogonally (bent connectors) rather than cutting diagonally across unrelated text boxes?
  * Are arrowheads clearly visible, sized appropriately, and unclipped?
* [ ] **Offline Fallback Architecture:** Is there an explicit visual path (e.g., dotted connector line to a local buffer/SQLite queue) showing how the system functions when external network connectivity drops?

---

## 4. Design, Spacing & Layout Rigor

* [ ] **Palette Discipline:** Does the slide adhere strictly to the established 3-color palette (Deep Navy `#0F2044`, Slate Blue `#2563EB`, Neutral `#F8FAFC`) with semantic accents (Green/Amber/Red) used only for status indication?
* [ ] **Stroke Weight Consistency:** Are connector lines and card borders rendered with consistent line weights (1.0pt to 1.5pt) rather than clumsy, heavy 3pt+ lines?
* [ ] **Container Padding & Containment:** Does all text fit comfortably within its container boxes and pill badges with at least 8pt of internal padding on all sides? Zero text overflow.
* [ ] **Icon Visual Language:** Are all icons monochrome, flat outlined glyphs of identical size (24x24px or 32x32px) and stroke weight? Zero colored, 3D, or menacing icons.
* [ ] **Hierarchy at 10-Foot Distance:** Is the hierarchy obvious from across a room: Primary Headline (20–24pt Bold) -> Sub-header/Thesis (14–16pt) -> Diagram Node Labels (11–13pt Bold) -> Secondary Evidence/Details (9–10pt)?

---

## 5. SIH Competition Compliance & Evaluation Rubric

* [ ] **Template Integrity:** Does the deck preserve the official mandatory headings and structure of the SIH template without adding extraneous slides?
* [ ] **Administrative Header Completeness:** Are Problem Statement ID, Problem Statement Title, Theme, Category (Software/Hardware), Team Name, and Team ID prominently displayed on Slide 1?
* [ ] **Statutory & Regulatory Alignment:** Does the solution cite compliance with mandatory Indian frameworks where applicable (DPDP Act 2023, Section 65B of Indian Evidence Act, BIS codes, CERT-In guidelines)?
* [ ] **Quantified Impact with Official Baselines:** Are societal and economic gains calculated against verified national baselines from official government reports (e.g., MoSPI, NITI Aayog, Ministry Annual Reports)?
* [ ] **Verifiable Proof Artifacts:** Does the final slide contain working, high-visibility badges for the GitHub source repository, 60-second prototype video, and interactive live demo?

---

## 6. Stage-Specific Quality Gates

### Stage A: Idea-Submission PDF (Silent 120-Second Jury Scan)
* Evaluators review hundreds of PDFs silently without team narration.
* Visual contrast must survive low-resolution screens and black-and-white printing.
* Slide 2 must communicate the core idea and capability badges in the first 2 vertical inches.
* Slide 3 architecture diagram must dominate the slide and be self-explanatory.

### Stage B: College Internal Jury (5–7 Minute Faculty & Industry Vetting)
* Clear division of team responsibilities must be defensible.
* The prototype must be shown solving the primary happy path and one unhappiest-case error path.
* Hardware bill of materials (BOM) and power budgets must be grounded in student-accessible components.

### Stage C: Grand Finale (Live Demonstration & Ministry Evaluation)
* Live demo must execute in under 90 seconds without network dependencies.
* Backup video of the happy path must be queued in volatile storage.
* Slide 4 and Slide 5 must present an actionable 90-day pilot deployment plan specifying exact organizational prerequisites.

---

## 7. The 11 Red-Team Judge Questions

Every presentation must explicitly answer these 11 questions before a jury member asks them:

1. **The Core Problem:** Exactly what physical, logistical, or computational failure occurs today that costs the organization time, money, or security?
2. **The Inaction Cost:** Who pays the cost if this problem is left unsolved for another 5 years?
3. **Existing Portals & Systems:** Why do existing government portals, commercial tools, or departmental software fail to solve this?
4. **Offline Resilience:** What happens when there is a total power blackout, cellular network failure, or severed fiber cable?
5. **Data Provenance & Bias:** Where does the training or operational data come from, how is it validated, and how is algorithmic bias mitigated?
6. **Statutory Legality:** How does this architecture comply with the Digital Personal Data Protection (DPDP) Act 2023 and relevant evidence laws?
7. **Human Command:** Is the machine replacing human personnel, or is it an explainable decision copilot where human authority is strictly preserved?
8. **Unit Economics & BOM:** What does it cost to deploy one unit in a remote block, outpost, clinic, or police station?
9. **Built vs Mock:** Exactly what code was written and verified in the prototype versus what is currently a simulated integration?
10. **The Unhappy Path:** What happens when bad data, weathered documents, presentation attacks, or corrupted sensors hit the system?
11. **90-Day Deployment:** If the sponsoring ministry awards ₹X and 90 days, exactly what hardware, software, and field pilots will ship?
