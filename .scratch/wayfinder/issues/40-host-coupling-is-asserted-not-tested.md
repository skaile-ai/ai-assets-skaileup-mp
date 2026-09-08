# 40: The checker's host coupling is asserted, not tested

**Type:** grilling
**Blocked by:** None — independent of 39, though it comes from the same failure family
**Status:** resolved

## Question

`scripts/check.py` is the collection's only gate, and it is right to be: forge-concept
validates no flow at all, and a `data.skill` that resolves to nothing returns a fabricated
`satisfied: true`. But roughly a dozen of its rules are **copies of facts in someone else's
repo**, each justified in a comment naming a `file:line` that nothing re-checks.

Measured 2026-09-07 against `forge/forge-concept` at `d16003d`: `check.py` carries **18 lines
citing host source, 14 distinct `file:line` refs**. Every underlying *fact* still holds —
`description`, `meta.icon`, `globals.research_depth`, `onboarding.input_style`/`fields`, the
`data.writes` fallback are all live. Every *pointer* has begun to rot:

- `profiles.get.ts:30` → the file is `server/api/**pipeline**/profiles.get.ts`, the line is 31
- `flow-manager.ts:361` → the file is `server/utils/flow-manager.ts`; line right, path wrong
- `flow-layout.ts:53-65` → still there, block shifted

Within roughly two weeks. So the coupling is not wrong, its **bookkeeping is unfalsifiable** —
which is this collection's own defect class (a reference that resolves to nothing quietly),
one level further out than ticket 39 found it.

Under that sits a second problem: `check.py` mixes three kinds of rule and reports them
identically.

- **Intrinsic** (~30) — `name:` == directory, links resolve, `requires:` ↔ node set, edges
  reference real nodes, reachability from `entry:`, `id` == stem == dir. Depend on nothing
  outside this repo.
- **Host-derived** (~12) — `metadata:` nesting, the `_concept/` prefix, `data.phase` presence
  and enum, `meta.onboarding` shape, `input_style` / `research_depth` enums, the
  `shared-contracts` slug rule.
- **House style** (~5) — the 140-line ceiling, the three "dead key" bans, the plural rule. A
  violation costs nothing at runtime; the banned keys are inert, not quiet.

When a host-derived rule fails you cannot tell whether the collection is wrong or the fact
expired, and ticket 34 could add five rules that depended on host behaviour with **no owner** —
nothing forced it to declare the dependency or leave a fixture behind.

Candidate moves, sketched 2026-09-07 and not settled:

1. **Cite by signature, not by line** — a distinctive token (`research_depth_options`,
   `flow.globals?.research_depth`) survives a refactor; `:47` does not.
2. **One host-facts table** (`scripts/host_facts.py`, or a contract plus a loader): host, path,
   signature, the claim in one sentence, date verified, and the rule ids that rest on it. The 18
   scattered comments collapse into one inventory — and so does the map's forge-concept register,
   which is the same table written as prose.
3. **`scripts/verify_host.py`** — point it at the local checkouts (`forge/forge-concept`,
   `platform`, `workspaces`, all present on this machine) and grep each signature. found / moved /
   **gone**. This is the move that decouples: the coupling becomes tested rather than asserted.
   Not in the push CI, where the hosts are absent — a separate scheduled or manual run.
4. **Tier the output**, so only the intrinsic tier can read as "the collection is broken", and a
   host-derived failure prints both readings with its fact id.
5. **Make the table gate itself** — `test_check.py` asserts every host-derived rule id appears in
   the table and every fact has at least one fixture, so a rule of that class cannot land unowned.
6. **Demote the house-style tier** to warnings or `--strict`.

The question is which of these earn their place, and what the fact record actually holds.

**Not this ticket:** removing the dependency. The collection's job is to fit the host, and a
schema-level handshake is the successor effort's ground (ticket 15's). Decoupling here means
**enumerable, dated, testable** — not absent.

## Answer

**Four of the six sketched moves earn their place; two do not.** The coupling stays — the
collection's job is to fit the host — but it becomes **enumerable, dated and testable**: one
imported fact table, cited by signature rather than by line, a manual verifier that greps the
local checkouts, and tiered output so a host-derived failure states both of its readings.

