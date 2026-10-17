# `_concept/` artifacts against industry standards — migration suggestions

Date: 2026-10-17. Facts about each standard (versions, status, URLs) are in
[`concept-standards-sources-2026-10-17.md`](./concept-standards-sources-2026-10-17.md); this
file only maps them onto the tree in `contracts/concept_structure.md` and says what to do.
Verdicts: **Migrate** (change the file's format), **Align** (keep the file, adopt the
standard's vocabulary or structure), **Add** (an artifact the standard covers and we lack),
**Keep** (no standard worth the cost).

## Shortlist, ranked by value / cost

| # | Artifact | Standard | Verdict | Why it pays |
|---|---|---|---|---|
| 1 | `03_brand/tokens.json` | W3C DTCG Format Module 2025.10 (+ Resolver Module) | Migrate | Build tools generate CSS/Tailwind from it (the hand-written `tailwind` block goes); light/dark becomes expressible; design tools import it |
| 2 | YAML/JSON data files + frontmatter | JSON Schema 2020-12 | Add | One shape definition for skills, `check.py`, editors and the host; the host's copy has already drifted |
| 3 | `11_build/interaction.yaml` (located violations) | OASIS SARIF 2.1.0 | Migrate | `file:line` findings are exactly SARIF's shape; GitHub code scanning shows them on PRs |
| 4 | API contract (absent) | OpenAPI 3.2 · AsyncAPI 3.1 | Add (api-service) | The `api-service` profile has no machine-readable interface artifact |
| 5 | `10_blueprint/decisions.md`, `11_build/decisions.md` | MADR 4.0.0 | Align | Names a known format; per-file option unlocks Structurizr/Log4brains import |
| 6 | `10_blueprint/architecture.md` | C4 model; arc42 9.0 as a map | Align | Shared vocabulary for levels; arc42 map exposes two gaps (deployment, risks) |
| 7 | `APP-DESIGN.md` | `AGENTS.md` convention (Linux Foundation AAIF) | Align | Coding agents load `AGENTS.md`, not `APP-DESIGN.md` |

Everything else is **Keep** — see the per-artifact table.

## 1. Design tokens → DTCG 2025.10 (Migrate)

Today `tokens.json` is a bespoke flat object (`colors.primary`, `fonts`, `radius`, `mode`,
`spacing_base`, `shadows`, `atmosphere`, `tailwind`), written by `design-brand`
(`skills/design-brand/SKILL.md:75-78`).

- **Gain.**
  - Style Dictionary v5 and Terrazzo build CSS custom properties and Tailwind config from a DTCG file. The `tailwind` block is a hand-kept second copy of the same values and goes.
  - The Resolver Module (`.resolver.json`) expresses light/dark sets. `build-scaffold` step 5 already asks for "both light and dark blocks when the tokens carry both", which today's single `mode` key cannot say.
  - Penpot, Tokens Studio and others import the format. `concept-reverse`'s brand detection already looks for `style-dictionary/` trees (`references/detection/brand.md:10`), so an existing app's tokens can come in as they are.
- **Shape.**
  - `$value`/`$type` per token. Colours are structured objects (`colorSpace`, `components`, optional `hex`).
  - Aliases are written `{color.primary}`. The extension is `.tokens.json`, so the file becomes `03_brand/brand.tokens.json`.
- **What doesn't map.**
  - `atmosphere` is prose and belongs in `identity.md`, or in `$extensions`.
  - The top-level `approved:` key (`contracts/artifact_frontmatter.md:23`) would parse as a group name. It has to go under `$extensions`, e.g. `"$extensions": {"ai.skaile": {"approved": "…"}}`.
- **Cost.**
  - The readers are `design-brand`, `build-scaffold`, `experience-shell`, `mockup-walkthrough`, `mockup-storybook` (+ `references/scaffold.md`), `quality-release`, `ops-review`, `concept-research` and `concept-reverse` (detection). Plus the tree line in `concept_structure.md`, the `produces` path and the `check.py` tree fence.
  - `mockup-walkthrough` flattens to `--token-<dotted-path>`, so the property names change with the tree.
- **Risk.**
  - Style Dictionary says its 2025.10 support is "a work in progress in v5". Stick to the token types it already handles (colour objects since 5.3, dimension objects since 5.4) and keep `hex` on every colour.
  - The host's `BrandTokens` TypeBox schema (`skaile-forge/shared/schemas/frontmatter.ts:77`) describes the old shape. A grep of `server/`, `app/` and `shared/` found no code that validates against it, only its declaration and `CONTRACT.md` [INFERENCE: no other consumer].

## 2. Data shapes → JSON Schema 2020-12 (Add)

The collection describes the shape of its machine files in prose and code fences. The host keeps its own TypeBox copies, and TypeBox compiles to JSON Schema.

- **Evidence of drift.**
  - The host's `BrandTokens` has no `tailwind` key, while `design-brand` says the file "carries every key above" including `tailwind`.
  - The host's `seed.ts` comment points at `_concept/06_datamodel/seed.json`, a tree that no longer exists.
- **Suggestion.** Put `contracts/schemas/*.schema.json` in the contracts asset. The candidates are:
  - `scope.yaml`
  - `answers.json`
  - `stories.yaml`
  - `model.json`
  - `seed.json`
  - `trace.yaml`
  - `interaction.yaml` / SARIF properties
  - the universal frontmatter block

  Each YAML file's first line is `# yaml-language-server: $schema=…`, so editors validate it as it is typed. `check.py` validates the templates in skill bodies against the schemas, and the host imports the same files instead of hand-copying.
- **Precedent:** `skills/mockup-annotate/references/session.schema.json` already exists.
- **Not in conflict with** `contracts/README.md:44` ("No `flow.schema.json`"). That decision is about flows, whose binding rules are graph properties. Artifact files are plain data shapes, which is what JSON Schema is good at.
- **Cost:**
  - one contract file per shape
  - a `check.py` rule that resolves `$schema` references
  - a host-side change to stop duplicating the shapes

## 3. Interaction verdict → SARIF 2.1.0 (Migrate)

`quality-interaction` writes violations with `file:line`, a rule id, severity and a fix.

- **Mapping to SARIF.**
  - Rule id → `ruleId`. The P1–P17 catalogue becomes `tool.driver.rules[]`, with `helpUri` pointing at `contracts/interaction_patterns.md`.
  - Severity → `level`: critical/high → `error`, medium → `warning`, low → `note`. The four-level severity stays in `properties.severity`.
  - Score, ordered changes and exceptions go into `runs[0].properties`.
- **File:** `11_build/interaction.sarif`. The spec allows `.sarif` or `.sarif.json`.
- **Gain:** GitHub code scanning accepts the upload and annotates PR diffs (verified). Other viewers were not checked.
- **`reviews/<slug>.yaml`:** keep it as YAML. Most of its findings are about spec conformance and criteria, not source locations. Adopt the same severity → `level` mapping in `contracts/evaluator.md` so a later SARIF export stays mechanical.

## 4. API contract → OpenAPI 3.2 / AsyncAPI 3.1 (Add, `api-service` profile)

- **The gap.** No skill or contract mentions OpenAPI or AsyncAPI (grep across `skills/`, `contracts/`, `profiles/`). For `api-service`, the interface is the product, yet it exists only as prose in `architecture.md`.
- **Suggestion.**
  - `architecture-system` writes `10_blueprint/openapi.yaml` (HTTP) and/or `10_blueprint/asyncapi.yaml` (events) when the profile or the techstack says so. AsyncAPI's documented convention is `asyncapi.yaml`; OpenAPI's file name is unverified.
  - `build-scaffold`/`build-implement` read it as the contract, and `quality-e2e` can drive contract tests from it.
- **Placement:** this stays inside `10_blueprint/`, so ADR 0010's first-level rule is untouched.
- **Needs** an ADR, because it is a new artifact with a profile-conditional gate.

## 5. Decision records → MADR 4.0.0 (Align)

The current format is tiny entries in one append-only file, behind a three-test gate (`contracts/domain_model.md:76-114`). Its optional lines already match MADR's sections:

| Ours | MADR |
|---|---|
| Status | `status` (front matter) |
| Options considered | Considered Options |
| Consequences | Decision Outcome → Consequences |

- **Option a (recommended): keep one file, rename to MADR vocabulary.** Use MADR's headings and status keys and cite MADR in the contract. This costs one contract edit and changes no paths. The tiny-entry rule and the three-test gate stay; MADR's bare-minimal template is compatible with them.
- **Option b: one file per decision, `10_blueprint/decisions/NNNN-title.md`.** Use this only if Structurizr's `!adrs` or Log4brains rendering is wanted; both import MADR per-file trees.
  - Costs: the tree, `produces`, and `ops-review`'s reads.
  - It also creates a `decisions.md` vs `decisions/` pair across the two phases, so name the build-side one differently.
  - This repo's own `docs/adr/NNNN-*.md` already follows the per-file convention.

## 6. Architecture → C4 + arc42 map (Align)

- **C4.** It is an approach without a file format. Structure `architecture.md` by C4 level: System Context (users + external integrations, which already live here per F32), then Containers (modules/deployables), then optional Components. The levels give reviewers and agents a shared granularity.
- **Structurizr DSL (`workspace.dsl`).** Adopt it only if something renders it. It would be a second form of the same content.
- **arc42 9.0** has 12 sections. Used as a mapping rather than a migration, it shows what the tree covers:

| arc42 | `_concept/` home |
|---|---|
| 1 Introduction & Goals | `brief.md`, `goals.md` |
| 2 Constraints | `goals.md` (constraints, non-goals) |
| 3 Context & Scope | `architecture.md` (context) |
| 4 Solution Strategy | `techstack.md` |
| 5 Building Block View | `architecture.md` (containers) |
| 6 Runtime View | `06_behaviors/`, `04_journeys/` |
| 7 Deployment View | **none** — `techstack.md` names hosting, nothing describes topology |
| 8 Crosscutting Concepts | `APP-DESIGN.md`, `07_screens/shell.md` |
| 9 Architecture Decisions | `decisions.md` ×2 |
| 10 Quality Requirements | `goals.md`, `contracts/evaluator.md § Release thresholds` |
| 11 Risks & Technical Debt | **none** |
| 12 Glossary | `glossary.md` |

The two gaps (7, 11) are real decisions to make, not formatting.

## 7. `APP-DESIGN.md` ↔ `AGENTS.md` (Align)

- **Background.**
  - `AGENTS.md` is the de-facto agent-instruction file, now stewarded by the Agentic AI Foundation (Linux Foundation) and read by Codex, Cursor, Aider, Zed, VS Code and others.
  - `contracts/app_design.md:16-17` keeps skills out of `CLAUDE.md`/`AGENTS.md` and only notes a missing link.
- **Suggestion.** Keep `APP-DESIGN.md`. When `build-scaffold` creates the project, which means the file is new and the skill's own, have it write an `AGENTS.md` line pointing at `APP-DESIGN.md`. Existing projects keep today's "say so, don't edit" rule. Without the pointer, a coding agent outside skaileup never sees the interaction rules.

## Per-artifact table (everything)

| Artifact | Today | Closest standard | Verdict | Reason |
|---|---|---|---|---|
| `brief.md`, `goals.md` | Markdown + frontmatter | Lean Canvas, OKR (methods); ISO 17469-1 StratML | Keep | No file format worth it; StratML is XML for strategic plans, no tooling in this space |
| `glossary.md` | Markdown, `_Avoid_` lists | W3C SKOS (RDF); Schema.org `DefinedTerm` | Keep | RDF has no consumer here; Markdown matches arc42 §12 / DDD practice |
| `01_meta/scope.yaml` | YAML | — | Keep (+ schema, §2) | |
| `02_grounding/onboarding/answers.json` | JSON | — | Keep (+ schema, §2) | |
| `02_grounding/research/*`, `findings/*` | Markdown | — | Keep | Prose evidence |
| `03_brand/identity.md` (tone, copy) | Markdown | BrandSpec v0.1.0, AdCP `brand.json`, BCP, `.grain`, MRBS | Keep, revisit | No standards body; all young vendor formats |
| `03_brand/tokens.json` | bespoke JSON | DTCG 2025.10 | **Migrate** (§1) | |
| `03_brand/brandbook.html` | HTML | — | Keep | Rendered view |
| `04_journeys/stories.yaml` | YAML, EARS criteria with ids | EARS (Mavin); story maps/personas have no standard | Keep (+ schema) | EARS is the de-facto form; Kiro uses the same `WHEN … THE SYSTEM SHALL` |
| `05_features/**` | Markdown + frontmatter | Spec Kit / Kiro / OpenSpec (tool conventions) | Keep | Fast-moving vendor layouts, not standards; ours already has their shape (per-feature file, EARS, separate tasks/plan) |
| `06_behaviors/*.md` | Markdown state tables | W3C SCXML; XState JSON; Mermaid `stateDiagram-v2` | Keep | SCXML's JS tooling is alpha (`@xstate/scxml` 1.0.0-alpha.2); XState is vendor-owned and moving to v6; tables carry guards better than a diagram |
| `07_screens/**` (`elements:` block) | Markdown + YAML block | none (Open UI is browser controls, not layouts) | Keep | |
| `08_dossiers/**` | Markdown | — | Keep | |
| `09_mockup/storybook/` | Storybook CSF 3 | CSF 3 | Already standard | |
| `09_mockup/walkthrough/manifest.json`, `feedback/` sessions | JSON (+ `session.schema.json`) | — | Keep | |
| `10_blueprint/techstack.md` | Markdown | — | Keep | |
| `10_blueprint/architecture.md` | Markdown | C4; arc42; ISO 42010 (no format) | **Align** (§6) | |
| `10_blueprint/decisions.md` | Markdown log | MADR 4.0.0 | **Align** (§5) | |
| `10_blueprint/datamodel/model.dbml` | DBML | DBML (de-facto) | Already standard | |
| `10_blueprint/datamodel/model.json` | bespoke JSON (host canvas) | JSON Schema; LinkML | Keep (+ schema) | Host editor reads it; LinkML would move the canonical model and the canvas |
| `10_blueprint/datamodel/seed.json` | JSON scenarios | — | Keep (+ schema) | |
| API contract | absent | OpenAPI 3.2, AsyncAPI 3.1 | **Add** (§4) | |
| `11_build/acceptance-criteria/**.ac.md` | checkbox ledger | JUnit XML (no spec), CTRF (pre-1.0) | Keep | Host parser reads the checkbox lines; a row's evidence pointer may cite a JUnit/CTRF report path |
| `11_build/trace.yaml` | YAML + commit trailer | git trailers (mechanism only); OSLC (server protocol) | Keep (+ schema) | No standard trailer key; OSLC needs a server |
| `11_build/interaction.yaml` | YAML | SARIF 2.1.0 | **Migrate** (§3) | |
| `11_build/reviews/*.yaml` | YAML | SARIF 2.1.0 | Keep, align severity map | Mostly non-located findings |
| `APP-DESIGN.md` | Markdown | `AGENTS.md` | **Align** (§7) | |

## Side finding: the host reads a different `11_build/`

This is not a standards question, but it came up while checking which formats the host pins. `skaile-forge/server/utils/review-coverage.ts:109-131` reads three paths, and none of them is where the collection writes (`contracts/concept_structure.md:85-91`):

| Host reads | Collection writes |
|---|---|
| `<project>/_implementation/trace.yaml` | `_concept/11_build/trace.yaml` |
| `_implementation/acceptance_criteria/` | `_concept/11_build/acceptance-criteria/` |
| `_implementation/review/` | `_concept/11_build/reviews/` |

The three differ in root, in separator and in number. [INFERENCE] The coverage page therefore reports nothing for a project built by this collection. A `host_facts.py` row on `join(projectRoot, "_implementation")` would make the mismatch visible in `verify_host.py`, the same way the `produced_by` dependency is tracked.
