---
name: ops-review
description: "Use when _concept/ needs a health check, its cross-references have drifted, or you want to know whether every feature is actually built and shipped. Produces the review verdict and the feature-to-code trace matrix, each finding naming the skill that fixes it. Triggers on 'audit the concept', 'check for issues', 'fix the links', 'is every feature done', 'what code belongs to no feature'."
version: "0.1.0"
metadata:
  artifacts:
    requires:
      - { id: brief }
      - { id: features }
      - { id: screens }
      - { id: datamodel }
  prerequisites:
    files:
      - { path: "_concept/brief.md", gate: hard }
      - { path: "_concept/05_features", gate: soft, min_entries: 1 }
      - { path: "_concept/11_build/slices", gate: soft }
      - { path: "_concept/10_blueprint/datamodel", gate: soft }
---

# ops-review

Inspects `_concept/` and reports what is wrong with it, in two halves. **Review** —
`11_build/review.yaml` — is the tree's integrity: structure, frontmatter, cross-references,
naming, coverage and decay. **Trace** — `11_build/trace.yaml` — is build coverage: for every
feature, the slices that built it, the commits behind them and the code they touched, plus
the tracked files that belong to no feature at all. It writes those two files and cross-
reference repairs the user approved; every other artifact belongs to the skill that owns it.

The stance, the flag shape and the verdict tiers are `contracts/evaluator.md`'s — read it
first and take its `blocking` / `warning` severities as the vocabulary. Paths are
`contracts/concept_structure.md`'s, frontmatter fields are
`contracts/artifact_frontmatter.md`'s, the link protocol is `contracts/feedback_loop.md`'s,
and the mechanical naming rules are `contracts/golden_principles.md`'s. This file sequences
those checks and does not restate them.

## Steps

1. **Inventory first, judge second.** Walk `_concept/` once and build the registry every
   check below reads: every markdown file with its frontmatter, every featureset and feature,
   every screen, the data model and its feature map, every slice dossier under
   `11_build/slices/`, and `git ls-files`. Gather it all before scoring anything — a check
   that reads files as it goes reports findings in the order it happened to walk the tree
   rather than in the order they matter.
2. **Check the structure.** Every path in the tree resolves to one of the eleven numbered
   top-level entries or the three root files; anything else is a file some skill invented a
   home for, and no reader will find it. A featureset directory under `05_features/` has a
   matching one under `07_screens/` only if a feature in it needed screens — the two trees
   are not required to mirror, because one writer owns both and screens follow features
   rather than featuresets.
3. **Check the frontmatter** of every markdown file against the contract for its artifact
   type: the fields that type requires, `last_updated` present and a real ISO date, and no
   `status:` field, which no artifact carries and which means somebody's template is stale.
4. **Check the cross-references, both directions.** A feature's `screens:` names files that
   exist, and each of those screens' `implements:` names it back. A screen's `implements:`
   names features that exist. Every name in a `data_entities:` array resolves to a model in
   the data model, and every model has a `feature-map.json` entry naming feature files that
   exist. A one-directional link is a screen the feature it belongs to cannot find, which is
   invisible until a renderer or a plan silently omits it.
5. **Check the mechanical rules** in `golden_principles.md` — entity, field, enum and relation
   naming, and the body structure a feature spec is required to have. These are the rules a
   generated or reverse-engineered concept fails first, because nothing enforced them while
   it was written.
6. **Check coverage.** Per feature: a spec, at least one screen that implements it, and an
   entity it reads or writes or an explicit statement that it needs none. Globally:
   `03_brand/tokens.json` and `10_blueprint/techstack.md` exist, since the renderers and the
   planner hard-gate on them. A gap here is not a defect in what was written — it is work
   that has not been done, and it is reported as the missing step rather than as a fault.
7. **Check for decay.** A screen no feature implements and a model no feature references are
   orphans; a file whose `last_updated` sits far behind its siblings is stale beside work that
   moved on without it. Report both; deleting is the user's call, since an orphan is as often
   planned work as it is a leftover.
8. **Build the trace matrix, one row per feature and N slices per row.** A feature's slices
   are the dossiers under `11_build/slices/` whose `plan.md` frontmatter names that feature —
   a feature has as many as it was cut into, and looking one up by a single reference finds
   the first and misses the rest. Per row: whether every slice is frozen (its `index.md`
   exists), the union of the commits and source files those slices recorded, the acceptance
   criteria and their status, and whether any doc page cites its source files. **Red** when a
   slice is unfrozen, or commits or source files are empty, or an acceptance criterion is
   failing or untested. **Amber** when the hard checks pass but the documentation does not.
   **Green** otherwise. `overall` is green exactly when no row is red; amber is surfaced, not
   blocking.
9. **Scan the other direction for orphan code.** Every file `git ls-files` reports under the
   source directories, minus the union of all features' source files, minus tests, build
   output, configuration, dotfiles and `_concept/` itself. What remains is code no feature
   claims. This half is advisory and never deletes anything: an orphan is a question for the
   user, and a skill that answers it by removing files is a skill nobody runs twice.
10. **Name the fixing skill on every finding.** A missing screen is `spec-feature`; a missing
    shell is `experience-shell`; missing tokens are `design-brand`; a missing stack or model is
    `architecture-techstack` or `architecture-datamodel`; an unplanned feature is `build-plan`;
    an unfrozen slice or empty back-links are `build-implement` and `build-branch`; a feature
    with no featureset is `spec-featuresets`. A finding without a next command is a finding
    the reader has to triage themselves, which is the work this skill was supposed to do.
11. **Show everything, then offer the repairs.** Present the review findings by severity and
    the trace matrix as a table with its orphan list, then offer only the fixes that are
    mechanical: adding a missing back-link, removing a reference to a file that no longer
    exists. Show the exact diff and get a yes before writing. Everything else — missing
    content, a renamed entity, a naming violation inside the model — is reported and left
    alone, because repairing it means deciding what it should have said.
12. **Write the two files.** `11_build/review.yaml`: the verdict, the per-category scores, and
    the findings in `evaluator.md`'s flag shape, each with its location, the quoted text and
    its fixing skill. `11_build/trace.yaml`: the matrix rows, the orphan list, the summary
    counts and `overall`. Both are written after the report, not before it — the report is what
    the user acts on, and a file written first is a verdict issued before it was shown.

**Done when** `review.yaml` and `trace.yaml` are on disk, every feature has exactly one trace
row, every finding names a fixing skill, and any repair that was applied was shown as a diff
first.