**The measurement that settles it** (2026-09-08, forge-concept `d16003d`, workspaces `cf1d222d`):
of `check.py`'s 14 distinct `file:line` refs, **4 have rotted in roughly two weeks and every
underlying fact still holds.** `validator.ts:81` (cited twice, the `_concept/` prefix rule) is now
`:86`; `profiles.get.ts:30` is `:31` and the path is missing its `pipeline/` segment;
`flow-manager.ts:508` is `:507`; `flow-layout.ts:53-65` has shifted around its `lanes: []` return.
The other nine are exact. So the defect is entirely in the bookkeeping — which is this repo's own
defect class, a reference that resolves to nothing quietly, one level further out than ticket 39
found it.

1. **The fact record is `scripts/host_facts.py`, imported by `check.py`, and a row is one
   *fact*, not one rule.** Prose in `contracts/` would rot exactly like the comments it replaces;
   only an imported table can be gated by a test. Fact-granular because one fact backs several
   rules (`profiles.get.ts` reading `meta.onboarding` backs three) and the verifier greps facts.
   A row holds: **host · path · signature · `expect` · claim (one sentence) · `verified:` date ·
   the rule ids resting on it.**
2. **Cite by signature; the line number stops being data.** A distinctive token
   (`research_depth_options`, `flow.globals?.research_depth`) survives a refactor and `:47` does
   not — that is precisely what the measurement shows. Error text **interpolates the path from
   the table** and appends the fact id, so the message stays readable, cannot drift out of step
   with the row, and has exactly one place to be corrected.
3. **`verify_host.py` gets built, manual-only.** This is the move that makes the coupling tested
   rather than asserted; it is ~40 lines over the table. It is **not** wired into push CI, where
   the hosts are absent — a scheduled job that checks out three sibling repos is more machinery
   than a fact set that changed zero times in two weeks deserves. Two verdicts, **holds** /
   **expired**, plus **`--update`**, which rewrites `verified:` dates and advisory line numbers
   after a clean run. Without the writeback the dates rot the way the line numbers just did.
   Advisory line numbers are fine once nothing depends on them: they are *output*, refreshed by
   the tool, never hand-maintained.
4. **A fact records absence as first-class**, via `expect: present | absent`. Several claims are
   negative — no `${...}` resolver in either host, `validateFlow` with zero call sites, the dead
   globals with no reader — and absence is where the rot is most dangerous: a host that *gains*
   a `${}` resolver silently makes a ban wrong, and today nothing would ever say so. The grep
   inverts: found = **expired**.
5. **The table gates itself through rule ids in code.** `rep.error(..., fact="host:...")` at the
   ~12 host-derived sites, and `test_check.py` asserts **every id used resolves to a row and every
   row is used by at least one rule** — dangles and orphans both fail. Asserting only that rows
   are well-formed would check the table's shape and not the thing that actually went wrong:
   ticket 34 added five host-dependent rules with no owner, and nothing forced it to declare
   them. The orphan half matters too — a deleted rule leaves its fact behind, which is how the
   map's register accumulated stale entries.
6. **`check.py` tiers its *output*, not its severity.** The summary groups intrinsic /
   host-derived / house style, and a host-derived failure prints both readings ("either this
   collection is wrong, or fact `host:...` expired — run `verify_host.py`"), because until
   someone runs the verifier that failure is genuinely ambiguous. **No second exit code**: a red
   gate is a red gate, and a distinct code invites a CI config that ignores it.
7. **The house-style tier stays errors.** The 140-line ceiling is ADR 0003 and the dead-key bans
   are how ticket 10's deletions stay deleted; both are decisions this map made, and a warning
   nobody is forced to read is how they come back. The complaint behind "demote them" was
   legibility, which (6) already answers.
8. **The map's forge-concept register does not merge into the table.** They look alike and are
   not: the register records **constraints the host forced and workarounds accepted**, a finished
   argument that is the successor effort's input; the table records **facts this checker depends
   on**, live machinery. Different lifetimes, different readers. Cross-reference, don't merge.

**The build is [41: Give the host facts an owner](41-host-facts-table.md), not this ticket.**
Adding the table, rewriting ~18 comments, threading fact ids through ~12 call sites, the verifier
and the tiered reporter is its own session — the same shape tickets 39 and 36 took.
