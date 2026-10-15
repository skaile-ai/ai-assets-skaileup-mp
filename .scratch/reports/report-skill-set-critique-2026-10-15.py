#!/usr/bin/env python3
"""Generate the report-html input for the skaileup-mp skill-set critique.

    python3 .scratch/reports/report-skill-set-critique-2026-10-15.py

Reads   .scratch/reports/skill-set-critique-2026-10-15.data/*.json   (written by dump-skill-set-critique-2026-10-15.py)
Writes  .scratch/reports/skill-set-critique-2026-10-15.json          (report-html input)
        .scratch/reports/skill-set-critique-2026-10-15.choice.json   (feature choice for build.py --check-choice)

Optional: .scratch/reports/skill-set-critique-2026-10-15.map-layout.json = {"pos": {...}, "off": [...]}
(paste of the "Copy layout" button of the `writers` map); it is merged into the map block on every run.

Every number comes from the dump. The only hand-held values are the scorecard ratings and the
"target shape" proposal (owners and order), which are the author's judgement.
"""
import json
import subprocess
import sys
from collections import Counter, OrderedDict
from pathlib import Path

STEM = "skill-set-critique-2026-10-15"
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]  # repo root: .scratch/reports/ -> .scratch/ -> root
DATA = HERE / f"{STEM}.data"
OUT = HERE / f"{STEM}.json"
CHOICE = HERE / f"{STEM}.choice.json"
LAYOUT = HERE / f"{STEM}.map-layout.json"
DUMP = f".scratch/reports/dump-{STEM}.py"

STAGE_ORDER = ["concept", "design", "experience", "spec", "mockup", "architecture", "build", "quality", "ops", "collection"]
SEVS = ["critical", "high", "medium", "low"]
LENSES = ["dup", "alt", "order", "disk", "wayfinding"]
STANDARD = "appbuilder-standard"
# Label of the stage-flow edge into a domain: the artifact that crosses the boundary.
CROSSING = {"design": "brief.md", "experience": "tokens.json", "spec": "stories.yaml", "mockup": "07_screens/",
            "architecture": "09_mockup/", "build": "10_blueprint/", "quality": "11_build/", "ops": "trace.yaml"}
# Scorecard: ratings are the author's judgement (0-10, higher is better); counts are measured.
RATINGS = {"dup": 6, "alt": 4, "order": 2, "disk": 4, "wayfinding": 5, "planning fit": 3}
FEATURES = ["tree", "data", "flow", "charts", "crossfilter", "badge-chart", "map"]

errors = []
warnings = []


def die(msg):
    sys.exit(f"{Path(__file__).name}: {msg}")


def load(name):
    p = DATA / f"{name}.json"
    if not p.is_file():
        die(f"missing {p.relative_to(ROOT)}; run `python3 {DUMP}` from the repo root first")
    rows = json.loads(p.read_text())
    if not isinstance(rows, list):
        die(f"{p.relative_to(ROOT)} is not a JSON array")
    return rows


if not DATA.is_dir():
    die(f"missing {DATA.relative_to(ROOT)}; run `python3 {DUMP}` from the repo root first")

skills = load("skills")
contracts = load("contracts")
flows = load("flows")
gates = load("gates")
artifacts = load("artifacts")
writes = load("writes")
findings = load("findings")
stages = load("stages")

# -- helpers ---------------------------------------------------------------------------------
stem_of = lambda cid: cid[2:] if cid.startswith("c-") else cid
cid_of = lambda stem: "c-" + stem_of(stem)
plural = lambda n, w: f"{n} {w}" + ("" if n == 1 else "s")
domain_of = lambda sid: sid.split("-", 1)[0].replace("skaileup", "collection")
short = lambda s: s.split("/")[-1].split(":")[-1]  # '@skaile-ai/concept-scope' -> 'concept-scope'


def unmet_hard(g):
    return bool(g["unmet_hard"]) if "unmet_hard" in g else (g.get("gate") == "hard" and not g.get("satisfied"))


def dedupe(seq):
    return list(OrderedDict.fromkeys(seq))


def code_at(at):
    return f"`{at}`" if at else "—"


def short_path(p):
    """`_concept/07_screens/` -> `07_screens/`; a folder keeps a trailing slash."""
    p = p[len("_concept/"):] if p.startswith("_concept/") else p
    return p if p.endswith("/") or "." in p.rsplit("/", 1)[-1] else p + "/"


