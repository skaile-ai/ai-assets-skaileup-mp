# APP-DESIGN.md — where an app's interaction decisions live

`APP-DESIGN.md` records how this app applies the rulebook in
`contracts/interaction_patterns.md`: where each object lives, which surface edits what, how
saving, messages, popups and buttons work, how people find and trigger things. It sits at
the project root — the directory holding `_concept/` — beside `_concept/`, and it
repeats none of its neighbours:

- `_concept/glossary.md` — what things are called (the nouns);
- `_concept/03_brand/identity.md` — how it looks and sounds;
- `_concept/07_screens/shell.md` — the concrete navigation;
- `docs/adr/` — decisions of architecture.

It holds *decisions*; findings, plans and questions stay in the output of the run that
raised them. Coding agents and reviewers cite its ids (`MOD-2`) instead of re-deriving a
rule. `build-scaffold` writes a line in the project's root `AGENTS.md` that points coding
agents here, creating the file when it creates the project. In a project that existed before
scaffolding the skills leave `CLAUDE.md` and `AGENTS.md` alone, and the plan says the link is
missing.

## Shape

```markdown
---
app: <name>
updated: YYYY-MM-DD
approved: YYYY-MM-DD
rulebook: interaction_patterns P1–P17
companions: { visual: _concept/03_brand/identity.md, glossary: _concept/glossary.md, shell: _concept/07_screens/shell.md, adr: docs/adr/ }
---
# App design – <name>
## Context              scale, roles, UI stack – the facts the decisions rest on
## Objects              floorplan table, representations, entity-page entries
## Surfaces             SURF
## Modals               MOD
## Popups               POP
## Editing              EDIT
## Messages             MSG
## Buttons              BTN
## Search and commands  FIND
## Navigation           NAV
## Language             LANG
## Exceptions           table: id · entry or rule · exception · reason
## Open                 table: id · question · recommendation
## Changelog            one line per write: date · skill or person · what changed
```

`approved:` is the collection's universal approval field (`contracts/artifact_frontmatter.md`,
universal fields): the date the user signed the file off, set beside `updated:`. A write
the user has not approved moves `updated:` and leaves `approved:` at its last value.

A section with nothing decided yet is left out; whoever fills it later inserts it in this
order. Entries are one line each, not hard-wrapped, so a diff shows one decision per line.
Budget about 100–200 lines; a floorplan table that outgrows it moves to
`docs/app-design/objects.md` and § Objects links it.

§ Objects holds, in order: the floorplan table (one row per type users act on — a `system`
type users only read is left out; class from `contracts/interaction_patterns.md`, plus
`simple` or `complex` for core and supporting types), the representations table (`row`,
`card`, `chip`, `peek` with their field subsets), per type its `task → surface` list and
palette actions, then the OBJ entries. Table rows are decided entries like any other: a
row resting on an unanswered question ends with `[open Qn]`, and a single cell resting on
one carries it in the cell (`change [open Q1]`).

§ Language holds the verb set (create / add / edit / save / delete / remove, in the UI
language) and points at `_concept/glossary.md` for the nouns; it lists no nouns itself, so
the glossary stays their one home. § Navigation holds the rule — which objects earn a
primary entry, how deep links work (P12, P9) — and not the concrete navigation, which
`shell.md` carries.

| area | decides | rules |
|---|---|---|
| OBJ | per type: class, home, index, editor, create, delete, representations, in search, editing tasks and their surfaces; entity-page anatomy; edit model of a page | P1, P2, P4–P8 |
| SURF | the edit-surface ladder and its local thresholds; what a drawer may host | P5 |
| MOD | footer layout, dismissal while dirty, stacking, linkable dialogs, narrow viewports | P5, P7, P14 |
| POP | tooltip, popover, dropdown menu, peek | P16, P2 |
| EDIT | save model, unsaved changes, validation and disabled Save, create flow, confirm vs undo | P14, P6, P7 |
| MSG | toast vs inline alert vs nothing, announcements, empty states | P15 |
| BTN | icon vs text, hierarchy, placement, labels, destructive styling, action registry | P17, P11 |
| FIND | search entry and scope, results page, palette content and order, shortcuts, list filters | P8–P11 |
| NAV | the navigation rule: which objects earn a primary entry, deep links | P12, P9 |
| LANG | the verb set; nouns come from the glossary | P13, P11 |

## Entries

One bullet per decision — imperative, applicable in a pull request without opening a source:

```markdown
- **MOD-2 Dirty dialogs ask before closing, in place.** <the rule>. *Why:* <one line: app fact or source>. *Ref:* `path/from/repo/root.vue:12-30`. *Rules:* P5, P14 adapt. [open Q3]
- **MOD-3 No modal over a modal.** <the rule>; two dialogs still stack it (change). *Ref:* none yet. *Change:* `path/to/a.vue:234`, `path/to/b.vue:241`. *Rules:* P5, P7.
```

