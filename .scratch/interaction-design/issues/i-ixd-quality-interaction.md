# i-ixd-quality-interaction: A quality skill checks the code against APP-DESIGN.md and writes a conformance verdict

**What to build:** New `skills/quality-interaction/SKILL.md` (plan § Skills): reads `APP-DESIGN.md` as intent, runs the surface census, walks entry by entry and type by type, and records each violation and one exemplar per rule with `file:line`. It computes the score, orders the changes (systemic first) with a coverage table, runs the citation check, and writes `_concept/11_build/interaction.yaml`. Contested items and proposed exceptions are handed back to `experience-interaction`. It never edits `APP-DESIGN.md`.

**Plan:** `.scratch/plans/IXD_INTERACTION_DESIGN_PLAN.md` - Decisions this plan takes 3, 8; Target shape › Skills › quality-interaction; Steps 5.

**Blocked by:** i-ixd-experience-interaction, i-ixd-reverse-census

**Status:** resolved

- [x] Frontmatter: requires `app-design` (hard on `APP-DESIGN.md`), `package.json` hard; `produces: [{ id: interaction-review, path: "_concept/11_build/interaction.yaml" }]`.
- [x] The verdict shape (violations, exemplars, score, changes, coverage, proposed exceptions) is defined at the step that writes it; counts come from the findings, never typed.
- [x] A rule with zero violations and zero exemplars is reported as unchecked; unread regions are named.
- [x] `interaction-review` added to `not_grown` in the same four profiles; `README.md` row.
- [x] `python3 scripts/check.py` exits 0 (collection + fixtures, not `--no-tests`); every skill body ≤ 140 lines; pushed run green per the `CLAUDE.md` watch rule.

**Resolution (2026-10-17):** `skills/quality-interaction/SKILL.md` (109 lines): APP-DESIGN.md + package.json hard; census reuses `findings/interaction.md` and re-verifies lines; violations/exemplars per `§ Recording findings`; counts computed by script; `unchecked` status for rules with neither; unread regions named; systemic-first changes with coverage; citation check; verdict shape defined at step 8; never edits APP-DESIGN.md. The `hard-gate-on-not-grown` rule now also exempts a skill whose every `produces` id the profile never grows (fixture fails without the change), which is why its APP-DESIGN.md gate can stay hard. check.py green, 169 fixtures.
