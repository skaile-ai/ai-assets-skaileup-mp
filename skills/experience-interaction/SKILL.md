---
name: experience-interaction
description: "Use when the glossary and the data model exist and the app's interaction rules are not written down yet — where information lives, one editor per object, inline vs modal vs page, saving, messages, popups, buttons, search and command palette — or when a code check has proposed changes to them. Decides the rules per object type with the user and writes APP-DESIGN.md. Triggers on 'write the app design', 'APP-DESIGN.md', 'when do we use a modal', 'UI rules for this app', 'interaction decisions'."
version: "0.1.0"
metadata:
  requires:
    - contract:@skaile-ai/shared-contracts
  artifacts:
    requires:
      - { id: glossary }
      - { id: journeys }
      - { id: datamodel }
    produces:
      - { id: app-design, path: "APP-DESIGN.md" }
  prerequisites:
    files:
      - { path: "_concept/glossary.md", gate: hard }
      - { path: "_concept/10_blueprint/datamodel/", gate: soft }
      - { path: "_concept/04_journeys/stories.yaml", gate: soft }
      - { path: "_concept/02_grounding/findings/interaction.md", gate: soft }
      - { path: "_concept/11_build/interaction.yaml", gate: soft }
      - { path: "APP-DESIGN.md", gate: soft }
---

# experience-interaction

The one writer of `APP-DESIGN.md` at the project root: the app's decisions on where each
object lives, which surface edits what, how saving, messages, popups and buttons work and how
people find and trigger things. It runs after the glossary and the data model and before any
screen is specified, because a screen spec applies these decisions and cannot invent them.
It decides and records; it writes no screen, no navigation and no code.

The rulebook is `contracts/interaction_patterns.md` (`P1`–`P17`). The file's shape, entry
format and reading and writing rules are `contracts/app_design.md`'s; this file covers the
procedure. Object names come from `model.json` and `glossary.md` and are never coined here:
two names for one object would split every later entry that cites it.

## Steps

1. **Read the ground.** Per `contracts/app_design.md § Reading it`, open an existing
   `APP-DESIGN.md` first as intent: its decided entries and exceptions are settled and later
   steps draft only what it lacks. Then `10_blueprint/datamodel/model.json` (without it, the
   glossary's nouns and the brief carry the object list), `glossary.md`, and
   `04_journeys/stories.yaml` for roles and the tasks each journey performs (without it, the
   brief's audience and hero flow). Where `02_grounding/findings/interaction.md` exists the
   app is a retrofit: every decision it records and grades is recommended as it stands
   wherever it passes the rule, so the file renames and fixes what the code does rather than
   redesigns it. Where `11_build/interaction.yaml` exists, this is a re-entry: go to step 7.
2. **Classify the objects.** One row per object the model or glossary names, with its class
   (`contracts/interaction_patterns.md`'s opening: `core`, `supporting`, `child`, `junction`,
   `system`), `simple` or `complex` for core and supporting types, and the roles that edit
   it (one line when the app has one role). A word on the glossary's `_Avoid_` list is
   renamed to its term. A concept the files do not name is not appended here: name it and
   hand back, and the flow re-enters `concept-glossary`, which pins it before this step goes
   on. A `system` type users only read is listed once and leaves the later tables.
3. **Decide the global rules.** For each of `P1`–`P17`: `adopt`, `adapt` with the adapted
   wording, or `reject`, each with a one-line reason grounded in this app's size, users and
   UI stack. An adaptation keeps the rule's obligation and changes its form; one that removes
   the obligation is a `reject` and is written as one, because it lands in § Exceptions.
4. **Draft each type's floorplan.** One row per non-system type: index · canonical home ·
   editor · create flow · delete confirmation · representations with their field subsets ·
   in search. Under it, per type, its editing tasks as `task → surface` and its palette
   actions. In a retrofit mark each cell `as-is` or `change`.
5. **Ask in rounds.** Everything above is a draft until the user has answered the decisions
   a reasonable maintainer could make the other way, taken from
   `references/decision-catalogue.md`: the ⚖ rows and the core and supporting types' calls
   first, those that change a screen's surface before the rest. A round is at most five
   questions, each its own message per `contracts/agent_patterns.md § Questions Are
   Standalone Messages`, each with the recommendation first and its reason; the rows
   without ⚖ go as one "take these defaults?" message. Open questions already in § Open come
   first. Without a user, the recommendation is written as the decision with `[open Qn]` on
   the entry and the question as a § Open row that stands alone: question, options,
   recommendation and why.
6. **Write `APP-DESIGN.md` after every round**, not once at the end, per
   `contracts/app_design.md § Writing it`: create it in the shape of
   `contracts/app_design.md § Shape`, or update it in place, leaving decided entries as
   written — flipping one needs the user's answer. Decisions become entries in their area
   (`contracts/app_design.md § Entries`); the floorplan and representations go to § Objects;
   a rejected rule or accepted deviation goes to § Exceptions only on the user's answer. Each
   write adds one § Changelog line and sets `updated:`. When the user says yes to the file in
   words, set `approved:` in the same write; an edit after that leaves it at its last value
   until the user says yes again.
7. **Fold in a code check.** Where `11_build/interaction.yaml` exists, read its violations,
   `(change)` candidates and proposed exceptions. Mark the entries it names `(change)` with
   their sites (past three sites, the count and the first), and ask each proposed exception
   in the next round: a yes enters § Exceptions, no answer becomes the § Open row
   `keep as exception?`. The verdict file is `quality-interaction`'s and stays as it is.
8. **Hand off.** Name what reads the file next: `spec-feature` applies the OBJ
   `task → surface` rows to every screen and hands a screen that needs a surface the floorplan
   lacks back to this skill; `experience-shell` derives the navigation under § Navigation and
   takes MSG, EDIT and MOD from the entries. Say which rows a re-entry changed, so those
   screens are re-checked.

**Done when** every rule `P1`–`P17` has a decision with a reason, every non-system type has a
floorplan row, every contested decision is answered or an `[open Qn]` entry with a stand-alone
§ Open row, `APP-DESIGN.md` was written after the last round and passes
`contracts/ui_detection.md § Verifying citations` for every `Ref` it cites, and `approved:` is
set — or § Open says why the user has not yet signed off.
