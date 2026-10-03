# i-opt-foreign-skills-adr: Record why the collection depends on five foreign skills and what it took from pstack and Pocock

**What to build:** ADR 0012 records, as landed, the decisions this effort made: the five external skills with their axis and hard/soft status and why they stay global (D1); the gate-enforced phrasing rule (D2); the todo-list and evidence-label patterns (D4, D5); the design red-flags screen (D6); why there is no principles layer (D7); and, one line each, what was not adopted and why (D9). Context cites the two-library comparison at `/Users/matthias/devBench/agent-tests/skill-libraries-pstack-vs-mattpocock-2026-10.md`. Consequences: adding a sixth external skill is a gate edit plus this ADR's list; the phrasing rule is CI-enforced; the principles-layer question is closed.

**Plan:** `.scratch/plans/OPT_SKAILEUP_MP_SKILL_OPTIMISATION_PLAN.md` — S6, decision D10 (recording D1–D9), findings F1, F3, F4; ticket-breakdown row T7.

**Blocked by:** `i-opt-skill-call-convention`, `i-opt-agent-patterns-rewrite`, `i-opt-design-red-flags`, `i-opt-readme-skill-index`

**Status:** resolved

- [ ] The ADR follows the format of ADR 0001 (title line, `**Status:** accepted`, Context / Decision / Consequences).
- [ ] It describes what actually landed in the blocking tickets; any deviation from the plan is stated, not papered over.
- [ ] The ADR index gains the row in its existing list format.
- [ ] `python scripts/check.py` exits 0 (doc links resolve).
