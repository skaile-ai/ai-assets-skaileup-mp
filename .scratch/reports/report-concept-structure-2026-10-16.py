#!/usr/bin/env python3
"""Build concept-structure-2026-10-16.json from the dump in concept-structure-2026-10-16.data/.

Every count, path, writer and reader comes from the dump. Every evidence citation
(`path:line` + quote) is checked against the file; a quote that is not on its line aborts.
Prose is written here and follows ASD-STE100 rules.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STEM = "concept-structure-2026-10-16"
D = ROOT / f".scratch/reports/{STEM}.data"
OUT = ROOT / f".scratch/reports/{STEM}.json"

entries = json.loads((D / "entries.json").read_text())
skills = json.loads((D / "skills.json").read_text())
flows = json.loads((D / "flows.json").read_text())
profiles = json.loads((D / "profiles.json").read_text())
unlisted = json.loads((D / "unlisted.json").read_text())
by_id = {e["id"]: e for e in entries}
by_path = {e["path"]: e for e in entries}
skill_by = {s["name"]: s for s in skills}
errors: list[str] = []


def cite(path: str, quote: str, near: int | None = None) -> str:
    """`path:line` of the first line holding `quote` (the one nearest `near`, if given)."""
    lines = (ROOT / path).read_text().splitlines()
    hits = [i + 1 for i, l in enumerate(lines) if quote in l]
    if not hits:
        errors.append(f"{path}: quote not found: {quote!r}")
        return path
    n = min(hits, key=lambda h: abs(h - near)) if near else hits[0]
    return f"{path}:{n}"


def code(s: str) -> str:
    return f"`{s}`"


def sref(name: str) -> str:
    return f"[[s-{name}]]"


def top_of(e: dict) -> dict:
    return by_id[e["top"]]


CONTRACT = "contracts/concept_structure.md"
LAYER = {}
for e in entries:
    t = top_of(e)["path"]
    LAYER[e["id"]] = "input" if t.startswith(("01_meta", "02_grounding")) else ("build" if t.startswith("11_build") else "design")

std = next(f for f in flows if f["name"] == "appbuilder-standard")
std_pos = {n["skill"]: n["position"] for n in std["order"] if n["skill"]}

# ------------------------------------------------------------------ entities
ents: list[dict] = []
for e in entries:
    writers = " · ".join(sref(w) for w in e["writers"]) if e["writers"] else (
        "none declared" + (f", the folder {code(e['owner_declared_on'])} declares it" if e["owner_declared_on"] else ""))
    step = e["standard_step"]
    ent = {
        "id": e["id"],
        "title": e["name"],
        "label": e["path"],
        "order": e["line"],
        "badges": {"kind": [e["kind"]], "layer": [LAYER[e["id"]]]},
        "meta": [
            e["desc"] or "—",
            f"writer: {writers}",
            f"readers: {len(e['readers'])}",
            f"first write: step {step} of {code('appbuilder-standard')}" if step else "first write: no step of `appbuilder-standard`",
            f"`{CONTRACT}:{e['line']}`",
        ],
        "refs": [f"s-{w}" for w in e["writers"]],
    }
    if e["parent"]:
        ent["parent"] = e["parent"]
    if e["not_grown_in"]:
        ent["badges"]["grows"] = ["some"]
    ents.append(ent)

for s in skills:
    ents.append({
        "id": f"s-{s['name']}", "title": s["name"], "tree": False,
        "meta": [f"domain: {code(s['domain'])}", f"flows: {len(s['flows'])}", f"`{s['file']}`"],
    })
for f in flows:
    ents.append({"id": f["id"], "title": f["name"], "tree": False,
                 "meta": [f"{f['nodes']} nodes", f"entry: {code(f['entry'])}", f"`{f['file']}`"]})
for p in profiles:
    ents.append({"id": p["id"], "title": p["name"], "tree": False,
                 "meta": [p["description"], f"`{p['file']}`"]})
for ent in ents:
    ent.setdefault("label", ent["title"].replace("`", ""))

# ------------------------------------------------------------------ q4: write order
order_nodes, order_edges, seen = [], [], set()
flow_file = std["file"]
prev = None
for n in std["order"]:
    sk = n["skill"]
    new = [e for e in entries if sk in e["writers"] and e["id"] not in seen]
    if not new:
        continue
    seen.update(e["id"] for e in new)
    paths = [e["path"] for e in new]
    label = paths[0] if len(paths) == 1 else f"{paths[0]} +{len(paths) - 1}"
    order_nodes.append({"id": n["node"], "label": label, "sub": f"step {n['position']} · {sk}",
                        "shape": "store", "ref": new[0]["id"]})
    if prev:
        order_edges.append({"from": prev, "to": n["node"], "label": "next written",
                            "at": cite(flow_file, f"target: {n['node']}")})
    prev = n["node"]

# ------------------------------------------------------------------ q6: map
tops = [e for e in entries if e["depth"] == 0]
map_nodes = [{"id": e["id"], "label": e["path"], "sub": f"{len(e['writers_below'])} writers", "ref": e["id"]} for e in tops]
map_edges = []
used_skills = set()
for s in skills:
    body = (ROOT / s["file"]).read_text()
    writes, reads = {}, {}
    for p in s["produces"]:
        t = by_id[p["entry"]]["top"]
        writes.setdefault(t, cite(s["file"], p["path"]))
    for q in s["prerequisites"]:
        if not q["path"].startswith("_concept/"):
            continue
        from_dump = [eid for eid in s["reads"] if q["path"].removeprefix("_concept/").startswith(by_id[eid]["path"].rstrip("/")) or by_id[eid]["path"].startswith(q["path"].removeprefix("_concept/"))]
        for eid in from_dump:
            t = by_id[eid]["top"]
            if t in writes:
                continue
            kind = "hard" if q["gate"] == "hard" else reads.get(t, ("soft", ""))[0]
            reads[t] = (kind if reads.get(t, ("soft",))[0] != "hard" else "hard", cite(s["file"], q["path"]))
    for eid in s["reads"]:
        t = by_id[eid]["top"]
        if t not in writes and t not in reads:
            reads[t] = ("soft", cite(s["file"], "requires:"))
    for t, at in writes.items():
        map_edges.append({"from": f"k-{s['name']}", "to": t, "kind": "writes", "at": at})
    for t, (kind, at) in reads.items():
        map_edges.append({"from": t, "to": f"k-{s['name']}", "kind": kind, "at": at})
    if writes or reads:
        used_skills.add(s["name"])
for s in skills:
    if s["name"] in used_skills:
        map_nodes.append({"id": f"k-{s['name']}", "label": s["name"], "sub": s["domain"], "shape": "external", "ref": f"s-{s['name']}"})

# ------------------------------------------------------------------ q8: one feature
F = "artifact_frontmatter.md"
feat_nodes = [
    {"id": "spec", "label": "05_features/<featureset>/<feature>.md", "sub": "spec-feature", "shape": "store", "ref": by_path["05_features/<featureset>/<feature>.md"]["id"]},
    {"id": "stories", "label": "04_journeys/stories.yaml", "sub": "experience-journeys", "shape": "store", "ref": by_path["04_journeys/stories.yaml"]["id"]},
    {"id": "model", "label": "10_blueprint/datamodel/", "sub": "model.json", "shape": "store", "ref": by_path["10_blueprint/datamodel/"]["id"]},
    {"id": "behav", "label": "06_behaviors/<featureset>.md", "sub": "experience-behaviors", "shape": "store", "ref": by_path["06_behaviors/<featureset>.md"]["id"]},
    {"id": "screen", "label": "07_screens/<feature_slug>/<screen>.md", "sub": "spec-feature", "shape": "store", "ref": by_path["07_screens/<feature_slug>/<screen>.md"]["id"]},
    {"id": "dossier", "label": "08_dossiers/<feature_slug>/index.md", "sub": "spec-feature", "shape": "store", "ref": by_path["08_dossiers/<feature_slug>/index.md"]["id"]},
    {"id": "ledger", "label": "11_build/acceptance-criteria/", "sub": "<featureset>/<feature_slug>.ac.md", "shape": "store", "ref": by_path["11_build/acceptance-criteria/"]["id"]},
    {"id": "trace", "label": "11_build/trace.yaml", "sub": "build-implement", "shape": "store", "ref": by_path["11_build/trace.yaml"]["id"]},
    {"id": "slices", "label": "11_build/slices/<slice_id>/", "sub": "build-plan · build-implement", "shape": "store", "ref": by_path["11_build/slices/<slice_id>/"]["id"]},
    {"id": "review", "label": "11_build/reviews/", "sub": "<feature_slug>.yaml", "shape": "store", "ref": by_path["11_build/reviews/"]["id"]},
]
FEAT_GRID = {"stories": (0, 0), "model": (1, 0), "ledger": (0, 1), "spec": (1, 1),
             "screen": (0, 2), "behav": (1, 2), "dossier": (2, 2),
             "slices": (0, 3), "trace": (1, 3), "review": (2, 3)}
for n in feat_nodes:
    n["col"], n["row"] = FEAT_GRID[n["id"]]
feat_edges = [
    {"from": "stories", "to": "spec", "label": "story_refs", "at": cite(f"contracts/{F}", "story_refs: []")},
    {"from": "model", "to": "spec", "label": "data_entities[]", "at": cite(f"contracts/{F}", "data_entities: []")},
    {"from": "spec", "to": "screen", "label": "screens:", "at": cite(f"contracts/{F}", "screens: []")},
    {"from": "screen", "to": "spec", "label": "implements:", "at": cite(f"contracts/{F}", "implements:")},
    {"from": "spec", "to": "behav", "label": "<featureset> name", "at": cite(CONTRACT, "<featureset>.md")},
    {"from": "spec", "to": "dossier", "label": "<feature_slug>", "at": cite("contracts/slice_loop.md", "names three things at once")},
    {"from": "stories", "to": "ledger", "label": "AC-<story-id>-<nn>", "at": cite("contracts/acceptance_criteria.md", "AC-<story-id>-<nn>")},
    {"from": "ledger", "to": "spec", "label": "feature_ref", "at": cite("contracts/acceptance_criteria.md", "feature_ref:")},
    {"from": "slices", "to": "trace", "label": "slices[]", "at": cite("contracts/feedback_loop.md", "features.<feature_slug>.slices[]")},
    {"from": "trace", "to": "review", "label": "commits", "at": cite("contracts/feedback_loop.md", "slices[].commits")},
]

# ------------------------------------------------------------------ q2 / q3 tables
art_entries = {}
for e in entries:
    for i in e["artifact_ids"]:
        art_entries.setdefault(i, []).append(e["id"])
prof_rows = []
for p in profiles:
    hit = [e["id"] for e in entries if p["name"] in e["not_grown_in"]]
    prof_rows.append({"anchor": p["id"], "cells": [
        code(p["name"]), len(hit), {"refs": hit} if hit else "nothing — the full tree",
        " ".join(code(x) for x in p["not_grown"]) or "—"]})

flow_names = [f["name"] for f in flows]
grow_rows = []
for e in tops:
    grow_rows.append([{"ref": e["id"]}] + ["yes" if fn in e["flows"] else "—" for fn in flow_names]
                     + [e["standard_step"] if e["standard_step"] else "—"])
flow_rows = [{"anchor": f["id"], "cells": [code(f["name"]), f["nodes"], code(f["entry"]),
                                            sum(1 for e in tops if f["name"] in e["flows"])]} for f in flows]

skill_rows = []
for s in skills:
    w = sorted({p["entry"] for p in s["produces"]}, key=lambda i: by_id[i]["line"])
    r = sorted(set(s["reads"]) - set(w), key=lambda i: by_id[i]["line"])
    skill_rows.append({"anchor": f"s-{s['name']}", "cells": [
        code(s["name"]), code(s["domain"]), {"refs": w} if w else "—", {"refs": r} if r else "—", len(s["flows"])]})

# ------------------------------------------------------------------ q9 gaps
def declares_folder(skill: str, folder: str) -> bool:
    """True when the skill's `produces` names the folder itself, not a file that only lands in it."""
    return any(p["path"].removeprefix("_concept/") == folder for p in skill_by[skill]["produces"])