skill_ids = [s["id"] for s in skills]
skill_set = set(skill_ids)
contract_ids = [cid_of(c["id"]) for c in contracts]
contract_set = set(contract_ids)
flow_ids = [f["id"] for f in flows]
flow_set = set(flow_ids)
artifact_ids = [a["id"] for a in artifacts]
artifact_set = set(artifact_ids)
finding_ids = [f["id"] for f in findings]
stage_ids = ["s-" + d for d in STAGE_ORDER]
stage_set = set(stage_ids)
stage_row = {s["id"]: s for s in stages}
for sid in stage_ids:
    if sid not in stage_row:
        errors.append(f"stages.json has no row {sid}")
entity_ids = set(skill_ids) | set(contract_ids) | set(flow_ids) | set(artifact_ids) | set(finding_ids) | stage_set
if len(entity_ids) != len(skill_ids) + len(contract_ids) + len(flow_ids) + len(artifact_ids) + len(finding_ids) + len(stage_ids):
    errors.append("entity ids collide across skills, contracts, flows, artifacts, findings, stages")


def L(eid, text=None):
    """[[id]] link when the entity exists, else plain code (with a warning)."""
    if eid in entity_ids:
        return f"[[{eid}|{text}]]" if text else f"[[{eid}]]"
    warnings.append(f"prose link to unknown entity {eid}")
    return f"`{eid}`"


def links(ids, sep=", "):
    return sep.join(L(i) for i in ids)


by_skill = {s["id"]: s for s in skills}
by_artifact = {a["id"]: a for a in artifacts}
by_flow = {f["id"]: f for f in flows}

# -- validate findings -----------------------------------------------------------------------
for f in findings:
    if f["sev"] not in SEVS:
        errors.append(f"{f['id']}: sev {f['sev']!r}")
    if f["lens"] not in LENSES:
        errors.append(f"{f['id']}: lens {f['lens']!r}")
    if f["stage"] not in stage_set:
        errors.append(f"{f['id']}: stage {f['stage']!r}")
    if len(f["title"]) > 80:
        warnings.append(f"{f['id']}: title has {len(f['title'])} chars (> 80)")
    for key, known in (("skills", skill_set), ("contracts", contract_set), ("flows", flow_set), ("artifacts", artifact_set)):
        for x in f.get(key, []):
            if x not in known:
                errors.append(f"{f['id']}: {key} entry {x!r} is no entity")
    if not f.get("evidence"):
        errors.append(f"{f['id']}: no evidence")


def finding_refs(f):
    refs = [*f.get("skills", []), *f.get("contracts", []), *f.get("flows", []), *f.get("artifacts", []), *f.get("refs", [])]
    out = []
    for r in dedupe(refs):
        if r == f["id"]:
            continue
        if r not in entity_ids:
            errors.append(f"{f['id']}: ref {r!r} is no entity")
            continue
        out.append(r)
    return out


# -- counts from the data --------------------------------------------------------------------
n_find = len(findings)
sev_n = Counter(f["sev"] for f in findings)
lens_n = Counter(f["lens"] for f in findings)
lens_hi = Counter(f["lens"] for f in findings if f["sev"] in ("critical", "high"))
stage_n = Counter(f["stage"] for f in findings)
skill_findings = {sid: [f["id"] for f in findings if sid in f.get("skills", [])] for sid in skill_ids}
n_stage_with = sum(1 for s in stage_ids if stage_n[s])
for s in stage_ids:
    if not stage_n[s]:
        warnings.append(f"stage {s} has no finding: the tree counts it as a leaf")
unmet = [g for g in gates if unmet_hard(g)]
unmet_by_flow = Counter(g["flow"] for g in unmet)
multi = [a for a in artifacts if a.get("multi_writer")]
contract_lines = {cid_of(c["id"]): c["lines"] for c in contracts}
longest = max(skills, key=lambda s: s["lines"])
max_contracts = max(skills, key=lambda s: s.get("contracts_n", len(s.get("contracts", []))))
elements_lines = contract_lines.get("c-elements_block", 0) + contract_lines.get("c-walkthrough_renderer", 0)

# -- badges ----------------------------------------------------------------------------------
badges = {
    "sev": {"label": "Severity", "shape": "square", "filter": "any", "values": {
        "critical": {"color": "red", "desc": "a flow or gate that fails today"},
        "high": {"color": "orange", "desc": "wrong order, two writers, reasons lost"},
        "medium": {"color": "yellow", "desc": "double home, late write, volume"},
        "low": {"color": "gray", "desc": "restated text, small gap"}}},
    "lens": {"label": "Lens", "shape": "pill", "filter": "any", "values": {
        "dup": {"color": "purple", "desc": "same text in two skills"},
        "alt": {"color": "teal", "desc": "two ways or homes for one thing"},
        "order": {"color": "blue", "desc": "hierarchy / sequence"},
        "disk": {"color": "pink", "desc": "not persisted or not editor-visible"},
        "wayfinding": {"color": "brown", "desc": "reads before acting"}}},
}

