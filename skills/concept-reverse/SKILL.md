---
name: concept-reverse
description: "Use when a repository already exists and the concept has to be extracted from it rather than designed. Detects the stack, the brand, the routes and the schema, and writes what the code actually says plus the evidence the rest of the pipeline reads. Triggers on 'reverse engineer this project', 'extract the concept from this codebase', 'document this existing app'."
version: "0.1.0"
metadata:
  requires:
    - contract:@skaile-ai/shared-contracts
  artifacts:
    requires:
      - { id: scope }
  prerequisites:
    files:
      - { path: "_concept/01_meta/scope.yaml", gate: soft }
    inputs_optional:
      - { id: repo_path, label: "Repository path", type: text, hint: "Defaults to the project root" }
      - { id: app_hint, label: "What does this app do?", type: text, hint: "Only needed when the README is thin" }
---

# concept-reverse

Reads an existing repository and writes down what it actually is: the brief its docs
describe, the stack its manifests declare, the brand its theme files carry, and the route,
screen and schema evidence behind everything else. It is one node in a flow, not a pipeline —
`experience-journeys`, `spec-featuresets`, `experience-shell`, the `spec-feature` loop,
`architecture-system`, `architecture-datamodel` and `quality-standards` run after it as their
own steps, and it writes none of their artifacts.

Paths are `contracts/concept_structure.md`'s and frontmatter shapes are
`contracts/artifact_frontmatter.md`'s. The detection recipes — which files to read, in which
order, and what each signal means — are in `references/detection/`, one file per dimension;
read the one the step names when you reach it.

## Steps

1. **Confirm the repository and find the app inside it.** The path has to be readable and
   hold at least one of a source tree, a README or a package manifest. A monorepo has more
   than one candidate: name them and ask which is the app rather than picking the first, since
   every later step scopes to that answer. Note which `_concept/` files already exist — this
   skill adds what is missing and shows a diff before touching anything that is there.
2. **Map the repository before reading any file deeply.** List the top two levels and
   identify the manifests, the README and `docs/`, the source root, the framework config
   files, the schema or migration directories, the tests and the CI configuration. Read
   selectively from that map: `dist/`, `build/`, `.next/`, `node_modules/` and lockfiles are
   generated, and loading them buys nothing but context.
3. **Grade every value you write, as you write it.** `extracted` — read verbatim from code,
   config or docs. `inferred` — reasoned from structure, defensibly, but nobody said it.
   `needs_review` — no signal found. The grade goes in an `extraction_confidence` field beside
   the value. It is the whole difference between a concept somebody can trust and one that
   reads exactly like a hand-written concept while being half guesswork, and it is what the
   report in step 8 is counted from.
4. **Write the brief from what the project already says about itself** — README, the
   manifest's `name`, `description`, `keywords` and `homepage`, the changelog, and anything
   under `docs/`. `brief.md` takes the pitch, audience, problem and hero flow; `goals.md`
   takes the roadmap, milestones and stated constraints; `comparable.md` takes the products
   the README names under "similar to", "inspired by" or "alternatives". A thin README yields
   a thin brief marked `needs_review`, never a rich one inferred from the code: motivation and
   audience are the two things source code never states.
5. **Detect the stack** per `references/detection/techstack.md` and write
   `10_blueprint/techstack.md` — platform, frontend, UI library, backend, database and ORM,
   auth, hosting and package manager, each graded, with the version constraints and odd
   combinations noted in the body.
6. **Detect the brand** per `references/detection/brand.md` and write `03_brand/identity.md`
   and `03_brand/tokens.json`. Write `tokens.json` even when every field is `needs_review`:
   both mockup renderers hard-gate on that file, and its absence stops them before they can
   report why. Colours come from the theme config, the CSS custom properties or the token
   file — a palette invented because none was found is a brand this app does not have.
7. **Put the route, screen and schema evidence into grounding**, per
   `references/detection/screens.md` and `references/detection/datamodel.md`:
   `02_grounding/findings/routes.md` (every route or endpoint with the file that defines it
   and what a user does there), `screens.md` (the page components behind those routes, their
   data bindings, interactions and visible states), and `datamodel.md` (the entities, fields,
   relations and enums the schema declares, mapped to `contracts/semantic_types.md` types).
   Feature specs, screen specs and the model itself are written by the skills that run after
   this one, from this evidence. Routes are evidence, not features — a feature file listing
   API paths describes the server rather than the user — and an entity name is not final until
   the model is built, so a name guessed into a spec now diverges from the model silently and
   nothing catches it.
8. **Verify the citations, then report.** Every file path written into any artifact is
   checked to exist on disk — a package subpath export such as `./store/react` is not a path,
   and a citation a reader cannot open defeats the field. Then present the counts per
   artifact of extracted, inferred and needs_review, list every `needs_review` field with
   what is missing, and note the ambiguities: two ORMs, no README, routes recovered from
   components because there is no router. A report claiming nothing needs review while the
   brief was inferred from a package description is the failure this step exists to prevent.
9. **Hand off to the nodes that follow**, naming what each one now has to work from — the
   journeys and featuresets from the routes evidence, the screens from `screens.md`, the model
   from `datamodel.md` — and what the user should correct first, which is always the
   `needs_review` list.

## What sits in `references/detection/`

One file per dimension — `techstack.md`, `datamodel.md`, `brand.md`, `screens.md` — each
carrying the file globs, the signal-to-value tables and the priority order for its dimension.
This is stack-specific knowledge nothing else in the collection owns; when a framework is
missing from a table, the table is what gets extended.

**Done when** `brief.md`, `goals.md`, `comparable.md`, `10_blueprint/techstack.md`,
`03_brand/tokens.json` and the three `02_grounding/findings/` files exist, every value in
them carries a confidence grade, and every cited path resolves on disk.
