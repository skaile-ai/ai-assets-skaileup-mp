# 38: Land ticket 35 upstream and prove `main` is green

**Type:** task
**Blocked by:** None — can start immediately
**Status:** ready-for-agent

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

- [ ] `68037b1` (ticket 35) pushed to `origin/main` on `ai-assets-skaileup-mp`
- [ ] Its CI run observed **green** — the first green run since `dc8dfea` (2026-09-05 19:47).
      If it fails, that failure is this ticket's work, not a handoff
- [ ] `ai-assets` submodule pointer bumped to the new `-mp` commit, committed and pushed
- [ ] `SKAILEdev` super-repo pointer bumped to the new `ai-assets` commit, committed and pushed
      straight to `main` (this super-repo uses no PRs)
- [ ] The map's Decisions entry for ticket 35 records the green run id
