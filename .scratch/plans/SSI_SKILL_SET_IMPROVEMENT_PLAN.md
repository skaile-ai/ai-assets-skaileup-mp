# SSI — Skill-set improvement - plan

Source: the critique report `.scratch/reports/skill-set-critique-2026-10-15.html` (44 findings,
data in `.scratch/reports/skill-set-critique-2026-10-15.data/findings.json`). Every finding id
below (`F01`..`F44`) is that report's. Facts about the repo were re-read on 2026-10-16; line
numbers are from that read.

## Context

The report's verdict: the collection has the right skills in the wrong order. The glossary is
pinned last and by three skills (F08, F30), the data model comes after every feature and screen
and gate-cycles with them (F17, F18), three of four flows contain a hard gate nothing upstream
writes (F01-F03) and `scripts/check.py` cannot see that (F04) because no skill declares what it
produces (F05). Approvals, answers and reasons stay in chat (F06, F13, F23, F39). The rest is
duplicated ownership (F09-F11, F16, F19-F22, F26-F28, F32, F33, F36, F37) and wayfinding cost
(F07, F14, F15, F29, F34, F41, F44).

Scope approved by the user: **all 44 findings, in four ordered phases**; each phase lands with
`python scripts/check.py` green on its own.

### Constraints the plan works inside

- `CLAUDE.md` invariants: flat `skills/<name>/SKILL.md`, name = dir, nine domains, 140-line
  ceiling, machine layer under `metadata:`, paths start with `_concept/`, flow nodes carry
  `data.phase`.
- ADR 0007: one root `_concept/`, first level fixed (`brief.md`, `goals.md`, `comparable.md`,
  `01_meta`..`11_build`). ADR 0010: no twelfth entry, no plan/status file. ADR 0004/0001: no
  artifacts registry; machine data lives in frontmatter. ADR 0011: `artifacts.requires[]` is
  `{id}` only. ADR 0012: five foreign skills, one call phrasing (`_check_skill_calls`).
- `check.py` (`scripts/check.py`, 1352 lines) has **no allowlist of `metadata` keys**: a new
  `metadata.artifacts.produces` passes silently today, so every new key needs its own rule plus
  a fixture in `scripts/test_check.py` (`write_repo` 74, `good_flow` 96, `only` 158, `body` 302).
  Host-derived rules need a `host_facts.py` row that lists the rule id.
- Host (`forge/skaile-forge`): node done-state comes from `artifact-contract.ts:150-152`, which
  reads `contracts/artifacts.yaml` (`path`, `produced_by[0]`), a file ADR 0004 dropped - so the
  editor cannot derive done state today (F05). `data.phase` is read inside the SDK; `requires`
  is read by nobody on the host. Brand/mockup folder fallbacks hardcode `04_brand`/`05_mockups`
  (`grounding.ts:39-40`), already out of step with the tree - not this plan's problem.
- No skill has `references/` or `templates/` under `concept-brief`, `spec-feature`,
  `architecture-datamodel` (glob returned nothing), so text moves stay inside `SKILL.md` bodies.

### Decisions already taken (user, 2026-10-16)

| Question | Decision |
|---|---|
| Glossary | **New skill `concept-glossary`** writes `_concept/glossary.md`, a root file beside `brief.md`; `10_blueprint/glossary.md` leaves the tree. One node right after `concept-brief` in every flow. |
| Data model | **Keep `10_blueprint/datamodel/`**, reorder only: `architecture-datamodel` runs after journeys + glossary and before `spec-featuresets`. No renumbering. |
| `concept-reverse` | **Findings only**: writes `02_grounding/findings/*` (+ nothing else). `concept-brief`, `design-brand`, `architecture-techstack` get a "seed from findings" step and run after it in the reverse flow. |
| Mockup renderers | **Keep both**; `mockup-storybook` reads `09_mockup/walkthrough/manifest.json` for screens and journeys instead of re-deriving them. |

### Decisions this plan takes (overridable)

