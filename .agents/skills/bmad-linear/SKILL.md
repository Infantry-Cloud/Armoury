---
name: bmad-linear
description: Set up a new BMAD project in Linear, agree and publish its planning steps, and reconcile its epics (with milestones), stories, bugs, implementation tasks and activity notes. Use when starting a named BMAD project, connecting its whole workflow to Linear, or retrying incomplete Linear publishing.
---

# BMAD Linear

Find the nearest project root containing `_bmad/`. Read
`_bmad/custom/linear-workflow.md` completely and follow it.
If it is missing, stop and ask the user to sync the shared customisations.

Choose the requested operation:

- New project, project kickoff, or agreeing a delivery plan: **Kickoff**.
- Publish existing work, backfill, reconcile, retry (including missing epic
  milestones and pending activity notes), realign Linear after epics or stories were
  refactored, renumbered, moved, split, merged or removed, or check for drift:
  **Reconcile**. Use its reconcile helper; `plan --check` alone answers "is Linear
  in sync?" without writing.
- Execute the next or a named approved planning step: **Run an agreed step**.
- Otherwise explain the integration and offer Kickoff; do not create speculative work.

Use the installed BMAD catalog/help and resolved configuration, not remembered skill
names or a fixed methodology checklist. The shared workflow describes both the
released epics/sprint layout and the newer ticket-tree layout; use the installed one.
This skill never installs or upgrades BMAD without explicit user approval.
