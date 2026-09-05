---
name: mockup-feedback
description: "Use when stakeholder annotations have come back from an annotated walkthrough and need to land in the concept. Routes each annotation to the file it belongs in, authors a reviewable diff for it, and — after you approve the review file — applies the approved diffs in one commit."
version: "0.1.0"
metadata:
  artifacts:
    requires:
      # Soft, not hard: step 1 adopts a session that has not landed yet, so a hard
      # gate would refuse the skill in exactly the case it exists to handle.
      - { id: feedback-sessions }
  prerequisites:
    files:
      - { path: "_concept/09_mockup/feedback/sessions", gate: soft, min_entries: 1 }
---

# mockup-feedback

One pass over one session file: adopt, triage, patch, apply. It ends with edited screen specs,
an audit trail, and exactly one commit. It never edits the walkthrough —
regenerating that from the updated specs is `mockup-walkthrough`'s next run.

The pass has a deliberate stop in the middle. Step 5 hands a human a review file and waits;
everything before it is proposal, everything after it is execution. Nothing is written into
`_concept/` until that approval.

`references/patch-format.md` is the format every diff in this skill uses. Read it before
step 4.

## Steps

1. **Adopt, if the file has not landed yet.** A reader's download sits wherever they sent it —
   a downloads folder, an attachment, a shared drive — and filing it is this skill's job, not
   theirs. Given a path, check it against `references/session.schema.json`, then copy it to
   `_concept/09_mockup/feedback/sessions/<sessionId>.json`, **taking the name from the file's own
   `sessionId` field and never from the path you were handed**: everything downstream keys on
   that field, so a stem that disagrees produces a round that reads as unapplied forever. Then
   ask the user what to call this round — *"the Sept 5 stakeholder review"* — and write it into
   the file as `label`. That is the only human-readable handle a session ever gets; the
   filename is machine-owned. A `sessions/<sessionId>.json` that already exists is the same
   round re-downloaded later with more in it: replace it, keeping the existing `label`.
2. **Pick the session.** A session is `_concept/09_mockup/feedback/sessions/<sid>.json` with no
   `_concept/09_mockup/feedback/applied/<sid>.json` beside it. Several unapplied? Name them **by their
   `label`** and let the user choose — sessions are stakeholder rounds, and merging two rounds
   into one commit loses which round asked for what.
3. **Triage — deterministic, no judgement.**

   ```
   python skills/mockup-feedback/scripts/triage.py \
       _concept/09_mockup/feedback/sessions/<sid>.json _concept/ _concept/09_mockup/feedback/triage/
   ```

   Each annotation routes by its `specRef`, screen before journey, to a file that must exist on
   disk — a journey annotation lands on the whole of `stories.yaml`, which is where journeys
   live, and there is no `feature` route because no renderer emits `data-spec-feature`.
   Unresolved annotations are recorded in the output with a reason rather than dropped, and the
   script still exits 0 — report the count and each reason, since an unresolved annotation is a
   comment nobody will ever see again. An annotation made on `index.html` is unresolved by
   design: the site root carries no screen and no journey.
4. **Author a patch per annotation.** Work one triage group — one target file — at a time.
   Read the file first; write the diff in that file's own voice, anchored to the section it
   changes. **`04_journeys/stories.yaml` is the exception: it takes no patches.** Every diff
   here anchors on a literal markdown heading, and `apply.py`'s no-removes path appends to the
   end of the file — against YAML that is a silent corruption, not a failed patch. Journey
   annotations become `needs_manual` entries quoting what was asked, so the reader's comment
   reaches a human instead of a `stories.yaml` rewritten as prose.

   `change` is the one category that needs judgement: read the section the annotated element
   appears in and rewrite it to carry the annotation's intent, scoped to the lines that
   actually move. `add`, `remove` and `question` follow the templates in
   `references/patch-format.md` — an LLM rewrite of a one-line append invents variation where
   the reader asked for none. Copy each annotation's `body` verbatim into its patch: the
   session file is gitignored and rotates, so this copy is the only lasting record of what was
   asked. Two patches are derived rather than requested — promoting a provisional element id
   once a human has annotated it, and promoting a navigation intent into a `target:` — and an
   annotation you cannot patch becomes a `needs_manual` entry naming why. Write
   `patches/<sid>.json` and `patches/<sid>.review.md` together.
5. **Hand over the review file and wait.** Every proposed patch is listed pre-checked in
   `patches/<sid>.review.md`; the user unchecks what to skip and may edit a diff in place. Say
   plainly that nothing is applied until they come back, and name any `needs_manual` bullets so
   they are not mistaken for silently-dropped comments. Then stop. Applying an unreviewed patch
   set is the one failure this skill cannot walk back: it edits the specs everything downstream
   is generated from.
6. **Pre-flight, then apply.** Three checks first: the git working tree is clean
   (`git status --porcelain` empty — apply commits, and a dirty tree puts unrelated work in
   that commit); `patches/<sid>.json` validates against
   `references/patches.schema.json`; and every checked patch id in the review file exists in
   the patch file. Then:

   ```
   python skills/mockup-feedback/scripts/apply.py \
       _concept/09_mockup/feedback/patches/<sid>.json _concept/09_mockup/feedback/patches/<sid>.review.md \
       _concept/ _concept/09_mockup/feedback/
   ```

   The script applies each checked patch best-effort, writes `applied/<sid>.json` and appends
   to `devlog.md`, and makes one commit. Exit 2 means every patch failed — nothing was written
   and nothing committed; fix the diffs and re-run, no `--force` needed. Exit 1 is a pre-flight
   refusal it caught itself. Exit 0 may still carry failures: they are recorded per patch with
   their error.
7. **Report** the applied and failed counts, the commit message, and the path of both
   `applied/<sid>.json` and the devlog. Print each failure with its reason and the retry —
   edit the review file, uncheck what already landed, re-run with `--force`. When the review
   file carried a `## Test impact` section, say that the changed specs affect test coverage and
   name the skill that regenerates it.

**Done when** one commit exists carrying the edited specs, `applied/<sid>.json` and the devlog
append, and every annotation in the session appears in `applied/<sid>.json`, in
`needs_manual`, or in the triage file's unresolved list.
