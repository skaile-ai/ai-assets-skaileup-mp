---
name: quality-review
description: "Use when a feature's slices are frozen and its code needs an adversarial review before it ships — resolves the fixed point from the trace and the spec from the feature file, runs `code-review`, and adds the security, accessibility and acceptance-criteria axes. Triggers on 'review this feature', 'code review the login feature', 'is this ready to ship'."
version: "0.1.0"
metadata:
  requires:
    - contract:@skaile-ai/shared-contracts
  artifacts:
    requires:
      - { id: features }
      - { id: slice-plan }
      - { id: acceptance-criteria }
    produces:
      - { id: review, path: "_concept/11_build/reviews/<feature_slug>.yaml" }
  prerequisites:
    files:
      - { path: "_concept/05_features", gate: hard, min_entries: 1 }
      - { path: "_concept/11_build/slices", gate: hard, min_entries: 1 }
      - { path: "_concept/11_build/trace.yaml", gate: hard }
      - { path: "_concept/11_build/acceptance-criteria", gate: soft }
---

# quality-review

Reviews **one feature's shipped code**. How to read a diff is the global `code-review`
skill's job and this file does not restate it; what this skill owns is the two inputs
`code-review` otherwise asks a human for — the fixed point, from the feature's row in
`11_build/trace.yaml`, and the spec, the feature file — plus the axes a two-axis diff review
does not carry. It is the one place in the collection that judges the built feature against
its spec; `build-implement`, `ops-review` and `quality-release` do not repeat that verdict.

Stance is `contracts/evaluator.md` § Stance. The verdict file and the ledger rows this skill
re-checks in step 5 are the only things it writes: a finding fixed during the review is a
finding that never reached the ledger.

## Steps

1. **Resolve the feature and its trace row.** Glob `05_features/*/<feature_slug>.md`; zero
   matches or two is a question for the user, not a guess. Read the feature's entry in
   `11_build/trace.yaml` — its slices' `commits` and `code`. **A missing entry or empty
   commits stops the run** — name `build-implement`, which writes the entry when a slice
   commits. Without it there is no fixed point, and a review with no fixed point quietly
   widens to the whole repository.
2. **Build and test before reading a line.** Run the project's own build and test commands.
   A red build makes every finding provisional, so stop there,
   call the Skill tool with "diagnosing-bugs" and come back once it is green; without it,
   hand the failure to the user with the failing command and stop.
3. **Call the Skill tool with "code-review" from a context that did not write the code.**
   If `code-review` is not installed, the review stops and names it rather than improvising
   one. The fixed point is the parent of the earliest sha in the trace row's `commits`; the
   spec is the feature file. Dispatch it as a
   subagent: the session that implemented the slice reads its own diff as correct, which is
   the whole reason an evaluator is independent. Hand it `02_grounding/standards/` alongside
   whatever the repo documents, where that exists — a convention this project was measured to
   follow outranks the generic smell baseline. Keep its two axes apart in your own report
   too — merging Standards and Spec into one ranked list is the masking the split prevents.
4. **Add the two axes `code-review` has no eye for**, per `references/checklists.md`:
   security and data integrity across every route the diff touches, and accessibility across
   every screen it renders. Each hit becomes a finding with a file and a line.
5. **Re-check the ledger.** Read
   `11_build/acceptance-criteria/<featureset>/<feature_slug>.ac.md`. For every row marked
   `PASS`, exercise the criterion against the running app rather than reading the code that
   claims it — a criterion is met when it is observed, and static inspection is exactly how a
   `PASS` row survives with nothing behind it. Overwrite each row you re-checked with your
   result and your own evidence, per `contracts/acceptance_criteria.md § Ledger updates`
   (`FAIL` beats an earlier `PASS` at the same commit). A row that fails is a `high` finding
   carrying its criterion id (`§ Criterion ids`); rows you did not exercise stay as they were.
6. **Read the accepted debt before writing findings.** `11_build/slices/<slice_id>/index.md`
   records what the simplification pass deliberately left in place. Debt recorded there is
   context, not a finding; re-flagging it spends the reader's attention on a decision that
   was already made and taught them to skim the rest.
7. **Write the verdict** to `11_build/reviews/<feature_slug>.yaml`. Severities and the
   blocking rule are `contracts/evaluator.md` § Flag shape — `approved` means zero blocking
   findings, which is zero `critical` and zero `high`.

   ```yaml
   feature: <feature_slug>          # the id the host joins trace, ledger and review on
   verdict: approved | changes-requested
   commits: [<sha>, ...]
   files_reviewed: [<path>, ...]
   findings:
     - id: F-1
       severity: high               # critical | high | medium | low
       category: security           # standards | spec | security | accessibility | criteria
       file: <path>
       line: <n>
       criterion: ""                # AC-<story-id>-<nn> when the finding is a ledger row that does not hold
       note: <what the code does, against what the spec or criterion says>
       resolution: <the specific change that clears it>
   last_updated: YYYY-MM-DD
   ```

   `feature`, `verdict` and `findings[].severity` are the three names forge-concept's review
   page reads; spelled any other way the feature renders with no verdict at all.
8. **Report by axis** — Standards, Spec, Security, Accessibility, Criteria — each with its
   findings ordered by severity inside that axis and never across them. On
   `changes-requested`, call the Skill tool with "diagnosing-bugs" against the findings and
   name this file as the one to re-run against; without it, the findings go to the user as
   they stand.

**Done when** `11_build/reviews/<feature_slug>.yaml` is on disk, every finding in it carries
a file, a line and a resolution, and the verdict is `approved` only where no finding is
`critical` or `high`.