# -- entities --------------------------------------------------------------------------------
entities = []
for i, sid in enumerate(stage_ids, 1):
    r = stage_row.get(sid, {})
    entities.append({"id": sid, "title": sid[2:], "order": i,
                     "meta": [plural(r.get("skills_n", 0), "skill"), f"{r.get('lines', 0)} lines"]})
for n, f in enumerate(findings, 1):
    entities.append({"id": f["id"], "parent": f["stage"], "order": n, "title": f["title"], "label": f["id"],
                     "badges": {"sev": [f["sev"]], "lens": [f["lens"]]},
                     "meta": [code_at(f.get("first_at") or f["evidence"][0]["at"])],
                     "refs": finding_refs(f)})
for s in skills:
    refs = [c if c.startswith("c-") else cid_of(c.replace("contracts/", "").replace(".md", "")) for c in s.get("contracts", [])]
    refs = [c for c in dedupe(refs) if c in contract_set] + [x for x in s.get("flows", []) if x in flow_set]
    entities.append({"id": s["id"], "title": s["id"], "tree": False,
                     "meta": [f"{s['lines']} lines · {s['steps']} steps", s.get("phase") or "none"], "refs": refs})
for c in contracts:
    entities.append({"id": cid_of(c["id"]), "title": c.get("file") or f"{stem_of(c['id'])}.md", "label": f"{stem_of(c['id'])}.md", "tree": False,
                     "meta": [f"{c['lines']} lines"]})
for f in flows:
    entities.append({"id": f["id"], "title": f["id"], "tree": False,
                     "meta": [f"{f['nodes_n']} nodes", f"research_depth: {f.get('research_depth')}"]})
for a in artifacts:
    entities.append({"id": a["id"], "title": a["path"], "label": short_path(a["path"]), "tree": False, "meta": [a["editor_form"]],
                     "refs": [w for w in a.get("writers", []) if w in skill_set]})

# -- stats -----------------------------------------------------------------------------------
stats = [
    ["Skills", {"count": "skills"}],
    ["Contracts", {"count": "contracts"}],
    ["Flows", {"count": "flows"}],
    ["Findings", {"count": "findings"}],
    ["Critical", {"count": "findings", "where": {"sev": "critical"}}],
    ["Unmet hard gates", {"count": "gates", "where": {"unmet_hard": True}}],
    ["Multi-writer artifacts", {"count": "artifacts", "where": {"multi_writer": True}}],
]

# -- section 1: the answer -------------------------------------------------------------------
std = by_flow.get(STANDARD)
if std is None:
    errors.append(f"flows.json has no {STANDARD}")
broken_flows = len(unmet_by_flow)
verdict = " ".join([
    "The collection has the right skills in the wrong order.",
    f"The domain vocabulary gets its final form last ({L('F08')}, {L('F30')}), and the data model comes after every feature and screen ({L('F17')}).",
    f"In {broken_flows} of {len(flows)} flows, a hard gate has no upstream node that satisfies it ({L('F01')}, {L('F02')}, {L('F03')}), and `check.py` does not look ({L('F04')}).",
    f"The editor cannot tell a finished node from the files, because no skill declares what it produces ({L('F05')}).",
    f"The reasons behind artifacts and the approvals stay in chat ({L('F13')}, {L('F23')}).",
    f"The review holds {n_find} findings: {sev_n['critical']} critical, {sev_n['high']} high, {sev_n['medium']} medium, {sev_n['low']} low.",
])
right = [
    f"The skills are flat: {len(skills)} skills in one directory level, and the longest ({L(longest['id'])}) has {longest['lines']} lines.",
    f"One artifact tree holds all {len(artifacts)} targets, from {L('a-brief')} to {L('a-11_build')}, so every skill writes to a known place.",
    f"`scripts/check.py` is the single gate of the collection; its flow rule has one gap ({L('F04')}).",
    "The glossary format keeps an `_Avoid_` list per term, so a rejected word has a home.",
    "A decision enters `decisions.md` only after the three-test check.",
    f"Feature dossiers are frozen records of the reasons ({L('a-08_dossiers')}).",
]
sec_answer = {"title": "The answer", "sub": "right pieces, wrong order", "blocks": [
    {"type": "p", "text": verdict},
    {"type": "p", "text": "What is already right:"},
    {"type": "bullets", "items": right},
]}

