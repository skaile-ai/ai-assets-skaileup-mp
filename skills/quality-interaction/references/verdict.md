# The verdict file — `interaction.sarif`

`_concept/11_build/interaction.sarif` is a SARIF 2.1.0 log (OASIS, errata 01) with exactly
one run. SARIF gives the verdict a place for each thing a code scanner already records — rule,
result, location, suppression — so a SARIF viewer or code-scanning upload reads it unchanged;
what SARIF has no field for goes in `properties` bags, which the spec reserves for tool data.

`$schema` is
`https://docs.oasis-open.org/sarif/sarif/v2.1.0/errata01/os/schemas/sarif-schema-2.1.0.json`
and `version` is `"2.1.0"`. The file is written whole each run and is valid JSON: no comments,
no trailing commas.

## Where each field goes

| What | SARIF field | Notes |
|---|---|---|
| the skill | `runs[0].tool.driver.name` = `quality-interaction` | `driver.properties.contract` = `contracts/interaction_patterns.md` |
| rules P1–P17 | `driver.rules[]`: `id` `P1`…, `name`, `shortDescription.text` | all seventeen, whether or not a result cites them |
| a violation | `results[]` with `kind: "fail"`, `ruleId`, `level`, `message.text`, `locations[]` | `level` from `contracts/evaluator.md § SARIF level`; `message.text` is "expected … / actual …" |
| a violation's own data | `result.properties`: `id` (`V-1`), `entry`, `also[]`, `type`, `severity`, `class`, `tag` | `severity` keeps the four-level value; `class` is `consistency` or `completeness`; `tag` is `Qn` or empty |
| an exemplar | `results[]` with `kind: "pass"`, `level: "none"`, `ruleId`, `locations[]` | one per rule where one exists |
| a location | `locations[0].physicalLocation.artifactLocation.uri` + `region.startLine` (`endLine` for a span) | `uri` is repo-relative; an absence cites the nearest line and says `absence: …` in `message.text` |
| a proposed exception | on the violation's result: `suppressions: [{ kind: "external", status: "underReview", justification, properties: { id: "E-1", entry } }]` | `underReview` is the state SARIF defines for "not yet accepted"; the user's answer reaches `APP-DESIGN.md`, never this file |
| run-level data | `runs[0].properties`: `app_design_updated`, `checked_at`, `score`, `changes[]`, `coverage`, `questions[]`, `unchecked[]`, `unread[]` | shapes below |

`runs[0].properties` shapes:

- `score`: `{ "P5": { "violations": 3, "exemplars": 1, "status": "violated", "also": 1 } }`.
  `status` is `violated`, `conformant`, `by-decision` or `unchecked`; `also` appears only when
  other rules file a finding here.
- `changes[]`: `{ "id": "C-1", "kind": "systemic" | "per-type", "title", "covers": ["V-1"],
  "files": ["app/a.vue"], "status": "open" | "done" }`. `build-plan` reads the `open` ones.
- `coverage`: `{ "V-1": "C-1", "V-2": "proposed: E-1" }` — a change id or a proposed exception id.
- `questions[]`: `{ "id": "Q-1", "entry": "OBJ-3", "question", "evidence": "app/c.vue:9" }`.
- `unchecked[]`: rule ids with no violation, no `also` and no exemplar. `unread[]`: region
  strings such as `"app/legacy/**: 40 files, sampled by grep"`.

## Example

```json
{
  "$schema": "https://docs.oasis-open.org/sarif/sarif/v2.1.0/errata01/os/schemas/sarif-schema-2.1.0.json",
  "version": "2.1.0",
  "runs": [{
    "tool": { "driver": {
      "name": "quality-interaction",
      "properties": { "contract": "contracts/interaction_patterns.md" },
      "rules": [
        { "id": "P5", "name": "one-editor-per-object", "shortDescription": { "text": "…" } },
        { "id": "P14", "name": "…", "shortDescription": { "text": "…" } }
      ]
    } },
    "results": [
      { "ruleId": "P5", "kind": "fail", "level": "error",
        "message": { "text": "expected: one editor per Room (MOD-2); actual: Room edited in a modal and a page" },
        "locations": [{ "physicalLocation": {
          "artifactLocation": { "uri": "app/a.vue" }, "region": { "startLine": 12 } } }],
        "properties": { "id": "V-1", "entry": "MOD-2", "also": ["P14"], "type": "Room",
                        "severity": "high", "class": "consistency", "tag": "" } },
      { "ruleId": "P7", "kind": "fail", "level": "note",
        "message": { "text": "expected: …; actual: …" },
        "locations": [{ "physicalLocation": {
          "artifactLocation": { "uri": "app/d.vue" }, "region": { "startLine": 40 } } }],
        "suppressions": [{ "kind": "external", "status": "underReview",
                           "justification": "…",
                           "properties": { "id": "E-1", "entry": "BTN-4" } }],
        "properties": { "id": "V-2", "entry": "BTN-4", "type": "Room",
                        "severity": "low", "class": "consistency", "tag": "" } },
      { "ruleId": "P5", "kind": "pass", "level": "none",
        "message": { "text": "conformant exemplar: single editor component" },
        "locations": [{ "physicalLocation": {
          "artifactLocation": { "uri": "app/b.vue" }, "region": { "startLine": 30, "endLine": 52 } } }] }
    ],
    "properties": {
      "app_design_updated": "YYYY-MM-DD",
      "checked_at": "YYYY-MM-DD",
      "score": { "P5": { "violations": 1, "exemplars": 1, "status": "violated", "also": 0 } },
      "changes": [
        { "id": "C-1", "kind": "systemic", "title": "…", "covers": ["V-1"],
          "files": ["app/a.vue"], "status": "open" }
      ],
      "coverage": { "V-1": "C-1", "V-2": "proposed: E-1" },
      "questions": [{ "id": "Q-1", "entry": "OBJ-3", "question": "…", "evidence": "app/c.vue:9" }],
      "unchecked": ["P12"],
      "unread": ["app/legacy/**: 40 files, sampled by grep"]
    }
  }]
}
```

## Counting

The score is computed, never typed: per `ruleId`, count results with `kind: "fail"` and
`kind: "pass"`, add `also` counts from each fail result's `properties.also`, then write the
object into `runs[0].properties.score`. A short Python `json` script or a `jq` filter does it;
write the results first and let it run last.