1. **Root-file count stays three.** F10 folds `comparable.md` into a `## Comparables` section of
   `brief.md` that cites `02_grounding/research/competitors.md`; `glossary.md` takes the freed
   slot. ADR 0014 amends ADR 0007's root list to `brief.md · goals.md · glossary.md`.
2. **`produces` is frontmatter, not a registry.** `metadata.artifacts.produces: [{ id, path }]`
   on every skill; `check.py` validates it; no `contracts/artifacts.yaml` is generated. The host
   reading done-state from it is a named external action (a `host_facts.py` row on
   `produced_by` in `artifact-contract.ts`, so the day the host switches, `verify_host.py` says
   EXPIRED). Until then the editor's done-state stays as it is - this plan does not fix the host.
3. **`appbuilder-mvp` gains `experience-journeys`** (F01) rather than softening the
   `stories.yaml` gate: journeys carry the criterion ids (F20) that `build-plan`'s ledger cites,
   and the mvp flow has nothing else that could. `07_screens` becomes a soft gate everywhere
   (F35: four profiles never grow screens).
4. **Single glossary writer, re-entry for new terms.** `spec-feature` and
   `architecture-datamodel` rename to the glossary; a concept with no term is handed back to
   `concept-glossary`, which is re-enterable like `spec-feature`. They never append themselves.
5. **`feature-map.json` is dropped** (F33): with the model before the features, each feature
   spec lists `data_entities[]` itself at write time (F17), and that is the single join.
6. **`quality-standards` joins `appbuilder-standard`** after `build-scaffold` (F40, option 1),
   and `build-plan`/`build-implement` read its index when present.

## Target shape

### `_concept/` after the plan

```
_concept/
├── brief.md          pitch, audience, problem, hero flow, ## Comparables  (concept-brief)
├── goals.md                                                              (concept-brief)
├── glossary.md       ubiquitous language, _Avoid_ lists                  (concept-glossary)
├── 01_meta/scope.yaml                                                    (concept-scope)
├── 02_grounding/     onboarding/answers.json · research/ · findings/     (onboard · research · reverse)
├── 03_brand/         identity.md tokens.json brandbook.html              (design-brand)
├── 04_journeys/      stories.yaml with criterion ids                     (experience-journeys)
├── 05_features/      featuresets.md · <slug>.md with data_entities[]     (spec-featuresets · spec-feature)
├── 06_behaviors/                                                         (experience-behaviors)
├── 07_screens/       shell.md (prose + nav) · <screen>.md                (experience-shell · spec-feature)
├── 08_dossiers/      opened at spec-feature step 2, frozen at the end    (spec-feature)
├── 09_mockup/        walkthrough/ (manifest.json) · storybook/ · sessions (mockup-*)
├── 10_blueprint/     techstack.md architecture.md decisions.md datamodel/ (architecture-* ; no glossary.md, no feature-map.json)
└── 11_build/         ledger, trace.yaml                                  (build-* · quality-*)
```

### `appbuilder-standard` after the plan

```mermaid
flowchart LR
  scope --> onboard --> research --> brief --> glossary --> brand --> journeys --> datamodel --> featuresets --> behaviors --> feature
  feature --> shell --> techstack --> system --> walkthrough --> storybook --> annotate --> feedback
  feedback --> scaffold --> database --> standards --> plan --> implement --> branch --> test --> e2e --> review --> opsreview --> release
```

- `appbuilder-mvp`: scope → onboard → brief → glossary → journeys → featuresets → techstack →
  scaffold → plan → implement → test (11 nodes).
- `skaileup-concept-only`: scope → onboard → research → brief → glossary → brand → journeys →
  datamodel → featuresets → behaviors → feature → shell → walkthrough → annotate → feedback →
  ops-review.
- `skaileup-concept-reverse`: scope → reverse → standards → brief → glossary → brand → journeys
  → datamodel → featuresets → shell → feature → techstack → system → ops-review
  (`concept-scope` is the entry and writes `scope.yaml` with the flow id: F03).

Hierarchy the order encodes: domain language (brief, glossary) → data model → features →
screens → mockups → architecture → build → quality.

### Ownership after the plan (one writer per artifact)

