# i-opt-skill-call-convention: One way to call a skill the collection does not ship, enforced by the gate

**What to build:** Every skill that relies on one of the five global skills (`grilling`, `tdd`, `code-review`, `diagnosing-bugs`, `triage`) phrases the call the same way, says what happens when that skill is absent, and the gate fails the build when a body drifts from the convention. A model-invoked skill is called as `Call the Skill tool with "<name>"`; the user-invoked `triage` is an instruction to the human (`tell the user to run /triage`), never a Skill-tool call. `tdd` and `code-review` are hard dependencies (the caller stops and names the missing one); `grilling`, `diagnosing-bugs` and `triage` are soft (the caller degrades and says so). The list of external skills and their invocation axis lives in exactly one place, in the gate.

**Plan:** `.scratch/plans/OPT_SKAILEUP_MP_SKILL_OPTIMISATION_PLAN.md` — S1 (steps 1–5), decisions D1, D2, D11(a–b), findings F4, F5, F5a; ticket-breakdown rows T1 and T2 (merged).

**Blocked by:** None (can start immediately)

**Status:** resolved

- [ ] The gate holds the external-skill list with each skill's axis (model / user) as its single source of truth.
- [ ] House rule: a Skill-tool call naming something that is neither a collection skill nor a model-axis external skill is reported; a Skill-tool call naming a user-axis skill is reported with the "tell the user to run" fix. Lower-case mid-sentence calls are matched too.
- [ ] House rule: a bare `/name` for a collection skill or a model-axis external skill is reported; other `/word` tokens (paths) are ignored.
- [ ] Fixture tests in the existing style: three negatives (unknown name, user-invoked name, bare `/tdd`) asserting on message text, and one positive (single call, "call the Skill tool twice, for …", "tell the user to run `/triage`") reporting nothing.
- [ ] `build-implement`, `quality-review`, `spec-feature` and `skaileup` reworded per plan S1.4, each with its hard/soft fallback; `quality-test`'s boundary mention left as a mention.
- [ ] The skill template's "rules behind it" gains the invocation bullet (S1.5).
- [ ] Phrasing sweep matches plan Verification step 3 exactly (6 Skill-tool calls across 3 skills; `/triage` only in `skaileup`, inside "tell the user to run").
- [ ] Every skill body stays at or under 140 lines; `python scripts/check.py` exits 0 with no error or house rows.
