# i-opt-agent-patterns-rewrite: Agent patterns in the house shape, pruned to what has a reader, with section citations checked

**What to build:** The shared run-time behaviours contract (`contracts/agent_patterns.md`) is rewritten in the house shape (at most 120 lines, no MUST/NEVER, no vocabulary for a host that does not exist: orchestrator, verbosity, research mode, observability events, `READS` blocks, `prog-expert-*`). It carries eight patterns: Read the tree first; **Steps are the todo list** (new, from pstack: a skill's numbered steps become the first todo items verbatim, non-applicable steps stay listed as `skip: <reason>`, **Done when** is last); Questions Are Standalone Messages; Answers persist; Standalone Mode; Next-Step Suggestion; Completion Summary (now with the **evidence label** — measured / inferred in the same sentence, guesses under their own `Unverified:` line, a runnable check is run, not handed over); Subagent Dispatch. Dropped patterns per plan S2.9. Every skill citation of a section keeps resolving, and the gate now proves it: a `` `contracts/<file> § <Section>` `` citation whose section is not a heading in that contract is an error.

**Plan:** `.scratch/plans/OPT_SKAILEUP_MP_SKILL_OPTIMISATION_PLAN.md` — S2 (steps 1–12), decisions D3, D4, D5, D11(f), findings F3, F10; ticket-breakdown row T3.

**Blocked by:** `i-opt-skill-call-convention`

**Status:** resolved

- [ ] The three cited headings survive character for character: `Pattern: Questions Are Standalone Messages`, `Pattern: Subagent Dispatch`, `Pattern: Next-Step Suggestion`.
- [ ] Exactly eight `## Pattern:` headings; the opening paragraph points to the feedback-loop contract for what the dropped Feedback Loop Update said.
- [ ] Any Skill-tool phrasing inside Subagent Dispatch follows the convention from `i-opt-skill-call-convention`.
- [ ] The two bare citations in `architecture-system` and `architecture-datamodel` gain `§ Questions Are Standalone Messages`; the contracts README row is updated per S2.10.
- [ ] Gate rule: section citations are matched across line wraps; a section resolves against a heading equal to it or to `Pattern: <section>`; a miss is an intrinsic error naming file and section.
- [ ] Fixtures: a citation of `§ Nowhere` reports the error; `§ Numbering` against the concept-structure fixture reports nothing.
- [ ] Plan Verification steps 4 and 6 hold (citation list, dead-host vocabulary grep empty); `python scripts/check.py` exits 0.
