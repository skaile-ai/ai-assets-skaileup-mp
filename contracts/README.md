# contracts/

The shared reference layer. A contract is here because a skill **reads it at a step in
its body** — naming a file is a citation, not a reading, and citations do not earn a
contract. Nothing here is invocable.

Thirteen files. The old collection had twenty-eight; the difference is almost entirely
documents that described the collection to itself.

| File | What reads it, and for what |
|---|---|
| `concept_structure.md` | Every skill that writes an artifact — the canonical `_concept/` tree. The only place the tree is stated; `scripts/check.py` parses this file's fenced block to decide whether a declared path exists |
| `artifact_frontmatter.md` | Every skill that writes a `_concept/` markdown file — the YAML fields per artifact type |
| `elements_block.md` | `spec-feature` writes the `elements:` block; both walkthrough renderers consume it |
| `walkthrough_renderer.md` | `mockup-walkthrough` (both renderers) and `mockup-annotate` — `data-spec-*` attributes, `kind` → DOM mapping, target resolution, `items[]` id derivation, the manifest schema |
| `feedback_loop.md` | `mockup-feedback` — the cross-reference protocol between features, screens and the data model |
| `slice_loop.md` | `spec-feature`, `build-plan`, `build-implement` — the dossier slug rule and the freeze lifecycle |
| `acceptance_criteria.md` | `spec-feature` (the EARS grammar), `build-plan` (creates the ledger), `build-implement` and `quality-e2e` (flip its rows), `quality-review` and `ops-review` (read it) — the criterion form and the ledger's row shape |
| `domain_model.md` | Any skill that pins a term or records a decision — glossary format, the ADR format, and the three-test gate that decides whether a decision is worth recording |
| `semantic_types.md` | The data-model skills — stack-independent types and the translation table |
| `seed_data.md` | The data-model skills — scenario-based seed conventions. Also the stack-neutral half of seeding: every template's `## Seed` section cites it for the scenario set and carries only the per-ORM layout |
| `golden_principles.md` | `architecture-datamodel` (entity, field and enum naming), `experience-behaviors` (the same names, one step earlier) and `ops-review` (checks artifacts against them) — the mechanical rules for `_concept/` artifacts. Kept on notice through ADR 0008 for want of a reader; the datamodel writer and the `ops` audit skill both arrived, so it is off notice |
| `agent_patterns.md` | Any skill that dispatches a subagent — dispatch shape, standalone mode, research mode |
| `evaluator.md` | `quality-review`, `quality-release` and `ops-review` — the shared adversarial stance, the four-level severity with its blocking boundary, and the three-tier verdict grammar the three verdict artifacts share |

## What is not here

**No `scripts/`.** The collection's own self-check lives at `scripts/check.py` in the
repo root, because it checks the whole repo and not just this folder. The per-skill
`validator.py` files are steps of their skills and ship inside
`skills/<name>/references/`, not here.

**No `flow.schema.json`.** The flow contract is enforced by `scripts/check.py` directly.
A JSON Schema could express roughly half the rules that matter and none of the ones that
bite — the sharpest is that an edge without `type: flow` orders nothing, which is a
graph property, not a shape. It also encoded three constructs no engine implements.

**No `preview_compatibility.md`.** It lives in `templates/`, beside its readers. Ticket 09
provisionally folded it into `walkthrough_renderer.md`; that fold never happened and was wrong —
its seven readers are the `## Preview Compatibility` sections of `templates/template-*/TEMPLATE.md`,
and none of them is in the mockup domain or is a skill at all. Reference data read by reference
data does not meet this folder's bar, so it sits with the templates instead (ADR 0009).

**No registry.** Machine-read data lives in each skill's own `SKILL.md` frontmatter,
resolved through its `name:`, because that is where the host already reliably looks.

**No `DOMAIN.md`, no grammar, no skill template.** Domain foldering is gone; the DSL is
gone; the skill template is documentation and lives in `docs/`.
