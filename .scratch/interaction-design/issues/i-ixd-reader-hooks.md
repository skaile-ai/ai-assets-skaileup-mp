# i-ixd-reader-hooks: Screens, shell, concept review and slice planning read the interaction decisions

**What to build:** `spec-feature` step 6: screens follow the `APP-DESIGN.md` OBJ `task → surface` rows; a missing surface is handed back to `experience-interaction`; soft prerequisite. `experience-shell`: step 2 cites § Navigation (P12), step 5 cites MSG/EDIT/MOD and keeps layout only. `ops-review`: a step that checks screen specs for P1, P4, P8 and P13 against `APP-DESIGN.md`, each finding naming its fixing skill. `build-plan`: soft-reads `11_build/interaction.yaml`; a feature's open changes join its slices, and systemic changes become a leading slice.

**Plan:** `.scratch/plans/IXD_INTERACTION_DESIGN_PLAN.md` - Decisions this plan takes 6; Target shape › Hooks; Steps 6; Risks (spec-feature ceiling, ops-review length).

**Blocked by:** i-ixd-experience-interaction, i-ixd-quality-interaction

**Status:** resolved

- [x] `spec-feature` stays ≤ 140 lines (fallback per Risks: the rule lives in `contracts/app_design.md § Reading it`, cited in one line).
- [x] `experience-shell` no longer decides empty, error or confirmation patterns itself.
- [x] `ops-review` finding rows name `spec-feature` or `experience-interaction` as fixer.
- [x] `build-plan` names the systemic-slice rule and the soft gate.
- [x] `python3 scripts/check.py` exits 0 (collection + fixtures, not `--no-tests`); every skill body ≤ 140 lines; pushed run green per the `CLAUDE.md` watch rule.

**Resolution (2026-10-17):** `spec-feature` (140 lines) soft-gates APP-DESIGN.md and step 6 applies the OBJ `task → surface` rows, handing a missing surface to `experience-interaction`; `experience-shell` derives nav under § Navigation and takes MSG/EDIT/MOD, keeping layout only (proposals without the file); `ops-review` step 4 checks screen specs for P1/P4/P8/P13, each finding naming `spec-feature` or `experience-interaction` (108 lines); `build-plan` soft-reads `11_build/interaction.yaml`, feature changes join that feature's slices, systemic changes become a leading slice. `artifacts.requires` gains app-design / interaction-review (cycle-detection only, ADR 0011). check.py green.
