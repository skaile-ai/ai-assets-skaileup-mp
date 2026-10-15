# i-crt-critique-dump: Measured data for the skill-set critique

**What to build:** a dump script that reads the collection (skills, contracts, flows, profiles, check.py) and the host's server code and writes the report's data collections — skills, contracts, flows, gates, artifacts, writes, findings, stages — as JSON. Every hand-held row (the writer map and the 44 findings) carries a file:line citation with a quote, and the script refuses to write when a quote is not on its line, so a stale critique cannot be published.

**Plan:** .scratch/plans/CRT_SKILL_SET_CRITIQUE_REPORT_PLAN.md — Approach Step 1 (collections, writer map, re-run rule), Step 2 (findings catalogue F01–F44), Verification 1.

**Blocked by:** None (can start immediately)

**Status:** resolved 2026-10-16 — dump runs green (skills 30 · contracts 13 · flows 4 · gates 152, hard 78, unmet hard 5 · artifacts 14 · writes 51 · findings 44 · stages 10); severity critical 3 / high 13 / medium 21 / low 7 (the plan's prose said 14/20, its own table gives 13/21); a wrong quote aborts with the row and writes nothing.

Approved breakdown (2026-10-15): 2 tickets — this one, then i-crt-critique-report.

- [ ] One run from the repo root writes all eight collections and prints their row counts (skills 30 · contracts 13 · flows 4 · gates 152 with 78 hard · artifacts 14 · findings 44 · stages 10) or the measured numbers where they differ, with the difference explained.
- [ ] Gates mark a hard prerequisite with no upstream producer in its flow as unmet; the unmet hard gates match findings F01–F03 and F35.
- [ ] Every writer-map row and every finding evidence row is asserted against its file and line (±6 line drift corrected in the source data, never by loosening the check); a deliberately wrong quote aborts the run naming the row.
- [ ] Severity and lens counts printed by the run; the report uses these, not the plan's.
- [ ] The run prints the newest source mtime against its own output so a stale dump is visible.
