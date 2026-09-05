# Detection — the brand

Read in this order; a later source refines what an earlier one already established rather
than replacing it.

1. `tailwind.config.{ts,js,mjs}` — `theme.extend.colors`, `fontFamily`, `borderRadius`,
   and the `darkMode` strategy
2. CSS custom-property files — `tokens.css`, `variables.css`, `globals.css`,
   `app.css`; the `:root` and `.dark` blocks
3. Design-token files — `tokens.json`, `design-tokens.json`, a `style-dictionary/` tree
4. Theme providers — `ThemeProvider.tsx`, `theme.ts`, a Chakra or Mantine theme object
5. Framework theme config — `nuxt.config.ts` `ui.colors`, a Vuetify theme block
6. The root layout or `app.vue` for global styles, the loaded fonts and the body classes

## What to extract

**Colours** — primary, secondary, accent, background, surface, text, muted text, border, and
the semantic set (success, warning, error). A palette expressed as a scale (`50`…`900`) gives
its `500` or its most-used step as the token value, with the scale noted in the body.

**Typography** — the heading, body and mono families, and the type scale where one is
defined. Fonts loaded in the layout count even when the config does not name them.

**Radius, spacing and elevation** — the default corner radius and the spacing unit tell you
the design language (sharp, moderate, rounded, pill) more reliably than any prose in the repo.

**Mode** — `light`, `dark` or `both`, from the `darkMode` strategy and whether a `.dark`
block actually defines values.

## Grading, and the empty case

A hex read from a config is `extracted`. A colour derived from usage frequency across
components is `inferred`, and worth saying so. A repository with no theme layer at all gets
`tokens.json` written with empty values and `needs_review` throughout — the file exists
because the walkthrough and storybook renderers hard-gate on it, and a skeleton they can
report against beats an absence they stop on. A palette assembled from taste, when the
repository declares none, is the one output of this dimension that is worse than nothing:
it is indistinguishable from a real one and it will be built against.
