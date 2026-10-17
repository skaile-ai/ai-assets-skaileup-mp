---
name: experience-shell
description: "Use when the screens are specified (or, on an existing codebase, recorded in the findings) and the app needs its frame — navigation, layout areas, breakpoints, and the patterns every screen reuses. Triggers on 'app shell', 'navigation structure', 'what does the layout look like', 'design the frame'."
version: "0.1.0"
metadata:
  requires:
    - contract:@skaile-ai/shared-contracts
  artifacts:
    requires:
      - { id: brief }
      - { id: featuresets }
      - { id: journeys }
      - { id: brand-tokens }
      - { id: screens }
      - { id: grounding-findings }
      - { id: app-design }
    produces:
      - { id: app-shell, path: "_concept/07_screens/shell.md" }
  prerequisites:
    files:
      - { path: "_concept/brief.md", gate: hard }
      - { path: "_concept/05_features", gate: hard, min_entries: 1 }
      - { path: "_concept/07_screens", gate: soft, min_entries: 1 }
      - { path: "_concept/02_grounding/findings", gate: soft }
      - { path: "_concept/04_journeys/stories.yaml", gate: soft }
      - { path: "_concept/03_brand/tokens.json", gate: soft }
      - { path: "APP-DESIGN.md", gate: soft }
---

# experience-shell

Writes exactly one file: `07_screens/shell.md`, the frame every screen appears inside —
navigation, layout areas, breakpoints, and the conventions screens are not each meant to
re-decide. It runs after the feature loop, so the frame is drawn around screens that exist;
in the reverse flow, where it runs before `spec-feature`, it is drawn around the screens the
codebase already has. `spec-feature` is the sole writer of individual screen specs and of the
rest of `07_screens/`; this skill never writes one, and `shell` is a reserved slug there.

Paths are `contracts/concept_structure.md § The tree`; the frontmatter shape is
`contracts/artifact_frontmatter.md § 07_screens/shell.md`.

## Steps

1. **Read what the app is for and where its screens are.** `brief.md` for the hero flow,
   `05_features/featuresets.md` for the featuresets and their features, `04_journeys/`
   for the order users move through them, and `03_brand/tokens.json` for the palette,
   type scale and spacing the frame is drawn in. Reference brand values by name; a hex
   invented here diverges from the tokens the renderers actually use. The screens come from
   `07_screens/<feature_slug>/*.md` — each file's `id` and title are a candidate nav
   destination. Where `07_screens/` holds none (the reverse flow runs this skill first), take
   them from the screens recorded in `02_grounding/findings/` (`screens.md`), and say in `shell.md` which
   source each destination came from. With neither, stop and name the missing step —
   `spec-feature` or `concept-reverse` — because a nav drawn without screens behind it is
   a nav invented here.
2. **Derive the navigation from those screens.** Every destination is a screen a spec or a
   finding names, under the screen id it already has; a destination nothing backs is dropped
   rather than added. Where `APP-DESIGN.md` exists, derive under its § Navigation (P12,
   `contracts/interaction_patterns.md § Finding and doing`): primary navigation lists core
   objects and the few workspaces its entries name, supporting objects sit behind their
   parent. Without it, group by featureset and let the journey stage (`stories.yaml §
   stages`) decide prominence: the hero and vital journeys earn primary navigation, hygiene
   flows sit behind a settings or admin entry. A nav with one item per screen is a menu of
   the file system rather than of the product.
3. **Describe the layout areas** — header, primary navigation, content region, and anything
   persistent beside them — as what each holds and what stays put while the content changes.
   A short ASCII sketch of the areas carries this faster than three paragraphs.
4. **Settle the responsive behaviour**: the breakpoints, and what the navigation becomes
   below each one. This is decided once, here, or it gets decided differently on every screen.
5. **Write the shared patterns** every screen reuses, as layout only: how a page header is
   composed, where breadcrumbs go, which regions persist and what the content region shows
   while loading. Empty, error, confirmation, message and editing patterns come from the
   `APP-DESIGN.md` MSG, EDIT and MOD entries, cited by id, never decided here. Without the
   file, record them as proposals under `## Proposed interaction patterns` and hand them to
   `experience-interaction` — a pattern this skill settles alone is the one every feature
   spec would otherwise make inconsistently.
6. **Mirror the navigation into the `elements:` block**: `shell.md`'s own frontmatter carries
   a `kind: nav` element whose `items[]` are the destinations from step 2, in the same
   order, each with its `target`. The block is written to `contracts/elements_block.md §
   Schema` with `items[]` shaped per `§ Content fidelity`, and the renderers treat it as the
   app nav per `contracts/walkthrough_renderer.md § App-shell navigation` — an unmirrored
   `## Navigation` section renders as a nav the user never designed. A target taken from the
   findings resolves once `spec-feature` writes that screen under the same id; until then it
   is reported as an unresolved target rather than a failure.
7. **Show the frame to the user in their terms** — where things live, what is always on
   screen, what happens on a phone — and iterate until they approve. Then point at the next
   step: `spec-feature` in the reverse flow, where it writes every screen inside this frame,
   and the walkthrough otherwise.

**Done when** `07_screens/shell.md` exists with its navigation, layout areas, breakpoints and
shared patterns, and its `elements:` nav block lists the same destinations as its
`## Navigation` section, in the same order.
