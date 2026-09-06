# 39: Make a red `main` impossible to miss

**Type:** grilling
**Blocked by:** 38 — pushing tells you whether a failure notifies anyone at all
**Status:** ready-for-agent

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

## Answer

_(pending)_
