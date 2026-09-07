# 37: What carries over from the old repo besides skills

**Type:** grilling
**Blocked by:** None — 35 resolved 2026-09-06: no docs site, so `improvements.mdx` goes with it
**Status:** resolved

## Question

Graduated from the last fog patch. The port moved skills, flows, contracts and templates.
Three things in the old repo moved nothing, and each is a different question:

- **`docs/devlog/` — 31 files.** A running record of how the old collection was built, dated
  and named per work item (`2A-scope-project.md`, `2026-05-07-skill-graph-migration.md`,
  `forge-concept-walkthrough.md`). `-mp` records decisions in **11 ADRs** instead, a different
  form with a different bar. Does the devlog carry, get mined for ADRs it should have
  produced, or stay in the old repo as its history?
- **The improvement backlog** — `docs/src/content/docs/improvements.mdx`, a page inside the
  Starlight site. Whether it survives at all is downstream of **ticket 35**; whether its
  *content* still applies to a collection one third the size is this ticket's.
- **Git history.** `-mp` was created fresh by ticket 11, so it has none of the old repo's.
  The old repo is not archived (ruled out of scope at charting), so the history stays
  reachable — the question is whether anything needs to be *in* `-mp`.

The map's standing bar applies to all three: this collection has deleted an artifact no one
reads **four times** (`artifacts.yaml`, `data.writes`, `review.yaml`, and the per-file
contract refs). A devlog nobody opens is the same shape of thing — but it is also the only
record of *why* the old collection is what it is, which is exactly what a migration destroys
and cannot re-derive.

Blocked by ticket 35 because two of the three physically live under `docs/`: if the site is
dropped, "carry the devlog" means something different than if it is ported.

## Resolution (2026-09-07)

**Nothing carries. All three, and the two mitigations that were offered with them.**

**`docs/devlog/` stays in the old repo.** The ticket's case for carrying it was that it is the
only record of *why* the old collection is what it is — "exactly what a migration destroys and
cannot re-derive". The measurement refutes the premise: **the devlog sat available for this
entire migration and was read zero times.** Across 39 tickets, 10 briefs and 3 research files,
every `devlog` hit in `.scratch/wayfinder/` is either this ticket, ticket 35 pointing at this
ticket, brief 13 counting the files, or a *different devlog* (below). 31 files, **32,293 lines**,
never opened.

It was not needed because this migration re-derived the why by **measuring the artifact** rather
than reading the record — 44% mechanical duplication (ticket 03), `artifacts.yaml` unreachable as
deployed (01), `EMIT` read by no code at all (03), `flows.md` with zero readers (09). None of
those facts were in the devlog, and a plan file would have asserted the opposite of several. So
mining it for ADRs was refused on a second ground beyond cost: it would author decision records
for decisions **`-mp` did not make**, about a tree that no longer exists.

**The improvement backlog was never a backlog.** `improvements.mdx` is a completed-phases history
— Phases 0–3, "All are complete", every item ✅ (ticket 35 had already called it "reorg, not a
live backlog"). Exactly one entry is not closed: *"Validator coverage — roughly half the skills
ship a `validator.py`; no rule yet requires one."* It does not transfer, because in `-mp` it is
not a gap but a decision: the old repo ships **38** validators, `-mp` ships **3**, after ticket 03
found `CHECKLIST` restated `validator.py` and `check.py` became the gate. Answered by design, not
deferred.

**Git history: nothing needs to be in `-mp`.** Old repo 330 commits (2026-04-27 → 2026-09-06),
`-mp` 34 (from 2026-09-03). Grafting the former would make `git log` lie about every `-mp` file,
and archiving the old repo was ruled out of scope at charting, so it stays reachable.

**Both mitigations were offered and both refused**, which is what makes this a clean cut rather
than a hedged one:

- **No `CONTEXT.md` entry for `devlog`**, despite the collision found below. The glossary carries
  the words skills use with each other; a word `-mp` inherits only through one artifact filename
  does not earn a definition.
- **No pointer line in `README.md`.** The old repo is already linked there twice; a sentence
  explaining that its history exists is the kind of note that is written once and read never —
  the same shape as the thing this ticket declined to carry.

**Recorded but not acted on: `devlog` names three different things** across the repos this
collection touches, and nothing distinguishes them. `docs/devlog/` is the old collection's build
record; `_feedback/devlog.md` is a **project artifact** the `mockup-feedback` apply step appends
to, and `-mp` ships it; `PF/_devlog/entries/` is **platform's**, which ticket 15's research mined
as a primary source. So "a devlog nobody opens" is false for platform's and true only for
skaileup's own — the form works, this instance was unused. Left as a finding because the map's
standing bar cuts here too: the collection has now deleted an artifact no one reads five times.

**The map stays in `.scratch/wayfinder/`.** It is tracked (55 files), so it is already durable,
and it — with the 11 ADRs — is the record the devlog would have been. Its `.scratch/` location was
raised and deliberately left alone; no ticket opened.
