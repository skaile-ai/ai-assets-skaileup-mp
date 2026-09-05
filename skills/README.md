# skills/

One directory per skill, flat. **The directory name equals the skill's `name:` field,
character for character** — it is also the install path (`.claude/skills/<name>/`), the
flow node's `data.skill`, and the directory the host names a skill's input-dialog file
after. That last path is still hardcoded under a `_grounding/` ADR 0007 abolished; it is
the host's on both ends, so no skill body names it and nothing here breaks.

Names are `domain-skill`, two segments by default, three only for a genuine sub-cluster
(`mockup-storybook-components`), never four. Separator is `-`, never `_`.

Start from [`../docs/skill-template.md`](../docs/skill-template.md).
