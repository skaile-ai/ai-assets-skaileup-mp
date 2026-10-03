# i-opt-design-red-flags: Screen custom modules for design red flags before they enter the architecture

**What to build:** When `architecture-system` writes down a custom module, protocol or integration, it first screens the candidate against four red flags phrased as questions — shallow module, information leakage, temporal decomposition, pass-through — each with a one-line fix direction, plus "design it twice": a module with two plausible interfaces gets both written as signatures before the deeper one is kept. The screen lives in the skill's own `references/` (single reader), not in a contract.

**Plan:** `.scratch/plans/OPT_SKAILEUP_MP_SKILL_OPTIMISATION_PLAN.md` — S4, decision D6, finding F7; ticket-breakdown row T5.

**Blocked by:** None (can start immediately)

**Status:** resolved

- [ ] A design-red-flags reference (about 40 lines) under `architecture-system`'s `references/`, with a footer citing pstack `architect/references/design-red-flags.md` and Pocock `codebase-design/DESIGN-IT-TWICE.md`.
- [ ] Step 4 of `architecture-system` points to the screen before it names a custom module, and notes that a module failing the shallow-module question is usually a feature's helper.
- [ ] The skill gains a short "What sits in references/" section (precedent: `concept-reverse`).
- [ ] The skill body stays at or under 140 lines; `python scripts/check.py` exits 0.