# -- section 2: findings ---------------------------------------------------------------------
if std:
    nl = {short(k): v for k, v in std.get("node_lines", {}).items()}
    seq = [domain_of(s) for s in std["order"]]
    dom_order = dedupe(d for d in seq if d in STAGE_ORDER and d != "collection")
    first_skill = {}
    for s in std["order"]:
        first_skill.setdefault(domain_of(s), s)
    flow_edges = []
    for a, b in zip(dom_order, dom_order[1:]):
        node = first_skill[b]
        if node not in nl:
            errors.append(f"{STANDARD} node_lines has no line for {node}")
            continue
        flow_edges.append({"from": "s-" + a, "to": "s-" + b, "label": CROSSING.get(b, ""),
                           "at": f"flows/{STANDARD}/{STANDARD}.flow.yaml:{nl[node]}"})
else:
    flow_edges = []
pipeline_nodes = []
for sid in stage_ids:
    node = {"id": sid, "label": sid[2:], "ref": sid, "sub": plural(stage_n[sid], "finding")}
    if sid == "s-collection":
        node.update({"shape": "external", "sub": f"{plural(stage_row.get('s-collection', {}).get('findings_n', stage_n[sid]), 'finding')} · flows, contracts, host"})
    pipeline_nodes.append(node)

sev_rows = [{"id": f["id"], "sev": f["sev"]} for f in findings]
lens_rows = [{"id": f["id"], "lens": f["lens"]} for f in findings]


def bar_spec(field, rows, title, order, select=True):
    spec = {
        "mark": {"type": "bar", "tooltip": True, "color": "#0969da"},
        "height": 200,
        "data": {"values": rows},
        "encoding": {
            "x": {"field": field, "type": "nominal", "title": title, "sort": order, "axis": {"labelAngle": 0}},
            "y": {"aggregate": "count", "type": "quantitative", "title": "Findings"},
        },
    }
    if select:
        spec["params"] = [{"name": "pick", "select": {"type": "point", "fields": [field]}}]
        spec["encoding"]["opacity"] = {"condition": {"param": "pick", "value": 1}, "value": 0.35}
    return spec


rows_findings = []
for f in findings:
    rows_findings.append({
        "id": f["id"], "title": f["title"], "sev": f["sev"], "lens": f["lens"],
        "stage": {"ref": f["stage"], "text": f["stage"][2:]},
        "skills": {"refs": f.get("skills", [])},
        "detail": f.get("detail", ""),
        "evidence": code_at(f.get("first_at") or f["evidence"][0]["at"]),
        "recommendation": f["recommendation"],
    })

sec_findings = {"title": "Findings", "sub": "toggle a badge, read the stages, filter the table", "blocks": [
    {"type": "p", "text": f"The review holds {n_find} findings in {n_stage_with} stages. Toggle a severity or lens badge: the stage flow and both charts follow. "
                          "Click a bar in the severity chart: the table keeps the rows of that severity."},
    {"type": "tree", "filter": ["sev", "lens"], "count_label": "findings visible",
     "hint": "the stage flow and the charts below follow the badges", "drives": ["pipeline", "sev-chart", "lens-chart"]},
    {"type": "flow", "id": "pipeline", "label": "Stages of the standard flow, findings per stage", "dir": "down",
     "nodes": pipeline_nodes, "edges": flow_edges},
    {"type": "p", "text": "The bars count the findings of each stage."},
    {"type": "bars", "items": [[s, stage_n[s], "blue"] for s in stage_ids]},
    {"type": "vega", "id": "sev-chart", "label": "Findings by severity", "entity": "id",
     "spec": bar_spec("sev", sev_rows, "Severity", [s for s in SEVS if sev_n[s]])},
    {"type": "vega", "id": "lens-chart", "label": "Findings by lens", "entity": "id",
     "spec": bar_spec("lens", lens_rows, "Lens", [l for l, _ in lens_n.most_common()])},
    {"type": "data", "id": "findings", "label": "All findings", "key": "id", "page": 25,
     "columns": [{"label": "ID", "key": "id"}, {"label": "Title", "key": "title"},
                 {"label": "Severity", "key": "sev"}, {"label": "Lens", "key": "lens"},
                 {"label": "Stage", "key": "stage"}, {"label": "Skills", "key": "skills"},
                 {"label": "Detail", "key": "detail"}, {"label": "Evidence", "key": "evidence"},
                 {"label": "Recommendation", "key": "recommendation"}],
     "rows": rows_findings,
     "listen": {"chart": "sev-chart", "param": "pick", "field": "sev"}},
]}

