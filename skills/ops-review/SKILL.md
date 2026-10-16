---
name: ops-review
description: "Use when _concept/ needs a health check, its cross-references have drifted, or you want to know whether every feature is actually built and shipped. Produces the review verdict and a build-coverage matrix read from the trace, each finding naming the skill that fixes it. Triggers on 'audit the concept', 'check for issues', 'fix the links', 'is every feature done', 'what code belongs to no feature'."
version: "0.1.0"
metadata:
  requires:
    - contract:@skaile-ai/shared-contracts
  artifacts:
    requires:
      - { id: brief }
      - { id: features }
      - { id: screens }
      - { id: datamodel }
      - { id: trace }
    produces: []
  prerequisites:
    files:
      - { path: "_concept/brief.md", gate: hard }
      - { path: "_concept/05_features", gate: soft, min_entries: 1 }
      - { path: "_concept/11_build/slices", gate: soft }
      - { path: "_concept/11_build/trace.yaml", gate: soft }
      - { path: "_concept/10_blueprint/datamodel", gate: soft }
---

# ops-review

Inspects `_concept/` and reports what is wrong with it, in two halves. **Review** is the
tree's integrity: structure, frontmatter, cross-references, naming, coverage and decay.
**Coverage** is build coverage: for every feature, the slices that built it, the commits
behind them and the code they touched, read from `11_build/trace.yaml` — which
`build-implement` writes as each slice commits — plus the tracked files that belong to no
feature at all. Both are verdicts recomputed from the tree every run, delivered as the report
and never written to disk; the only writes are the cross-reference repairs the user approved.

The stance, the flag shape and the verdict tiers are `contracts/evaluator.md`'s — read it
first and take its `blocking` / `warning` severities as the vocabulary. Paths are
`contracts/concept_structure.md`'s, frontmatter fields `contracts/artifact_frontmatter.md`'s,
the link protocol `contracts/feedback_loop.md`'s, and the mechanical naming rules
`contracts/golden_principles.md`'s. This file sequences those checks and does not restate them.

## Steps

1. **Run the mechanical check.** `python3 <skill-dir>/scripts/check_concept.py <project>`
   prints one `path: message` line per problem: entries the tree does not own (the retired
   `comparable.md`, `10_blueprint/glossary.md` and `datamodel/feature-map.json` included),
   frontmatter fields and dates, `screens:` and `implements:` links in both directions,
   `data_entities[]` against `model.json`, criterion ids against `stories.yaml`, and the
   ledger rows' format. Take every line as a `blocking` finding, unedited; reading the files
   again to second-guess it spends the run on what the script already settled. A project
   with no `_concept/` is the missing step, not a finding.
2. **Inventory what the script does not read**, once and before scoring anything: every
   featureset, feature and screen, the data model, the `11_build/slices/` dossiers and
   `git ls-files`. Then **check the naming rules** in `golden_principles.md` — entity, field,
   enum and relation naming, and the body a feature spec must have — which a generated or
   reverse-engineered concept fails first, because nothing enforced them while it was written.
3. **Check coverage.** Per feature: a spec, at least one screen that implements it, and an
   entity it reads or writes or an explicit statement that it needs none. Globally:
   `03_brand/tokens.json` and `10_blueprint/techstack.md` exist, since the renderers and the
   planner hard-gate on them. A gap here is work not yet done, reported as the missing step
   rather than as a fault.
4. **Check for decay.** A screen no feature implements and a model no feature's
   `data_entities[]` lists are orphans; a file whose `last_updated` sits far behind its
   siblings is stale beside work that moved on without it. Report both; deleting is the
   user's call, since an orphan is as often planned work as it is a leftover.
5. **Build the coverage matrix, one row per feature**, from the trace and the dossiers,
   never stored. A feature's slices are its `11_build/trace.yaml` entries, cross-checked
   against the `11_build/slices/` dossiers whose `plan.md` frontmatter names the feature — a
   dossier the trace lacks is a slice that committed without recording itself, reported
   against `build-implement`. No trace at all is the finding when any slice dossier exists,
   and the missing step on a project that has built nothing. Per row: whether every slice is
   frozen (its `index.md` exists), the commits and code the trace recorded, the ledger rows
   of the feature's criteria (`contracts/acceptance_criteria.md § Ledger updates`) and their
   status, and whether any doc page cites its source files. **Red** when a slice is
   unfrozen, commits or code are empty, or a ledger row is `FAIL` or untested. **Amber** when
   the hard checks pass but the documentation does not. **Green** otherwise. `overall` is
   green exactly when no row is red; amber is surfaced, not blocking.
6. **Scan the other direction for orphan code.** Every file `git ls-files` reports under the
   source directories, minus the union of every feature's `code` in the trace, minus tests,
   build output, configuration, dotfiles and `_concept/`. What remains is code no feature
   claims — advisory, never deleted: an orphan is a question for the user.
7. **Name the fixing skill on every finding**, the script's included. A missing screen is
   `spec-feature`; a missing shell is `experience-shell`; missing tokens are `design-brand`;
   a missing stack or model is `architecture-techstack` or `architecture-datamodel`; a
   retired path or missing glossary is `concept-brief` or `concept-glossary`; an unplanned
   feature is `build-plan`; an unfrozen slice or missing trace entry is `build-implement` or
   `build-branch`; a feature with no featureset is `spec-featuresets`. A finding without a
   next command leaves the reader to triage it themselves.
8. **Show everything, then offer the repairs.** Present the findings by severity and the
   coverage matrix as a table with its orphan list and `overall`, then offer only the
   mechanical fixes: adding a missing back-link, removing a reference to a file that no
   longer exists. Show the exact diff and get a yes before writing. Everything else — missing
   content, a renamed entity, a naming violation in the model, a missing trace entry — is
   reported and left alone, because repairing it means deciding what it should have said, or
   rebuilding a record only the committing skill can vouch for.

**Done when** every feature has exactly one coverage row, every review finding was reported
with its severity and its fixing skill, and any repair that was applied was shown as a diff
first. A reader who wants yesterday's verdict runs the skill again.
