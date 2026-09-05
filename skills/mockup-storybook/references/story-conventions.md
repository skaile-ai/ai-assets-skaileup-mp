# Story conventions

Identical on every stack. Only the file extension moves, and it is `story_extension` from
step 1.

## Directory layout

```
_concept/09_mockup/storybook/
├── package.json
├── .storybook/{main,theme,preview}.<ts|js>
└── src/
    ├── styles/brand.css
    ├── @types/{README.md, <entity>.<ts|js>, index.<ts|js>}
    ├── components/{AppShell.<ext>, <ComponentName>.<ext>, index.<ts|js>}
    ├── pages/{<Group>/<PageName>.<ext>, manifest.json}
    └── stories/
        ├── Components/<ComponentName>.stories.<ext>
        ├── Pages/00 Layout/AppShell.stories.<ext>
        ├── Pages/<NN Group>/<PageName>.stories.<ext>
        └── Journeys/{Hero,Vital,Hygiene}/<FlowName>.stories.<ext>
```

`AppShell` lives in `components/`, not `pages/` — pages render inside it, so it is a
building block that happens to be page-shaped.

## Group naming

A screen spec's directory segment carries both a sort key and a label:
`01_user_auth` → prefix `01`, label `User Auth`. Page components go to
`src/pages/01_user_auth/`; their stories go to `src/stories/Pages/01 User Auth/` (space, not
underscore — Storybook renders the folder name in the sidebar).

## Story titles

| Layer | Title |
|---|---|
| Components | `Components/<ComponentName>` |
| App shell | `Pages/00 Layout/AppShell` |
| Pages | `Pages/<NN> <GroupName>/<PageName>` |
| Journeys | `Journeys/<Stage>/<JourneyLabel>` |

Component stories carry the `autodocs` tag. Page and journey stories set
`layout: 'fullscreen'`.

## Named variants

| Layer | Exports |
|---|---|
| Component | `Default`, `AllVariants`, plus `WithData` / `Empty` / `Loading` where the component supports them |
| AppShell | `DesktopExpanded`, `DesktopCollapsed`, `Mobile` |
| Page | one per state the screen spec lists (`Default`, `Populated`, `Empty`, `Loading`, `Error`, …), plus `Mobile` and `Tablet` |
| Journey | a single `Interactive` story |

A component that appears in several screens with different configurations gets one variant
per configuration.

Story data is realistic and domain-appropriate — drawn from `seed.json` scenarios where a
data model exists, from the screen spec's own examples otherwise. Lorem ipsum in a
stakeholder review reads as an unfinished screen rather than a filled one, and hides the
layout questions the review exists to answer.

## `src/pages/manifest.json`

One entry per screen spec, keyed by the spec's path relative to `_concept/`:

```json
{
  "07_screens/01_user_auth/login.md": {
    "component": "01_user_auth/Login",
    "import": "./src/pages/01_user_auth/Login",
    "route": "/login"
  }
}
```

The journeys layer resolves each story map's `candidate_screens` through this file; a screen
missing from it falls back to matching on route or purpose against the screen specs.

## The click-dummy pattern

One `Interactive` story per journey, built only from existing page components and `AppShell`:

- Track the current step in framework-local reactive state; render the matching page
  component as AppShell's content.
- Wire the advance on **real** UI: a nav item, an action button, a link the screen spec
  already declares. The journey is testing whether the design's own affordances carry a
  person through the flow, so an added Prev/Next control would answer the wrong question.
- Highlight the active nav item for the current step, and show a small banner with the
  persona name, `Step N of M`, and the step description.
- When the reader clicks something that does not advance, add a `click-hint` class to the
  elements that do and drop it again after about three seconds — a dead click with no
  feedback reads as a broken prototype rather than a wrong guess.
- Let the data reflect progression: after a "create project" step, the next screen shows
  that project.
- Reuse the interfaces in `src/@types/`; keep per-step data inline in the story file.
