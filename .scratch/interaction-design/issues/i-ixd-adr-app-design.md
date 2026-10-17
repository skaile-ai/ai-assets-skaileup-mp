# i-ixd-adr-app-design: ADR 0015 puts the interaction decisions in APP-DESIGN.md at the project root

**What to build:** Record decisions 1-3 and 5: `APP-DESIGN.md` at the project root (the directory holding `_concept/`) is the one named project-root artifact, so it amends ADR 0011/0013. The rulebook is forked from the global `experience-app-*` 0.3.2 skills, which the collection never calls. Only `experience-interaction` writes the file, and `quality-interaction` writes its own verdict. The host consequence is stated: once the host reads `produces`, it joins this path to the project root. Add the vocabulary and the tree lines the later tickets need.

**Plan:** `.scratch/plans/IXD_INTERACTION_DESIGN_PLAN.md` - Decisions (user) and Decisions this plan takes 1-3, 5; Steps 1; Risks (host done-state, ADR number).

**Blocked by:** None (can start immediately)

**Status:** resolved

- [x] `docs/adr/0015-interaction-decisions-live-in-app-design.md` in the existing ADR style (Status, Context, Decision, Alternatives, Consequences), naming the forked version and the host join.
- [x] `docs/adr/README.md` row 0015; ADR 0011 and 0013 each get a trailing amendment note in the style of ADR 0007's.
- [x] `CONTEXT.md` gains **App design**, **Object class**, **Floorplan**, **Surface**, **Representation**: definitions only, no paths.
- [x] `contracts/concept_structure.md`: a `## Beside the tree` section naming `APP-DESIGN.md` and its writer; tree lines `02_grounding/findings/interaction.md` (concept-reverse) and `11_build/interaction.yaml` (quality-interaction).
- [x] `python3 scripts/check.py` exits 0 (collection + fixtures, not `--no-tests`); every skill body ≤ 140 lines; pushed run green per the `CLAUDE.md` watch rule.

**Resolution (2026-10-17):** ADR 0015 (APP-DESIGN.md at the project root, forked rulebook, one writer, names read not coined) indexed; 0011 and 0013 carry amendment notes; CONTEXT.md gains App design, Object class, Floorplan, Surface, Representation; `concept_structure.md` tree lists `findings/interaction.md` and `11_build/interaction.yaml`, the findings section counts seven, and `## Beside the tree` names APP-DESIGN.md. check.py green.
