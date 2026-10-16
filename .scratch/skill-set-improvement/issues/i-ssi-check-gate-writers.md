# i-ssi-check-gate-writers: The gate fails a hard prerequisite that nothing upstream writes

**What to build:** `check.py` walks each flow from its entry along `type: flow` edges, accumulates the `produces` paths of the nodes passed, and reports any `hard` prerequisite with no upstream writer (directory gates match by prefix). The critique's dump shows zero unmet hard gates.

**Plan:** `.scratch/plans/SSI_SKILL_SET_IMPROVEMENT_PLAN.md` — Phases › Phase 2 step 9 (F04); Verification (Phase 2 proof).

**Blocked by:** i-ssi-flow-rewrite

**Status:** resolved

- [x] Gate rule implemented; passes on all four flows.
- [x] Fixture: a flow whose gate has no writer yields exactly one error.
- [x] `python3 .scratch/reports/dump-skill-set-critique-2026-10-15.py` reports `unmet hard 0`.
- [x] `python scripts/check.py` exits 0 (collection + fixtures, not `--no-tests`); every skill body ≤ 140 lines; pushed run green per the `CLAUDE.md` watch rule.

**Resolution (2026-10-16):** `_check_gate_writers` (intrinsic): per flow, a skill node's hard `_concept/` gate must be covered by an upstream node's `produces` path (equal or directory prefix, `<…>`/`*` placeholders). Fixtures: no writer, writer upstream, writer only downstream, prefix/placeholder cases, soft and project-root gates exempt; fixture default gate now soft. All four real flows pass. check.py green (161 fixtures). The dump's `unmet hard 0` is verified in the finish step, once the critique dump's writer map is re-cited to the new tree.
