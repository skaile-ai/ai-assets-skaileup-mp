---
name: quality-release
description: "Use as the last gate before a release — walks the whole running application against the brief and goals it started from and grades it on seven axes, then writes the release verdict. Triggers on 'is this ready to release', 'grade the app', 'final gate', 'release review'."
version: "0.1.0"
metadata:
  artifacts:
    requires:
      - { id: brief }
      - { id: goals }
      - { id: journeys }
      - { id: brand-tokens }
      - { id: acceptance-criteria }
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

1. **Refuse on an incomplete trace.** Read `11_build/trace.yaml`. A missing matrix means
   `ops-review` has not run — say so and stop. Any red feature row means something claimed
   done is not: list each row with the check that failed and stop. Carry the amber rows
   forward: they are not blocking, and a report that hides them grades an app whose gaps
   nobody restated. Then read `11_build/reviews/*.yaml`; a feature still at
   `changes-requested` is the same refusal.
2. **Extract the intent.** From `brief.md` and `goals.md`, list every goal, success metric,
   constraint and stated non-goal, one line each. Where there is no `goals.md`, the brief's
   problem statement and hero flow are the goal set. This list is the grading sheet, and it
   is written down before the app is opened so the app cannot supply it.
3. **Walk the whole product, not the features.** Enter where a new user enters and follow
   the journeys in `04_journeys/stories.yaml` in the order a person would, without jumping
   straight to a route. What this catches is only visible from the seams: a journey that
   works but leaves the user with no idea what to do next, two features that each pass and
   contradict each other, a dead end between them.
4. **Score goal achievement** — for each goal from step 2, `achieved`, `partial` or
   `not_achieved`, with what you did in the app as the evidence. Re-testing acceptance
   criteria here is duplicated work: `quality-review` and `quality-e2e` already own them.
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
8. **Report** the verdict, the goal tally, the seven scores on one line, the amber trace rows
   carried from step 1, and the ranked improvements — each naming the skill that owns the
   fix, so the verdict routes somewhere instead of ending the run.

**Done when** `11_build/release.yaml` is on disk, every goal in it carries evidence from the
running app, every design score cites the elements behind it, and the verdict follows the
thresholds above rather than an impression of the app.
