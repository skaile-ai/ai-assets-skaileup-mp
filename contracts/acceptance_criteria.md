# Acceptance criteria — the EARS grammar and the status ledger

Two things live here: how a testable acceptance criterion is written, and the **ledger** that
tracks whether each one has been proved.

The ledger is a **join, not a copy**. A criterion is written once, in its feature spec, and
the ledger holds one row per criterion carrying its id, its status and what proved it. The
row never restates the criterion's text: two copies of a requirement drift, and the copy in
the build half is the one that quietly becomes what the code is checked against.

## Where the ledger lives

```
_concept/11_build/acceptance-criteria/<featureset>/<feature_slug>.ac.md
```

One file per feature, mirroring its place under `05_features/`.

## Ledger format

```markdown
---
feature: <feature_slug>
feature_ref: _concept/05_features/<featureset>/<feature_slug>.md
last_updated: YYYY-MM-DD
---

# Criteria — <Feature Name>

- [ ] AC-checkout_flow-01
- [PASS] AC-checkout_flow-02 — tests/checkout/total.test.ts · build-implement · 4f2a9c1 · 2026-09-05
- [FAIL] AC-checkout_flow-03 — journey "checkout" step 4: total unchanged · quality-e2e · 4f2a9c1 · 2026-09-05
- [ ] AC-cart-01
```

**Rows are checkbox lines, not a table.** The only machine that reads this file matches
`- [PASS|FAIL|x|X| ] <text>` line by line (forge-concept's `review-coverage.ts`); a table
parses as zero criteria and the coverage page reports the feature as untested. `feature:` in
frontmatter is what every other build artifact is joined on — without it the id falls back to
the directory name, which is the featureset.

- The marker is the status: empty is untested, `PASS` and `FAIL` are what they say.
- The text after the id is the **evidence**, `<pointer> · <evaluator> · <commit> · <date>`:
  the check that set the row (a test path, or a journey and step), the skill that set it, the
  short commit the evaluated tree was at, and the date. An untested row carries the id alone.
- The id is a criterion id per `## Criterion ids`; the row never carries the criterion's text.

## Ownership

| Skill | What it does to the ledger |
|---|---|
| `build-plan` | creates the file when it cuts the feature into slices — one row per criterion id in the spec, every one untested |
| `build-implement` | evaluates the rows its slice gate exercised, each with the check behind it |
| `quality-e2e` | evaluates the rows a journey covered, end to end in the browser |
| `quality-review` | evaluates the rows it re-checks against the running app |
| `quality-release` | reads the rows — it does not re-walk journeys |
| `ops-review` | reads the rows — any `FAIL` or untested row makes the feature's coverage row red |

## Ledger updates

Every skill that writes a row follows the same rule, so two evaluations of one criterion
cannot leave the ledger telling two stories.

1. **One row per criterion id, created once.** `build-plan` creates the rows; no other skill
   adds, removes or renumbers one. An evaluator that finds no ledger for a feature stops and
   names `build-plan` as the missing step — a ledger built afterwards holds whatever happened
   to get tested.
2. **An evaluation overwrites.** The evaluator replaces the row's marker with `PASS` or
   `FAIL` and replaces its evidence with its own — pointer, evaluator, commit, date. The
   earlier verdict is not kept in the row; git history holds it.
3. **Only evaluated rows change.** A row the run did not exercise stays exactly as it was. A
   row set on inference costs the ledger its value: every reader downstream trusts it instead
   of re-reading the code.
4. **`FAIL` beats `PASS` at the same commit.** When two evaluations of one commit disagree,
   the row ends `FAIL`, carrying the failing evaluation's evidence; a later `PASS` at the
   same commit does not overwrite it. At a newer commit, rule 2 applies and the newer
   evaluation wins either way.
5. **`quality-e2e` writes its journey verdict into the rows.** The verdict on each criterion
   id a journey evaluated goes into that id's row, with the journey and step as the pointer;
   an id the journey never reached stays as it was. The rows are the record: a report cites
   them and keeps no second verdict.
6. **`quality-release` reads the rows.** It takes each feature's status from its ledger and
   does not walk the journeys again; an untested or `FAIL` row is what blocks the release.

## EARS template

Canonical acceptance-criterion form — cite this section instead of restating it:

    WHEN <trigger>, THE SYSTEM SHALL <response>

Variants: `WHILE <state>, THE SYSTEM SHALL <response>` (state-driven);
`IF <unwanted condition>, THEN THE SYSTEM SHALL <response>` (unwanted behaviour). One
observable response per line; every criterion independently verifiable.

## Criterion ids

Every criterion has one id for its whole life, and every artifact that refers to a criterion
refers to it by that id.

    AC-<story-id>-<nn>

- `<story-id>` is the `id` of the story in `04_journeys/stories.yaml` the criterion belongs
  to — a story is one entry under `journeys:`, so it is that journey's `id` — a snake_case
  slug (lowercase letters, digits, `_`), unique across the file. Because it never contains
  `-`, the trailing `-<nn>` is unambiguous.
- `<nn>` is two digits, numbered per story in the order the criteria are written: `01`,
  `02`, …
- A criterion `spec-feature` adds that no story holds (grill-derived, or observable only
  through the service layer) takes the same shape with the feature slug as scope,
  `AC-<feature_slug>-<nn>`, using a slug that is not a story id.
- `experience-journeys` (step 5) assigns the ids at write time, as an `id:` on each EARS
  criterion in `stories.yaml`; `spec-feature` assigns them for the criteria it adds. No other
  skill coins an id.
- **Stability.** An id never changes and is never reused once written. A criterion that is
  dropped has its id retired — the number stays unused, and a replacement takes the next one.
  A criterion whose wording is edited keeps its id; one whose meaning changes is a new
  criterion with a new id.
- **Cite, never retype.** The feature spec, slice plans, ledger rows, e2e verdicts and
  behavior tables carry the id (plus a place or evidence where they need one) and not the
  criterion's text: the text lives in `stories.yaml` or the feature spec that wrote it, and a
  second copy is the one that drifts.

## Deriving the criteria

Criteria are written into the feature spec by `spec-feature`, each cited by its id from
`## Criterion ids`. Where to look:

| Source | What it yields |
|---|---|
| the grill and the scope line | every item ruled IN becomes a criterion; nothing else does |
| `_concept/04_journeys/stories.yaml` | story-level criteria, state transitions, guard conditions |
| `_concept/07_screens/<feature_slug>/<screen>.md` | one criterion per state — default, loading, error, empty, success — and per user action |
| `_concept/06_behaviors/<featureset>.md` | `requires` guards become the WHEN clause, postconditions the SHALL |
| `_concept/10_blueprint/datamodel/seed.json` | the concrete data a criterion is stated against |

Rules:

1. **One criterion per observable behaviour.** Two behaviours in one line cannot be flipped
   independently, and the ledger row becomes half true.
2. **Specific over vague.** "the user sees 'Invalid email or password'", not "an error".
3. **Concrete values** — seed data names, exact routes, exact status codes.
4. **Independently verifiable.** No criterion depends on another one's side effects.
5. **Error states are criteria.** Every error state the screen spec lists is one.
