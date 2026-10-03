# i-opt-readme-skill-index: The README lists every skill, and the gate keeps the list complete

**What to build:** The README's stale "Status: Skeleton" section is replaced by a `## Skills` index: one row per skill directory (30 today), `skaileup` first and then grouped by domain in the nine-domain order, each row linking the skill and giving a one-line purpose drawn from its own description. The documentation-site and gate paragraphs move under a `## Gate` heading. The gate already rejects a row naming a skill that does not exist; it now also reports a skill missing from the index — only when the README has a `## Skills` heading, so READMEs without an index (including the existing doc fixtures) are untouched.

**Plan:** `.scratch/plans/OPT_SKAILEUP_MP_SKILL_OPTIMISATION_PLAN.md` — S5, decision D8, D11(c), findings F8, F11; ticket-breakdown row T6.

**Blocked by:** None (can start immediately). Edits the gate and its tests in a different function from `i-opt-skill-call-convention`; whoever lands second rebases.

**Status:** resolved

- [ ] Row links are written `skills/<name>/` without a `./` prefix, so the existing skill-path token reader sees them.
- [ ] Completeness rule (house rule) reuses the same skill-path reader as the phantom-name check, so both directions read the table identically; message names the missing skill.
- [ ] Fixture tests: a `## Skills` README missing one skill reports it; a README without the heading reports nothing; the two existing root-README fixtures still pass.
- [ ] Negative proof per plan Verification step 2b: removing one row makes the gate report it; restored afterwards.
- [ ] `python scripts/check.py` exits 0.
