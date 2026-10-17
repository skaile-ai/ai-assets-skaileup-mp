# i-ixd-flows: The interaction nodes sit in the standard, concept-only and reverse flows

**What to build:** Insert `interaction` (experience-interaction) after `datamodel` and before `featuresets` in `appbuilder-standard`, `skaileup-concept-only` and `skaileup-concept-reverse`. Insert `interaction-check` (quality-interaction) after `review` in standard and after `system` in reverse, both before `ops-review`. Update edges, `requires`, group membership, `data.phase` and `flows/README.md` orders. `appbuilder-mvp` is unchanged.

**Plan:** `.scratch/plans/IXD_INTERACTION_DESIGN_PLAN.md` - Target shape › Flows after the plan; Steps 7; Verification (step 7).

**Blocked by:** i-ixd-experience-interaction, i-ixd-quality-interaction

**Status:** resolved

- [x] Node orders match the plan; every edge is `type: flow`; each node carries `data.phase`.
- [x] The F04 gate-writers rule passes on all four flows (the `APP-DESIGN.md` gate is written upstream).
- [x] `python3 .scratch/reports/dump-skill-set-critique-2026-10-15.py` still prints `unmet hard 0`.
- [x] `python3 scripts/check.py` exits 0 (collection + fixtures, not `--no-tests`); every skill body ≤ 140 lines; pushed run green per the `CLAUDE.md` watch rule.

**Resolution (2026-10-17):** `interaction` after `datamodel` in standard, concept-only and reverse; `interaction-check` in `g-review` after `review` (standard) / `system` (reverse), before `ops-review`; mvp unchanged; groups resized; requires exact; flows/README orders and the APP-DESIGN.md paragraph updated. Critique dump: writer rows for both skills, PROJECT_ROOT_ARTIFACTS mirrored, line citations re-pointed; prints `unmet hard 0` (2 pre-existing mockup-feedback writes-vs-produces disagreements left). check.py green.