# -- section 3: where the flows break --------------------------------------------------------
n_hard = sum(1 for g in gates if g.get("gate") == "hard")
per_flow = ", ".join(f"{L(fid)}: {unmet_by_flow[fid]}" for fid in flow_ids if unmet_by_flow[fid])
gate_rows = []
for g in sorted(gates, key=lambda g: (bool(g["satisfied"]), g.get("gate") != "hard", g["flow"], g["position"])):
    gate_rows.append({
        "flow": {"ref": g["flow"]}, "position": g["position"], "skill": {"ref": g["skill"]},
        "path": f"`{g['path']}`", "gate": g["gate"],
        "producer": {"ref": g["producer"]} if g.get("producer") else "—",
        "satisfied": g.get("satisfied_s") or ("yes" if g["satisfied"] else "no"),
        "prereq_at": code_at(g.get("prereq_at")),
    })
sec_gates = {"title": "Where the flows break", "sub": "every prerequisite of every flow node", "blocks": [
    {"type": "p", "text": f"{len(unmet)} of {n_hard} hard gates have no producer upstream in the flow that runs them. By flow: {per_flow}. "
                          f"`scripts/check.py` has no rule for this ({L('F04')}). The producer is the nearest upstream skill whose declared write target covers the path."},
    {"type": "data", "id": "gates", "label": "Every prerequisite of every flow node", "page": 25,
     "columns": [{"label": "Flow", "key": "flow"}, {"label": "Pos", "key": "position", "type": "number"},
                 {"label": "Skill", "key": "skill"}, {"label": "Path", "key": "path"}, {"label": "Gate", "key": "gate"},
                 {"label": "Producer", "key": "producer"}, {"label": "Satisfied", "key": "satisfied"},
                 {"label": "Prerequisite at", "key": "prereq_at"}],
     "rows": gate_rows},
]}

# -- section 4: who writes what --------------------------------------------------------------
art_match = []  # (match prefix, artifact id), longest first
for a in artifacts:
    p = a["path"]
    folder = p.endswith("/") or "." not in p.rsplit("/", 1)[-1]
    art_match.append((p.rstrip("/") + "/" if folder else p, folder, a["id"]))
art_match.sort(key=lambda t: -len(t[0]))


def artifact_of(path):
    if not path:
        return None
    for pref, folder, aid in art_match:
        if (folder and (path.rstrip("/") + "/").startswith(pref)) or (not folder and path == pref):
            return aid
    return None


edge_map = OrderedDict()  # (from, to, kind) -> [at, ...]
for w in writes:
    aid = w.get("artifact") if w.get("artifact") in artifact_set else artifact_of(w.get("path"))
    if aid is None or w["skill"] not in skill_set:
        continue
    edge_map.setdefault((w["skill"], aid, "write"), []).append(w["at"])
gate_at = {(g["skill"], g["path"]): g.get("prereq_at") for g in gates}
gate_edges = OrderedDict()
for s in skills:
    for p in s.get("prereqs", []):
        aid = artifact_of(p["path"])
        if aid is None:
            continue
        kind = p["gate"]
        if kind not in ("hard", "soft"):
            errors.append(f"{s['id']}: prerequisite gate {kind!r}")
            continue
        at = p.get("at") or gate_at.get((s["id"], p["path"]))
        if not at:
            errors.append(f"{s['id']}: prerequisite {p['path']} has no `at`")
            continue
        gate_edges.setdefault((aid, s["id"], kind), []).append(at)
for (aid, sid, kind), ats in list(gate_edges.items()):
    if kind == "soft" and (aid, sid, "hard") in gate_edges:
        del gate_edges[(aid, sid, kind)]  # keep the stronger edge between one pair
edge_map.update(gate_edges)
map_edges = [{"from": a, "to": b, "kind": k, "at": ", ".join(dedupe(ats))} for (a, b, k), ats in edge_map.items()]
map_nodes = [{"id": s["id"], "ref": s["id"], "shape": "process", "sub": domain_of(s["id"])} for s in skills]
map_nodes += [{"id": a["id"], "ref": a["id"], "shape": "external", "label": a["path"], "sub": a["editor_form"]} for a in artifacts]
map_block = {"type": "map", "id": "writers", "label": "Skills → artifact targets", "nodes": map_nodes, "edges": map_edges,
             "kinds": {"write": {"label": "writes", "color": "blue"},
                       "hard": {"label": "hard gate", "color": "red"},
                       "soft": {"label": "soft gate", "color": "gray", "dash": "dash"}},
             "off": []}
if LAYOUT.is_file():
    lay = json.loads(LAYOUT.read_text())
    ids = {n["id"] for n in map_nodes}
    pos = {k: v for k, v in lay.get("pos", {}).items() if k in ids}
    off = [k for k in lay.get("off", []) if k in ids]
    if len(pos) != len(lay.get("pos", {})):
        warnings.append("map-layout.json: dropped pos entries for unknown nodes")
    if pos:
        map_block["pos"] = pos
    map_block["off"] = off

