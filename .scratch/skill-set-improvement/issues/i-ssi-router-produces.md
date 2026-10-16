# i-ssi-router-produces: The router finds the next node from produces, and scope owns the defaults

**What to build:** `skaileup` picks the next flow node by comparing each node skill's `produces` against the project tree instead of scanning folders; `concept-scope` is the single owner of the `web-app` default and the flow choice, and `skaileup` points at it rather than restating them.

**Plan:** `.scratch/plans/SSI_SKILL_SET_IMPROVEMENT_PLAN.md` — Phases › Phase 1 step 5 (F15, F44).

**Blocked by:** i-ssi-produces-list

**Status:** ready-for-agent

- [ ] `skaileup` body resolves the next node via `produces` paths, with no hand-kept folder scan.
- [ ] `web-app` default and flow choice stated only in `concept-scope`; `skaileup` cites it.
- [ ] `python scripts/check.py` exits 0 (collection + fixtures, not `--no-tests`); every skill body ≤ 140 lines; pushed run green per the `CLAUDE.md` watch rule.
