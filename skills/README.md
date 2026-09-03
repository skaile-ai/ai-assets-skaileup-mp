# skills/

One directory per skill, flat. **The directory name equals the skill's `name:` field,
character for character** — it is also the install path (`.claude/skills/<name>/`), the
flow node's `data.skill`, and the grounding input path
(`_concept/_grounding/<name>/input.json`).

Names are `domain-skill`, two segments by default, three only for a genuine sub-cluster
(`mockup-storybook-components`), never four. Separator is `-`, never `_`.

Start from [`../docs/skill-template.md`](../docs/skill-template.md).