sec_map = {"title": "Who writes what", "sub": "30 skills, the targets they write and the gates they read", "blocks": [
    {"type": "p", "text": f"{plural(len(skills), 'skill')} write to or read from {len(artifacts)} targets. {len(multi)} targets have more than one writer: "
                          f"{links([a['id'] for a in multi])}. Edge kinds: write, hard gate, soft gate. Click a legend entry to hide a kind."},
    map_block,
]}

# -- section 5: scorecard --------------------------------------------------------------------
why = {
    "dup": f"The same text sits in several skills, for example the one-question rule ({L('F14')}). No runtime effect.",
    "alt": f"{lens_n['alt']} findings name a double home, among them permissions ({L('F19')}), EARS criteria ({L('F20')}) and mockups ({L('F26')}).",
    "order": f"Gate cycle ({L('F17')}), glossary last ({L('F08')}), {broken_flows} broken flows ({L('F01')}).",
    "disk": f"Artifacts land on disk; reasons and approvals do not ({L('F13')}). The editor cannot derive done ({L('F05')}).",
    "wayfinding": f"{L(max_contracts['id'])} cites {max_contracts.get('contracts_n', len(max_contracts.get('contracts', [])))} contracts; two contracts hold {elements_lines} lines ({L('F07')}).",
    "planning fit": f"Features come before the model ({L('F17')}); no skill lists what it produces ({L('F05')}).",
}
score_rows = []
for lens in LENSES:
    score_rows.append([{"badge": ["lens", lens]}, lens_n[lens], lens_hi[lens], RATINGS[lens], why[lens]])
score_rows.append(["planning fit (all findings)", n_find, sum(lens_hi.values()), RATINGS["planning fit"], why["planning fit"]])
sec_score = {"title": "Scorecard", "sub": "counts are measured, ratings are judged", "blocks": [
    {"type": "p", "text": "The counts come from the dump. The ratings are the author's judgement: 10 is best, 0 is worst."},
    {"type": "table", "columns": ["Lens", "Findings", "Critical+high", "Rating 0–10", "Why"], "numeric": [1, 2, 3], "rows": score_rows},
]}

# -- section 6: inventory --------------------------------------------------------------------
skill_rows = []
for s in skills:
    skill_rows.append({"anchor": s["id"], "cells": [
        f"`{s['id']}`", s["lines"], s["steps"], s.get("hard_n", 0), s.get("soft_n", 0),
        s.get("contracts_n", len(s.get("contracts", []))), len(s.get("flows", [])), {"refs": skill_findings[s["id"]]}]})
contract_rows = [{"anchor": cid_of(c["id"]), "cells": [
    f"`{c.get('file') or stem_of(c['id']) + '.md'}`", c["lines"], {"refs": [r for r in c.get("readers", []) if r in skill_set]}]} for c in contracts]
flow_rows = []
for f in flows:
    n_unmet = f["unmet_hard"] if "unmet_hard" in f else unmet_by_flow[f["id"]]
    flow_rows.append({"anchor": f["id"], "cells": [
        f"`{f['id']}`", f["nodes_n"], " → ".join(L(s) for s in f["order"]), n_unmet]})
artifact_rows = [{"anchor": a["id"], "cells": [
    f"`{a['path']}`", a["editor_form"], {"refs": [w for w in a.get("writers", []) if w in skill_set]},
    a.get("readers_n", len(a.get("readers", [])))]} for a in artifacts]
sec_inventory = {"title": "Inventory", "sub": "every skill, contract, flow and artifact target", "blocks": [
    {"type": "p", "text": f"Skills: {len(skills)} rows. The Findings column lists the findings that name the skill."},
    {"type": "table", "columns": ["Skill", "Lines", "Steps", "Hard gates", "Soft gates", "Contracts", "Flows", "Findings"],
     "numeric": [1, 2, 3, 4, 5, 6], "rows": skill_rows},
    {"type": "p", "text": f"Contracts: {len(contracts)} files, {sum(c['lines'] for c in contracts)} lines. The Readers column lists the skills that cite the file."},
    {"type": "table", "columns": ["File", "Lines", "Readers"], "numeric": [1], "rows": contract_rows},
    {"type": "p", "text": f"Flows: {len(flows)}. The order is the path of `type: flow` edges from the entry node."},
    {"type": "table", "columns": ["Flow", "Nodes", "Order", "Unmet hard gates"], "numeric": [1, 3], "rows": flow_rows},
    {"type": "p", "text": f"Artifact targets: {len(artifacts)}. The editor form is how the editor shows the files that the tree lists under the path."},
    {"type": "table", "columns": ["Path", "Editor form", "Writers", "Readers"], "numeric": [3], "rows": artifact_rows},
]}

