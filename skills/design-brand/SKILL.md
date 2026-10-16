---
name: design-brand
description: "Use when the brief is approved and the project has no visual identity yet, or the user wants to change it. Discovers a direction in plain language, extracts from reference sites, and writes the palette, tokens and brandbook. Triggers on 'brand', 'colors', 'fonts', 'design tokens', 'make it look good'."
version: "0.1.0"
metadata:
  requires:
    - contract:@skaile-ai/shared-contracts
  artifacts:
    requires:
      - { id: brief }
      - { id: research-design-inspiration }
      - { id: grounding-findings }
    produces:
      - { id: brand-identity, path: "_concept/03_brand/identity.md" }
      - { id: brand-tokens, path: "_concept/03_brand/tokens.json" }
      - { id: brand-book, path: "_concept/03_brand/brandbook.html" }
      - { id: grounding-findings, path: "_concept/02_grounding/findings/" }
  prerequisites:
    files:
      - { path: "_concept/brief.md", gate: hard }
      - { path: "_concept/02_grounding/research/design-inspiration.md", gate: soft }
      - { path: "_concept/02_grounding/findings", gate: soft }
    inputs_optional:
      - { id: reference_urls, label: "Reference websites", type: text, hint: "A site you love — the palette and style get extracted from it" }
      - { id: mood, label: "Desired feeling", type: text, hint: "calm, bold, editorial, technical, playful…" }
      - { id: light_dark, label: "Colour mode", type: select, options: [light, dark, both] }
---

# design-brand

Writes `03_brand/` — `identity.md`, `tokens.json` and `brandbook.html`; the reference
screenshots behind them go to `02_grounding/findings/`. Every downstream skill that renders
anything reads `tokens.json`, and both mockup renderers hard-gate on it, so this is the file
the visual half of the project stands on. This skill settles what the product looks like and
how it sounds: `identity.md` is the one home of the tone of voice and the copy guidelines.

Paths are `contracts/concept_structure.md`'s and frontmatter shapes are
`contracts/artifact_frontmatter.md`'s.

## Steps

1. **Read the ground.** `brief.md` for the app, its audience and its comparables;
   `02_grounding/research/design-inspiration.md` and `colors-fonts.md` where research ran;
   `02_grounding/onboarding/answers.json` for an existing brand (`has_brand`) and where its
   files are (`brand_files`). A project that already has a brand gets that brand extracted
   and recorded, not replaced. When `02_grounding/findings/brand.md` exists — the reverse
   flow — seed the draft from it and show each graded value as a proposal: only `extracted`
   values are what the code says, and `inferred` or `needs_review` ones are the user's to
   settle before they reach `tokens.json`.
2. **Discover the direction, one question at a time.** A site whose look they love; the
   feeling the product should give, offered as a spectrum rather than a dropdown; a
   calibration between two opposing examples that both fit this kind of app; light, dark or
   both; and any font they are bound to. Build each question on the last answer.
3. **Extract from any reference URL they give.** Open it, screenshot it into
   `02_grounding/findings/` with a row in `findings/index.md` (source, date, `step:
   design-brand`), and read off the dominant colours, the type pairing, the density,
   the elevation and the corner radius. Then show what you found and ask whether to take it
   as-is, adapt it, or go the other way. A reference URL is the user's taste stated more
   precisely than they can say it, and skipping it throws away the best input in the room.
4. **Propose a whole brand before writing anything** — the aesthetic and why it fits this
   product, each colour with the job it does rather than just its hex, the type choices
   justified against the direction, and the **memorable element**: the one thing that makes
   this app visually unmistakable. A palette of primary blue, grey secondary and Inter is the
   default any project would get, which is exactly why it says nothing about this one.
   Iterate until they approve in words.
5. **Write the three files.** `identity.md` carries the direction, the colour usage rules,
   the type hierarchy, spacing, elevation, atmosphere and the memorable element, a short
   **Tone and copy** section, and — for the approval from step 4 — `approved: <date>` in its
   frontmatter. Tone and copy: how the product speaks (three or four adjectives with what each
   rules out), how it addresses the user, how errors, empty states and buttons read, and words
   it avoids. Take it from the brief and the direction the user approved; ask only when those
   leave the voice open, as one question built on the feeling they chose in step 2.
   `tokens.json` carries the machine-readable form: `colors` (primary, secondary, accent,
   background, surface, text, text_muted, border, error, success, warning), `fonts`,
   `radius`, `mode`, `spacing_base`, `shadows`, `atmosphere`, and a `tailwind` block of CSS
   custom properties — walkthroughs flatten this file into custom properties and storybook
   themes from it, so a missing key becomes a bland default in every rendered screen.
   `brandbook.html` is self-contained (inline CSS, Google Fonts links only, under 50KB) and
   demonstrates the brand rather than listing it: swatches, type in use, spacing, elevation,
   and live button, card, input and nav previews, all drawn with its own tokens.
6. **Report the distinctive choices in a sentence or two** and name what reads the tokens
   next — the feature loop's screen specs, then the walkthrough and storybook.

**Done when** `identity.md`, `tokens.json` and `brandbook.html` exist, the token file carries
every key above, and the user has approved the direction, which `approved:` in `identity.md`
records.
