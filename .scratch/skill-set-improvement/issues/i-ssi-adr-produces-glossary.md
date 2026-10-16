# i-ssi-adr-produces-glossary: Two ADRs record that a skill declares what it produces and that the glossary is a root file

**What to build:** A reader of `docs/adr/` finds the two shape decisions the rest of the effort builds on before any skill changes: ADR 0013 says every skill declares `metadata.artifacts.produces: [{ id, path }]` (ids are what `artifacts.requires` names, paths are `_concept/`-prefixed and appear in `concept_structure.md`'s tree fence), that no registry is generated, and that the host's `produced_by` read is an external dependency. ADR 0014 amends ADR 0007's root list to `brief.md · goals.md · glossary.md` and folds `comparable.md` into a `## Comparables` section of `brief.md`.

**Plan:** `.scratch/plans/SSI_SKILL_SET_IMPROVEMENT_PLAN.md` — Phases › Phase 1 step 1; Decisions this plan takes 1–2; Risks (host done-state).

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] ADR 0013 "A skill declares what it produces" written in the existing ADR style, naming the no-registry decision and the host `produced_by` dependency.
- [ ] ADR 0014 "The glossary is a root file" written, explicitly amending ADR 0007's root list; `comparable.md` → `brief.md § Comparables`.
- [ ] `docs/adr/README.md` indexes both.
- [ ] `python scripts/check.py` exits 0 (collection + fixtures, not `--no-tests`); every skill body ≤ 140 lines; pushed run green per the `CLAUDE.md` watch rule.
