#!/usr/bin/env python3
"""Generate the report-html input for the skaileup-mp skill-set critique.

    python3 .scratch/reports/report-skill-set-critique-2026-10-15.py

Reads   .scratch/reports/skill-set-critique-2026-10-15.data/*.json   (written by dump-skill-set-critique-2026-10-15.py)
Writes  .scratch/reports/skill-set-critique-2026-10-15.json          (report-html input)
        .scratch/reports/skill-set-critique-2026-10-15.choice.json   (feature choice for build.py --check-choice; written once, never overwritten)

Optional: .scratch/reports/skill-set-critique-2026-10-15.map-layout.json = {"pos": {...}, "off": [...]}
(paste of the "Copy layout" button of the `writers` map); it is merged into the map block on every run.

Every number comes from the dump. The only hand-held values are the scorecard ratings and the
"target shape" proposal (owners and order), which are the author's judgement.
"""
import json
import subprocess
import sys
from collections import Counter, OrderedDict
from datetime import datetime
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
finding_ids = [f["id"] for f in findings]
stage_ids = ["s-" + d for d in STAGE_ORDER]
stage_set = set(stage_ids)
stage_row = {s["id"]: s for s in stages}
entity_ids = set(skill_ids) | set(contract_ids) | set(flow_ids) | set(artifact_ids) | set(finding_ids) | stage_set
if len(entity_ids) != len(skill_ids) + len(contract_ids) + len(flow_ids) + len(artifact_ids) + len(finding_ids) + len(stage_ids):
    errors.append("entity ids collide across skills, contracts, flows, artifacts, findings, stages")


def link(eid, text=None):
    """[[id]] link when the entity exists, else plain code (with a warning)."""
    if eid in entity_ids:
        return f"[[{eid}|{text}]]" if text else f"[[{eid}]]"
    warnings.append(f"prose link to unknown entity {eid}")
    return f"`{eid}`"


def links(ids, sep=", "):
    return sep.join(link(i) for i in ids)


by_flow = {f["id"]: f for f in flows}


def finding_refs(f):
    refs = [*f["skills"], *f["contracts"], *f["flows"], *f["artifacts"], *f["refs"]]
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
unmet = [g for g in gates if g["unmet_hard"]]
unmet_by_flow = Counter(g["flow"] for g in unmet)
multi = [a for a in artifacts if a["multi_writer"]]
contract_lines = {cid_of(c["id"]): c["lines"] for c in contracts}
longest = max(skills, key=lambda s: s["lines"])
max_contracts = max(skills, key=lambda s: s["contracts_n"])
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
    r = stage_row[sid]
    entities.append({"id": sid, "title": sid[2:], "order": i,
                     "meta": [plural(r["skills_n"], "skill"), f"{r['lines']} lines"]})
for n, f in enumerate(findings, 1):
    entities.append({"id": f["id"], "parent": f["stage"], "order": n, "title": f["title"], "label": f["id"],
                     "badges": {"sev": [f["sev"]], "lens": [f["lens"]]},
                     "meta": [code_at(f["first_at"])],
                     "refs": finding_refs(f)})
for s in skills:
    refs = [c if c.startswith("c-") else cid_of(c.replace("contracts/", "").replace(".md", "")) for c in s["contracts"]]
    refs = [c for c in dedupe(refs) if c in contract_set] + [x for x in s["flows"] if x in flow_set]
    entities.append({"id": s["id"], "title": s["id"], "tree": False,
                     "meta": [f"{s['lines']} lines · {s['steps']} steps", s["phase"]], "refs": refs})
for c in contracts:
    entities.append({"id": cid_of(c["id"]), "title": c["file"], "label": f"{stem_of(c['id'])}.md", "tree": False,
                     "meta": [f"{c['lines']} lines"]})
for f in flows:
    entities.append({"id": f["id"], "title": f["id"], "tree": False,
                     "meta": [f"{f['nodes_n']} nodes", f"research_depth: {f['research_depth']}"]})
for a in artifacts:
    entities.append({"id": a["id"], "title": a["path"], "label": short_path(a["path"]), "tree": False, "meta": [a["editor_form"]],
                     "refs": [w for w in a["writers"] if w in skill_set]})

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
if STANDARD not in by_flow:
    die(f"flows.json has no {STANDARD}")
