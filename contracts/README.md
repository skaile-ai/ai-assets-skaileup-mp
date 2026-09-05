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
| `acceptance_criteria.md` | `build-plan` and `build-implement` — the EARS grammar and the ledger's shape |
| `domain_model.md` | Any skill that pins a term or records a decision — glossary format, the ADR format, and the three-test gate that decides whether a decision is worth recording |
| `semantic_types.md` | The data-model skills — stack-independent types and the translation table |
| `seed_data.md` | The data-model skills — scenario-based seed conventions |
| `golden_principles.md` | The mechanical rules for `_concept/` artifacts: entity naming, enums, cross-references |
| `iron_laws.md` | The gates that decide whether a skill may run at all, expressed in each skill's `prerequisites.files[].gate` |
| `agent_patterns.md` | Any skill that dispatches a subagent — dispatch shape, standalone mode, research mode |
| `evaluator.md` | The shared stance and deduction mechanics every evaluator skill cites. **No reader in this repo yet** — the `quality` and `ops` skills that read it are not written; it is kept against them, and dies with them if they do not arrive |

## What is not here

**No `scripts/`.** The collection's own self-check lives at `scripts/check.py` in the
repo root, because it checks the whole repo and not just this folder. The per-skill
`validator.py` files are steps of their skills and ship inside
`skills/<name>/references/`, not here.

**No `flow.schema.json`.** The flow contract is enforced by `scripts/check.py` directly.
A JSON Schema could express roughly half the rules that matter and none of the ones that
bite — the sharpest is that an edge without `type: flow` orders nothing, which is a
graph property, not a shape. It also encoded three constructs no engine implements.

**No registry.** Machine-read data lives in each skill's own `SKILL.md` frontmatter,
resolved through its `name:`, because that is where the host already reliably looks.

**No `DOMAIN.md`, no grammar, no skill template.** Domain foldering is gone; the DSL is
gone; the skill template is documentation and lives in `docs/`.