- **Ids** are `AREA-n`, never reused. A revised decision keeps its id; a dropped one is
  struck through in § Changelog, not renumbered.
- **Ref** is the exemplar a fix copies; `Ref: none yet` when the code has none. A
  deviation the code still has is marked `(change)` in the rule text and its sites go in a
  `*Change:*` field after *Ref* — `*Change:* path/a.vue:12, path/b.vue:40` — not explained;
  past three sites, the count and the first site — the rest are in the findings. A
  deviation that is an absence (a missing query parameter) has no site; the rule text
  names what is missing.
- **Rules** names the rules the entry applies; `adapt` after a rule id when the entry
  changes the rule's form (P5's ~8 fields become ~12). An adapted rule is not an exception.
- **Contracts** sit in the entry that owns them, as a short code block in the stack's
  syntax: the editor shape (`mode`, section subset, events) under the OBJ entry, the action
  registry entry (`id`, `label`, `icon`, `shortcut`, `scope`, `available`, `run`) under BTN.
- **§ Exceptions** holds rejected rules and accepted deviations from an entry, each with
  its reason.
- **Status:** an entry is decided unless it carries `[open Qn]`; the question and its
  recommended answer are in § Open. A § Open row stands alone — question, options,
  recommendation and its reason — because the person who answers it may never see the run
  that raised it; an empty § Open says "No open questions."
  A rule adopted unchanged is decided by adoption and needs no question; `[open Qn]` marks
  an entry that rests on a question asked and not yet answered. Every citation in the file
  passes `contracts/ui_detection.md § Verifying citations`, like any artifact.

## Reading it

Each reader opens the file at its first step, as intent, before judging anything:

- `spec-feature` — each screen takes the surface of each editing task from the OBJ
  `task → surface` rows. A screen that needs a surface the floorplan lacks is handed back
  to `experience-interaction`; the screen spec does not invent one.
- `experience-shell` — derives the navigation under the NAV rule and takes MSG, EDIT and
  MOD patterns from the entries instead of deciding them.
- `ops-review` — checks screen specs against the entries.
- `quality-interaction` — checks the app's source against the entries.
- `build-plan` — reads the file through `quality-interaction`'s verdict, not directly.

How a reader applies what it reads:

- A decided entry replaces the default of the rules it cites. Code that deviates is one
  finding, filed under the entry with the rule tagged (`MOD-2 / P5`), counted once.
- A deviation listed in § Exceptions is not reported.
- An `[open Qn]` entry is judged by its recommendation, and the finding is tagged `[Qn]`.
- An entry that removes a rule's obligation without being listed as an exception is
  reported once, as a question for § Open, and neither followed nor overruled in silence.
- An entry whose *Why* or *Ref* the code contradicts (the cited line says otherwise, the
  stated fact is false) is reported once, as a question for § Open with the evidence; the
  entry stays as written until the user answers.

## Writing it

- **One writer.** `experience-interaction` creates the file and keeps every section; it is
  the only skill that edits it. Any other skill that has something to say about the file
  records it in its own output and leaves the file as it is.
- **`quality-interaction` records, `experience-interaction` folds in.** `quality-interaction`
  never edits the file. It records its findings as a SARIF 2.1.0 log in
  `_concept/11_build/interaction.sarif`: violations as `fail` results, `(change)` candidates
  in `runs[0].properties.changes`, proposed exceptions as results with an `underReview`
  suppression, and open questions in `runs[0].properties.questions`. On re-entry
  `experience-interaction` folds them in: `(change)` marks go on the entries with their
  sites; an exception enters § Exceptions only on the user's answer, and otherwise becomes a
  § Open row (`keep as exception?`).
- **Exceptions need the user.** A deviation enters § Exceptions only on the user's answer.
- **Missing file.** `experience-interaction` creates it from the shape above with the
  sections it fills, plus § Open and § Changelog.
- **Existing file.** Update in place: add entries, add `(change)` marks, and leave decided
  entries as written. Flipping one needs the user's answer; until then it is a question in
  § Open.
- **No user available.** Entries that rest on a *contested* recommendation the user has not
  given — the ⚖ rows of `experience-interaction`'s decision catalogue and any call a
  reasonable maintainer could make the other way — carry `[open Qn]`; the file does not
  present an unconfirmed choice as decided. A default that adopts a rule or records what the
  code does and passes is decided by adoption and carries none. New questions take the next
  number after the highest `Qn` the file has ever used, § Changelog included.
  `quality-interaction`'s verdict lists its open questions in `runs[0].properties.questions`, and
  `experience-interaction` asks them in its next round as new `Qn`.
- **Every write** adds one § Changelog line and sets `updated:`; `approved:` moves only
  when the user signs the write off.