std = by_flow[STANDARD]
broken_flows = len(unmet_by_flow)
verdict = " ".join([
    "The collection has the right skills in the wrong order.",
    f"The domain vocabulary gets its final form last ({link('F08')}, {link('F30')}), and the data model comes after every feature and screen ({link('F17')}).",
    f"In {broken_flows} of {len(flows)} flows, a hard gate has no upstream node that satisfies it ({link('F01')}, {link('F02')}, {link('F03')}), and `check.py` does not look ({link('F04')}).",
    f"The editor cannot tell a finished node from the files, because no skill declares what it produces ({link('F05')}).",
    f"The reasons behind artifacts and the approvals stay in chat ({link('F13')}, {link('F23')}).",
    f"The review holds {n_find} findings: {sev_n['critical']} critical, {sev_n['high']} high, {sev_n['medium']} medium, {sev_n['low']} low.",
])
right = [
    f"The skills are flat: {len(skills)} skills in one directory level, and the longest ({link(longest['id'])}) has {longest['lines']} lines.",
    f"One artifact tree holds all {len(artifacts)} targets, from {link('a-brief')} to {link('a-11_build')}, so every skill writes to a known place.",
    f"`scripts/check.py` is the single gate of the collection; its flow rule has one gap ({link('F04')}).",
    "The glossary format keeps an `_Avoid_` list per term, so a rejected word has a home.",
    "A decision enters `decisions.md` only after the three-test check.",
    f"Feature dossiers are frozen records of the reasons ({link('a-08_dossiers')}).",
]
sec_answer = {"title": "The answer", "sub": "right pieces, wrong order", "blocks": [
    {"type": "p", "text": verdict},
    {"type": "p", "text": "What is already right:"},
    {"type": "bullets", "items": right},
]}

# -- section 2: findings ---------------------------------------------------------------------
if "edge_lines" not in std:
    die(f"flows.json has no `edge_lines` for {STANDARD}; re-run `python3 {DUMP}` from the repo root")
dom_order = dedupe(d for d in map(domain_of, std["order"]) if d in STAGE_ORDER and d != "collection")
flow_edges = []
for upstream, downstream in zip(dom_order, dom_order[1:]):
    # first `type: flow` edge, in file order, that crosses into the downstream domain
    crossing = next((e for e in std["edge_lines"]
                     if domain_of(e["source"]) != domain_of(e["target"]) and domain_of(e["target"]) == downstream), None)
    if crossing is None:
        errors.append(f"{STANDARD} has no `type: flow` edge into the {downstream} domain")
        continue
    flow_edges.append({"from": "s-" + upstream, "to": "s-" + downstream, "label": CROSSING[downstream],
                       "at": f"flows/{STANDARD}/{STANDARD}.flow.yaml:{crossing['line']}"})
pipeline_nodes = []
for sid in stage_ids:
    node = {"id": sid, "label": sid[2:], "ref": sid, "sub": plural(stage_n[sid], "finding")}
    if sid == "s-collection":
        node.update({"shape": "external", "sub": f"{plural(stage_row[sid]['findings_n'], 'finding')} · flows, contracts, host"})
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
        "skills": {"refs": f["skills"]},
        "detail": f["detail"],
        "evidence": code_at(f["first_at"]),
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
n_hard = sum(1 for g in gates if g["gate"] == "hard")
per_flow = ", ".join(f"{link(fid)}: {unmet_by_flow[fid]}" for fid in flow_ids if unmet_by_flow[fid])
gate_rows = []
for g in sorted(gates, key=lambda g: (g["satisfied"], g["gate"] != "hard", g["flow"], g["position"])):
    gate_rows.append({
        "flow": {"ref": g["flow"]}, "position": g["position"], "skill": {"ref": g["skill"]},
        "path": f"`{g['path']}`", "gate": g["gate"],
        "producer": {"ref": g["producer"]} if g["producer"] else "—",
        "satisfied": g["satisfied_s"],
        "prereq_at": code_at(g["prereq_at"]),
    })
