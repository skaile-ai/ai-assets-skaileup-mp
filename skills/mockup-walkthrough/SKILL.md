---
name: mockup-walkthrough
description: "Use when stakeholders need a clickable walkthrough of the application — one page per screen and per journey, openable in a browser, plus the manifest.json mockup-annotate reads. Renders zero-build static HTML or a built Astro site; the renderer comes from the project, not from you."
version: "0.1.0"
metadata:
  requires:
    - contract:@skaile-ai/shared-contracts
  artifacts:
    requires:
      - { id: screens }
      - { id: journeys }
      - { id: brand-tokens }
      - { id: features }
  prerequisites:
    files:
      - { path: "_concept/07_screens", gate: hard, min_entries: 1 }
      - { path: "_concept/04_journeys/stories.yaml", gate: hard }
      - { path: "_concept/03_brand/tokens.json", gate: hard }
      - { path: "_concept/05_features", gate: soft, min_entries: 1 }
---

# mockup-walkthrough

Turns screen specs, journeys and brand tokens into a clickable site at
`_concept/09_mockup/walkthrough/<renderer>/` — `index.html`, one page per screen, one per
journey, and a `manifest.json`. Every rendered node carries `data-spec-*` attributes so a
stakeholder's click resolves back to the artifact that produced it. This skill stops at the
built site; instrumenting it for comments is `mockup-annotate`.

`contracts/walkthrough_renderer.md` owns everything the two renderers share: the
`data-spec-*` attributes, `kind` → DOM tag mapping, target resolution, app-shell nav,
auto-slug fallback, `items[]` id derivation, the spec reference panel, the manifest schema
and field semantics, the `warnings[].kind` enum, and error handling. Read it — the steps
below sequence it and never restate it.

## Steps

1. **Resolve the renderer, once, before anything else.** `02_grounding/onboarding/onboarding.yaml`
   key `mockup.renderer` wins when set (`static-html` | `astro`). Absent, the flow in
   `01_meta/scope.yaml` decides: `appbuilder-mvp` gets **static-html**, `appbuilder-standard`
   and `skaileup-concept-only` get **astro**. The answer names both the
   output root `_concept/09_mockup/walkthrough/<renderer>/` and the reference directory you work
   from — read `references/<renderer>/RENDERER.md` now; it carries the render steps this one
   only outlines. A flow the table does not list is a project that has not been scoped: say so
   and stop, rather than guessing a renderer whose output the annotator may not find.
2. **Preserve intent.** If `_concept/09_mockup/feedback/devlog.md` exists, read it. Each session block
   lists the screen and feature files it touched under `### <file>` headers, with one applied
   line per patch. Treat every applied line for a file you are about to render as a constraint:
   a stakeholder already asked for that change and a regeneration that quietly reverts it reads
   as the tool ignoring the feedback round.
3. **Read the inputs and build one in-memory model.** Glob `07_screens/*/*.md`
   — one level, so the root `shell.md` is not a screen — sorted by path, and **build the set of rendered screen ids before
   resolving any `target`** — resolution then never depends on parse order. Resolve every
   `target` / `row_target` / `items[].target` against that set; unresolved means `href: null`
   plus an `unresolved_target` warning, never a hard failure. Auto-slug what `elements:` leaves
   uncovered and derive ids for id-less `items[]`, both per the contract. Build the app nav —
   shell-authoritative when `07_screens/shell.md` declares a `kind: nav` element with items,
   derived per rendered screen otherwise. Flatten `03_brand/tokens.json` into `--token-<dotted-path>`
   custom properties. Read `04_journeys/stories.yaml`; a journey without a
   `screen_sequence` gets a `missing_screen_sequence` warning and is skipped. Glob
   `05_features/*/*.md` for manifest traceability only — one level again, because
   `05_features/featuresets.md` is the roster, not a feature. They are never rendered, and
   their absence costs the manifest its feature links rather than stopping the render.
   Element-schema validation is authoring-time work; handle render-time semantics only, and
   let a screen file with malformed YAML stop the run naming the file rather than shipping a
   half-rendered site.
4. **Render**, following `references/<renderer>/RENDERER.md`. Escape every label, id,
   `screen_path` and `journey_id` before it reaches the document — frontmatter is authored
   prose and will contain quotes and angle brackets. Never write back into
   `07_screens/`: promoting a provisional id is `mockup-feedback`'s job, and a renderer
   that edits its own inputs makes the next render unreproducible.
5. **Write `manifest.json`** from the in-memory model. Element `target` / `row_target` /
   `items[].target` echo the **declared** `screen_id[#fragment]` verbatim — only `app_nav[].target`
   carries a resolved value, because the annotator resolves declared targets itself and a
   pre-resolved one hides which screen the author actually named. Sort `screens[]` by
   `screen_path`, `journeys[]` by `journey_id`, `features[]` by `feature_path`; leave `app_nav[]`
   in rendered order. Write atomically (tmp → fsync → rename). Set `renderer` to
   `mockup-walkthrough-<renderer>` and `renderer_version` to this file's `version`.
6. **Validate**: `python skills/mockup-walkthrough/references/<renderer>/validator.py
   _concept/09_mockup/walkthrough/<renderer>` from the repo root. Exit 0 is ready for
   `mockup-annotate`; exit 2 prints the violations as `<file>:<line>: <message>`.

## What sits in `references/`

- **`<renderer>/RENDERER.md`** — the render steps that renderer alone performs, and the
  handful of places it reads the shared contract differently.
- **`astro/scaffold/`** — the seven real files the astro renderer copies at init, plus
  `astro/specs-json.md`, the shape of the pre-resolved data the templates read.
- **`<renderer>/validator.py`** — step 6's check, and the executable statement of what the
  contract requires of output.
- **`<renderer>/tests/`** — a fixture project and a hand-curated expected snapshot for that
  validator. Worth reading when a contract rule is ambiguous: the snapshot is what correct
  output looks like.

**Done when** the validator exits 0 and `manifest.json` names every screen under
`07_screens/` and every journey in `stories.yaml`.
