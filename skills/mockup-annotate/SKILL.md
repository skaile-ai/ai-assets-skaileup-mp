---
name: mockup-annotate
description: "Use when a built walkthrough is ready for stakeholders to comment on. Injects the annotation overlay so a reader can click any element and leave a note, and prepares the session directory their notes come back to. Run mockup-feedback once the notes are in."
version: "0.1.0"
artifacts:
  requires:
    - { id: walkthrough, gate: hard }
prerequisites:
  files:
    - { path: "mockup-walkthrough", gate: hard, min_entries: 1 }
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

1. **Locate the site.** `_concept/mockup-walkthrough/<renderer>/`, where `<renderer>` is the
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
   <script type="module" src="<relative-prefix>annotation-overlay.js"></script>
   ```

4. **Prepare the return path** under the project's `_concept/_feedback/`: create `sessions/`
   and, when absent, `index.json` holding `{"schema_version": "1.0", "sessions": []}`. Append
   `_concept/_feedback/sessions/` and `_concept/_feedback/patches/` to the project `.gitignore`
   if they are not already there. `applied/` and `devlog.md` stay committed — they are the
   audit trail of what feedback actually changed.
5. **Validate**: `python skills/mockup-annotate/validator.py _concept/mockup-walkthrough/<renderer>`.
   Exit 0 means every page carries the overlay as its last script and nothing external crept in;
   exit 2 lists the pages that do not.
6. **Report and hand over.** Name the site root, the injected/skipped counts, the session
   directory, and the provisional-id count. Then tell the user the two things only they can do:
   open the site and check that clicking an element in Annotate mode opens the popover, and
   share the link.

## Getting the notes back

Inside forge-concept the overlay posts each annotation to the host frame and the host stores
the session. Opened straight from the filesystem there is no host, so the overlay collects
annotations in the page and offers a **Download** button, which saves
`annotations-<short-id>.json` wherever the reader's browser puts downloads.

That file has to be moved by hand to `_concept/_feedback/sessions/<sid>.json`, and **the name
it is saved under becomes the session id** every later step keys on — patches, the review file
and the audit trail all inherit it. So rename it to something a person will recognise weeks
later (`2026-09-05-stakeholder-review.json`), not the browser's short hash. Say this in the
report; a downloaded file nobody moves is a feedback round that silently never happened.

Each annotation carries the element, screen, journey and route it was made against, the
reader's text, one of `change` / `add` / `remove` / `question`, and whether the element's id
was provisional. `references/session.schema.json` is the shape `mockup-feedback` expects.

**Done when** the validator exits 0, `_concept/_feedback/sessions/` exists, and the user has
the site root and the rename convention in front of them.
