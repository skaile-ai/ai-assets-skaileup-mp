---
name: concept-reverse
description: "Use when a repository already exists and the concept has to be extracted from it rather than designed. Reads the routes, screens, schema, stack, brand, interaction surfaces and docs, and writes what the code actually says as graded findings the owning skills seed from. Triggers on 'reverse engineer this project', 'extract the concept from this codebase', 'document this existing app'."
version: "0.1.0"
metadata:
  requires:
    - contract:@skaile-ai/shared-contracts
  artifacts:
    requires:
      - { id: scope }
    produces:
      - { id: grounding-findings, path: "_concept/02_grounding/findings/" }
  prerequisites:
    files:
      - { path: "_concept/01_meta/scope.yaml", gate: soft }
    inputs_optional:
      - { id: repo_path, label: "Repository path", type: text, hint: "Defaults to the project root" }
      - { id: app_hint, label: "What does this app do?", type: text, hint: "Only needed when the README is thin" }
---

# concept-reverse

Reads an existing repository and writes down what it actually is, as findings and nothing
else: the brief its docs describe, the stack its manifests declare, the brand its theme files
carry, and the route, screen, schema and interaction evidence behind everything else. It is one
node in a flow, not a pipeline. `concept-brief`, `design-brand` and `architecture-techstack`
seed their drafts from these findings and put every value in front of the user;
`experience-journeys`, `spec-featuresets`, `experience-shell`, the `spec-feature` loop,
`architecture-datamodel`, `architecture-system` and `quality-standards` read them as evidence;
`experience-interaction` seeds `APP-DESIGN.md` from `interaction.md`, and `quality-interaction`
reads it as the census to judge against. This skill writes none of their artifacts.

Paths are `contracts/concept_structure.md`'s and frontmatter shapes are
`contracts/artifact_frontmatter.md`'s. The detection recipes — which files to read, in which
order, and what each signal means — are in `references/detection/`, one file per dimension;
read the one the step names when you reach it.

## Steps

1. **Confirm the repository and find the app inside it.** The path has to be readable and
   hold at least one of a source tree, a README or a package manifest. A monorepo has more
   than one candidate: name them and ask which is the app rather than picking the first, since
   every later step scopes to that answer. Note which `02_grounding/findings/` files already
   exist — this skill adds what is missing and shows a diff before touching anything there.
2. **Map the repository before reading any file deeply.** List the top two levels and
   identify the manifests, the README and `docs/`, the source root, the framework config
   files, the schema or migration directories, the tests and the CI configuration. Read
   selectively from that map: `dist/`, `build/`, `.next/`, `node_modules/` and lockfiles are
   generated, and loading them buys nothing but context.
3. **Grade every value you write, as you write it.** `extracted` — read verbatim from code,
   config or docs. `inferred` — reasoned from structure, defensibly, but nobody said it.
   `needs_review` — no signal found. The grade goes in an `extraction_confidence` field beside
   the value. It is the whole difference between a finding somebody can trust and one that
   reads exactly like a hand-written concept while being half guesswork, and it is what the
   report in step 5 is counted from.
4. **Write the seven findings into `02_grounding/findings/`**, each cited to the file that
   backs it and graded per value:
   - `brief-seeds.md` — from the README, the manifest's `name`, `description`, `keywords` and
     `homepage`, the changelog and `docs/`: pitch, audience, problem, hero flow, roadmap and
     constraints, and the products named under "similar to", "inspired by" or "alternatives".
     A thin README yields thin seeds marked `needs_review`, never rich ones inferred from the
     code: motivation and audience are what source code never states.
   - `stack.md` — per `references/detection/techstack.md`: platform, frontend, UI library,
     backend, database and ORM, auth, hosting and package manager, with the version
     constraints and odd combinations noted in the body.
   - `brand.md` — per `references/detection/brand.md`: colours, type, radius, spacing, mode.
     Colours come from the theme config, the CSS custom properties or the token file; when
     there is none, every field is `needs_review`, because a palette invented because none was
     found is a brand this app does not have.
   - `routes.md` — every route or endpoint, the file that defines it, and what a user does
     there. `screens.md` — the page components behind those routes, their data bindings,
     interactions and visible states. Both per `references/detection/screens.md`.
   - `datamodel.md` — the entities, fields, relations and enums the schema declares, mapped
     to `contracts/semantic_types.md` types, per `references/detection/datamodel.md`.
   - `interaction.md` — how the app lets a user work, per `contracts/ui_detection.md` §
     Editors and surfaces: the surface census (modal, drawer, popover, palette — each with
     purpose, host component and trigger) and the editor per object type. Add the finders
     (search, palette) per § Finders, and the save models, message channels and confirm
     components per § Saving, messages, popups and buttons. Every value carries a
     repository-root `file:line` and its grade; a surface seen only in a vendored UI library
     is not in the census (§ Generated and vendored code). A rule with no hit is
     `needs_review` with the grep that found nothing, because an absence nobody searched for
     reads exactly like one nobody found.

   Add a row per file to `findings/index.md` — path, source, date, and `step: concept-reverse`.
   Routes are evidence, not features — a feature file listing API paths describes the server
   rather than the user — and an entity name is not final until the model is built, so a name
   guessed into a spec now diverges from the model silently and nothing catches it.
5. **Verify the citations, then report.** Every file path written into a finding is checked
   to exist on disk — a package subpath export such as `./store/react` is not a path, and a
   citation a reader cannot open defeats the field. In `interaction.md` the check follows
   `contracts/ui_detection.md` § Verifying citations: the full path from the repository root,
   with a line that exists. Then present the counts per file of
   extracted, inferred and needs_review, list every `needs_review` value with what is
   missing, and note the ambiguities: two ORMs, no README, routes recovered from components
   because there is no router. A report claiming nothing needs review while the brief seeds
   came from a package description is the failure this step exists to prevent.
6. **Hand off to the nodes that follow**, naming what each one now has to work from — the
   brief from `brief-seeds.md`, the brand from `brand.md`, the stack from `stack.md`, the
   journeys and featuresets from `routes.md`, the screens from `screens.md`, the model from
   `datamodel.md`, the interaction decisions from `interaction.md` — and what the user should
   correct first, which is always the `needs_review`
   list. Once the user has accepted the report — corrections made, the `needs_review` list
   acknowledged — write `approved: <date>` into the frontmatter of every findings file this run
   wrote. A run the user has not accepted leaves the key out.

## What sits in `references/detection/`

One file per dimension — `techstack.md`, `datamodel.md`, `brand.md`, `screens.md` — each
carrying the file globs, the signal-to-value tables and the priority order for its dimension.
This is stack-specific knowledge nothing else in the collection owns; when a framework is
missing from a table, the table is what gets extended. The recipes for `interaction.md` are
the grep tables in `contracts/ui_detection.md`, shared with `quality-interaction`.

**Done when** `brief-seeds.md`, `stack.md`, `brand.md`, `routes.md`, `screens.md`,
`datamodel.md` and `interaction.md` exist in `02_grounding/findings/` and are listed in
`findings/index.md`, every value in them carries a confidence grade, and every cited path
resolves on disk.
