# Brief — 40: The checker's host coupling is asserted, not tested

Measured 2026-09-08 against the local checkouts: `forge/forge-concept` at `d16003d`,
`workspaces` at `cf1d222d`, `platform` at `f08a37528`. Findings only; the answer is the ticket's.

## The drift

`check.py` carries 18 comment lines citing host source, **14 distinct `file:line` refs**.
Verified one by one:

| citation | today | |
|---|---|---|
| `validator.ts:81` (×2 — the `_concept/` prefix rule) | the join is `path.join(projectDir, req.path)` at **`:86`** | expired |
| `profiles.get.ts:30` (`description` published verbatim) | **`:31`** (`:30` is now `name`), and the file is `server/api/**pipeline**/profiles.get.ts` | expired |
| `flow-manager.ts:361,508` (`data.writes`) | `:361` exact; the second read is **`:507`** | half expired |
| `flow-layout.ts:53-65` (positioned nodes ⇒ `lanes: []`) | block shifted; the early return is **`:64`** | drifted, still inside |
| `profiles.get.ts:47` (`research_depth_options`) | exact | holds |
| `profiles.get.ts:29-40`, `:31`, `:33-36` (icon, `input_style` cast) | block now spans `:29-42`; the cast is `:34-37` | drifted |
| `flow-layout.ts:87-93` (group phase wins) | exact | holds |
| `run.post.ts:62` (`edges.filter(type === "flow")`) | exact | holds |
| `flow-extended-state.ts:48` (same filter, state side) | exact | holds |
| `flow-extended.ts:47` (`data.parameters.flow` as sub-flow child id) | exact | holds |
| `OnboardingWizard.vue:82-99` (freeform textarea binds `placeholder`) | exact | holds |
| `shared/flow-phases.ts` (no line cited) | exact | holds |

**Every underlying fact still holds. Four refs rotted in ~2 weeks.** The failure is bookkeeping,
not coupling — and it is unfalsifiable, since nothing re-checks a comment.

## The rule population

`check.py` is 985 lines with **71 `rep.error` call sites**. The host-derived cluster is not
spread evenly: it concentrates in `_check_presentation` (`:605-668` — icon, `input_style`,
`placeholder`, `research_depth`, `meta`), `_check_nodes` (`:669-777` — `data.phase`, the dead-key
bans, authored geometry), plus the `_concept/` prefix rule (`:379`) and the `shared-contracts`
slug rule. The rest are intrinsic: `name:` == directory, links resolve, `requires:` ↔ node set,
edge targets, reachability from `entry:`, `id` == stem == dir.

## Absence-claims

At least four rules or rationales assert that something is **not** there, and a signature grep
verifies them by inverting:

- `check.py:99` — no `${...}` resolver in either host; the string reaches the prompt verbatim.
- `check.py:17` — `validateFlow` / `FlowManifestSchema` have zero call sites in forge-concept.
- `check.py:351` — forge-concept never reads `name:` for resolution.
- `check.py:660` — the dead globals have no reader in either host.

A host that *gains* one of these silently invalidates a rule, and nothing today would report it.

## Existing machinery

- `.github/workflows/ci.yml` — two steps, `check.py --no-tests` then `pytest scripts/test_check.py`,
  split so a red run names which half failed. Push + PR on `main`. **The hosts are not checked out
  there**, so nothing that needs them can run in CI.
- `scripts/test_check.py` — 751 lines, a failing fixture per rule. Note the fixtures test the
  *rule*, never the host fact: `test_research_depth_outside_the_options` proves `check.py` rejects
  a bad value, not that `profiles.get.ts` still publishes those four.
- All three host repos are present as sibling checkouts on this machine, so a verifier has
  everything it needs locally.
