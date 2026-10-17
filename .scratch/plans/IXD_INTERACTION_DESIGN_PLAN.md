# IXD - Interaction design: the experience-app skills as collection variants - plan

## Context

Three global skills (`~/.agents/skills/experience-app-guideline`, `-objects`, `-interview`,
all 0.3.2) decide and audit an app's interaction logic: where each attribute lives, one editor
per object type, inline vs popover vs modal vs drawer vs page, create/delete flows, saving,
messages, popups, buttons, search, command palette, navigation and naming. They share three
byte-identical references (`app-patterns.md` P1-P17, `app-design.md` the `APP-DESIGN.md`
shape, `ui-detection.md` per-stack greps), and `-interview` has a fourth
(`decision-catalogue.md`). They write `APP-DESIGN.md` at the app root and findings into
`_concept/02_grounding/findings/<skill>/`.

This collection has no interaction layer at all. Today each screen spec in `spec-feature`
step 6 decides modal vs inline on its own, and `experience-shell` step 5 decides "where
confirmations and destructive actions surface" app-wide. No skill checks that `src/`
follows any of it. The user asked for collection variants that serve three uses:

1. **Planning** - decide the interaction rules before screens are specified.
2. **Clean application logic** - check the concept and the code against those rules.
3. **Retrofit** - on an existing app, seed the rules from what the code does and check the
   code against them.

### Decisions (user, 2026-10-17)

|Question|Decision|
|---|---|
|Home of the decisions|**`APP-DESIGN.md` at the project root**, beside `_concept/`, not inside the tree. Coding agents and the global skills find it where they expect it.|
|Skill split|**Two skills plus hooks**: `experience-interaction` (planning, writer of record), `quality-interaction` (code conformance). `concept-reverse` adds an interaction census finding; `ops-review` checks the screen specs against the rules.|
|Process|Plan + tickets, then `/implement IXD` in a fresh session.|

### Decisions this plan takes (overridable)

1. **One project-root artifact, named.** `APP-DESIGN.md` is the only `produces` path allowed
   outside `_concept/`. It is listed in `check.py` as `PROJECT_ROOT_ARTIFACTS =
   {"APP-DESIGN.md"}`, the same pattern as `PROJECT_ROOT_PREREQUISITES`. ADR 0015 records
   this and amends ADR 0011 and 0013. The project root is the directory that holds
   `_concept/`. A monorepo with several apps has one `_concept/` per project, so it also has
   one `APP-DESIGN.md` per project.
2. **Forked, not called.** The rulebook and shape are copied into `contracts/` and adapted.
   The collection never calls the global `experience-app-*` skills, so they are not
   `EXTERNAL_SKILLS` (ADR 0012). Different names (`experience-interaction`,
   `quality-interaction`) mean the two never collide on install. The global skills stay
   untouched for projects outside this collection.
3. **One writer of `APP-DESIGN.md`.** The global contract lets every skill add `(change)`
   marks. Here only `experience-interaction` writes the file, so it is single-writer like
   every other artifact after SSI. `quality-interaction` writes its own verdict,
   `_concept/11_build/interaction.yaml`: violations, exemplars, score, ordered changes,
   coverage, proposed exceptions. Re-entering `experience-interaction` folds that verdict
   into `(change)` marks and § Exceptions, after the user answers.
4. **The interview is a mode of the planning skill.** In this collection, asking the user is
   the approval step every concept skill already has. The catalogue becomes
   `skills/experience-interaction/references/decision-catalogue.md`, because only that skill
   reads it. Rounds: at most five questions each, recommendation first, and the file is
   written after every round. Without a user, entries carry `[open Qn]` and the questions go
   to § Open.
5. **Names are read, never coined.** Objects are `model.json` entities plus derived objects
   named in `glossary.md`. § Language cites `glossary.md` for nouns and keeps only the verb
   set (Create/Add/Edit/Delete/Remove). P13 points at `_concept/glossary.md`, not
   `CONTEXT.md`. An object with no glossary term is handed back to `concept-glossary`.
6. **Nav and shared patterns split by level.** `APP-DESIGN.md` § Navigation holds the rule
   (P12: primary nav = core indexes plus cross-object workspaces, deep links). `shell.md`
   holds the concrete nav it derives under that rule. `experience-shell` step 5 stops
   deciding empty, error and confirmation patterns; it cites MSG/EDIT/MOD entries and keeps
   only layout patterns (page header, breadcrumbs).
7. **Contracts, because there are several readers.**
   `contracts/interaction_patterns.md` (P1-P17 + § Recording findings) is read by
   `experience-interaction`, `quality-interaction`, `ops-review`, `spec-feature` and
   `experience-shell`. `contracts/app_design.md` (shape, entries, reading, writing) is read
   by all five plus `build-plan`. `contracts/ui_detection.md` (per-stack greps, citation
   check) is read by `concept-reverse` and `quality-interaction`.
8. **Profiles.** `app-design` and `interaction-review` join `not_grown` wherever `screens`
   already is: `api-service`, `cli-tool`, `data-pipeline`, `library`. `mobile-app` and
   `web-app` grow both.

## Target shape