sec_gates = {"title": "Where the flows break", "sub": "every prerequisite of every flow node", "blocks": [
    {"type": "p", "text": f"{len(unmet)} of {n_hard} hard gates have no producer upstream in the flow that runs them. By flow: {per_flow}. "
                          f"`scripts/check.py` has no rule for this ({link('F04')}). The producer is the nearest upstream skill whose declared write target covers the path."},
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


def artifact_covering(path):
    """Artifact target that holds a prerequisite path (writes carry their own `artifact`)."""
    for pref, folder, aid in art_match:
        if (folder and (path.rstrip("/") + "/").startswith(pref)) or (not folder and path == pref):
            return aid
    return None


edge_map = OrderedDict()  # (from, to, kind) -> [at, ...]
for w in writes:
    if w["artifact"] is None:
        continue
    edge_map.setdefault((w["skill"], w["artifact"], "write"), []).append(w["at"])
gate_edges = OrderedDict()
for s in skills:
    for p in s["prereqs"]:
        aid = artifact_covering(p["path"])
        if aid is None:
            continue
        gate_edges.setdefault((aid, s["id"], p["gate"]), []).append(p["at"])
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

sec_map = {"title": "Who writes what", "sub": f"{plural(len(skills), 'skill')}, the targets they write and the gates they read", "blocks": [
    {"type": "p", "text": f"{plural(len(skills), 'skill')} write to or read from {len(artifacts)} targets. {len(multi)} targets have more than one writer: "
                          f"{links([a['id'] for a in multi])}. Edge kinds: write, hard gate, soft gate. Click a legend entry to hide a kind."},
    map_block,
]}

# -- section 5: scorecard --------------------------------------------------------------------
why = {
    "dup": f"The same text sits in several skills, for example the one-question rule ({link('F14')}). No runtime effect.",
    "alt": f"{lens_n['alt']} findings name a double home, among them permissions ({link('F19')}), EARS criteria ({link('F20')}) and mockups ({link('F26')}).",
    "order": f"Gate cycle ({link('F17')}), glossary last ({link('F08')}), {broken_flows} broken flows ({link('F01')}).",
    "disk": f"Artifacts land on disk; reasons and approvals do not ({link('F13')}). The editor cannot derive done ({link('F05')}).",
    "wayfinding": f"{link(max_contracts['id'])} cites {max_contracts['contracts_n']} contracts; two contracts hold {elements_lines} lines ({link('F07')}).",
    "planning fit": f"Features come before the model ({link('F17')}); no skill lists what it produces ({link('F05')}).",
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
        f"`{s['id']}`", s["lines"], s["steps"], s["hard_n"], s["soft_n"],
        s["contracts_n"], len(s["flows"]), {"refs": skill_findings[s["id"]]}]})
contract_rows = [{"anchor": cid_of(c["id"]), "cells": [
    f"`{c['file']}`", c["lines"], {"refs": [r for r in c["readers"] if r in skill_set]}]} for c in contracts]
flow_rows = []
for f in flows:
    flow_rows.append({"anchor": f["id"], "cells": [
        f"`{f['id']}`", f["nodes_n"], " → ".join(link(s) for s in f["order"]), f["unmet_hard"]]})
artifact_rows = [{"anchor": a["id"], "cells": [
    f"`{a['path']}`", a["editor_form"], {"refs": [w for w in a["writers"] if w in skill_set]},
    a["readers_n"]]} for a in artifacts]
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
    f"{link('concept-scope')} and {link('concept-onboard')}: `answers.json` is the one record of every answer ({link('F06')}, {link('F16')}).",
    f"{link('concept-brief')}: `brief.md` and `goals.md`. {link('concept-reverse')} writes findings only ({link('F09')}).",
    f"Domain language (new): `_concept/glossary.md`, first level, one writer. Every later skill reads it first ({link('F08')}, {link('F30')}).",
    f"{link('concept-research')} runs alongside, before brand and journeys ({link('F12')}).",
    f"{link('experience-journeys')}: stories use glossary terms and carry no `candidate_entities` ({link('F18')}).",
    f"Data model: {link('architecture-datamodel')} moves ahead of the features (`10_blueprint/datamodel/`, conceptually `05_datamodel/`). It names entities from the glossary only, and `feature-map.json` goes ({link('F17')}, {link('F33')}).",
    f"{link('spec-featuresets')} and {link('experience-behaviors')} read the entities and never coin names ({link('F18')}, {link('F19')}).",
    f"{link('architecture-techstack')} and {link('architecture-system')} run before any renderer ({link('F02')}, {link('F32')}).",
    f"Feature loop with {link('spec-feature')}: spec and screens. The dossier opens at step 2 ({link('F23')}).",
    f"{link('experience-shell')} runs after the loop. Navigation comes from real screens ({link('F25')}).",
    f"{link('mockup-walkthrough')} is the one mockup renderer, then {link('mockup-annotate')} and {link('mockup-feedback')} ({link('F26')}).",
    f"Build: {link('build-scaffold')}, {link('build-database')}, {link('build-plan')}, {link('build-implement')}.",
    f"Quality: {link('quality-test')}, {link('quality-e2e')}, {link('quality-review')}.",
    f"{link('ops-review')} and {link('quality-release')}. `trace.yaml` is the single trace ({link('F36')}).",
]

