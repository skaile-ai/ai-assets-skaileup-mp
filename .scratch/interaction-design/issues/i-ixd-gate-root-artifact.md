# i-ixd-gate-root-artifact: The gate accepts APP-DESIGN.md as the one project-root artifact

**What to build:** `scripts/check.py` gets `PROJECT_ROOT_ARTIFACTS = {"APP-DESIGN.md"}`. `_check_produces` accepts a path in that set as well as a `_concept/` tree path. `APP-DESIGN.md` joins `PROJECT_ROOT_PREREQUISITES`. `_check_gate_writers` matches a hard project-root gate in that set against upstream `produces`, where today it skips such gates. Any other root path is still an error. `docs/skill-template.md` names the exception.

**Plan:** `.scratch/plans/IXD_INTERACTION_DESIGN_PLAN.md` - Decisions this plan takes 1; Steps 2; Verification (step 2).

**Blocked by:** i-ixd-adr-app-design

**Status:** resolved

- [x] `produces: [{ id: app-design, path: "APP-DESIGN.md" }]` passes; `path: "NOTES.md"` is an error naming the allowed set.
- [x] A hard `APP-DESIGN.md` prerequisite with no upstream writer in a flow yields exactly one gate-writers error; with a writer upstream, none.
- [x] Three fixtures in `scripts/test_check.py` in the existing style, failing before the change and passing after it.
- [x] `docs/skill-template.md` states the one project-root artifact beside the `produces` block.
- [x] `python3 scripts/check.py` exits 0 (collection + fixtures, not `--no-tests`); every skill body ≤ 140 lines; pushed run green per the `CLAUDE.md` watch rule.

**Resolution (2026-10-17):** `PROJECT_ROOT_ARTIFACTS = {"APP-DESIGN.md"}` in check.py: accepted as a `produces` path, any other root path errors naming the set; a hard gate on it is matched against upstream `produces` (package.json gates still skipped); APP-DESIGN.md added to project-root prerequisites. Four fixtures (4 of 6 root tests fail with check.py stashed). Template sentence added. check.py green, 168 fixtures.
