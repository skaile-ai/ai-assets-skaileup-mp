---
name: mockup-annotate
description: "Use when a built walkthrough is ready for stakeholders to comment on. Injects the annotation overlay so a reader can click any element and leave a note, and prepares the session directory their notes come back to. Run mockup-feedback once the notes are in."
version: "0.1.0"
metadata:
  requires:
    - contract:@skaile-ai/shared-contracts
  artifacts:
    requires:
      - { id: walkthrough }
  prerequisites:
    files:
      - { path: "_concept/09_mockup/walkthrough", gate: hard, min_entries: 1 }
---

# mockup-annotate

Turns a rendered walkthrough into a surface people can comment on, and stops there. It edits
only the built site — never a screen spec — and it is idempotent: running it again over an
already-instrumented site changes nothing. Reading what comes back, and turning it into edits,
is `mockup-feedback`.

The overlay resolves a click to the nearest `[data-spec-element]` and reads `data-spec-screen`
/ `data-spec-journey` off `<body>`, so it works against any renderer that honours
`contracts/walkthrough_renderer.md`.

## Steps

1. **Locate the site.** `_concept/09_mockup/walkthrough/<renderer>/`, where `<renderer>` is the
   single subdirectory containing a `manifest.json`. Neither the directory nor the manifest
   present means no walkthrough was built: say which is missing and stop. Read the manifest and
   note how many screens it lists and how many elements carry `"provisional": true` — the
   report tells the user, because a provisional id is one a reader's comment will promote.
2. **Copy the overlay** from this skill's `overlay/annotation-overlay.js` to the **site root**,
   one copy for the whole site. Identical file already there — skip it and say so.
3. **Inject the script tag into every `.html` under the site root**, as the last line before
   `</body>`. The `src` is relative to the page, so a page one directory down gets
   `../annotation-overlay.js` and `screen/<group>/<name>.html` gets
   `../../annotation-overlay.js`; a bare filename on a nested page resolves against that page's
   own directory and silently loads nothing, which reads as an overlay that just does not
   appear. Find the insertion point with a right-hand search for `</body>` rather than a
   regex — the tag appears exactly once in a well-formed page, and matching from the right
   survives any whitespace layout. A file that already references the overlay in a `<script>`
   tag is skipped whole.

   ```html
   <script src="<relative-prefix>annotation-overlay.js"></script>
   ```

   No `type="module"`. The overlay has no imports, and a module script is fetched with CORS
   against an origin `file://` does not have — so the one tag a stakeholder opening
   `index.html` from a shared folder can load is the plain one. The validator in step 5
   rejects a module tag for that reason.

4. **Prepare the return path** under the project's `_concept/09_mockup/feedback/`: create `sessions/`.
   Append `_concept/09_mockup/feedback/sessions/` and `_concept/09_mockup/feedback/patches/` to the project
   `.gitignore` if they are not already there. `applied/` and `devlog.md` stay committed —
   they are the audit trail of what feedback actually changed.
5. **Validate**: `python skills/mockup-annotate/validator.py _concept/09_mockup/walkthrough/<renderer>`.
   Exit 0 means every page carries the overlay as its last script and nothing external crept in;
   exit 2 lists the pages that do not.
6. **Report and hand over.** Name the site root, the injected/skipped counts, the session
   directory, and the provisional-id count. Then tell the user the two things only they can do:
   open `index.html` and check that clicking an element in Annotate mode opens the popover, and
   share the site with the readers along with the one instruction *Getting the notes back*
   below turns on — download before closing the tab, and send the file back unrenamed.

## Getting the notes back

The reader opens the site in a browser, ticks **Annotate**, comments across as many pages as
they like, and clicks **Download**. The overlay carries the round in `sessionStorage`, so it
survives moving between screens; it ends when the tab closes, which is why the report tells
the reader to download before they finish, not after they think of it.

The download lands wherever their browser puts downloads, named `<session-id>.json`. **Do not
rename it.** The id inside the file is what triage, patching and the audit trail key on, and a
filename that disagrees with it produces a round that reads as never applied. The
human-readable name for the round is asked for later, by `mockup-feedback`, and stored inside
the file.

So the reader's last act is to send that file back — attach it, drop it in a shared folder,
whatever the team already does. `mockup-feedback` takes it from any path and files it itself;
nobody has to place it in `_concept/` by hand. Say this in the report: a downloaded file
nobody sends on is a feedback round that silently never happened.

Inside an embedding host the overlay posts each annotation to the parent frame instead. **No
host implements that listener today** — forge-concept has none — so the wiring is kept correct
but the browser path above is the one that works.

Each annotation carries the element, screen, journey and route it was made against, the
reader's text, one of `change` / `add` / `remove` / `question`, and whether the element's id
was provisional. `references/session.schema.json` is the shape `mockup-feedback` expects.

**Done when** the validator exits 0, `_concept/09_mockup/feedback/sessions/` exists, and the user has
the site root and the reader instruction in front of them.