| Artifact | Writer | Findings closed |
|---|---|---|
| `glossary.md` | `concept-glossary` | F08, F18, F30, F34 |
| `brief.md` (incl. comparables), `goals.md` | `concept-brief` | F09, F10 |
| `02_grounding/findings/*` (+ screenshots, `index.md` with `step`) | `concept-reverse`, `concept-research` (own subfolders) | F09, F11 |
| `02_grounding/onboarding/answers.json` (only answer record) | `concept-onboard` | F06, F16 |
| `03_brand/tokens.json`, `identity.md` (incl. tone) | `design-brand` | F09, F43 |
| `04_journeys/stories.yaml` (criteria with ids, stage definitions) | `experience-journeys` | F20, F24 |
| `05_features/<slug>.md` (permissions, scope line, `data_entities[]`) | `spec-feature` | F19, F22, F33 |
| `07_screens/shell.md` (prose + nav `elements:`, named in contract) | `experience-shell` | F21, F25 |
| `10_blueprint/techstack.md` (no integrations) / `architecture.md` (integrations) | `architecture-techstack` / `architecture-system` | F32 |
| `10_blueprint/datamodel/{model.dbml,model.json,seed.json}` | `architecture-datamodel` | F17, F31 |
| `11_build/trace.yaml` | `build-implement` | F36 |
| acceptance ledger rows (overwrite rule, `FAIL` beats `PASS`) | `build-plan` creates; `quality-e2e`, `quality-review` evaluate | F37, F39 |

## Phases

Each phase ends with `python scripts/check.py` green and a commit per ticket (the `CLAUDE.md`
watch rule applies on push).

### Phase 1 - machine layer and disk truth (F04 prep, F05, F06, F13, F15, F35, F44)

1. **ADR 0013 "A skill declares what it produces"** - `metadata.artifacts.produces: [{ id,
   path }]`; `id` is the artifact id other skills name in `artifacts.requires`; `path` is
   `_concept/`-prefixed and must appear in `contracts/concept_structure.md`'s tree fence
   (`check.py` already parses it). Records that no registry is generated and that the host's
   `produced_by` read is the external dependency. **ADR 0014 "The glossary is a root file"** -
   amends ADR 0007 root list; `comparable.md` folds into `brief.md`. Update `docs/adr/README.md`.
