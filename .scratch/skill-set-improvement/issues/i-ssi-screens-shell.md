# i-ssi-screens-shell: Screen elements and journey stages each have a named owner

**What to build:** `contracts/elements_block.md` names both writers (`spec-feature` for screens, `experience-shell` for `kind: nav` in `shell.md`), and `spec-feature`'s intro says so correctly. Stage definitions are owned by `experience-journeys`; `spec-featuresets` and `experience-shell` cite `stories.yaml § stages`.

**Plan:** `.scratch/plans/SSI_SKILL_SET_IMPROVEMENT_PLAN.md` — Phases › Phase 3 step 12 (F21, F24, F25).

**Blocked by:** i-ssi-flow-rewrite, i-ssi-spec-truth

**Status:** ready-for-agent

- [ ] Both writers named in the elements contract; `spec-feature` intro corrected.
- [ ] Stage definitions only in `experience-journeys`; the two others cite them.
- [ ] `python scripts/check.py` exits 0 (collection + fixtures, not `--no-tests`); every skill body ≤ 140 lines; pushed run green per the `CLAUDE.md` watch rule.
