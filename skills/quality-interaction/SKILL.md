---
name: quality-interaction
description: "Use when an app's code exists and its interaction decisions are written down in APP-DESIGN.md — checks the code against them entry by entry and type by type, counts violations and exemplars per rule, and writes the ordered changes that close them. Triggers on 'check the app against APP-DESIGN.md', 'does the UI follow our patterns', 'interaction review', 'where do we still break the rules'."
version: "0.1.0"
metadata:
  requires:
    - contract:@skaile-ai/shared-contracts
  artifacts:
    requires:
      - { id: app-design }
    produces:
      - { id: interaction-review, path: "_concept/11_build/interaction.yaml" }
  prerequisites:
    files:
      - { path: "APP-DESIGN.md", gate: hard }
      - { path: "package.json", gate: hard }
---

# quality-interaction

Checks the app's source (`src/`, or the stack's own roots such as `app/` + `server/`)
against the decisions in `APP-DESIGN.md` and writes what it finds to
`_concept/11_build/interaction.yaml`: violations, one exemplar per rule, a score, ordered
changes and the questions it cannot settle. It judges conformance and nothing else. It does
not change application code and it does not edit `APP-DESIGN.md`, whose one writer is
`experience-interaction`; a deviation worth keeping becomes a proposed exception in the
verdict, and the user's answer reaches the file through that skill. The stance is
`contracts/evaluator.md § Stance`: a finding is measured at a `file:line`, or it is not one.

Findings are recorded per `contracts/interaction_patterns.md § Recording findings`: one
finding per distinct cause, filed under the most specific rule and counted once. Where
things sit per stack and how citations are checked is `contracts/ui_detection.md`.

**Subagents.** Evidence passes that only collect — the surface census, the button scan, one
grep pass per area — run in parallel on a small, fast model. Brief each with the
`ui_detection.md` rows it needs and the citation rule (paths from the repository root). They
return `file:line` lists and write nothing; classifying and judging stay in this session,
which checks their citations before using them.

## Steps

1. **Read the intent.** Open `APP-DESIGN.md` per `contracts/app_design.md § Reading it`, then
   `_concept/glossary.md` for the nouns, `docs/adr/` and the UI concept files named in
   `ui_detection.md § Intent and vocabulary`. A decided entry replaces the default of the
   rules it cites; a deviation listed in § Exceptions is not reported; an `[open Qn]` entry
   is judged by its recommendation and tagged `[Qn]`. Confirm the app root, the code roots
   and the stack — a monorepo with several apps is a question for the user, not a guess.
2. **Take the surface census.** Every modal, drawer, popover and palette with purpose, host
   and trigger (`ui_detection.md § Editors and surfaces`), plus screens, object types and
   finders from their own sections. When `_concept/02_grounding/findings/interaction.md`
   exists, start from it and re-verify each line at its cited `file:line`; a line the code no
   longer backs is dropped, because code that changed since the census is the usual cause of
   a finding nobody can reproduce. Skip generated and vendored code (`§ Generated and
   vendored code`).
3. **Walk the entries.** Go entry by entry through `APP-DESIGN.md`, then type by type through
   § Objects' floorplan: index, home, editor, create flow, delete confirmation,
   representations, search. Sample large files by pattern grep and keep a list of the regions
   left unread — a verdict that does not name them reads as complete when it is not. On a large
   app walk the core types and the entries of every area, and record each type or area not
   reached as `unread`.
4. **Record violations and exemplars.** Each violation carries the entry and rule id
   (`MOD-2 / P5`), the type, expected (quoted from the entry), actual, `file:line`,
   severity and kind (`consistency` or `completeness`). An absence cites
   `absence: <what is missing>` with the nearest `file:line`. Record one conformant exemplar
   per rule where one exists — it is what a fix copies. An entry whose *Why* or *Ref* the
   code contradicts, or that drops a rule's obligation without an exception, is not a
   violation: it becomes a question with its evidence, and the entry stands as written.
5. **Count.** Per rule P1–P17: violations, exemplars, and a status — `violated` (a violation
   is filed under the rule or lists it in `also:`), `conformant`, `by-decision` (satisfied
   only because an entry loosened it; name the obligation that remains) or `unchecked` (no
   violation, no `also:` and no exemplar: nobody looked or nothing was found, which is not a
   pass). Counts come from counting the two lists in the file, with a script or grep over
   `interaction.yaml`, never from typing: write the lists first, then let the script insert
   `score:` above `violations:`. A finding filed under another rule shows there as `(+n)` from
   its `also:` list.
6. **Order the changes.** Systemic first — a shared editor, the action registry, one confirm
   component — because each closes violations across many types; then per-type changes. Each
   change lists the violations it covers and the files it touches. End with a coverage table:
   every violation maps to a change, or to a proposed exception awaiting the user's answer.
   A violation in neither is an unfinished plan.
7. **Check the citations.** Run `ui_detection.md § Verifying citations` over the draft
   verdict, including the `: <line>` shorthand grep it ends with, and read a sample of the
   cited lines for meaning. A failing citation is fixed or the finding dropped before
   anything is written.
8. **Write the verdict** to `_concept/11_build/interaction.yaml`, replacing the previous
   run's file whole, so the file always describes the code as it is now:

   ```yaml
   app_design_updated: YYYY-MM-DD      # `updated:` of APP-DESIGN.md this run read
   checked_at: YYYY-MM-DD
   score:                              # computed from the lists below
     P5: { violations: 3, exemplars: 1, status: violated }   # + `also: 1` when others file here
   violations:
     - { id: V-1, entry: MOD-2, rule: P5, also: [P14], type: Room, severity: high,
         kind: consistency, expected: "…", actual: "…", ref: "app/a.vue:12", tag: "" }
   exemplars:
     - { rule: P5, ref: "app/b.vue:30-52" }
   changes:
     - { id: C-1, kind: systemic, title: "…", covers: [V-1], files: [app/a.vue], status: open }   # kind: systemic | per-type
   coverage: { V-1: C-1, V-2: "proposed: E-1" }   # a change id, or a proposed exception id
   proposed_exceptions: [{ id: E-1, entry: BTN-4, reason: "…", covers: [V-2] }]
   questions: [{ id: Q-1, entry: OBJ-3, question: "…", evidence: "app/c.vue:9" }]
   unread: ["app/legacy/**: 40 files, sampled by grep"]
   ```

   `build-plan` reads the `open` changes. Hand `proposed_exceptions` and `questions` back to
   the user and name `experience-interaction` as the skill that folds them into
   `APP-DESIGN.md`; the exception enters § Exceptions only on the user's answer.
9. **Report.** The score table first, then the changes in order with what each closes, then
   the unchecked rules, the unread regions and the questions.

**Done when** `_concept/11_build/interaction.yaml` is on disk with every violation citing a
`file:line` the citation check passes, every rule counted or marked `unchecked`, every
violation covered by a change or a proposed exception, and the unread regions named.
