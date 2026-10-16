# i-ssi-screens-shell: Screen elements and journey stages each have a named owner

**What to build:** `contracts/elements_block.md` names both writers (`spec-feature` for screens, `experience-shell` for `kind: nav` in `shell.md`), and `spec-feature`'s intro says so correctly. Stage definitions are owned by `experience-journeys`; `spec-featuresets` and `experience-shell` cite `stories.yaml § stages`.

**Plan:** `.scratch/plans/SSI_SKILL_SET_IMPROVEMENT_PLAN.md` — Phases › Phase 3 step 12 (F21, F24, F25).

**Blocked by:** i-ssi-flow-rewrite, i-ssi-spec-truth

**Status:** resolved

- [x] Both writers named in the elements contract; `spec-feature` intro corrected.
- [x] Stage definitions only in `experience-journeys`; the two others cite them.
- [x] `python scripts/check.py` exits 0 (collection + fixtures, not `--no-tests`); every skill body ≤ 140 lines; pushed run green per the `CLAUDE.md` watch rule.

**Resolution (2026-10-16):** `elements_block.md § Writers` names spec-feature (screen `elements:`) and experience-shell (`kind: nav` in shell.md); spec-feature intro corrected (138 lines). experience-journeys writes `stories.yaml` `stages:` as the one definition; spec-featuresets and experience-shell cite `stories.yaml § stages`; experience-shell cites `elements_block.md § Schema`. The `stages:` key in artifact_frontmatter.md's stories.yaml schema lands in the i-ssi-build-quality-joins commit (same file). check.py green.
