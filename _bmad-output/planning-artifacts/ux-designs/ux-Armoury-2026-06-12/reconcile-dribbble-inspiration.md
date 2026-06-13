# Inspiration Reconciliation — Dribbble References

Both references are URL-only (Dribbble blocks scraping; recorded as such in `.decision-log.md`, Discovery: visual inspiration). This note audits how each stated reaction landed in `DESIGN.md` / `EXPERIENCE.md`.

## 1. Weblytics Dark Dashboard
https://dribbble.com/shots/15754500-Weblytics-Dark-Dashboard — Daniel liked the **soft graphs/tables/bar charts**.

**Landed — strongly.**
- The "soft data" reaction became DESIGN's hard posture #2: "Charts, bands, and graph edges are rounded and muted — severity fills at 0.6–0.85 opacity, no neon, no glow."
- Concrete specs trace directly: severity-band component (30px, 3px gaps, 4px per-segment radius, soft-opacity fills — named "the 'soft chart' signature" in Shapes), chip fills at 0.13–0.16 alpha, soft bezier graph edges, rounded-never-sharp shape system.
- The dark-theme reaction ("dark seems the right fit for security tools") became dark-only with three themes — exceeded, not just met.
- Credited in EXPERIENCE's Inspiration & Anti-patterns ("Lifted — soft data visualization", `imports/weblytics.html`) and in EXPERIENCE's frontmatter-adjacent composition note.
- *Tables*: Daniel's reaction included soft tables; the spines' findings table went **dense operator-console** (30px rows, hairline rules — lifted from the rejected operator-console direction) rather than soft/card-like. The softness survives in the table's *chrome* (rounded containers, muted hairlines, tonal hovers), but this is a deliberate hybrid, not a 1:1 carry — worth knowing it was a fusion, not a drop.

## 2. SaaS Cyber Phishing Platform (AmazingUI)
https://dribbble.com/shots/27020465-SaaS-Cyber-Phishing-Platform-UI-UX-Design-by-AmazingUI — liked **primarily a graph in one image**.

**Landed — amplified.**
- The graph reaction matured into the round-1 requirement "you actually see the relational points, it's more striking" (.decision-log.md), and then into *two* surfaces: the blast-radius 4-tier node-edge graph and the dedicated Graph explorer, plus the full graph token set in DESIGN (graph-node, running ring, dashed not-running, severity-hued affected edges).

**Not reflected:**
- Unlike Weblytics, this shot is **never credited in either spine** — its lineage exists only in `.decision-log.md`. The Inspiration & Anti-patterns section lifts Weblytics, Linear, and internal explorations, but the AmazingUI reference that seeded the graph view is uncited. Cosmetic, but if provenance of inspiration matters to the record, this is the one missing citation.

No other stated reactions exist in the log for either reference; nothing else was promised, nothing else is owed.
