---
name: experience-shell
description: "Use when the featuresets are settled and the app needs its frame before individual screens are specified — navigation, layout areas, breakpoints, and the patterns every screen reuses. Triggers on 'app shell', 'navigation structure', 'what does the layout look like', 'design the frame'."
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
  prerequisites:
    files:
      - { path: "_concept/brief.md", gate: hard }
      - { path: "_concept/05_features", gate: hard, min_entries: 1 }
      - { path: "_concept/04_journeys/stories.yaml", gate: soft }
      - { path: "_concept/03_brand/tokens.json", gate: soft }
---

# experience-shell

Writes exactly one file: `07_screens/shell.md`, the frame every screen appears inside —
navigation, layout areas, breakpoints, and the conventions screens are not each meant to
re-decide. `spec-feature` is the sole writer of individual screen specs and of the rest of
`07_screens/`; this skill never writes one, and `shell` is a reserved slug there.

Paths are `contracts/concept_structure.md`'s, the frontmatter shape is
`contracts/artifact_frontmatter.md`'s, and the `elements:` block is
`contracts/elements_block.md`'s — with the app-shell nav case owned by
`contracts/walkthrough_renderer.md`.

## Steps

1. **Read what the app is for and how it is grouped.** `brief.md` for the hero flow,
   `05_features/featuresets.md` for the featuresets and their features, `04_journeys/`
   for the order users move through them, and `03_brand/tokens.json` for the palette,
   type scale and spacing the frame is drawn in. Reference brand values by name; a hex
   invented here diverges from the tokens the renderers actually use.
2. **Decide the navigation from the featuresets, not from the screens.** Screens do not
   exist yet — the feature loop writes them after this — so the destinations are the ones a
   featureset will need, named as the screen ids they will get. Journey stage decides
   prominence: the hero and vital journeys earn primary navigation, hygiene flows sit behind
   a settings or admin entry. A nav with one item per feature is a menu of the file system
   rather than of the product.
3. **Describe the layout areas** — header, primary navigation, content region, and anything
   persistent beside them — as what each holds and what stays put while the content changes.
   A short ASCII sketch of the areas carries this faster than three paragraphs.
4. **Settle the responsive behaviour**: the breakpoints, and what the navigation becomes
   below each one. This is decided once, here, or it gets decided differently on every screen.
5. **Write the shared patterns** every screen reuses: how a page header is composed, where
   breadcrumbs go, what an empty state, a loading state and an error look like, where
   confirmations and destructive actions surface. Each of these is a decision a feature spec
   would otherwise make alone, and inconsistently.
6. **Mirror the navigation into the `elements:` block.** `shell.md`'s own frontmatter carries
   a `kind: nav` element whose `items[]` are the destinations from step 2, in the same order,
   each with its `target`. The walkthrough renderers treat that block as authoritative for
   the app nav and derive one per rendered screen when it is absent — so an unmirrored
   `## Navigation` section renders as a nav the user never designed. A target naming a screen
   the feature loop has not written yet resolves to nothing and is reported as an unresolved
   target rather than a failure; it resolves once that screen is specified.
7. **Show the frame to the user in their terms** — where things live, what is always on
   screen, what happens on a phone — and iterate until they approve. Then point at the
   feature loop: `spec-feature` writes every screen inside this frame.

**Done when** `07_screens/shell.md` exists with its navigation, layout areas, breakpoints and
shared patterns, and its `elements:` nav block lists the same destinations as its
`## Navigation` section, in the same order.
