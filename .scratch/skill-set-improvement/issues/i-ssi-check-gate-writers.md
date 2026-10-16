# i-ssi-check-gate-writers: The gate fails a hard prerequisite that nothing upstream writes

**What to build:** `check.py` walks each flow from its entry along `type: flow` edges, accumulates the `produces` paths of the nodes passed, and reports any `hard` prerequisite with no upstream writer (directory gates match by prefix). The critique's dump shows zero unmet hard gates.

**Plan:** `.scratch/plans/SSI_SKILL_SET_IMPROVEMENT_PLAN.md` — Phases › Phase 2 step 9 (F04); Verification (Phase 2 proof).

**Blocked by:** i-ssi-flow-rewrite

**Status:** ready-for-agent

- [ ] Gate rule implemented; passes on all four flows.
- [ ] Fixture: a flow whose gate has no writer yields exactly one error.
- [ ] `python3 .scratch/reports/dump-skill-set-critique-2026-10-15.py` reports `unmet hard 0`.
- [ ] `python scripts/check.py` exits 0 (collection + fixtures, not `--no-tests`); every skill body ≤ 140 lines; pushed run green per the `CLAUDE.md` watch rule.