# a file the tree lists, with no writer of its own and no writer that declares its folder as a whole
no_writer = [e for e in entries if e["kind"] == "file" and not e["writers"]
             and not (e["owner_declared_on"] and any(declares_folder(s, e["owner_declared_on"]) for s in e["owner"]))]
no_writer_folder = [e for e in entries if not e["writers_below"] and not e["owner"] and e["kind"] == "folder"]
folder_only: dict[str, list[dict]] = {}
for e in entries:
    if e["kind"] != "pattern" and not e["writers"] and e not in no_writer and e not in no_writer_folder and e["owner_declared_on"]:
        folder_only.setdefault(e["owner_declared_on"], []).append(e)
seeds = by_path["02_grounding/seeds/"]
gap_items = []
for u in unlisted:
    gap_items.append(f"{sref(u['skill'])} writes {code(u['path'].removeprefix('_concept/'))}. The tree names only "
                     f"[[{by_path[u['lands_in']]['id']}]] (`{cite(skill_by[u['skill']]['file'], u['path'])}`).")
for e in no_writer:
    gap_items.append(f"No skill declares a write of [[{e['id']}]]. The tree lists it at `{CONTRACT}:{e['line']}`.")
for e in no_writer_folder:
    gap_items.append(f"No skill writes into [[{e['id']}]]. That is by design: the contract says \"{e['desc']}\".")
