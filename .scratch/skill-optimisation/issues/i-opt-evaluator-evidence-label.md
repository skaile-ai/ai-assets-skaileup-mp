# i-opt-evaluator-evidence-label: Every review finding says how it was obtained

**What to build:** The evaluator contract's stance tells every verdict-writing skill (`ops-review`, `quality-review`, `quality-release`) to state in the same sentence whether a finding is **measured** (seen in the artifact or the running app, quoted or reproduced) or **inferred** (follows from something measured, and names it). A claim that is neither is not a finding: the agent runs the check that would make it one, or leaves it out, and never hands the user a check it could have run. An absence counts as measured, with the quote marking where the missing statement should have been.

**Plan:** `.scratch/plans/OPT_SKAILEUP_MP_SKILL_OPTIMISATION_PLAN.md` — S3, decision D5, D11(d), finding F6; ticket-breakdown row T4.

**Blocked by:** None (can start immediately)

**Status:** resolved

- [ ] The paragraph is appended to the evaluator contract's `## Stance`, in the house voice (no MUST/NEVER tokens).
- [ ] No mapping from evidence label to severity is introduced; the four levels of `§ Flag shape` are unchanged.
- [ ] `## Laws` is left as it is (restyle deferred per D9).
- [ ] No reader skill changes; `python scripts/check.py` exits 0.
