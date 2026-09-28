# hackathon-presentation-builder

an agent skill for building diagram-first, research-backed presentation decks for the smart india hackathon (sih) and technical competitions.

## what is this

most ai slide generators produce unreadable decks: walls of bullet points, generic rounded cards that look like a saas landing page, and random decorative graphics like floating leaves or futuristic glass tablets. 

in a hackathon like sih, evaluators scan hundreds of pdfs silently in about two minutes. if they have to read long paragraphs or decipher generic buzzwords, they move on.

we built this skill after tearing down 50 winning sih decks (including team lumora, storm surge, and coalworks) and rebuilding real competition slides. it turns vague problem statements into structured, diagram-first visual arguments that judges can understand in seconds.

## why most ai decks get rejected

when an llm generates presentation slides without strict guardrails, it almost always makes the same mistakes:
* text walls: dumping full paragraphs copied straight from the problem description.
* decorative ai clutter: adding floating leaves, tree silhouettes, and geometric shapes that mean nothing.
* the card trap: putting 4 to 6 identical rounded boxes on every slide.
* fake numbers: claiming 99.9% accuracy or sub-second speeds without naming a dataset or hardware benchmark.
* domain-blind buzzwords: using corporate fintech terms like "kyc" on a border security or rural agriculture deck.
* no offline path: assuming 24/7 high-speed cloud internet for problems set in remote villages, coal mines, or border outposts.

## the rules that actually win

1. 80% diagrams, 20% text. every slide centers around one dominant visual (a hub-and-spoke cluster, a numbered pipeline, a comparison matrix, or a user journey ribbon).
2. bullets stay under 8 words. if an idea needs 3 lines of prose, it belongs in a diagram, not a bullet.
3. numbers beat adjectives. write "ghostfacenet-v2 (512-d) inference in 35ms on edge cpu" instead of "ultra-fast cutting-edge deep learning model".
4. keep humans in the loop. judges know automated ai makes mistakes under dust, glare, and real-world wear. always include an explainable review tier where human personnel make the final call.
5. show the offline fallback. if the internet cuts out, show exactly how the local device queues data and syncs later.
6. stick to three colors. deep navy for structure, blue for active steps, and light slate for background. use green, amber, and red strictly for status.

## the official 6-slide structure

* slide 1: administrative details. clean grid with problem id, title, theme, category, and team info. zero marketing slogans.
* slide 2: problem and solution. left side has a central problem hub with radial failure spokes; right side has colored capability badges that directly solve each spoke.
* slide 3: technical architecture. a numbered 6-station pipeline with labeled data payloads and a clear dotted line showing the offline fallback route.
* slide 4: feasibility and viability. top half compares cost, time, and error rates against existing methods; bottom half pairs real field risks with technical mitigations.
* slide 5: impact and benefits. a 4-step stakeholder journey (frontline user to ministry) paired with quantified math against official government baseline numbers.
* slide 6: research and proof. a tam/sam/som market sizing bullseye, a 3-tier matrix of government and ieee citations, and clickable proof-of-work badges for github, video, and demo.

## quick start

### install with github cli
```bash
gh skill install sparsh101sparsh/skills hackathon-presentation-builder
```

### manual install
copy the skill folder into your agent directory:
```bash
# for antigravity
cp -r hackathon-presentation-builder ~/.gemini/config/skills/

# for claude / cursor
cp -r hackathon-presentation-builder ~/.claude/skills/
```

## what is inside

```
hackathon-presentation-builder/
├── SKILL.md                          # core instructions for the ai agent
├── README.md                         # this overview
└── references/
    ├── lessons-from-iteration.md     # full breakdown of real prompts, mistakes, and fixes
    ├── slide-quality-checklist.md    # evaluation matrix and 11 red-team judge questions
    └── visual-decision-framework.md  # guide for choosing diagrams, layouts, and connectors
```

## license

mit
