---
name: build-scaffold
description: "Use when the stack is chosen and no project exists yet — runs the template's scaffold recipe, then themes it, wires auth and builds the app shell, leaving a running app to build features into. Triggers on 'scaffold', 'bootstrap the project', 'set up the repo', 'create the app'."
version: "0.1.0"
metadata:
  artifacts:
    requires:
      - { id: brief }
      - { id: techstack }
      - { id: brand-tokens }
      - { id: screens }
  prerequisites:
    files:
      - { path: "_concept/brief.md", gate: hard }
      - { path: "_concept/10_blueprint/techstack.md", gate: hard }
      - { path: "_concept/03_brand/tokens.json", gate: soft }
      - { path: "_concept/07_screens", gate: soft, min_entries: 1 }
---

# build-scaffold

Takes an empty directory to a running, themed, authenticated, navigable app by walking the
chosen template's recipe sections in order: `## Scaffold Recipe`, `## CSS Variables /
Theming`, `## Auth Setup`, `## App Shell`. The recipe belongs to the template; the order,
the checkpoints and the verification are this skill's.

It stops at the shell. No schema and no seed data — that is `build-database`, once, rather
than three skills each doing half of it. No feature code — `build-plan` cuts it and
`build-implement` builds it. No plan file and no status file: order is the flow graph and
completion is git, so the scaffold's record is its commit (ADR 0010). And no Storybook — the
one at `09_mockup/storybook/` belongs to the mockup domain, and an app that wants its own
gets it as ordinary build work behind the template's `## Storybook Config`.

## Steps

1. **Resolve the stack and read its atoms by name.** `10_blueprint/techstack.md` names
   `tech_stack_skill`; `templates/<that id>/TEMPLATE.md` carries `scaffold_command`,
   `package_manager`, `project_structure`, `build_command`, `lint_command`,
   `type_check_command` and `env_setup_command` under `metadata.atoms`. Every template
   declares every atom with a value or an explicit `null`, and a `null` is the answer rather
   than a missing one: `env_setup_command: null` means that scaffolder ships no `.env.example`
   and the env file's contents are recipe material under `## Scaffold Recipe`;
   `lint_command: null` means the recipe installs no linter and step 8 has one less check to
   run. `tech_stack_skill: custom` means there is no template — take each command from
   `techstack.md` and confirm it with the user before running it.
2. **Confirm before creating anything.** App name and slug from `brief.md`, the resolved
   scaffold command verbatim, the directory it will run in, and what this run will not do —
   no database, no seed data, no features. This is the last cheap moment: after the scaffolder
   runs, changing the stack means deleting the tree.
3. **Run `## Scaffold Recipe` end to end.** The `scaffold_command` in the empty directory,
   dependencies with `package_manager`, then the recipe's remaining steps in the order it
   gives them — config files, environment files, the directories it names. Check the result
   against `project_structure` before going further: a layout that came out different means a
   flag was dropped, and every path in the three sections after this one is written against
   the layout that was supposed to appear.
4. **Commit the scaffold on the build branch.** `build-branch` opens `build/<app-slug>` when
   the flow runs it; find that branch and commit onto it. When there is none — `appbuilder-mvp`
   has no branch step — initialize the repo if needed and cut `build/<app-slug>` here, because
   a generated project committed to the default branch drops thousands of unreviewed lines
   where the user's own work lives.
5. **Theme it — `## CSS Variables / Theming`.** With `03_brand/tokens.json` present, every
   colour, font, radius, spacing value and shadow traces to a token, both light and dark
   blocks when the tokens carry both, fonts imported from the provider the tokens name, and
   `03_brand/identity.md` read for atmosphere. Without it — `appbuilder-mvp` runs no brand
   step — take the stack's own defaults from that section and tell the user which defaults you
   took and how to replace them later. Refusing to run without tokens would make every run of
   that flow fail; inventing hex values would make the app disagree with a brand it is
   supposed to wear. Applying what exists and naming what did not is the only branch that is
   true in both flows.
6. **Wire auth — `## Auth Setup`.** Config files, plugins and middleware, packages, and the
   role mapping, all at the locations the section gives. Roles come from the `permissions:`
   blocks in `05_features/`; where the auth feature itself has no spec yet, leave placeholder
   logic with a TODO naming the feature that will replace it. Credentials come from the
   environment — a literal in a config file is one `git push` from being public.
7. **Build the app shell — `## App Shell`.** Layout at the location the section names,
   navigation carrying every screen under `07_screens/`, plus active state, the icons the
   screen specs name, and mobile collapse. `07_screens/shell.md` is the spec when it exists;
   without it derive the nav from the screen directories. Nav items typed in by hand stop
   matching the specs at the first screen anyone adds.
8. **Verify, then show it.** `build_command`, plus `lint_command` and `type_check_command`
   wherever they are not `null`, until all of them pass. Then start the app and walk it with
   the user: the shell renders, the theme is applied, the nav reaches every screen, the login
   page loads. Approve, or name what to change and fix it here — a scaffold with a broken
   build is a foundation every later slice inherits. Then land steps 5 to 7 as one commit
   each: a bisect that has to separate a broken theme from a broken shell can only do it if
   they arrived separately.

**Done when** the app builds and runs, its theme traces to tokens or to a named stack default,
its nav covers every screen spec, and the scaffold plus one commit per section are on
`build/<app-slug>`.