for folder, items in folder_only.items():
    gap_items.append(f"{len(items)} {'entry' if len(items) == 1 else 'entries'} under [[{by_path[folder]['id']}]] "
                     f"{'has' if len(items) == 1 else 'have'} no writer of their own: {', '.join(f'[[{e['id']}]]' for e in items)}. "
                     f"{', '.join(sref(s) for s in by_path[folder]['writers'])} "
                     f"{'declares' if len(by_path[folder]['writers']) == 1 else 'declare'} only the folder.")

# ------------------------------------------------------------------ q7 rules
rules = [
    ("The first level has a number. Nothing below it has a number.", "first level is numbered and nothing below it is."),
    ("The number is the only order signal. The host sidebar removes the prefix before it shows the name.", "strips `^\\d+_` before display"),
    ("The numbers are contiguous. A twelfth folder renumbers every folder after it.", "Numbers are contiguous."),
    ("File names are lowercase and hyphenated. One artifact has exactly one path.", "Artifact filenames are lowercase and **hyphenated**"),
    ("Two siblings never differ only by singular and plural.", "No two siblings may differ only by singular and plural."),
    ("`shell` is a reserved slug under [[e-07-screens]].", "`shell` is a reserved slug"),
    ("Folders under [[e-05-features]] and [[e-07-screens]] are slugs: lowercase, hyphenated, no number.", "Directories under `05_features/` and `07_screens/` are slugs"),
    ("Each folder under [[e-02-grounding-research-step-skill-name]] has the name of the skill that sent the research.", "subfolders are named for the skill"),
]
rule_items = [f"{t} (`{cite(CONTRACT, q)}`)" for t, q in rules]

