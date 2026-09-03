---
name: mockup-walkthrough-astro
description: "Use when stakeholders need a clickable Astro walkthrough of the application — built static site, Tailwind-styled, openable directly in a browser. Generates one HTML file per screen and per journey, plus a manifest.json that the mockup-feedback cluster reads. Best for appbuilder-standard tier."
version: "0.2.0"
artifacts:
  requires:
    - { id: screens, gate: hard }
    - { id: journeys, gate: hard }
    - { id: brand-tokens, gate: hard }
    - { id: features, gate: soft }
  produces: [walkthrough]
prerequisites:
  files:
    - { path: "experience/screens", gate: hard, min_entries: 1 }
    - { path: "experience/journeys/stories.yaml", gate: hard }
    - { path: "design/tokens.json", gate: hard }
    - { path: "experience/features", gate: soft, min_entries: 1 }
---

# mockup-walkthrough-astro

One of the walkthrough renderers. Same four inputs and the same `manifest.json` as every
other renderer; the output is a built Astro site at `_concept/mockup-walkthrough/astro/`,
Tailwind-styled from the brand tokens, one HTML file per screen and per journey.

`contracts/walkthrough_renderer.md` (schema_version 1.2) is the source of truth for
everything shared: the `data-spec-*` attributes, `kind` → DOM tag mapping, target
resolution, auto-slug fallback, the spec reference panel, the manifest schema and field
semantics, the `warnings[].kind` enum, and error handling. Read it; this file covers only
what Astro does differently.

## What is different about Astro

The `.astro` templates are scaffolded **once**, at init, and then belong to the user. They
run at build time, long after the agent that could resolve a target or derive an auto-slug
id has finished. So this renderer resolves everything up front and hands the templates a
fully-resolved `src/data/specs.json`: the template interpolates `el.href ?? '#'` and never
derives anything itself. Every other renderer may resolve at render time because its
templates run then too.

Three consequences, all Astro-only:

- **Hrefs are root-relative and extension-less** (`/screen/<group>/<name>`, `/journey/<id>`,
  `/`), not static-html's `../<group>/<name>.html`. The build emits real `.html` files
  (`build.format: 'file'`), but the served URL is the clean form.
- **`provisional: true` sits on the element object**, and on every normalised `items[]`
  entry, rather than in a separate top-level `auto_slugged[]` array. The `auto_slugged`
  warning entry is still required.
- **`items[]` ids are derived once, here.** An id-less `nav`/`tabs`/`list` item is the
  normal case: derive its id with the contract's kebab-slug algorithm scoped to that
  element's own `items[]`, set `element_id` and `provisional: true`, and add one
  `auto_slugged` warning per item. An explicit `id:` is used verbatim, `provisional: false`.

## Steps

1. **Preserved intent.** If `_concept/_feedback/devlog.md` exists, read the entries whose
   `target_paths` touch this project and treat each `patch_summary` as a constraint that
   regeneration must not undo.
2. **Read inputs and build the in-memory model**, applying the shared contract's rules —
   parse the screens, build the rendered-screen-id set *before* resolving any target so
   resolution never depends on parse order, resolve every `target` / `row_target` /
   `items[].target` into an `href` (unresolved → `href: null` plus an `unresolved_target`
   warning), auto-slug what `elements:` leaves uncovered, build the app nav (shell-
   authoritative if `00_layout/shell.md` declares a `kind: nav` element with items,
   otherwise derived per rendered screen), flatten `design/tokens.json` into
   `--token-<dotted-path>` vars, and render each screen's spec-panel `body_html`.
   Element-schema validation belongs to `lab/validate-elements-block` at authoring time;
   handle render-time semantics only.
3. **Detect the mode.** `astro.config.mjs` absent → **init**: copy `references/scaffold/`
   into the project and run `bun install`. Present → **update**: the scaffold is the user's,
   so leave `astro.config.mjs`, `tailwind.config.mjs` and every `.astro` file untouched, and
   check for staleness — if `src/pages/screen/[...slug].astro` lacks the literal `el.href`
   or `spec-panel`, record a `stale_scaffold` warning naming the fix (delete the scaffold to
   regenerate, or port the template changes by hand). Run the check before regenerating, so
   the warning describes the scaffold as it stood at the start of the run. It is a warning,
   not a failure; the build proceeds and ships whatever the stale template renders.
4. **Write `src/data/specs.json` and `src/styles/global.css`** on every run, overwriting.
   Shape and the `specs.json` → `manifest.json` projection: `references/specs-json.md`.
   `global.css` is the Tailwind base plus one `--token-*` line per flattened token. On
   update runs, compare the token count against the CSS var count in the existing file
   first; a mismatch means `tailwind.config.mjs` needs a hand edit — record
   `stale_tailwind_config`.
5. **Build** with `bun run build` from the project root. On non-zero exit, print the full
   stderr, stop, and leave `manifest.json` alone.
6. **Write `manifest.json`** from the in-memory model, not by serialising `specs.json` —
   the two shapes differ, and `references/specs-json.md` lists the template-only fields the
   manifest must not carry. Element `target` / `row_target` / `items[].target` echo the
   **declared** `screen_id[#fragment]` verbatim; only `app_nav[].target` carries a resolved
   value, per the contract's field semantics. Sort `screens[]` by `screen_path`,
   `journeys[]` by `journey_id`, `features[]` by `feature_path`; leave `app_nav[]` in
   rendered order. Write atomically (tmp → fsync → rename). Set
   `renderer: "mockup-walkthrough-astro"` and `renderer_version:` to this file's `version`.
7. **Validate**: `python mockup-walkthrough/astro/validator.py _concept/mockup-walkthrough/astro`
   from the repo root. Exit 0 is ready; exit 2 prints the violations.

## The Astro config is load-bearing

`outDir: '.'`, `emptyOutDir: false`, `build.format: 'file'`, and `getStaticPaths()` slugs
without trailing slashes. These four together are what put the built HTML where the feedback
cluster expects it and keep the previous build's files alive. A `dist/` directory appearing
under the project root means `outDir` drifted: fail with that message rather than shipping a
walkthrough the annotator cannot find. `references/scaffold/astro.config.mjs` already
encodes all four — copy it rather than writing one.

Two failures are worth stopping for: `bun install` and `bun run build` exiting non-zero.
Everything else in the shared `warnings[].kind` enum is soft — render the node, record the
warning, keep going — plus this renderer's own `stale_scaffold` and `stale_tailwind_config`.

**Done when** the validator exits 0 and `manifest.json` names every screen in
`experience/screens/` and every journey in `stories.yaml`.