# -- section 7: target shape -----------------------------------------------------------------
proposal_steps = [
    f"{L('concept-scope')} and {L('concept-onboard')}: `answers.json` is the one record of every answer ({L('F06')}, {L('F16')}).",
    f"{L('concept-brief')}: `brief.md` and `goals.md`. {L('concept-reverse')} writes findings only ({L('F09')}).",
    f"Domain language (new): `_concept/glossary.md`, first level, one writer. Every later skill reads it first ({L('F08')}, {L('F30')}).",
    f"{L('concept-research')} runs alongside, before brand and journeys ({L('F12')}).",
    f"{L('experience-journeys')}: stories use glossary terms and carry no `candidate_entities` ({L('F18')}).",
    f"Data model: {L('architecture-datamodel')} moves ahead of the features (`10_blueprint/datamodel/`, conceptually `05_datamodel/`). It names entities from the glossary only, and `feature-map.json` goes ({L('F17')}, {L('F33')}).",
    f"{L('spec-featuresets')} and {L('experience-behaviors')} read the entities and never coin names ({L('F18')}, {L('F19')}).",
    f"{L('architecture-techstack')} and {L('architecture-system')} run before any renderer ({L('F02')}, {L('F32')}).",
    f"Feature loop with {L('spec-feature')}: spec and screens. The dossier opens at step 2 ({L('F23')}).",
    f"{L('experience-shell')} runs after the loop. Navigation comes from real screens ({L('F25')}).",
    f"{L('mockup-walkthrough')} is the one mockup renderer, then {L('mockup-annotate')} and {L('mockup-feedback')} ({L('F26')}).",
    f"Build: {L('build-scaffold')}, {L('build-database')}, {L('build-plan')}, {L('build-implement')}.",
    f"Quality: {L('quality-test')}, {L('quality-e2e')}, {L('quality-review')}.",
    f"{L('ops-review')} and {L('quality-release')}. `trace.yaml` is the single trace ({L('F36')}).",
]

PROSE = "prose (TipTap)"
CODE = "code editor"


def writers_of(*needles):
    """Skills whose write row path contains one of the needles."""
    return dedupe(w["skill"] for w in writes if w.get("path") and any(n in w["path"] for n in needles) and w["skill"] in skill_set)


# artifact id -> (proposed owners, change text)
PLAN = {
    "a-brief": (["concept-brief"], f"One owner. {L('concept-reverse')} stops writing it ({L('F09')})."),
    "a-goals": (["concept-brief"], f"One owner. {L('concept-reverse')} stops writing it ({L('F09')})."),
    "a-comparable": (["concept-brief"], f"One file for competitor knowledge, shared with `research/competitors.md` ({L('F10')})."),
    "a-01_meta": (["concept-scope"], "No change: one writer."),
    "a-02_grounding": (["concept-onboard", "concept-research", "quality-standards"],
                       f"One owner per subfolder: `onboarding/`, `research/` and `findings/`, `standards/`. Screenshots live in `findings/` only ({L('F11')})."),
    "a-03_brand": (["design-brand"], f"{L('concept-reverse')} stops writing `identity.md` and `tokens.json` ({L('F09')})."),
    "a-04_journeys": (["experience-journeys"], f"Stories carry the criterion id; spec and ledger cite it ({L('F20')})."),
    "a-05_features": (["spec-feature"], f"The feature spec has one owner. The data model no longer writes into it ({L('F17')}, {L('F33')})."),
    "a-06_behaviors": (["experience-behaviors"], f"Permissions move to the feature spec ({L('F19')})."),
    "a-07_screens": (["spec-feature"], f"Shell runs after the loop ({L('F25')}). Feedback patches through the contract ({L('F28')})."),
    "a-08_dossiers": (["spec-feature"], f"Open at step 2, append per step ({L('F23')})."),
    "a-09_mockup": (["mockup-walkthrough"], f"One renderer ({L('F26')}); one annotation schema ({L('F27')})."),
    "a-10_blueprint": (["architecture-techstack", "architecture-system", "architecture-datamodel"],
                       f"One owner per file. `glossary.md` leaves the folder ({L('F08')})."),
    "a-11_build": (["build-plan", "quality-review", "ops-review", "quality-release"],
                   f"One owner per subfolder or file: `slices/` and `acceptance-criteria/`, `reviews/`, `trace.yaml`, `release.yaml` ({L('F36')}, {L('F37')})."),
}
owner_rows = []
for a in artifacts:
    owners, change = PLAN.get(a["id"], (None, None))
    if owners is None:
        errors.append(f"PLAN has no row for artifact {a['id']}")
        continue
    cell = {"ref": owners[0]} if len(owners) == 1 else {"refs": owners}
    owner_rows.append([f"`{a['path']}`", {"refs": [w for w in a.get("writers", []) if w in skill_set]}, cell, a["editor_form"], change])
