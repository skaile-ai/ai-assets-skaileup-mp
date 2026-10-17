# i-ixd-retrofit-smoke: Census, decisions and verdict run end to end on a real app

**What to build:** Copy `forge/skaile-forge` (Nuxt app with `_concept/`, without `node_modules`) to a temp dir. Run `concept-reverse`'s census step, then `experience-interaction` without a user, then `quality-interaction`, following the skill bodies literally. Wherever a step misled or could not be followed, fix the skill or contract text. Delete the temp copy.

**Plan:** `.scratch/plans/IXD_INTERACTION_DESIGN_PLAN.md` - Steps 8; Verification (step 8).

**Blocked by:** i-ixd-reverse-census, i-ixd-reader-hooks, i-ixd-flows

**Status:** ready-for-agent

- [ ] `findings/interaction.md`, `APP-DESIGN.md` and `11_build/interaction.yaml` produced in the temp copy; every `file:line` passes the `ui_detection.md` citation check.
- [ ] Every core type has a floorplan row; every unanswered choice is `[open Qn]` with a § Open row.
- [ ] The verdict has a score, ordered changes and a coverage table that maps every violation to a change or `accepted`.
- [ ] Skill or contract fixes from the run are committed; the resolution lists them; no temp files remain.
- [ ] `python3 scripts/check.py` exits 0 (collection + fixtures, not `--no-tests`); every skill body ≤ 140 lines; pushed run green per the `CLAUDE.md` watch rule.
