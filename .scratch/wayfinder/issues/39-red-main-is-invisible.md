# 39: Make a red `main` impossible to miss

**Type:** grilling
**Blocked by:** 38 — pushing tells you whether a failure notifies anyone at all
**Status:** resolved

## Question

Two consecutive CI failures sat on `main` for ~13 hours and were found only because ticket 35
happened to open the same file. That is the exact failure class this collection's whole gate
exists to prevent — a defect that resolves to nothing quietly — reappearing one level up, in the
gate itself.

The cause is precise and worth keeping in view: ticket 34's resolution says its four checks were
"each verified by breaking it and watching it fail", which is true and was not enough. Breaking a
check proves the check; it does not prove the suite. Locally, `python scripts/check.py` prints a
confident `0 error(s)` while `pytest scripts/test_check.py` is 58-failed — **two commands, and
only one of them was in the habit.** CI is the only thing that runs both, and nobody was reading
CI.

So: **what makes the next red `main` visible within minutes rather than a day?**

1. **Notifications** — GitHub Actions failure email/mobile may simply be off for this repo or
   this account. Cheapest possible fix if that is all it is, and it needs no repo change.
2. **One command means green** — a `make check` or `scripts/check.sh` that runs `check.py` **and**
   `pytest`, so a session cannot report green having run half of it. Fixes the habit at the
   source rather than catching the consequence, but only for whoever runs it.
3. **A pre-push hook** — refuse the push when either is red. Strongest, and the most likely to be
   resented at the wrong moment.
4. **A status badge in `README.md`** — passive, but it is on the page every session opens first.

These are not exclusive; 1 and 2 compose well. What the ticket must not produce is a fourth thing
to remember.

Blocked by [38](38-land-ticket-35-upstream.md) because that push is the experiment: if its
failure or success arrives as a notification unprompted, option 1 is already in place and the
question narrows to the local habit.

## Resolution (2026-09-07)

**Option 1 is struck, not adopted: the notifications were already on and they worked.** The
failure mail for `736522f` (run 33997272072) did arrive. So the gap was never a missing signal
— it was ~13 hours between the signal and anyone acting on it, because the channel is an inbox
and the work happens in a session. That kills the ticket's cheapest option and reframes the
rest: **prevent, then let the session notice; do not amplify a channel nobody is standing in.**

Four changes, no fifth thing to remember:

1. **`check.py` runs `test_check.py` as its last phase** (`scripts/check.py`). The command
   already in the habit becomes the complete gate rather than half of one — no `Makefile`, no
   `check.sh`, no second entry point to drift. A missing pytest is an **error, not a skip**,
   since a skipped test phase prints the same confident green as the defect this closes.
   `--no-tests` exists for iterating on a rule and says on its own line that the run does not
   mean green. Verified by simulating ticket 34 — a fixture left asserting a rule that changed
   under it — where the old `check.py` printed `0 error(s)` and exited 0, and this one exits 1.
2. **The gate is written where a session reads it.** It appeared in no agent-read file:
   `CLAUDE.md` never mentioned it, and `README.md` named `check.py` once and `pytest` zero
   times — the repo documented precisely the half-gate that failed. Both now say green means
   `python scripts/check.py`, and that is the whole gate.
3. **A push is not finished until its run is green** — `gh run watch --exit-status`, one line
   beside the other in `CLAUDE.md`. This is the actual fix for the 13 hours: the human channel
   answers in hours, the session is standing there in seconds, and change 1 is what makes it
   rarely fire.
4. **A CI badge at the top of `README.md`** — a backstop for whoever did not push, not the fix.
   Same passive class as the mail that lost; kept because it is free and on the first page.

**Refused: the pre-push hook and branch protection.** A hook is not committed by git, so it
needs `core.hooksPath` plus a per-clone setup step — exactly the fourth thing the ticket
forbade. Branch protection with `ci` required would work but blocks push-to-main, which is how
this repo ships.

**CI keeps two steps.** Folding the fixtures into `check.py` is right for a session; for CI the
two named steps say which half failed on the summary page without opening a log, so the first
step passes `--no-tests` rather than running them twice.

Surfaced while resolving this, and opened rather than absorbed:
[40: The checker's host coupling is asserted, not tested](40-host-coupling-is-asserted-not-tested.md)
— roughly a dozen `check.py` rules copy facts from forge-concept, justified in comments naming a
`file:line` nothing re-checks, and measured drift shows the pointers rotting within two weeks
while the facts hold. Same failure family, one level further out.