PROSE = "prose (TipTap)"
CODE = "code editor"


def writers_of(*needles):
    """Skills whose write row path contains one of the needles."""
    return dedupe(w["skill"] for w in writes if w.get("path") and any(n in w["path"] for n in needles) and w["skill"] in skill_set)


# artifact id -> (proposed owners, change text)
OWNER_PROPOSALS = {
    "a-brief": (["concept-brief"], f"One owner. {link('concept-reverse')} stops writing it ({link('F09')})."),
    "a-goals": (["concept-brief"], f"One owner. {link('concept-reverse')} stops writing it ({link('F09')})."),
    "a-comparable": (["concept-brief"], f"One file for competitor knowledge, shared with `research/competitors.md` ({link('F10')})."),
    "a-01_meta": (["concept-scope"], "No change: one writer."),
    "a-02_grounding": (["concept-onboard", "concept-research", "quality-standards"],
                       f"One owner per subfolder: `onboarding/`, `research/` and `findings/`, `standards/`. Screenshots live in `findings/` only ({link('F11')})."),
    "a-03_brand": (["design-brand"], f"{link('concept-reverse')} stops writing `identity.md` and `tokens.json` ({link('F09')})."),
    "a-04_journeys": (["experience-journeys"], f"Stories carry the criterion id; spec and ledger cite it ({link('F20')})."),
    "a-05_features": (["spec-feature"], f"The feature spec has one owner. The data model no longer writes into it ({link('F17')}, {link('F33')})."),
    "a-06_behaviors": (["experience-behaviors"], f"Permissions move to the feature spec ({link('F19')})."),
    "a-07_screens": (["spec-feature"], f"Shell runs after the loop ({link('F25')}). Feedback patches through the contract ({link('F28')})."),
    "a-08_dossiers": (["spec-feature"], f"Open at step 2, append per step ({link('F23')})."),
    "a-09_mockup": (["mockup-walkthrough"], f"One renderer ({link('F26')}); one annotation schema ({link('F27')})."),
    "a-10_blueprint": (["architecture-techstack", "architecture-system", "architecture-datamodel"],
                       f"One owner per file. `glossary.md` leaves the folder ({link('F08')})."),
    "a-11_build": (["build-plan", "quality-review", "ops-review", "quality-release"],
                   f"One owner per subfolder or file: `slices/` and `acceptance-criteria/`, `reviews/`, `trace.yaml`, `release.yaml` ({link('F36')}, {link('F37')})."),
}
owner_rows = []
for a in artifacts:
    owners, change = OWNER_PROPOSALS.get(a["id"], (None, None))
    if owners is None:
        errors.append(f"OWNER_PROPOSALS has no row for artifact {a['id']}")
        continue
    cell = {"ref": owners[0]} if len(owners) == 1 else {"refs": owners}
    owner_rows.append([f"`{a['path']}`", {"refs": [w for w in a["writers"] if w in skill_set]}, cell, a["editor_form"], change])
