# 41: Give the host facts an owner

**Type:** task
**Blocked by:** 40 — which settled the shape; this ticket builds it
**Status:** ready-for-agent

## Question

Nothing to decide — [40: The checker's host coupling is asserted, not tested](40-host-coupling-is-asserted-not-tested.md)
settled the shape and measured the evidence. This is the build, and it is a decision's-worth of
work only because it touches every host-derived rule in the collection's only gate.

Five pieces, in order:

1. **`scripts/host_facts.py`** — one row per host *fact*. Fields: `id` (`host:<slug>`), `host`
   (`forge-concept` | `workspaces` | `platform`), `path`, `signature` (a grep-able token, not a
   line), `expect` (`present` | `absent`), `claim` (one sentence), `verified` (ISO date), `rules`
   (the rule ids resting on it), and an advisory `seen_at` line the verifier refreshes. Seed it
   from the 18 comment lines / 14 distinct refs already in `check.py`, and from the four rot
   corrections ticket 40 measured: `validator.ts:81`→`:86`, `profiles.get.ts:30`→`:31` under
   `server/api/pipeline/`, `flow-manager.ts:508`→`:507`, `flow-layout.ts:53-65` shifted.
2. **Thread fact ids through `check.py`** — `rep.error(..., fact="host:...")` at the host-derived
   sites (~12 rules across `_check_presentation`, `_check_nodes`, the `_concept/` prefix rule and
   the `shared-contracts` slug rule). Error text interpolates the path from the table and appends
   the id; the inline `file:line` comments go, replaced by the id.
3. **`scripts/verify_host.py`** — manual, takes the sibling checkouts (`--hosts ../..` resolves
   `forge/forge-concept`, `platform`, `workspaces`). Greps each signature, honours `expect`, and
   prints **holds** / **expired** per fact. `--update` rewrites `verified:` and `seen_at` in place
   after a clean run. Not in push CI: the hosts are absent there.
4. **Tier the reporter** — group the summary as intrinsic / host-derived / house style; a
   host-derived failure prints both readings and names the verifier. No new exit code; house
   style stays an error.
5. **`test_check.py` gates the table** — every `fact=` id used resolves to a row, every row is
   used by at least one rule. Dangles and orphans both fail. Plus fixtures for the tiering.

Then cross-reference: one line in the map's forge-concept register pointing at the table, saying
what each holds and why they stay apart.

**Watch for:** `check.py` runs `test_check.py` as its last phase (ticket 39's rule — one command
means green). A `fact=` kwarg added to `rep.error` without updating the fixtures is exactly the
ticket-34 failure this ticket exists to make impossible.

## Answer

_(pending)_
