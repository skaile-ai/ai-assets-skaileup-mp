---
name: quality-e2e
description: "Use when the app runs and its journeys need proving end to end in a real browser — drives every story from stories.yaml with agent-browser, screenshots each step, checks the database behind it, and flips the acceptance-criteria ledger. Triggers on 'test the app', 'e2e tests', 'browser testing', 'walk the journeys'."
version: "0.1.0"
metadata:
  artifacts:
    requires:
      - { id: journeys }
      - { id: features }
      - { id: screens }
      - { id: datamodel }
  prerequisites:
    files:
      - { path: "_concept/04_journeys/stories.yaml", gate: hard }
      - { path: "_concept/05_features", gate: hard, min_entries: 1 }
      - { path: "_concept/07_screens", gate: soft, min_entries: 1 }
      - { path: "_concept/10_blueprint/datamodel", gate: soft }
---

# quality-e2e

Drives the running application through **every story in `04_journeys/stories.yaml`**, one
journey per story, and reports what a user can and cannot actually do. Where `quality-test`
asserts against units, this asserts against the product: the pass condition for a journey is
its own EARS acceptance criteria, observed in the browser.

The tool is `agent-browser`. Screenshots are test output and live beside the tests in the
codebase, not under `_concept/` — the concept tree holds what the project decided, never
what one run of it looked like.

## Steps

1. **Clear the platform gate.** `agent-browser` supports Linux, WSL and macOS: on anything
   else, stop and say so rather than half-running. Then confirm a browser-reachable frontend
   exists (a dev script, a pages tree, an `index.html`) and that `agent-browser --version`
   answers; install it if it does not.
2. **Build the journey list.** Read every story in `stories.yaml` — hero and vital stages
   first — and carry each story's acceptance criteria forward as that journey's explicit pass
   conditions. Screen specs under `07_screens/` give the routes and the per-state elements to
   look for; without them, discover routes from the running app's own navigation and record
   in the report that they were inferred. Read `10_blueprint/datamodel/` for the entities a
   journey writes and the queries that confirm them, and note that a project with no data
   model gets journeys proved through the UI alone.
3. **Start the app and pin the seed.** Install, start the dev server in the background, wait
   until it answers, then open it. Every input a journey types comes from a named scenario in
   `10_blueprint/datamodel/seed.json` per `contracts/seed_data.md`. Invented test data proves
   the app handles data that does not exist in it.
4. **Walk each journey, screenshotting every step.** Re-snapshot after every navigation —
   element references go stale the moment the page changes, and acting on a stale reference
   fails in a way that reads like a product defect. Read the screenshots back rather than
   assuming the click landed, check the console for errors after each step, and after any
   step that writes data query the store to confirm the record matches what the data model
   declares. A journey passes only when **all** of its criteria hold; otherwise it fails,
   named by the first criterion that did not.
5. **Test the key pages responsively** at 375×812, 768×1024 and 1440×900. A layout that
   works at one width is one third of a claim.
6. **Flip the ledger.** For every feature a journey covered, open
   `11_build/acceptance-criteria/<featureset>/<feature_slug>.ac.md` and set the rows whose
   criteria this run actually evaluated to `PASS` or `FAIL` per
   `contracts/acceptance_criteria.md`, stamped with this skill and today's date and the
   journey as evidence. Rows the run did not evaluate stay exactly as they were — a row
   flipped on inference is what makes the whole ledger unusable to `quality-review`. Where a
   ledger is missing, warn and continue; `build-plan` creates it.
7. **Stop the dev server and close the browser session**, whatever the outcome. A server
   left running is the next run's mystery port conflict.
8. **Report** per journey: pass or fail, the failing criterion, the screenshots, the console
   errors, and any record the database did not hold. Group the failures by feature so the
   next reader knows which spec to reopen.

**Done when** every story in `stories.yaml` has been run, each with a pass or a fail and a
named criterion behind it, the ledger rows this run evaluated are flipped, and no dev server
or browser session is left alive.
