# i-ssi-mockup-loop: Mockup renderers and feedback share one source each

**What to build:** `mockup-storybook` reads the walkthrough manifest for screens and journeys (soft prerequisite) instead of re-deriving them. One session schema lives under `mockup-annotate`'s references and `mockup-feedback` cites it by path; prose and templates stop listing the enum. `contracts/feedback_loop.md` gains a `## mockup-feedback` section (screen edits, id promotion) cited at step 4. `mockup-walkthrough` lists only the resolved renderer's references and moves the devlog check into that reference.

**Plan:** `.scratch/plans/SSI_SKILL_SET_IMPROVEMENT_PLAN.md` — Phases › Phase 3 step 13 (F26–F29); Decisions already taken (mockup renderers).

**Blocked by:** i-ssi-flow-rewrite

**Status:** resolved

- [x] `mockup-storybook` reads `walkthrough/manifest.json`.
- [x] Exactly one `session.schema.json`; no enum restated elsewhere.
- [x] `feedback_loop.md § mockup-feedback` exists and is cited.
- [x] `mockup-walkthrough` reference listing and devlog check moved.
- [x] `python scripts/check.py` exits 0 (collection + fixtures, not `--no-tests`); every skill body ≤ 140 lines; pushed run green per the `CLAUDE.md` watch rule.

**Resolution (2026-10-16):** mockup-storybook reads `walkthrough/<renderer>/manifest.json` (soft; falls back to 07_screens + stories.yaml); one session schema under mockup-annotate/references (feedback copy deleted, enums cited); `feedback_loop.md § mockup-feedback` (screen edits, id promotion) cited at feedback step 4; mockup-walkthrough reads only the resolved renderer's references and the devlog check lives in each RENDERER.md. check.py green.
