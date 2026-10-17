# i-ixd-quality-interaction: A quality skill checks the code against APP-DESIGN.md and writes a conformance verdict

**What to build:** New `skills/quality-interaction/SKILL.md` (plan § Skills): reads `APP-DESIGN.md` as intent, runs the surface census, walks entry by entry and type by type, and records each violation and one exemplar per rule with `file:line`. It computes the score, orders the changes (systemic first) with a coverage table, runs the citation check, and writes `_concept/11_build/interaction.yaml`. Contested items and proposed exceptions are handed back to `experience-interaction`. It never edits `APP-DESIGN.md`.

**Plan:** `.scratch/plans/IXD_INTERACTION_DESIGN_PLAN.md` - Decisions this plan takes 3, 8; Target shape › Skills › quality-interaction; Steps 5.

**Blocked by:** i-ixd-experience-interaction, i-ixd-reverse-census

**Status:** ready-for-agent

- [ ] Frontmatter: requires `app-design` (hard on `APP-DESIGN.md`), `package.json` hard; `produces: [{ id: interaction-review, path: "_concept/11_build/interaction.yaml" }]`.
- [ ] The verdict shape (violations, exemplars, score, changes, coverage, proposed exceptions) is defined at the step that writes it; counts come from the findings, never typed.
- [ ] A rule with zero violations and zero exemplars is reported as unchecked; unread regions are named.
- [ ] `interaction-review` added to `not_grown` in the same four profiles; `README.md` row.
- [ ] `python3 scripts/check.py` exits 0 (collection + fixtures, not `--no-tests`); every skill body ≤ 140 lines; pushed run green per the `CLAUDE.md` watch rule.