if errors:
    for e in errors:
        print("ABORT:", e)
    sys.exit(1)

n_files = sum(1 for e in entries if e["kind"] == "file")
n_patterns = sum(1 for e in entries if e["kind"] == "pattern")
mvp = next(f for f in flows if f["name"] == "appbuilder-mvp")
n_folders = sum(1 for e in entries if e["kind"] == "folder")
mvp_skips = [e["id"] for e in tops if "appbuilder-mvp" not in e["flows"]]
ui_profiles = [p["name"] for p in profiles if "screens" in p["not_grown"]]
most_read = max(entries, key=lambda e: len(e["readers"]))
feature_owned = [n for n in feat_nodes if n["id"] in ("spec", "screen", "dossier", "ledger", "slices", "review")]
report = {
    "title": "The _concept/ folder: structure",
    "lang": "en",
    "profile": "structure",
    "data_dir": f"{STEM}.data",
    "meta": [
        f"Source: `{CONTRACT}` (the tree fence), the `metadata` of {len(skills)} `skills/*/SKILL.md`, {len(flows)} flows, {len(profiles)} profiles",
        "Dump: `dump-concept-structure-2026-10-16.py`, read on 2026-10-16",
    ],
    "numbered": True,
    "stats": [
        ["Tree entries", {"count": "entries"}],
        ["First-level entries", {"count": "first_level"}],
        ["Skills", {"count": "skills"}],
        ["Flows", {"count": "flows"}],
        ["Project types", {"count": "profiles"}],
    ],
    "badges": {
        "kind": {"label": "Kind", "shape": "square", "values": {
            "folder": {"color": "gray", "desc": "a directory"},
            "file": {"color": "blue", "desc": "one file with a fixed name"},
            "pattern": {"color": "purple", "desc": "one file per feature, screen or featureset"}}},
        "layer": {"label": "Layer", "shape": "pill", "values": {
            "input": {"color": "teal", "desc": "scope and material from outside the room"},
            "design": {"color": "navy", "desc": "the design half: brief to blueprint"},
            "build": {"color": "orange", "desc": "the build half: slices, ledger, trace, reviews"}}},
        "grows": {"label": "Project type", "shape": "dashed", "filter": "hide", "values": {
            "some": {"label": "not every type", "color": "yellow", "desc": "at least one profile never grows it"}}},
    },
    "entities": ents,
    "sections": [
        {"title": "The answer", "blocks": [
            {"type": "p", "text": (
                f"`_concept/` is one root folder in the project. It holds {len(tops)} first-level entries: "
                f"three root files ([[e-brief-md]], [[e-goals-md]], [[e-glossary-md]]) and eleven numbered folders from [[e-01-meta]] to [[e-11-build]]. "
                f"{sum(1 for s in skills if s['produces'])} of {len(skills)} skills write into it. Each skill names its paths in `metadata.artifacts.produces`. "
                f"{sum(1 for e in entries if len(e['writers']) > 1)} entries have more than one writer.")},
            {"type": "p", "text": (
                "The numbers sort the folders for the reader. They do not give the write order: "
                "[[e-10-blueprint-datamodel]] is written before [[e-05-features]], and [[e-09-mockup]] comes after the screens. "
                "Everything before [[e-11-build]] is design. Everything in [[e-11-build]] is build.")},
        ]},
        {"title": "What each folder holds and who writes it", "sub": "What is in it", "question": "q1", "blocks": [
            {"type": "p", "text": (
                f"The tree has {len(entries)} entries: {n_folders} folders, "
                f"{n_files} files and {n_patterns} patterns. A pattern is one file per feature, screen or featureset. "
                "Each row shows the description from the contract, the writer skill, the number of reader skills and the first write step. "
                "[[e-02-grounding]] holds everything from outside the project: [[e-02-grounding-onboarding]], [[e-02-grounding-research]] and the graded findings of `concept-reverse`: "
                + ", ".join(f"[[{e['id']}]]" for e in entries if e["path"].startswith("02_grounding/findings/") and e["path"] != "02_grounding/findings/") + ". "
                "The badges filter the tree and the map in the section on readers.")},
            {"type": "tree", "filter": ["kind", "layer", "grows"], "count_label": "entries visible",
             "hint": "Click a badge to hide or show entries. The map of readers below follows the same filter.",
             "reset": "Show all", "drives": ["readers"]},
        ]},
        {"title": "What each project type never grows", "sub": "What is in it", "question": "q2", "blocks": [
            {"type": "p", "text": (
                f"`concept-scope` reads `project_type` and resolves it against one of {len(profiles)} profiles. "
                "A profile lists the artifacts a project of that type never grows. "
                f"{len(ui_profiles)} types never grow journeys, screens, brand, behaviors or mockups: "
                + ", ".join(code(n) for n in ui_profiles) + ". "
                "A `library` also never grows a data model. A `web-app` grows the full tree.")},
            {"type": "table", "columns": ["Profile", "Entries", "Not grown", "`not_grown` value"], "numeric": [1], "rows": prof_rows},
        ]},
        {"title": "Which flows grow which folders", "sub": "What is in it", "question": "q3", "blocks": [
            {"type": "p", "text": (
                f"A flow grows an entry when a writer of that entry is a node of the flow. "
                f"[[{std['id']}]] grows all first-level entries. [[{mvp['id']}]] has {mvp['nodes']} nodes and skips {len(mvp_skips)} of them: "
                + ", ".join(f"[[{i}]]" for i in mvp_skips) + ". "
                "The last column gives the step of [[f-appbuilder-standard]] that writes the entry first.")},
            {"type": "table", "columns": ["Entry"] + [code(n) for n in flow_names] + ["First write (standard)"], "numeric": [5], "rows": grow_rows},
            {"type": "table", "columns": ["Flow", "Nodes", "Entry node", "First-level entries grown"], "numeric": [1, 3], "rows": flow_rows},
        ]},
        {"title": "The order in which folders are written", "sub": "How it fills up", "question": "q4", "blocks": [
            {"type": "p", "text": (
                f"The diagram follows [[f-appbuilder-standard]] from `scope` to the end. Each box is a step that writes an entry for the first time. "
                f"The order is domain language, then data model, then features and screens, then architecture, then mockups, then build. "
                f"The data model ({code('10_blueprint/datamodel/')}) comes before every feature, so no feature skill coins an entity name.")},
            {"type": "flow", "id": "order", "label": "First write of each entry in appbuilder-standard", "dir": "down",
             "nodes": order_nodes, "edges": order_edges},
        ]},
        {"title": "Which skills read and write each folder", "sub": "How it fills up", "question": "q6", "blocks": [
            {"type": "p", "text": (
                f"The map joins the {len(tops)} first-level entries with the skills that read or write them. "
                "A green edge is a write from `metadata.artifacts.produces`. A blue edge is a `hard` prerequisite: the skill stops without the file. "
                "A dashed edge is a `soft` prerequisite or a `requires` id. "
                f"[[{most_read['id']}]] has the most readers: {len(most_read['readers'])} skills.")},
            {"type": "map", "id": "readers", "label": "First-level entries and the skills that touch them", "height": 720,
             "kinds": {"writes": {"label": "writes", "color": "green"},
                       "hard": {"label": "reads (hard gate)", "color": "blue"},
                       "soft": {"label": "reads (soft or requires)", "color": "gray", "dash": "dash"}},
             "nodes": map_nodes, "edges": map_edges},
            {"type": "table", "columns": ["Skill", "Domain", "Writes", "Reads", "Flows"], "numeric": [4], "rows": skill_rows},
        ]},
        {"title": "How one feature spreads across the tree", "sub": "Rules and gaps", "question": "q8", "blocks": [
            {"type": "p", "text": (
                f"A feature owns files in {len(feature_owned)} places. It shares {len(feat_nodes) - len(feature_owned)} more files with other features. The feature spec is the center. "
                "Its `<feature_slug>` names the screen folder and the dossier. "
                "Frontmatter fields join the rest: `story_refs`, `data_entities[]`, `screens:` and `implements:`. "
                "On the build side, the ledger names the spec in `feature_ref`, and [[e-11-build-trace-yaml]] joins the feature to its slices and commits.")},
            {"type": "flow", "id": "feature", "label": "The files of one feature and the fields that join them", "dir": "down", "gap": [110, 60],
             "nodes": feat_nodes, "edges": feat_edges},
        ]},
        {"title": "Where the tree and the skills disagree", "sub": "Rules and gaps", "question": "q9", "blocks": [
            {"type": "p", "text": (
                f"The gate accepts a written path when it lies under a folder of the tree. So {len(unlisted)} written paths are valid but the tree does not name them. "
                "Most are files inside a folder the tree describes in words. "
                "The other direction also has gaps: entries that the tree lists and that no skill names on its own.")},
            {"type": "bullets", "items": gap_items},
        ]},
        {"title": "The numbering and naming rules", "sub": "Rules and gaps", "question": "q7", "blocks": [
            {"type": "p", "text": "The contract states one numbering rule and five naming rules. The gate checks the singular and plural rule."},
            {"type": "bullets", "items": rule_items},
        ]},
    ],
}
OUT.write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n")
print(f"{OUT.name}: {len(ents)} entities, {len(map_nodes)} map nodes, {len(map_edges)} map edges, {len(order_nodes)} order nodes, {len(gap_items)} gaps")