EXTRA = [
    ("`_concept/glossary.md` (new)", writers_of("glossary.md"), ["concept-brief"], PROSE,
     f"New: first-level file, written by one domain-language step after the brief; every later writer reads it ({L('F08')})."),
    ("`_concept/02_grounding/onboarding/answers.json`", writers_of("02_grounding/onboarding/"), ["concept-onboard"], CODE,
     f"The record of every answer and approval; seeded from the host's `_grounding/<step>/user_input.json` ({L('F06')}, {L('F13')})."),
    ("`_concept/11_build/acceptance-criteria/`", writers_of("acceptance-criteria"), ["build-plan"], PROSE,
     f"`build-plan` owns the rows; the others flip a `status` field ({L('F37')})."),
    ("`_concept/11_build/trace.yaml`", writers_of("trace.yaml"), ["ops-review"], CODE,
     f"The single trace of feature to code ({L('F36')})."),
]
for label, today, proposed, form, change in EXTRA:
    owner_rows.append([label, {"refs": today}, {"ref": proposed[0]}, form, change])
for o in [x for _, _, ps, _, _ in EXTRA for x in ps] + [x for ps, _ in PLAN.values() for x in ps]:
    if o not in skill_set:
        errors.append(f"proposal names unknown skill {o}")

workarounds = [
    f"Run {L('experience-journeys')} by hand before {L('spec-featuresets')} in {L('appbuilder-mvp')} ({L('F01')}).",
    f"Run {L('architecture-techstack')} before {L('mockup-storybook')} in {L('appbuilder-standard')} ({L('F02')}).",
    f"Create `_concept/01_meta/scope.yaml` by hand before {L('spec-feature')} in {L('skaileup-concept-reverse')} ({L('F03')}).",
    f"For a project whose profile does not grow screens (cli-tool, api-service, library, data-pipeline), create an empty `_concept/07_screens/` so the hard gates of {L('build-plan')} and {L('build-implement')} open ({L('F35')}).",
    f"Copy `_grounding/<step>/user_input.json` into `answers.json` at onboarding ({L('F06')}).",
]
sec_target = {"title": "Target shape", "sub": "one hierarchy, one owner per artifact", "blocks": [
    {"type": "p", "text": f"The principle: one hierarchy (domain language, data model, features, screens), one owner per artifact, and every decision of the user lands in a markdown file that the editor opens ({L('F08')}, {L('F17')}, {L('F13')})."},
    {"type": "p", "text": "Proposed order of the standard flow:"},
    {"type": "steps", "items": proposal_steps},
    {"type": "p", "text": f"One owner per artifact. The first {len(artifacts)} rows are the artifact targets; the other rows are files that today have several writers or no home."},
    {"type": "table", "columns": ["Artifact", "Owner today", "Owner proposed", "Editor form", "Change"], "rows": owner_rows},
    {"type": "p", "text": "Workarounds today (no skill edited):"},
    {"type": "bullets", "items": workarounds},
]}

# -- assemble --------------------------------------------------------------------------------
if errors:
    die("data problems:\n  " + "\n  ".join(dict.fromkeys(errors)))

try:
    sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
except (OSError, subprocess.CalledProcessError):
    sha = "unknown"

report = {
    "title": "skaileup-mp — skill-set critique",
    "lang": "en",
    "profile": "critique",
    "numbered": True,
    "meta": [f"Source: ai-assets-skaileup-mp @ {sha}, skaile-forge/server for host facts",
             f"Dump: 2026-10-15, dump-{STEM}.py"],
    "stats": stats,
    "badges": badges,
    "entities": entities,
    "sections": [sec_answer, sec_findings, sec_gates, sec_map, sec_score, sec_inventory, sec_target],
}
OUT.write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n")
CHOICE.write_text(json.dumps({"profile": "critique", "features": FEATURES}, indent=1) + "\n")
for w in dict.fromkeys(warnings):
    print(f"warning: {w}", file=sys.stderr)
print(f"{OUT.relative_to(ROOT)}: {len(entities)} entities "
      f"({len(stage_ids)} stages, {n_find} findings, {len(skills)} skills, {len(contracts)} contracts, {len(flows)} flows, {len(artifacts)} artifacts), "
      f"{len(map_edges)} map edges, {len(gate_rows)} gate rows")
print(f"{CHOICE.relative_to(ROOT)}: {len(FEATURES)} features")
