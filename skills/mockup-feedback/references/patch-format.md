# Patch format

## Section-anchored diffs

Every diff anchors to a heading, never to a line number — concept files are edited by hand
between feedback rounds, so an offset computed at proposal time is wrong by the time it is
applied.

```
@@ ## Section Name @@
- line to remove (full content, including the markdown bullet)
+ line to add
```

Frontmatter edits use the `frontmatter:elements` anchor instead:

```
@@ frontmatter:elements @@
-  - id: <element-id>
-    provisional: true
+  - id: <element-id>
+    provisional: false
```

What `apply.py` does with these, and what it therefore requires:

- The anchor must match a heading line **exactly** — `@@ ## Layout @@` needs a literal
  `## Layout` line in the file.
- Removed lines must exist in that section as a **consecutive block**, matched exactly. The
  first mismatch fails that patch and only that patch.
- There are no context lines. Any line that starts with neither `-` nor `+` is ignored.
- A diff with no removes is an insert at the end of the section; if the section does not
  exist at all, the adds are appended to the file and the patch is `kind: create-section`.

## Categories

`change` is authored; the other three are templates. Match them.

| Category | Diff |
|---|---|
| `change` | Rewrite the section the annotated element sits in, scoped to the lines that move. |
| `add` | `@@ ## States @@` then `+ - <annotation body>`, under the section the addition belongs to — `## States` for a state, `## Behavior` for a behaviour. |
| `remove` | `@@ ## <section> @@`, then the original line as a remove and the same line struck through as an add: `+ - ~~<original line>~~`. Strikethrough rather than deletion, so the review file shows what a reader asked to drop. |
| `question` | `@@ ## Open Questions @@` then `+ - <annotation body>`, creating the section if it is absent. |

## Derived patches

Two patches are emitted alongside a content patch rather than in response to a comment.

**`provisional-promotion`** — the annotated element's id was auto-slugged. A human has now
pointed at it, which makes the id worth keeping, so flip `provisional: true` to `false` in the
element's frontmatter entry. Read the file's `elements:` block first for its exact
indentation; if the frontmatter is missing or unparseable, skip the promotion, warn, and keep
the content patch.

```json
{
  "id": "p-<annotationId>-promotion",
  "annotationId": "<annotationId>",
  "file": "<same file>",
  "section": "frontmatter:elements",
  "kind": "provisional-promotion",
  "category": null,
  "diff": "@@ frontmatter:elements @@\n-  - id: <element-id>\n-    provisional: true\n+  - id: <element-id>\n+    provisional: false\n"
}
```

**`target-promotion`** — the annotation asks for navigation ("this should link to…",
"clicking this should open…") and the element has no `target:` yet. Resolve the destination to
a `screen_id` through the walkthrough manifest's screen list. Resolve it with confidence or
not at all: an unresolvable destination becomes a `needs_manual` entry reading
`navigation intent unresolved — no matching screen`, because a wrong `target:` silently
rewires the walkthrough.

```json
{
  "id": "p-<annotationId>-target",
  "kind": "target-promotion",
  "section": "frontmatter:elements",
  "diff": "@@ frontmatter:elements @@\n-  - id: <element-id>\n+  - id: <element-id>\n+    target: <resolved-screen-id>\n"
}
```

## `patches/<sid>.json`

`file` is relative to the concept root, with no `_concept/` prefix. Ids follow
`p-<annotationId>-content` / `-promotion` / `-target`.

```json
{
  "sessionId": "<sid>",
  "proposedAt": "<ISO-8601 UTC>",
  "patches": [
    {
      "id": "p-ann-c1-content",
      "annotationId": "ann-c1",
      "file": "experience/screens/01_user_auth/login.md",
      "section": "## Layout",
      "kind": "content",
      "category": "change",
      "body": "this should be on the right",
      "diff": "@@ ## Layout @@\n-- submit-button: centered below form\n+- submit-button: right-aligned below form\n"
    }
  ],
  "needs_manual": [
    { "annotationId": "<id>", "reason": "<why no patch could be authored>" }
  ]
}
```

Every triaged annotation ends in `patches[]` (once or more) or `needs_manual[]` (exactly
once), never both and never neither — `scripts/validate_patches.py` checks that partition
along with the anchor grammar and the category templates.

## `patches/<sid>.review.md`

The approval gate. `apply.py` reads exactly one thing from it: `- [x] **<patch-id>**`, so the
patch id is bold and immediately follows the checkbox.

```markdown
# Review patches for session <sid> (N patches across M files)

## Needs manual review

- annotation `<id>` — <reason>

## <file path>

- [x] **<patch-id>** · category=<category> · annotation: "<body preview>"
  ```diff
  <diff text>
  ```

## Test impact

Re-run the test-plan skill after applying — these spec changes affect coverage:

- `<file>` — <Happy|Error|Edge|Permissions>: <suggested scenario> (AC: <story-id>)
```

Every auto-generated patch starts checked; the user unchecks to skip. Omit the
`## Needs manual review` and `## Test impact` sections when they would be empty.

A patch changes testable behaviour when it touches `## Requirements`, `## Error States`,
`## Success Criteria` or `## Permissions` in a feature file, or `## Behavior` or `## States`
in a screen file, or when an `add` introduces a new state, behaviour or error case. Those get
one suggested scenario each under `## Test impact`. The scenarios are notes, not patches: no
checkbox, and `apply.py` ignores them. Copy, token and layout changes have no test impact —
leave them out rather than listing them as unaffected.

## `applied/<sid>.json`

Written by `apply.py`, committed, and the durable record once `sessions/` has rotated. It
carries one item per checked patch — applied and failed alike — with the annotation id, the
patch id, its target file and section, the verbatim annotation body, and `status` plus an
`error` on failure.
