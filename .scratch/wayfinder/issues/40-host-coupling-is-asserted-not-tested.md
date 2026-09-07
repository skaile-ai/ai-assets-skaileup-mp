# 40: The checker's host coupling is asserted, not tested

**Type:** grilling
**Blocked by:** None — independent of 39, though it comes from the same failure family
**Status:** ready-for-agent

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

_(pending)_
