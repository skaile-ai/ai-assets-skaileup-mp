---
name: mockup-storybook
description: "Use when screen specs are approved and stakeholders want a living component library — Storybook stories for custom components, full-page screen compositions, and clickable journey walkthroughs. Framework-agnostic: the addon, story format and component library come from the project's template."
version: "0.1.0"
metadata:
  artifacts:
    requires:
      - { id: screens }
      - { id: brand-tokens }
      - { id: techstack }
      - { id: journeys }
      - { id: datamodel }
  prerequisites:
    files:
      - { path: "_concept/07_screens", gate: hard, min_entries: 1 }
      - { path: "_concept/03_brand/tokens.json", gate: hard }
      - { path: "_concept/10_blueprint/techstack.md", gate: hard }
      - { path: "_concept/04_journeys/stories.yaml", gate: soft, min_entries: 1 }
---

# mockup-storybook

Builds a standalone Storybook at `_concept/09_mockup/storybook/` in three layers: custom
components, full-page screen compositions, and one clickable click-dummy per user journey.
This is a concept artifact — a surface for reviewing the design before the app exists. An
app that wants its own Storybook gets it as ordinary build work behind the template's
`## Storybook Config`; the two never share a directory.

Nothing here is framework-specific except the values step 1 resolves. Directory layout, story
titles, variant names and the page manifest are the same on every stack —
`references/story-conventions.md` holds them, and steps 3–5 assume you have read it.

## Steps

1. **Resolve the stack and read its atoms by name.** `10_blueprint/techstack.md` names
   `tech_stack_skill`; `templates/<that id>/TEMPLATE.md` carries `storybook_addon`,
   `story_format`, `story_extension`, `component_import`, `component_library`, `icon_library`
   and `package_manager` under `metadata.atoms`. Every template declares every atom with a
   value or an explicit `null`, and a `null` is the answer rather than a missing one:
   `component_library: null` means the stack ships none, so step 3's split puts every element
   on the custom side, and `icon_library: null` means inline the SVGs. Confirm the set with the
   user before scaffolding — a wrong addon is discovered at the end of step 6, after every story
   has been written against it. Carry them as the only stack-shaped values in the run; every
   later step names an atom rather than a framework.
2. **Scaffold, when `_concept/09_mockup/storybook/package.json` is absent.** Write the project
   files listed in `references/scaffold.md` — `package.json` on the resolved addon,
   `.storybook/main`, `theme` and `preview`, and `src/styles/brand.css` — then install with
   the resolved package manager and confirm `run build` passes before writing a single story.
   Every colour, font, radius and spacing value comes from `03_brand/tokens.json` and
   viewport presets come from `07_screens/shell.md`: a hardcoded breakpoint
   or an invented colour makes the prototype disagree with the brand it exists to show.
   Present already? Leave it alone and go to step 3 — the scaffold is the user's by then.
3. **Build the components layer.** Read every screen spec's `UI Elements` section and take the
   deduplicated union. Split it against what the component library actually exports — read the
   installed package's type declarations rather than guessing — into *library* elements, which
   pages import directly and which get no story, and *custom* elements, which you build. Show
   both lists and confirm the split before building. For each custom element write the
   component under `src/components/`, a minimal interface under `src/@types/` covering only the
   properties it renders, and a story under `src/stories/Components/`. Where
   `10_blueprint/datamodel/seed.json` exists, source the `WithData` and `Empty` variants from its
   `populated` and `empty` scenarios, so the stories and the tests later share one fixture.
   Finish with the `src/components/index` barrel — step 4 imports from it, and an empty barrel
   with a comment is the right output when the library covered everything.
4. **Build the pages layer.** `AppShell` first, from `07_screens/shell.md`, with its nav items
   derived from the shell spec: it is the frame every page renders inside, so a page built
   before it gets composed twice. Then one page component and one story per screen spec, with
   a named variant for every state the spec lists and `Mobile` / `Tablet` variants alongside.
   Close with `src/pages/manifest.json` mapping each screen spec path to its component and
   route — step 5 reads it to turn a journey's `candidate_screens` into imports.
5. **Build the journeys layer**, when `04_journeys/stories.yaml` exists. One story per
   `hero`, `vital` and `hygiene` story map — `backlog` maps are out of scope by stage, and
   there is exactly one hero. Each is a single interactive story that renders the AppShell and
   swaps the page component as the reader clicks: navigation happens through the real nav
   items and the real action buttons, never through added Prev/Next controls, because a
   walkthrough with its own navigation is not evidence that the design's navigation works.
   Carry a banner with the persona and `Step N of M`, and highlight the elements that do
   advance when the reader clicks one that does not. Mark the hero flow as the default story.
   No `stories.yaml`? Note the skipped layer in the project README naming what to run.
6. **Verify.** `run build` from the storybook directory, then count the story files per layer
   and report the three counts with the command that opens the result. A build that fails here
   is fixed here — a Storybook nobody can start is not reviewable.

## What sits in `references/`

- **`scaffold.md`** — the project files step 2 writes, with the token keys each one reads.
- **`story-conventions.md`** — directory layout, story titles, the named variants per layer,
  the `pages/manifest.json` shape, and the click-dummy pattern.

**Done when** `run build` passes and every screen spec has a page story, every custom
component has a component story, and every non-backlog story map has a journey story.
