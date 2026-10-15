# i-crt-critique-report: The skill-set critique HTML report

**What to build:** the static report a reader opens to see the verdict, the 44 findings filterable by severity and lens, where each flow's gates break, who writes which artifact, a scorecard, the inventory, and the proposed target shape (re-ordered flow with the domain language and the data model ahead of features, one owner per artifact, workarounds that need no skill edit). Built with the report-html skill (profile `critique`; features tree, data, flow, charts, crossfilter, badge-chart, map) from the dump's data.

**Plan:** .scratch/plans/CRT_SKILL_SET_CRITIQUE_REPORT_PLAN.md — Approach Step 3 (report JSON, entities, badges, seven sections, choice file), Step 4 (build and check), Verification 2–5.

**Blocked by:** i-crt-critique-dump

**Status:** claimed (orchestrator session, 2026-10-16) — generator drafted in parallel against the dump's data contract

Approved breakdown (2026-10-15): 2 tickets — i-crt-critique-dump, then this one (verification merged in here).

- [ ] The build passes with the choice file (all seven features chosen and used) and again with `--strict`; every lint line is fixed or justified.
- [ ] No count in the report is typed by hand: stats, bars, charts and tables come from the dump; only the scorecard ratings are judgement and the report says so.
- [ ] In a browser at 1280 px and 390 px: no horizontal overflow, no console errors; badge toggles drive the tree counter, the stage flow and both charts; a severity bar click filters the findings table and a background click restores it; the gates table sorts and searches; the writer map hides a legend kind, keeps it across reload, and resets; CSV export downloads.
- [ ] The writer map's layout is pasted back so edges do not cross boxes.
- [ ] No skill, contract or flow in the collection is edited.
