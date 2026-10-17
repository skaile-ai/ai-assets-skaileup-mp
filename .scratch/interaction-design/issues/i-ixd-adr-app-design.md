# i-ixd-adr-app-design: ADR 0015 puts the interaction decisions in APP-DESIGN.md at the project root

**What to build:** Record decisions 1-3 and 5: `APP-DESIGN.md` at the project root (the directory holding `_concept/`) is the one named project-root artifact, so it amends ADR 0011/0013. The rulebook is forked from the global `experience-app-*` 0.3.2 skills, which the collection never calls. Only `experience-interaction` writes the file, and `quality-interaction` writes its own verdict. The host consequence is stated: once the host reads `produces`, it joins this path to the project root. Add the vocabulary and the tree lines the later tickets need.

**Plan:** `.scratch/plans/IXD_INTERACTION_DESIGN_PLAN.md` - Decisions (user) and Decisions this plan takes 1-3, 5; Steps 1; Risks (host done-state, ADR number).

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] `docs/adr/0015-interaction-decisions-live-in-app-design.md` in the existing ADR style (Status, Context, Decision, Alternatives, Consequences), naming the forked version and the host join.
- [ ] `docs/adr/README.md` row 0015; ADR 0011 and 0013 each get a trailing amendment note in the style of ADR 0007's.
- [ ] `CONTEXT.md` gains **App design**, **Object class**, **Floorplan**, **Surface**, **Representation**: definitions only, no paths.
- [ ] `contracts/concept_structure.md`: a `## Beside the tree` section naming `APP-DESIGN.md` and its writer; tree lines `02_grounding/findings/interaction.md` (concept-reverse) and `11_build/interaction.yaml` (quality-interaction).
- [ ] `python3 scripts/check.py` exits 0 (collection + fixtures, not `--no-tests`); every skill body ≤ 140 lines; pushed run green per the `CLAUDE.md` watch rule.
