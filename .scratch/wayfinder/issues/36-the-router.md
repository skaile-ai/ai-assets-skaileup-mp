# 36: The router — the last absorbed skill with no body

**Type:** grilling
**Blocked by:** None — graduated from the map's fog 2026-09-06
**Status:** resolved

## Question

Graduated from the **five absorbed skills' bodies** fog patch, which is down to one. Ticket 08
placed three (`research` and `to-questionnaire` became steps inside `concept-research` and
`concept-onboard`; `to-spec` became `spec-feature`), and **ticket 26 closed `grilling`** — it
turned out to be a global mp install, not a `-mp` asset. What is left is the **router**, named
`skaileup` by ticket 04 and never written.

Measured: `-mp` ships **29 skills and no router**. `concept-scope` — the closest candidate,
and the entry point of every flow — contains **no routing, triage or intake language at all**.

Two things want it, and they do not want the same thing:

- **Ticket 13's intake rule.** 13 refused a triage *skill* but kept the rule, and it has to
  live somewhere: for work the collection did not create, call the global `/triage`, then
  enter at `spec-feature` (a new or changed feature) or `build-plan` (a defect against built
  code). `CONTEXT.md` is glossary-only, so it cannot be there. It is currently written down
  **only in this map**.
- **An `ask-matt`-style front door** (premise 6) — "I have a thing to do, which skill?" for
  someone driving the collection outside a host.

And one thing makes it arguably redundant: **in forge-concept the flow choice is the host's,
not a skill's.** The user picks a profile in `OnboardingWizard.vue`, and the profile key *is*
the flow id (`profiles.get.ts`); `-mp` ships six `profiles/*.yaml`. A router that picks a flow
would be re-deciding what the host already asked. That leaves the router's real territory as
the **non-host** case and the **mid-project** case — someone already inside `_concept/` who
does not know which skill comes next.

So: **does `-mp` ship a `skaileup` router skill, and what is its job?**

1. **Yes, as an intake router** — carries ticket 13's rule and the entry points, for work
   arriving from outside a flow. Redundant inside forge-concept, load-bearing outside it.
2. **Yes, as a "what next" skill** — reads `_concept/01_meta/scope.yaml` and the tree, says
   which skill is next. Overlaps the flow graph, which already encodes exactly that.
3. **No skill; the rule lands in prose** — `README.md` or `contracts/`, and the collection
   keeps 29 skills.

Whichever wins, ticket 13's sentence stops living only in a wayfinder map.

## Answer

**Option 1, widened by one job: `-mp` ships `skaileup`, and no flow contains it.**

Two of the question's premises were wrong, and correcting them is most of the answer.

- **"`concept-scope` contains no routing, triage or intake language at all"** — false.
  `skills/concept-scope/SKILL.md:44-56` step 4 reads *"Where nothing has chosen, put the four
  to the user with your recommendation from the signals"* and carries the four-row flow table.
  **The non-host flow choice already shipped.** So the router's territory is not "which flow";
  that question has two answers already (the host's profile picker, and this step).
- **"the profile key *is* the flow id ...; `-mp` ships six `profiles/*.yaml`"** — conflates two
  words. `profiles.get.ts:29` derives the host's onboarding profiles **from flows** (4 of them);
  `-mp`'s `profiles/` is project-type data read by `concept-scope` step 3 (6 files), and ADR
  0002 already pinned **profile = project type** inside the collection. The collision is with
  the host's vocabulary, not the collection's, so nothing was renamed — `CONTEXT.md`'s
  **Profile** entry grew the host's sense as an `_Avoid_`.

**Option 2 survived, one case wide.** `contracts/agent_patterns.md` already ships
`§ Standalone Mode` (`:73-82`) and `§ Next-Step Suggestion` (`:86-95`): every skill already
suggests its successors **on completion**. The uncovered slice is the **cold open** — a
`_concept/` tree entered with nothing running and no skill just finished. So the router reads
`01_meta/scope.yaml`, opens the flow it names, and walks the edges; it **reads** the graph and
never restates it, which keeps the flow the single source of order.

**Option 3 lost on the evidence that the hole is already load-bearing.** Three references
pointed at a router-shaped absence, each resolving to nothing — the same defect class ticket 34
swept out of the contracts:

- `docs/skill-template.md:77` sent cross-cutting prose to *"`CONTEXT.md` or the router"*.
- `contracts/agent_patterns.md:81,90` cited a `next_flows` field **defined nowhere** — zero
  flows carry it, grepped repo-wide.
- Ticket 13's intake rule existed **only in the wayfinder map**: `grep -ri 'triage|intake|router'`
  over the repo returned no hit for it.

### What landed

| File | Change |
|---|---|
| `skills/skaileup/SKILL.md` | new — 70 lines. Intake (global `/triage`, then `spec-feature` for a changed capability or `build-plan` for a defect) + cold start. Names one skill and stops. |
| `contracts/agent_patterns.md:81,90` | `next_flows` deleted; successors are the edges leaving the node. A parallel hint field would be the second source of order the router itself refuses to be. |
| `docs/skill-template.md:77` | "`CONTEXT.md` or the router" → `contracts/agent_patterns.md`, which already carries both patterns. The router does **not** claim them. |
| `CONTEXT.md` | **Router** added; **Profile** widened with the host's sense. |
| `README.md` | the one non-domain name explained; stale `build-slice-implement` example corrected to `build-implement`. |

**Name kept as ticket 04 set it**, and verified harmless: `phaseForSkill`
(`shared/flow-phases.ts:20-28`) falls through to `conceptualization` for an unprefixed name, and
`check.py` enforces no domain prefix. `skaileup` is what someone types cold.

**No flow contains it.** A flow whose first node asks which flow you are in is circular. It
installs as an ordinary skill asset, which means every workspace listing skills by hand
(ticket 29) lists it too.

Measured at landing: **30 skills · 4 flows · 0 errors**, `pytest scripts/test_check.py` **69
passed**.