### Where the files sit

```
<project root>/
├── APP-DESIGN.md            interaction decisions: objects, surfaces, editing, messages, buttons,
│                            search, nav rule, verb set, exceptions, open, changelog (experience-interaction)
└── _concept/
    ├── 02_grounding/findings/interaction.md   census of what the code does today (concept-reverse)
    ├── 07_screens/…                           screens apply OBJ/SURF entries (spec-feature reads)
    ├── 07_screens/shell.md                    concrete nav under NAV rule (experience-shell reads)
    └── 11_build/interaction.yaml              conformance verdict + ordered changes (quality-interaction)
```

### Skills

**`experience-interaction`** (experience domain, phase `conceptualization`, < 140 lines)
- requires: `glossary`, `journeys`, `datamodel`. Soft: `grounding-findings`
  (`findings/interaction.md`), `interaction-review` (re-entry after a check), and an
  existing `APP-DESIGN.md`.
- Steps: (1) read model, glossary, journeys, existing `APP-DESIGN.md` per
  `app_design.md § Reading it`. Where `findings/interaction.md` exists, recommend what the
  code already does when it passes the rule (retrofit). (2) classify objects (class, simple
  or complex, roles), with names read from model and glossary. (3) global decisions P1-P17:
  adopt, adapt or reject, each with a reason. (4) floorplan per type: index, home, editor,
  create, delete, representations, in search, `task → surface`, palette actions. (5) ask in
  rounds per the catalogue, existing § Open first. (6) write `APP-DESIGN.md` after every
  round, set `approved:`, add a § Changelog line. (7) where `11_build/interaction.yaml`
  exists, fold its changes into `(change)` marks and its proposed exceptions into § Open or
  § Exceptions per the user. (8) hand off to `spec-feature` (screens apply OBJ/SURF) and
  `experience-shell` (NAV).
- produces: `{ id: app-design, path: "APP-DESIGN.md" }`.

**`quality-interaction`** (quality domain, phase `review`, < 140 lines)
- requires: `app-design` (hard). Gate on `package.json` hard as the "code exists" proof
  (already a named project-root prerequisite).
- Steps: (1) read `APP-DESIGN.md` as intent (`§ Reading it`). (2) surface census per
  `ui_detection.md § Editors and surfaces`. (3) walk entry by entry and type by type, and
  name the regions left unread. Evidence passes may run in parallel. (4) each violation:
  entry and rule id, expected, actual, `file:line`, severity, kind, per
  `interaction_patterns.md § Recording findings`. Record one exemplar per rule. (5) score
  table computed from the findings, never typed. (6) ordered changes: systemic first, then
  per type, with a coverage table. (7) run the citation check (`ui_detection.md § Verifying
  citations`). (8) write `_concept/11_build/interaction.yaml` and hand contested items back
  to `experience-interaction`.
- produces: `{ id: interaction-review, path: "_concept/11_build/interaction.yaml" }`.

### Hooks in existing skills

|Skill|Change|
|---|---|
|`concept-reverse`|step 4 writes a seventh finding, `findings/interaction.md`: surface census, editors per type, save models, message channels, confirm components, palette/search. Graded like the others, cited by `ui_detection.md`.|
|`spec-feature`|step 6: each screen's editing surfaces follow the `APP-DESIGN.md` OBJ `task → surface` rows. A screen that needs a surface the floorplan lacks hands back to `experience-interaction`. Soft prerequisite `APP-DESIGN.md`. The body is at 135/140, so the net growth is at most 5 lines.|
|`experience-shell`|step 2 cites `APP-DESIGN.md` § Navigation (P12). Step 5 cites MSG/EDIT/MOD and keeps layout only.|
|`ops-review`|new step: screen specs against `APP-DESIGN.md`, covering P1 (attribute editable on two screens), P4 (two editors of one type), P8 (two indexes of one type) and P13 (label not in glossary). Each finding names `spec-feature` or `experience-interaction` as the fixing skill.|
|`build-plan`|soft-reads `11_build/interaction.yaml`. Open changes touching a feature's files join that feature's slices. Systemic changes (shared editor, action registry, one confirm component) become a leading slice.|

### Flows after the plan

- `appbuilder-standard`: … journeys → datamodel → **interaction** → featuresets → … →
  review → **interaction-check** → ops-review → release.
- `skaileup-concept-only`: … datamodel → **interaction** → featuresets → …
- `skaileup-concept-reverse`: scope → reverse → standards → brief → glossary → brand →
  journeys → datamodel → **interaction** → featuresets → shell → feature → techstack →
  system → **interaction-check** → ops-review. This is the retrofit loop: the census seeds
  the decisions, and the check lists what the existing code breaks.
- `appbuilder-mvp`: unchanged (no screens).

Hierarchy: domain language → data model → **interaction rules** → features → screens →
mockups → architecture → build → quality.

## Steps

