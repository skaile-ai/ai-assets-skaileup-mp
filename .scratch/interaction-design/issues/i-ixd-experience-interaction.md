# i-ixd-experience-interaction: A planning skill decides the app's interaction rules before any screen is specified

**What to build:** New `skills/experience-interaction/SKILL.md` (plan § Skills): reads model, glossary, journeys, an existing `APP-DESIGN.md` and, when present, `findings/interaction.md` (retrofit: recommend what the code already does when it passes the rule). It classifies objects, decides P1-P17, draws floorplans, asks in rounds from the catalogue, writes `APP-DESIGN.md` after every round, and folds a `11_build/interaction.yaml` verdict back in. Lands with `contracts/interaction_patterns.md` (P1-P17 + Recording findings; P13 points at `_concept/glossary.md`) and `contracts/app_design.md` (shape, entries, reading, writing: one writer, the verdict file, nav rule vs shell nav), plus `references/decision-catalogue.md`.

**Plan:** `.scratch/plans/IXD_INTERACTION_DESIGN_PLAN.md` - Decisions this plan takes 2-8; Target shape › Skills › experience-interaction; Steps 3.

**Blocked by:** i-ixd-gate-root-artifact

**Status:** ready-for-agent

- [ ] Frontmatter: requires `glossary`, `journeys`, `datamodel`; soft gates on `findings/interaction.md`, `11_build/interaction.yaml` and `APP-DESIGN.md`; `produces: [{ id: app-design, path: "APP-DESIGN.md" }]`.
- [ ] Object names are read from `model.json` / `glossary.md`; an object with no term is handed back to `concept-glossary`.
- [ ] Rounds of at most five questions, recommendation first, file written after each round; without a user, `[open Qn]` entries and § Open rows.
- [ ] Both contracts exist, adapted from the global references (no `CONTEXT.md`, no multi-writer `(change)` rule); `contracts/README.md` lists them; `§` cites resolve.
- [ ] `app-design` added to `not_grown` in `api-service`, `cli-tool`, `data-pipeline`, `library`; `README.md` `## Skills` row.
- [ ] `python3 scripts/check.py` exits 0 (collection + fixtures, not `--no-tests`); every skill body ≤ 140 lines; pushed run green per the `CLAUDE.md` watch rule.
