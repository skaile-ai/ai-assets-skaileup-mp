# i-ixd-flows: The interaction nodes sit in the standard, concept-only and reverse flows

**What to build:** Insert `interaction` (experience-interaction) after `datamodel` and before `featuresets` in `appbuilder-standard`, `skaileup-concept-only` and `skaileup-concept-reverse`. Insert `interaction-check` (quality-interaction) after `review` in standard and after `system` in reverse, both before `ops-review`. Update edges, `requires`, group membership, `data.phase` and `flows/README.md` orders. `appbuilder-mvp` is unchanged.

**Plan:** `.scratch/plans/IXD_INTERACTION_DESIGN_PLAN.md` - Target shape › Flows after the plan; Steps 7; Verification (step 7).

**Blocked by:** i-ixd-experience-interaction, i-ixd-quality-interaction

**Status:** ready-for-agent

- [ ] Node orders match the plan; every edge is `type: flow`; each node carries `data.phase`.
- [ ] The F04 gate-writers rule passes on all four flows (the `APP-DESIGN.md` gate is written upstream).
- [ ] `python3 .scratch/reports/dump-skill-set-critique-2026-10-15.py` still prints `unmet hard 0`.
- [ ] `python3 scripts/check.py` exits 0 (collection + fixtures, not `--no-tests`); every skill body ≤ 140 lines; pushed run green per the `CLAUDE.md` watch rule.