1. **ADR and vocabulary.** `docs/adr/0015-interaction-decisions-live-in-app-design.md`
   (decisions 1-3, 5; forked from `experience-app-*` 0.3.2; host consequence: when the host
   reads `produces`, it joins `APP-DESIGN.md` to the project root, not to `_concept/`).
   `docs/adr/README.md` row. `CONTEXT.md` terms: **App design**, **Object class**,
   **Floorplan**, **Surface**, **Representation**. `contracts/concept_structure.md`: a
   `## Beside the tree` section naming `APP-DESIGN.md` and its writer, plus tree lines for
   `11_build/interaction.yaml` and `02_grounding/findings/interaction.md`.
2. **Gate.** `scripts/check.py`: `PROJECT_ROOT_ARTIFACTS`. `_check_produces` accepts those
   paths. `APP-DESIGN.md` joins `PROJECT_ROOT_PREREQUISITES`. `_check_gate_writers` matches
   a project-root gate against `produces` when the path is in `PROJECT_ROOT_ARTIFACTS`
   instead of skipping it. Fixtures: an accepted root artifact, a rejected unnamed root path,
   and a hard `APP-DESIGN.md` gate with no upstream writer giving one error.
   `docs/skill-template.md` names the exception.
3. **`experience-interaction`** + `contracts/interaction_patterns.md` +
   `contracts/app_design.md` (writing rules rewritten for one writer, the verdict file and
   the collection's glossary) + `references/decision-catalogue.md` + `contracts/README.md`
   and `README.md` rows + `app-design` in four profiles.
4. **Census.** `concept-reverse` seventh finding + `contracts/ui_detection.md`.
5. **`quality-interaction`** + `README.md` row + `interaction-review` in four profiles.
6. **Readers.** `spec-feature`, `experience-shell`, `ops-review` and `build-plan` per the
   hooks table.
7. **Flows.** Three flows get the nodes, edges, `requires` and phases, and `flows/README.md`
   lists the orders. The F04 rule (`_check_gate_writers`) stays green.
8. **Retrofit smoke run.** Copy one real web app from SKAILEdev (`forge/skaile-forge`'s
   editor app) to a temp dir. Run the reverse census step, `experience-interaction` without
   a user, and `quality-interaction` on it. Check that every artifact passes the citation
   check, every core type has a floorplan row, and the verdict has a coverage table. Fix
   skill text wherever it misled the run. Delete the temp copy.

## Verification

- Each ticket: `python3 scripts/check.py` green (collection + fixtures), bodies ≤ 140 lines,
  no `MUST`/`NEVER` block, README index complete. The pushed run is green per the
  `CLAUDE.md` watch rule.
- Step 2: the three new fixtures fail before the change and pass after it.
- Step 7: the F04 rule passes on all four flows. Re-running
  `.scratch/reports/dump-skill-set-critique-2026-10-15.py` still prints `unmet hard 0`.
- Step 8: the smoke run is the end-to-end proof of all three uses: census → decisions →
  conformance verdict on real code.
- `python3 scripts/verify_host.py`: no new expired facts.

## Risks

- **`spec-feature` at 135/140 lines.** If the screen-step sentence does not fit, the rule
  moves into `contracts/app_design.md § Reading it` (screen specs apply OBJ rows), and
  `spec-feature` cites that section in one line.
- **Host done-state for a project-root artifact.** No host reads `produces` today
  (ADR 0013). The day it does, `APP-DESIGN.md` must join the project root. ADR 0015 states
  this, and the existing `host:node-done-from-produced-by` fact will expire at the same
  moment.
- **Two copies of the rulebook** (global `experience-app-*` and `contracts/`) drift apart.
  This is accepted: the fork is deliberate and has its own lifecycle. ADR 0015 names the
  version it forked from.
- **ADR number 0015** is also what the TRE plan uses in its sibling repo
  (`ai-assets-skaileup-tree`). If TRE carries ADRs over after IXD lands, TRE renumbers its
  own.
- **`ops-review` grows past the SSI target of < 100 lines.** That target was a plan goal,
  not an invariant. The 140 ceiling still holds.

## Ticket breakdown

Effort code `IXD`. Tickets live in `.scratch/interaction-design/issues/`. Each lands with
`check.py` green and one commit.

|#|Ticket|Step|Blocked by|
|---|---|---|---|
|1|`i-ixd-adr-app-design` - ADR 0015, ADR index, CONTEXT terms, tree lines + `## Beside the tree`|1|-|
|2|`i-ixd-gate-root-artifact` - `PROJECT_ROOT_ARTIFACTS` in produces, prerequisites, gate-writers; fixtures; template|2|1|
|3|`i-ixd-experience-interaction` - planning skill, two contracts, catalogue, profiles, indexes|3|2|
|4|`i-ixd-reverse-census` - `findings/interaction.md`, `ui_detection.md`|4|3|
|5|`i-ixd-quality-interaction` - conformance skill, `11_build/interaction.yaml`, profiles, index|5|3, 4|
|6|`i-ixd-reader-hooks` - spec-feature, experience-shell, ops-review, build-plan|6|3, 5|
|7|`i-ixd-flows` - three flows + flows/README|7|3, 5|
|8|`i-ixd-retrofit-smoke` - census → decisions → verdict on a real app, fixes|8|4, 6, 7|

Ready at start: 1. Tickets 6 and 7 can run in parallel; the rest follow the edges.
