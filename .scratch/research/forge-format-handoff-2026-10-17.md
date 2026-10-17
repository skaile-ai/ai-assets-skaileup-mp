# Handoff — make `skaile-forge` read the collection's current `_concept/` formats

Written 2026-10-17 by the session that landed the formats in `ai-assets-skaileup-mp`
(`/Users/matthias/devBench/SKAILEdev/ai-assets/ai-assets-skaileup-mp`, `main` at `da47632`).
This file is a brief, not a plan: the forge session plans and decides.

## Goal

`forge/skaile-forge` (`/Users/matthias/devBench/SKAILEdev/forge/skaile-forge`) reads and edits
projects whose `_concept/` tree is written by the `skaileup-mp` skills. Those skills changed
the tree and several file formats; the host still reads the old ones. Make the host read and
write what the collection now writes, and stop reading what it no longer writes.

## Sources of truth (read these, not this summary)

All paths relative to the collection repo above.

| What | Where |
|---|---|
| The tree, every path and its one writer | `contracts/concept_structure.md` (`## The tree` fence, `## Beside the tree`, `## arc42 map`) |
| Why the formats changed | `docs/adr/0016-published-formats-where-one-exists.md` |
| Skills declare their outputs (no `artifacts.yaml` registry) | `docs/adr/0013-a-skill-declares-what-it-produces.md`, `docs/adr/0004-*.md`; each `skills/*/SKILL.md` frontmatter `metadata.artifacts.produces` |
| Glossary at the root, `comparable.md` folded into `brief.md` | `docs/adr/0014-the-glossary-is-a-root-file.md` |
| `APP-DESIGN.md` at the project root | `docs/adr/0015-interaction-decisions-live-in-app-design.md`, `contracts/app_design.md` |
| Brand tokens (DTCG 2025.10) | `contracts/design_tokens.md`, `contracts/schemas/brand-tokens.schema.json` |
| JSON Schemas for machine files | `contracts/schemas/*.schema.json` (scope, onboarding-answers, journeys, datamodel-model, datamodel-seed, trace, frontmatter, brand-tokens) |
| Frontmatter fields incl. `approved:` and the YAML-date rule | `contracts/artifact_frontmatter.md` |
| Interaction verdict (SARIF 2.1.0) | `skills/quality-interaction/references/verdict.md`, `contracts/evaluator.md § SARIF level` |
| API contracts | `skills/architecture-system/SKILL.md` (`openapi.yaml` 3.2, `asyncapi.yaml` 3.1, written only when due) |
| Acceptance ledger and trace | `contracts/acceptance_criteria.md`, `skills/build-implement/SKILL.md` |
| Host facts the collection pins | `scripts/host_facts.py` (+ `scripts/verify_host.py`) |

## What changed, as the host sees it

- `03_brand/tokens.json` → `03_brand/brand.tokens.json` (DTCG: `$type`/`$value`, colour
  objects with `colorSpace`/`components`/`hex`, approval under `$extensions["ai.skaile"]`),
  plus optional `brand.dark.tokens.json` and `brand.resolver.json`. No `tailwind` block.
- `11_build/interaction.yaml` → `11_build/interaction.sarif`.
- `10_blueprint/openapi.yaml`, `10_blueprint/asyncapi.yaml`: new, optional.
- `_concept/glossary.md` at the root; `10_blueprint/glossary.md` and `comparable.md` are gone;
  `10_blueprint/datamodel/feature-map.json` is gone (features list `data_entities[]`).
- `model.json`: `entities[].id` is the PascalCase model name `data_entities[]` uses.
- Build ledger lives under `_concept/11_build/` (`trace.yaml`, `acceptance-criteria/**/*.ac.md`,
  `reviews/<feature_slug>.yaml`), not `_implementation/`.
- `APP-DESIGN.md` at the project root, beside `_concept/`.
- Done-state: a node is done when every `produces` path of its skill exists; conditional files
  are deliberately not listed. The host still reads `contracts/artifacts.yaml`, which no longer
  exists.

## Forge files that touch these (grep on 2026-10-17, not exhaustive)

`server/utils/artifact-contract.ts` (reads `artifacts.yaml`, `produced_by`),
`server/utils/review-coverage.ts` + `server/api/workspaces/[id]/review/coverage.get.ts` +
`app/pages/concept/[id]/review.vue` (`_implementation/`), `shared/schemas/frontmatter.ts`
(`BrandTokens`), `shared/schemas/seed.ts`, `shared/schemas/datamodel.ts`,
`shared/schemas/CONTRACT.md`, `server/utils/grounding.ts` (hardcoded `04_brand`/`05_mockups`),
`docs/api.md`, tests `test/unit/review-coverage.test.ts`, `test/unit/concept-flows-routes.test.ts`,
`tests/e2e/concept-docs.spec.ts`, `tests/e2e/concept-flows.spec.ts`. Treat this as a starting
point and find the rest yourself.

## Constraints

- Code changes happen in `skaile-forge` under its own `CLAUDE.md`, branches and review rules.
- Do not edit the collection repo. When a forge change makes a row in its
  `scripts/host_facts.py` stale, list the row in the plan's hand-back section; the collection
  session updates it.
- Existing projects with the old files are not migrated by the collection. Whether forge reads
  both formats for a transition or cuts over is the plan's decision to make with the user.
