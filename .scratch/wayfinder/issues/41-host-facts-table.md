# 41: Give the host facts an owner

**Type:** task
**Blocked by:** 40 — which settled the shape; this ticket builds it
**Status:** resolved

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

**Built 2026-09-09, all five pieces, with two amendments to ticket 40's shape and one
correction to a claim it did not measure.**

`scripts/host_facts.py` holds **23 facts** — forge-concept 16, workspaces 7. No rule rests on
`platform`: the "platform's `validateFlow` requires `name`" comment was misattributed, and the
schema (`FlowManifestSchema`, `name: z.string().min(1)`) lives in
`@skaile/workspaces/factory-assets/connectors/flow/engine/flow-manifest.ts`. `platform` stays a
legal `HOSTS` key because the collection is installed there too.

`check.py` cites facts at **30 `rep.error(..., fact=...)` sites**; `{host}` in a message is
replaced by the row's host and path, so a message cannot drift out of step with its row. Every
inline `file:line` is gone — the two remaining host mentions name functions
(`extractFlowRequires`, `slugifyAssetName`), not lines. `scripts/verify_host.py` greps the
signatures against sibling checkouts and reports **holds** / **expired** per fact, with
`--update` rewriting `verified:` and the advisory `seen_at`. `print_report` groups intrinsic /
host-derived / house style, and a host-derived failure prints both readings and names the
verifier — one exit code throughout.

**Amendment 1: `fact=` takes a string or a tuple.** The edge-type rule rests on two facts in two
files — `run.post.ts` gathers handoff context along `type: flow`, `flow-extended-state.ts`
computes readiness along it — and they can rot apart. Ticket 40 covered one fact backing several
rules but not the reverse; forcing one id here would have meant either an orphan row or merging
two files behind one grep, which is the coverage the table exists to buy. `{host}` interpolates
the first.

**Amendment 2: `data.parameters` and `data.writes` are host-derived, not house style.** Ticket 40
put "the three dead key bans" in house style. Two of them still have live reads
(`shared/flow-extended.ts` for `parameters.flow`, `flow-manager.ts` twice for `writes`), so those
bans change meaning the day the host stops reading — which is the definition of host-derived.
House style ends up at the same five rules by a truer cut: the 140-line ceiling, `meta.category`,
the dead globals, the plural rule, and the node-kind ban.

**The self-gate is an AST reconciliation, not a text scan.** `test_check.py` parses `check.py`
and collects every string constant matching `^host:[a-z][a-z0-9-]*$`. Comments are invisible to
the AST, which is the point: a fact named only in prose is precisely the unowned rule ticket 34
shipped. Dangles and orphans each fail. It found one orphan on the first run
(`host:flow-edge-gates-state`), which is what forced amendment 1.

**A fifth rotted claim, found by the same method ticket 40 used.** `check.py` banned `${...}`
because "no resolver exists anywhere in either host". @skaile/workspaces has **three** —
`contract/expression.ts`, `contract/normalize.ts`, `engine/bindings.ts`. The rule survives: the
node-run path in forge-concept concatenates the skill body into the prompt and calls none of
them. So the fact is now scoped to that one file and expressed as `expect: absent`, which makes
the dangerous direction loud — if forge-concept ever gains a resolver there, `verify_host.py`
says **expired** instead of the ban silently becoming wrong. Ticket 40's argument for
first-class absence, confirmed by the first negative fact it was applied to.

**Evidence.** All 23 facts verify **holds** against forge-concept `d16003d` and workspaces
`995deb12`. `python scripts/check.py` is green: 30 skills, 4 flows, 0 errors, **107 fixtures**
(69 before, 38 added). Four rot corrections ticket 40 measured are folded into the seed rows;
`flow-manager.ts` reads `data.writes` at **L361 and L508** at this HEAD, not `:507` — which is
the last argument for line numbers being output rather than data.

**Cross-referenced, not merged:** the map's forge-concept register gains a leading entry saying
what each holds and why they stay apart (ticket 40 (8)).

### Amended after review

Two reviewers, independently, found the same hole: **the `rules` column was prose no test read.**
27 of its 30 ids appeared nowhere in code, `verify_host.py` printed them on every expiry, and
`test_fact_rows_are_well_formed` asserted only that the tuple was non-empty. That is this
ticket's own defect class one field further in — the thing it was built to abolish, rebuilt in
the artifact abolishing it. Fixed properly rather than noted: every one of the 30 sites now
passes **`rule=`** beside `fact=`, `Report.error` **refuses** a rule id the cited row does not
list (and refuses a fact with no rule, and a rule with no fact), and `test_check.py` reconciles
both directions against the AST. This is a deviation from the spec's `rep.error(..., fact=...)`
shape, taken because the spec's own gate — 40 (5), "every row is used by at least one rule" —
cannot be honoured while rule ids exist only in the table.

Also from review: the AST scan **excluded docstrings**, which are `ast.Constant` and would have
satisfied the orphan gate without a citation (latent — zero cases); five stale `file:line` refs
in `test_check.py` fixture docstrings replaced by fact ids, three of them already contradicted by
the new table; the unused `ABSENT` import, `where()` and `rule_ids()` deleted; `verify_host.py`
no longer warns about a missing `platform` checkout, since no fact rests on it. CONTEXT.md gains
a **Host** entry — the word was already used there in two senses (the harness, and forge-concept)
and defined in neither.

**Declined, with reasons.** *Duplicated Code between each `claim` and the message it backs*: they
are not the same statement — the claim records host behaviour, the message says what is wrong
with this collection — and neither can become a reference that resolves to nothing, which is the
drift the table exists to stop. *Feature Envy, `check_fact` → `Fact.check`*: it would put
filesystem I/O into the data module the checker imports. *Divergent Change in `check.py`*: one
script, one gate is the documented shape (CLAUDE.md), not an accident of this ticket.

**Disclosed deviations.** `verify_host.py` gained a `--fact <id>` flag the spec did not name; the
tiered reporter prints it, so it is coupled rather than speculative. `flow-manager.ts:508` is
**not** corrected to `:507` as the spec's four seed corrections listed: at `d16003d` the reads are
at L361 and L508, re-measured. `seen_at` is refreshed output, never data (40 (3)), so this is the
line-numbers-are-not-data rule working, not an omission.

**Final state.** 23 facts, 30 rule ids, 30 citing sites; all verify **holds** against forge-concept
`d16003d` and workspaces `995deb12`. `python scripts/check.py`: 30 skills, 4 flows, 0 errors,
**113 fixtures**.
