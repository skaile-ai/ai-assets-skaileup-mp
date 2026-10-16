---
name: quality-release
description: "Use as the last gate before a release — walks the whole running application against the brief and goals it started from and grades it on seven axes, then writes the release verdict. Triggers on 'is this ready to release', 'grade the app', 'final gate', 'release review'."
version: "0.1.0"
metadata:
  requires:
    - contract:@skaile-ai/shared-contracts
  artifacts:
    requires:
      - { id: brief }
      - { id: goals }
      - { id: journeys }
      - { id: brand-tokens }
      - { id: acceptance-criteria }
      - { id: trace }
    produces:
      - { id: release-verdict, path: "_concept/11_build/release.yaml" }
  prerequisites:
    files:
      - { path: "_concept/brief.md", gate: hard }
      - { path: "_concept/11_build/trace.yaml", gate: hard }
      - { path: "_concept/goals.md", gate: soft }
      - { path: "_concept/03_brand/tokens.json", gate: soft }
---

# quality-release

The last gate. Every feature has been built, reviewed and traced; what nothing before this
has asked is whether the thing that exists is the thing the project set out to build. This
skill is **the only one in the collection that reads `brief.md` and `goals.md` against the
running application** — everything upstream checks a part against its own spec, which is how
a product ships with every criterion green and none of its goals met.

It grades and refuses; it never edits code. Stance is `contracts/evaluator.md` § Stance,
which here means walking the app as a user rather than reading what it was supposed to do.

## Steps

1. **Refuse on an incomplete trace or ledger.** Read `11_build/trace.yaml`. A missing file
   means `build-implement` has recorded no slice — say so and stop. Every feature under
   `05_features/` needs an entry with commits, and every slice in it a frozen dossier (its
   `index.md` exists); list each feature that falls short and stop. Then read each feature's
   ledger under `11_build/acceptance-criteria/` (`contracts/acceptance_criteria.md § Ledger
   updates`, which `quality-e2e` and `quality-review` have already written their verdicts
   into): a `FAIL` or untested row is the same refusal, listed by criterion id with its
   evidence. Then read `11_build/reviews/*.yaml`; a feature still at `changes-requested` is
   the same refusal.
2. **Extract the intent.** From `brief.md` and `goals.md`, list every goal, success metric,
   constraint and stated non-goal, one line each. Where there is no `goals.md`, the brief's
   problem statement and hero flow are the goal set. This list is the grading sheet, and it
   is written down before the app is opened so the app cannot supply it.
3. **Walk the whole product, not the features.** Enter where a new user enters and pursue
   each goal from step 2 through the app in the order a person would, without jumping
   straight to a route; `04_journeys/stories.yaml` says where people start. Each journey's
   own verdict is already in the ledger rows, so this walk does not re-run its steps — what
   it catches is only visible from the seams: a journey that works but leaves the user with
   no idea what to do next, two features that each pass and contradict each other, a dead end
   between them.
4. **Score goal achievement** — for each goal from step 2, `achieved`, `partial` or
   `not_achieved`, with what you did in the app as the evidence. Criteria status comes from
   the ledger rows read in step 1; re-testing them here is duplicated work.
5. **Score the four design axes** — quality, originality, craft, functionality — 0-10 each,
   strictly, per `references/rubrics.md`. Read the rubric before scoring rather than
   afterwards, cite the exact screens and elements behind every number, and check the surface
   against `03_brand/tokens.json` where it exists. "Looks clean" is the absence of a score,
   and originality above 7 needs named distinctive choices or it is a generic app being
   graded politely.
6. **Score the three technical axes.**
   - **Performance**, from the browser's own tooling: LCP under 2.5s good, 2.5-4s warn, over
     4s poor; CLS under 0.1 / 0.1-0.25 / over 0.25; first interaction under 100ms / 100-300ms
     / over 300ms.
   - **Accessibility**, 0-100: every journey completable without a mouse, interactive
     elements labelled, text and controls meeting contrast against their real background.
   - **Mobile**, 0-100, at 375px: all content reachable, no horizontal scroll, touch targets
     at least 44px.
7. **Write the verdict** to `11_build/release.yaml` — goals with their evidence, the seven
   scores, the blocking findings, and `improvement_priorities` ranked by impact on the goals
   rather than by how easy each is to fix. Severities are `contracts/evaluator.md` § Flag
   shape; the verdict names here are `pass`, `needs_iteration` and `fail`:
   - **pass** — at least two thirds of goals `achieved` or `partial`, design average ≥ 7,
     accessibility ≥ 70, LCP under 4s, and no blocking finding.
   - **needs_iteration** — any goal `not_achieved`, or design average under 7, or
     accessibility under 70.
   - **fail** — most goals `not_achieved`, or LCP over 4s together with CLS over 0.25.
8. **Report** the verdict, the goal tally, the seven scores on one line and the ranked
   improvements — each naming the skill that owns the fix, so the verdict routes somewhere
   instead of ending the run.

**Done when** `11_build/release.yaml` is on disk, every goal in it carries evidence from the
running app, every design score cites the elements behind it, and the verdict follows the
thresholds above rather than an impression of the app.