2. **`produces` on all 30 skills** + `docs/skill-template.md` block + `check.py` rules:
   `produces` present and non-empty for every skill that writes under `_concept/` (the
   writer map in the report's `writes.json` is the source list); each `path` in the tree fence;
   each `requires[].id` resolves to some skill's `produces[].id`. Fixtures in `test_check.py`.
3. **Soft gates for never-grown artifacts (F35)** - in `build-plan`, `build-implement`,
   `spec-featuresets`: `07_screens`/`stories.yaml` gates that `profiles/*.yaml` mark
   `not_grown` become `soft`, and the step that reads them states what happens without the file
   (plan from the featureset roster; implement from the spec alone). `check.py` rule: a `hard`
   gate on a path any profile lists as not grown is an error.
4. **Approvals and answers on disk (F06, F13, F16)** - `contracts/artifact_frontmatter.md`
   gains `approved: <date>` in the universal fields; `concept-brief`, `design-brand`,
   `concept-onboard`, `concept-reverse` write it at their approval step. `concept-onboard`
   step 1 merges the host's `_grounding/<step>/user_input.json` into `answers.json` once
   (`host_facts.py` row `host:grounding-user-input`); `onboarding.yaml` is derived from
   `answers.json` or dropped; `architecture-techstack` step 1 reads the confidence grade.
5. **Router (F15, F44)** - `skaileup` resolves the next node by comparing each node skill's
   `produces` list against the tree instead of scanning; `concept-scope` is the sole owner of
   the `web-app` default and the flow choice, `skaileup` points at it.

### Phase 2 - hierarchy: glossary first, model before features (F01-F04, F08, F10, F12, F17, F18, F25, F30, F31, F33, F34, F40)

6. **`concept-glossary` skill** (new, `skills/concept-glossary/SKILL.md`, < 140 lines):
   reads `brief.md`, `02_grounding/research/*`, `02_grounding/findings/*`; grills the user on
   the words (per `contracts/agent_patterns.md`); writes `_concept/glossary.md` in
   `domain_model.md`'s format; re-enterable. `contracts/domain_model.md` path and ownership
   sentence updated; `concept_structure.md` tree: `glossary.md` at root, `10_blueprint/glossary.md`
   removed, `comparable.md` removed, read-direction table updated. `concept-brief` step 6 and
   step 4 (comparables → `brief.md` section), `spec-feature` step 3, `architecture-datamodel`
   step 6 stop writing the glossary and read it instead (decision 4). `skills/README.md` index.
7. **Data model before features (F17, F18, F30, F31, F33, F34)** - `architecture-datamodel`:
   prerequisites become `stories.yaml` hard, `glossary.md` hard, `techstack.md`/`architecture.md`
   soft (F31 declares it), `05_features` and `06_behaviors` removed; step 1 reads journeys +
   glossary (not every feature), vocabulary step before step 3 (F30), approval before any write,
   step 5 (`feature-map.json`) and step 7 (register back) deleted; contract section citations
   (`seed_data.md § ...`) replace whole-file cites and restated rules (F34). `spec-feature`,
   `spec-featuresets`, `experience-journeys`, `experience-behaviors`: never coin entity names;
   read `model.json` when present else the glossary (F18); `spec-feature` writes
   `data_entities[]` at step 5 (F33). `concept_structure.md`: `datamodel/` line loses
   `feature cross-reference`; names one owner for the stack-specific schema file (F31).
8. **Flow rewrite (F01, F02, F03, F12, F25, F40)** - all four `flows/*/*.flow.yaml` to the
   target order above: insert `glossary` nodes, move `datamodel` before `featuresets`, move
   `techstack`/`system` before mockups, `research` before `brief`, `shell` after the feature
   loop, add `journeys` to mvp, add `standards` after scaffold in standard, `scope` as reverse
   entry; `requires` lists and group memberships updated; `concept-research` intro loses "not
   a pipeline step". `experience-shell` derives nav from existing screens (F25).
9. **`check.py` F04 rule** - walk each flow's `type: flow` edges from `entry`, accumulate
   `produces[].path`, fail on a `hard` prerequisite with no upstream writer (directory gates
   match by prefix). Fixture: a flow whose gate has no writer → exactly one error. Blocked by 8
   because today's flows would fail it.

### Phase 3 - one owner per artifact, reasons on disk (F09, F11, F16, F19-F24, F26-F28, F36-F39, F43)

10. **`concept-reverse` findings only (F09, F11)** - steps 4-6 removed; step 7 grows to
    `routes.md`, `screens.md`, `datamodel.md`, `stack.md`, `brand.md`, `brief-seeds.md`, each
    value graded; `Done when` lists only findings. `concept-brief`, `design-brand`,
    `architecture-techstack` get step 1b "seed from `02_grounding/findings/` when present".
    Screenshots: `02_grounding/findings/` only, `findings/index.md` with a `step` field
    (`concept-research`, `design-brand` updated).
11. **Spec truth (F19, F20, F22, F23)** - `experience-journeys` step 5 gives every EARS
    criterion an id (`contracts/acceptance_criteria.md` gets the id grammar); `spec-feature`,
    `build-plan`, `quality-e2e`, `experience-behaviors` cite ids, never retype text.
    Permissions: `spec-feature` owns the role × action table; `experience-behaviors`,
    `spec-featuresets`, `architecture-datamodel` (seed `permissions`) cite it. Scope line: the
    spec's `## Scope` section is the record; dossier links to it; `decisions.md` only for
    three-test decisions. Dossier opened at `spec-feature` step 2 and appended after each step;
    `experience-behaviors` names the feature file it re-runs when a rule changes.
12. **Screens and shell (F21, F24)** - `contracts/elements_block.md` names both writers
    (`spec-feature` for screens, `experience-shell` for `kind: nav` in `shell.md`);
    `spec-feature` intro sentence corrected. Stage definitions owned by `experience-journeys`;
    `spec-featuresets` and `experience-shell` cite `stories.yaml § stages`.
13. **Mockup loop (F26-F29)** - `mockup-storybook` reads `walkthrough/manifest.json` for
    screens and journeys (prerequisite soft on it); one `session.schema.json` under
    `mockup-annotate/references/`, `mockup-feedback` references it by path, prose and templates
    stop listing the enum; `contracts/feedback_loop.md` gains `## mockup-feedback` (screen edits,
    id promotion) cited at step 4; `mockup-walkthrough` lists only the resolved renderer's
    references and moves the devlog check into the renderer reference.
14. **Build and quality joins (F36-F39, F43)** - `build-implement` writes `11_build/trace.yaml`
    as the one feature→commit join; `ops-review`, `quality-release`, `quality-review` read it;
    spec review stays only in `quality-review`. `contracts/acceptance_criteria.md` ledger rule:
    later evaluation overwrites the row and stamps evidence, `FAIL` beats `PASS`; `quality-e2e`
    stops on a missing ledger and writes its per-journey verdict into ledger rows that
    `quality-release` reads instead of re-walking (F39; scaffold/branch stay git-only per ADR
    0010). `build-plan` cites `domain_model.md` instead of both decision paths; `build-branch`
    states its two rules (F38). `concept_structure.md` names `design-brand` as owner of tone and
    copy (F43).

### Phase 4 - dedup and wayfinding (F07, F14, F32, F41, F42)

15. **Contract sections (F07, F14, F32, F42)** - `spec-feature`, `architecture-datamodel`,
    `experience-shell` cite `§` sections (`elements_block.md § Schema`,
    `walkthrough_renderer.md § App-shell navigation`); the six "one question per message"
    restatements drop, the contract carries it; integrations live in `architecture.md` only and
    `architecture-techstack` step 3 skips questions an input field answered; release thresholds
    move to a table in `contracts/evaluator.md`, cited at `quality-release` step 7.
16. **`check_concept.py` (F41)** - `skills/ops-review/scripts/check_concept.py` (stdlib +
    yaml) runs the mechanical half of `ops-review` against a project's `_concept/`: frontmatter
    fields, `screens:`/`implements:` resolution, `data_entities[]` against `model.json`,
    criterion ids against `stories.yaml`, ledger rule. `ops-review` calls it at its first step
    and keeps judgement and the trace; its body drops under 100 lines. Fixture: a tmp
    `_concept/` with one broken link → one error.

## Verification

- Every ticket: `python scripts/check.py` green (collection + fixtures), skill bodies ≤ 140
  lines (`check.py` house rule), no `MUST`/`NEVER` block.
- Phase 2 proof: the F04 rule passes on all four flows and fails the fixture; the report's dump
  re-run (`python3 .scratch/reports/dump-skill-set-critique-2026-10-15.py`) shows
  `unmet hard 0` instead of 5 - the dump's gate/producer computation is the independent check.
- Re-run the critique generator and build after each phase; the number of findings whose
  evidence quotes still resolve is the regression meter (a finding whose quoted line no longer
  exists is closed - the dump aborts on it, so edit the findings file to mark it `closed` with
  the ticket id rather than deleting the row).
- Phase 4 `check_concept.py`: run against a throwaway `_concept/` built from the templates in
  the skills' `Done when` lists.
- Host: `python scripts/verify_host.py` after phase 1 reports the new `produced_by` row as
  HOLDS (meaning the host still reads the registry) - the plan's external dependency stays
  visible, not hidden.

## Risks

- **Host done-state stays broken** until the host reads `produces` (decision 2). Alternative:
  generate `contracts/artifacts.yaml` from frontmatter; rejected because ADR 0004 dropped the
  registry and a generated asset would need its own freshness rule.
- **ADR 0012's one-call phrasing** covers foreign skills only; `concept-glossary` re-entry is a
  flow re-entry, not a skill call, so `_check_skill_calls` is unaffected. If a body phrases it as
  a call, the check will say so.
- **Existing `_concept/` trees** that have `comparable.md` and `10_blueprint/glossary.md`: no
  migration tooling here; `ops-review`/`check_concept.py` reports the old paths as unowned.
- **Flow rewrite touches 4 files × ~30 nodes**; `check.py`'s `_check_requires` and
  `_check_reachability` catch missed `requires` entries and orphan nodes.
- **140-line ceiling** on `spec-feature` (already 106+ lines) when it gains the dossier-early
  and permissions-owner text; the removed glossary/decision text and the contract-section cites
  (phase 4) pay for it - if not, split the permissions table into `references/permissions.md`.

## Ticket breakdown

Effort code `SSI`. Tickets live in `.scratch/skill-set-improvement/issues/`. Each lands with
`check.py` green and one commit.

| # | Ticket | Phase | Blocked by |
|---|---|---|---|
| 1 | `i-ssi-adr-produces-glossary` - ADR 0013 + 0014, README index | 1 | - |
| 2 | `i-ssi-produces-list` - `produces` on 30 skills, template, check rules, fixtures | 1 | 1 |
| 3 | `i-ssi-soft-gates-profiles` - F35 soft gates with stated fallbacks + profile cross-check rule | 1 | 2 |
| 4 | `i-ssi-approved-answers` - `approved:` field, `answers.json` single record, host fact | 1 | - |
| 5 | `i-ssi-router-produces` - `skaileup` lookup by `produces`, `concept-scope` owns defaults | 1 | 2 |
| 6 | `i-ssi-concept-glossary` - new skill, tree + contract changes, three writers become readers | 2 | 1, 2 |
| 7 | `i-ssi-datamodel-first` - `architecture-datamodel` rewrite, entity names read not coined, `feature-map.json` dropped | 2 | 3, 6 |
| 8 | `i-ssi-flow-rewrite` - four flows to target order, mvp journeys, reverse entry, standards node | 2 | 3, 6, 7 |
| 9 | `i-ssi-check-gate-writers` - F04 rule + fixture | 2 | 8 |
| 10 | `i-ssi-reverse-findings-only` - `concept-reverse` writes findings; owners seed from them | 3 | 4, 8 |
| 11 | `i-ssi-spec-truth` - criterion ids, permissions owner, scope record, dossier early | 3 | 7 |
| 12 | `i-ssi-screens-shell` - `elements_block.md` two writers, stage definitions owned once | 3 | 8, 11 |
| 13 | `i-ssi-mockup-loop` - storybook reads manifest, one session schema, feedback contract section | 3 | 8 |
| 14 | `i-ssi-build-quality-joins` - `trace.yaml`, ledger overwrite rule, e2e verdict rows, tone owner | 3 | 11 |
| 15 | `i-ssi-contract-sections` - `§` cites, question-rule dedup, integrations home, thresholds table | 4 | 11, 12, 14 |
| 16 | `i-ssi-check-concept-script` - `check_concept.py` called by `ops-review` | 4 | 14 |

Ready at start: 1 and 4. Four edges were added at breakdown approval (2026-10-16) because the
paired tickets edit the same files: 6←2 (`concept-glossary` carries `produces`; glossary path vs
tree-fence rule), 7←3 (`spec-featuresets` gates), 10←4 (`concept-reverse` approval step),
12←11 (`spec-feature`/`spec-featuresets` bodies).

Published tickets, in breakdown order (`.scratch/skill-set-improvement/issues/`):

1. `i-ssi-adr-produces-glossary`
2. `i-ssi-produces-list`
3. `i-ssi-soft-gates-profiles`
4. `i-ssi-approved-answers`
5. `i-ssi-router-produces`
6. `i-ssi-concept-glossary`
7. `i-ssi-datamodel-first`
8. `i-ssi-flow-rewrite`
9. `i-ssi-check-gate-writers`
10. `i-ssi-reverse-findings-only`
11. `i-ssi-spec-truth`
12. `i-ssi-screens-shell`
13. `i-ssi-mockup-loop`
14. `i-ssi-build-quality-joins`
15. `i-ssi-contract-sections`
16. `i-ssi-check-concept-script`