EXTRA_OWNER_ROWS = [
    ("`_concept/glossary.md` (new)", writers_of("glossary.md"), ["concept-brief"], PROSE,
     f"New: first-level file, written by one domain-language step after the brief; every later writer reads it ({link('F08')})."),
    ("`_concept/02_grounding/onboarding/answers.json`", writers_of("02_grounding/onboarding/"), ["concept-onboard"], CODE,
     f"The record of every answer and approval; seeded from the host's `_grounding/<step>/user_input.json` ({link('F06')}, {link('F13')})."),
    ("`_concept/11_build/acceptance-criteria/`", writers_of("acceptance-criteria"), ["build-plan"], PROSE,
     f"`build-plan` owns the rows; the others flip a `status` field ({link('F37')})."),
    ("`_concept/11_build/trace.yaml`", writers_of("trace.yaml"), ["ops-review"], CODE,
     f"The single trace of feature to code ({link('F36')})."),
]
for label, today, proposed, form, change in EXTRA_OWNER_ROWS:
    owner_rows.append([label, {"refs": today}, {"ref": proposed[0]}, form, change])
for o in [x for _, _, ps, _, _ in EXTRA_OWNER_ROWS for x in ps] + [x for ps, _ in OWNER_PROPOSALS.values() for x in ps]:
    if o not in skill_set:
        errors.append(f"proposal names unknown skill {o}")

workarounds = [
    f"Run {link('experience-journeys')} by hand before {link('spec-featuresets')} in {link('appbuilder-mvp')} ({link('F01')}).",
    f"Run {link('architecture-techstack')} before {link('mockup-storybook')} in {link('appbuilder-standard')} ({link('F02')}).",
    f"Create `_concept/01_meta/scope.yaml` by hand before {link('spec-feature')} in {link('skaileup-concept-reverse')} ({link('F03')}).",
    f"For a project whose profile does not grow screens (cli-tool, api-service, library, data-pipeline), create an empty `_concept/07_screens/` so the hard gates of {link('build-plan')} and {link('build-implement')} open ({link('F35')}).",
    f"Copy `_grounding/<step>/user_input.json` into `answers.json` at onboarding ({link('F06')}).",
]
sec_target = {"title": "Target shape", "sub": "one hierarchy, one owner per artifact", "blocks": [
    {"type": "p", "text": f"The principle: one hierarchy (domain language, data model, features, screens), one owner per artifact, and every decision of the user lands in a markdown file that the editor opens ({link('F08')}, {link('F17')}, {link('F13')})."},
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

# Last commit that changed a collection source: stable across commits that only touch the report.
SOURCE_PATHS = ["skills", "contracts", "flows", "profiles", "scripts"]
git = subprocess.run(["git", "log", "-1", "--format=%h", "--", *SOURCE_PATHS], cwd=ROOT, capture_output=True, text=True)
sha = git.stdout.strip()
if git.returncode != 0 or not sha:
    die(f"`git log -1 -- {' '.join(SOURCE_PATHS)}` gave no commit: {git.stderr.strip() or 'no output'}")
# The dump date is the date of the newest data file.
dump_date = datetime.fromtimestamp(max(p.stat().st_mtime for p in DATA.glob("*.json"))).strftime("%Y-%m-%d")

report = {
    "title": "skaileup-mp — skill-set critique",
    "lang": "en",
    "profile": "critique",
    "numbered": True,
    "meta": [f"Source: ai-assets-skaileup-mp @ {sha}, skaile-forge/server for host facts",
             f"Dump: {dump_date}, dump-{STEM}.py"],
    "stats": stats,
    "badges": badges,
    "entities": entities,
    "sections": [sec_answer, sec_findings, sec_gates, sec_map, sec_score, sec_inventory, sec_target],
}
OUT.write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n")
choice_written = not CHOICE.exists()
if choice_written:
    CHOICE.write_text(json.dumps({"profile": "critique", "features": FEATURES}, indent=1) + "\n")
for w in dict.fromkeys(warnings):
    print(f"warning: {w}", file=sys.stderr)
print(f"{OUT.relative_to(ROOT)}: {len(entities)} entities "
      f"({len(stage_ids)} stages, {n_find} findings, {len(skills)} skills, {len(contracts)} contracts, {len(flows)} flows, {len(artifacts)} artifacts), "
      f"{len(map_edges)} map edges, {len(gate_rows)} gate rows")
print(f"{CHOICE.relative_to(ROOT)}: {'written' if choice_written else 'kept as written'}")
