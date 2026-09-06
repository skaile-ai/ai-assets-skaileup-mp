# 38: Land ticket 35 upstream and prove `main` is green

**Type:** task
**Blocked by:** None — can start immediately
**Status:** resolved

## What to build

`ai-assets-skaileup-mp` `main` is **red on GitHub** and has been since 2026-09-05 22:55: run
[33997272072](https://github.com/skaile-ai/ai-assets-skaileup-mp/actions/runs/33997272072)
(ticket 34) and [34030077992](https://github.com/skaile-ai/ai-assets-skaileup-mp/actions/runs/34030077992)
(the map move) both failed, because ticket 34 changed `check.py`'s rules without updating
`test_check.py` and CI runs both. Ticket 35 repaired it locally — **69 passed**, `29 skill(s) ·
4 flow(s) · 0 error(s)` — but that repair is sitting in an unpushed commit, so nothing outside
this machine knows the collection is healthy.

Land it, and let CI say so rather than a local run. Then carry the pointer up: the super-repo
rule is push the submodule **first**, because it only records commit SHAs and pushing it ahead
of the submodule leaves a dangling reference for everyone else. `-mp` sits two levels down —
`SKAILEdev` → `ai-assets` → `ai-assets-skaileup-mp` — so both levels move, innermost first.

The end state is the delivery repo pointing at a commit CI has verified.

## Acceptance criteria

- [x] `68037b1` (ticket 35) pushed to `origin/main` on `ai-assets-skaileup-mp`
- [x] Its CI run observed **green** — the first green run since `dc8dfea` (2026-09-05 19:47).
      If it fails, that failure is this ticket's work, not a handoff
- [~] ~~`ai-assets` submodule pointer bumped~~ — struck: no such repo, see Resolution
- [x] `SKAILEdev` super-repo pointer bumped to the new `-mp` commit, committed and pushed
      straight to `main` (this super-repo uses no PRs)
- [x] The map's Decisions entry for ticket 35 records the green run id

## Resolution (2026-09-06)

Landed. `8e483e7` (carrying `68037b1`) pushed to `origin/main`; run
[34054544742](https://github.com/skaile-ai/ai-assets-skaileup-mp/actions/runs/34054544742)
passed — the first green `main` since `dc8dfea` (2026-09-05 19:47), ending ~21 hours of red.
Local gate agreed before the push: `check.py` 29 skills · 4 flows · 0 errors, `test_check.py`
69 passed.

**One acceptance criterion was written against a repo layout that does not exist.** The ticket
assumed three levels — `SKAILEdev` → `ai-assets` → `ai-assets-skaileup-mp` — and asked for a
pointer bump at each. There is no `ai-assets` repo: `.gitmodules` registers
`path = ai-assets/ai-assets-skaileup-mp` directly, and `ai-assets/` is a plain directory holding
five sibling submodules, one of which is confusingly *named* `ai-assets/ai-assets`. So `-mp` is a
**direct** submodule of the super-repo and there is exactly one pointer to move, not two. The
criterion is struck rather than met.

The super-repo's working tree carries unrelated modifications across eight other submodules;
only `ai-assets/ai-assets-skaileup-mp` was staged.
