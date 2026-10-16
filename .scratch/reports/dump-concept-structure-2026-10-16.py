#!/usr/bin/env python3
"""Dump facts about the `_concept/` tree for the concept-structure report.

Writes .scratch/reports/concept-structure-2026-10-16.data/<collection>.json. Every fact is
read from the repo: the tree and its descriptions from the first fence of
`contracts/concept_structure.md`, writers from each skill's `metadata.artifacts.produces`,
readers from `prerequisites.files` and `artifacts.requires` (resolved through `produces`),
flow order from the `type: flow` edges of `flows/*/*.flow.yaml`, profile exclusions from
`profiles/*.yaml`, and the read-direction table from the contract. Nothing is hand-held.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / ".scratch/reports/concept-structure-2026-10-16.data"
CONTRACT = ROOT / "contracts/concept_structure.md"
sys.path.insert(0, str(ROOT / "scripts"))
from check import split_frontmatter  # noqa: E402  the gate's own frontmatter reader

NODE_RE = re.compile(r"^(?P<indent>(?:[\u2502 ] {3})*)[\u251c\u2514]\u2500\u2500 (?P<name>\S+)(?:\s{2,}(?P<desc>.*))?$")
ROOT_RE = re.compile(r"^_concept/\s*$")


def wild(seg: str) -> bool:
    return "<" in seg or "*" in seg


def slug(path: str) -> str:
    s = re.sub(r"[<>*]", "", path).strip("/")
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return "e-" + (s or "root")


def segs(path: str) -> list[str]:
    return [s for s in path.removeprefix("_concept/").split("/") if s]


# ---------------------------------------------------------------- the tree
def read_tree() -> list[dict]:
    entries: list[dict] = []
    stack: list[dict] = []
    inside = False
    for n, line in enumerate(CONTRACT.read_text().splitlines(), 1):
        if line.strip().startswith("```"):
            if inside:
                break
            inside = True
            continue
        if not inside:
            continue
        m = NODE_RE.match(line)
        if not m:
            continue
        depth = len(m.group("indent")) // 4
        raw = m.group("name")
        del stack[depth:]
        parent = stack[-1] if stack else None
        if parent is not None:
            parent["kind"] = "folder"
        base = parent["path"] if parent else ""
        path = base + raw
        is_dir = raw.endswith("/")
        entry = {
            "id": slug(path),
            "path": path,
            "name": raw,
            "depth": depth,
            "line": n,
            "desc": (m.group("desc") or "").strip(),
            "kind": "folder" if is_dir else ("pattern" if wild(raw) else "file"),
            "parent": parent["id"] if parent else None,
            "top": (parent["top"] if parent else slug(path)),
        }
        if is_dir and wild(raw):
            entry["kind"] = "folder"
        entries.append(entry)
        stack.append(entry)
    return entries


def match_entry(entries: list[dict], path: str) -> dict | None:
    """The most specific tree entry a `_concept/` path names or lies under."""
    want = segs(path)
    best, best_len = None, -1
    for e in entries:
        have = segs(e["path"])
        if len(have) > len(want):
            continue
        if all(h == w or wild(h) for h, w in zip(have, want)):
            exact = sum(1 for h, w in zip(have, want) if h == w)
            score = len(have) * 10 + exact
            if score > best_len:
                best, best_len = e, score
    return best


# ---------------------------------------------------------------- skills
def read_skills() -> list[dict]:
    skills = []
    for p in sorted((ROOT / "skills").glob("*/SKILL.md")):
        fm, body = split_frontmatter(p.read_text())
        meta = fm.get("metadata") or {}
        art = meta.get("artifacts") or {}
        pre = (meta.get("prerequisites") or {}).get("files") or []
        skills.append({
            "id": "s-" + p.parent.name,
            "name": p.parent.name,
            "domain": p.parent.name.split("-")[0],
            "produces": [{"id": e["id"], "path": e["path"]} for e in art.get("produces") or []],
            "requires": [e["id"] for e in art.get("requires") or [] if isinstance(e, dict) and "id" in e],
            "prerequisites": [{"path": e["path"], "gate": e.get("gate", "soft")} for e in pre if isinstance(e, dict) and "path" in e],
            "file": f"skills/{p.parent.name}/SKILL.md",
            "lines": len(p.read_text().splitlines()),
        })
    return skills


# ---------------------------------------------------------------- flows
def read_flows() -> list[dict]:
    flows = []
    for p in sorted((ROOT / "flows").glob("*/*.flow.yaml")):
        d = yaml.safe_load(p.read_text())
        by_id = {n["id"]: n for n in d.get("nodes", [])}
        nxt = {}
        for e in d.get("edges", []):
            if e.get("type") == "flow":
                nxt.setdefault(e["source"], []).append(e["target"])
        order, cur, seen = [], d.get("entry"), set()
        while cur and cur not in seen:
            seen.add(cur)
            n = by_id.get(cur, {})
            data = n.get("data") or {}
            order.append({"node": cur, "skill": data.get("skill"), "phase": data.get("phase")})
            cur = (nxt.get(cur) or [None])[0]
        flows.append({
            "id": "f-" + p.parent.name,
            "name": p.parent.name,
            "title": d.get("name", p.parent.name),
            "file": str(p.relative_to(ROOT)),
            "entry": d.get("entry"),
            "nodes": len(order),
            "order": order,
        })
    return flows


# ---------------------------------------------------------------- profiles
def read_profiles() -> list[dict]:
    out = []
    for p in sorted((ROOT / "profiles").glob("*.yaml")):
        d = yaml.safe_load(p.read_text()) or {}
        out.append({"id": "p-" + d.get("profile", p.stem), "name": d.get("profile", p.stem),
                    "description": d.get("description", ""), "not_grown": d.get("not_grown") or [],
                    "file": str(p.relative_to(ROOT))})
    return out


# ---------------------------------------------------------------- read direction
def read_direction() -> list[dict]:
    rows, inside = [], False
    for n, line in enumerate(CONTRACT.read_text().splitlines(), 1):
        if line.startswith("## Read direction"):
            inside = True
            continue
        if inside and line.startswith("## "):
            break
        if inside and line.startswith("| ") and not line.startswith("| writes to") and not set(line) <= set("|- "):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            rows.append({"writes_to": cells[0], "may_read": cells[1], "line": n})
    return rows


def main() -> int:
    entries = read_tree()
    skills = read_skills()
    flows = read_flows()
    profiles = read_profiles()
    readdir = read_direction()
    by_id = {e["id"]: e for e in entries}
    for e in entries:
        e.update(writers=[], readers=[], hard_readers=[], artifact_ids=[], flows=[], not_grown_in=[])

    produced_by: dict[str, list[str]] = {}
    problems = []
    for s in skills:
        for p in s["produces"]:
            e = match_entry(entries, p["path"])
            if e is None:
                problems.append(f"{s['name']}: produces {p['path']} matches no tree entry")
                continue
            p["entry"] = e["id"]
            produced_by.setdefault(p["id"], []).append(p["path"])
            if s["name"] not in e["writers"]:
                e["writers"].append(s["name"])
            if p["id"] not in e["artifact_ids"]:
                e["artifact_ids"].append(p["id"])

    for s in skills:
        read_paths = [(q["path"], q["gate"]) for q in s["prerequisites"] if q["path"].startswith("_concept/")]
        for rid in s["requires"]:
            read_paths += [(path, "requires") for path in produced_by.get(rid, [])]
        s["reads"] = []
        for path, gate in read_paths:
            e = match_entry(entries, path)
            if e is None:
                continue
            if e["id"] not in s["reads"]:
                s["reads"].append(e["id"])
            if s["name"] not in e["readers"] and s["name"] not in e["writers"]:
                e["readers"].append(s["name"])
            if gate == "hard" and s["name"] not in e["hard_readers"]:
                e["hard_readers"].append(s["name"])

    skill_flows: dict[str, list[str]] = {}
    for f in flows:
        for i, n in enumerate(f["order"]):
            if n["skill"]:
                skill_flows.setdefault(n["skill"], []).append(f["name"])
                n["position"] = i + 1
    for s in skills:
        s["flows"] = sorted(set(skill_flows.get(s["name"], [])))

    # flows that grow an entry: a writer of it or of anything under it runs in the flow
    for e in entries:
        under = [x for x in entries if x["path"].startswith(e["path"])] if e["kind"] == "folder" else [e]
        writers = {w for x in under for w in x["writers"]}
        e["writers_below"] = sorted(writers)
        e["flows"] = sorted({fl for w in writers for fl in skill_flows.get(w, [])})

    for p in profiles:
        for item in p["not_grown"]:
            hits = [e for e in entries if item in e["artifact_ids"]]
            if not hits:  # a skill name or a domain prefix
                hits = [e for e in entries if any(w == item or w.startswith(item + "-") for w in e["writers"])]
            for e in hits:
                if p["name"] not in e["not_grown_in"]:
                    e["not_grown_in"].append(p["name"])

    # owner: the entry's own writers, else the nearest folder above that declares one
    for e in entries:
        cur = e
        while cur is not None and not cur["writers"]:
            cur = by_id.get(cur["parent"])
        e["owner"] = cur["writers"] if cur else []
        e["owner_declared_on"] = cur["path"] if cur else None

    # produced paths deeper than the tree entry they land in: the tree does not name them
    unlisted = [
        {"skill": s["name"], "id": p["id"], "path": p["path"], "lands_in": by_id[p["entry"]]["path"]}
        for s in skills for p in s["produces"]
        if "entry" in p and len(segs(p["path"])) > len(segs(by_id[p["entry"]]["path"]))
    ]

    # first written: earliest position of a writer in the standard flow
    std = next((f for f in flows if f["name"] == "appbuilder-standard"), None)
    if std:
        pos = {n["skill"]: n["position"] for n in std["order"] if n["skill"]}
        for e in entries:
            ps = [pos[w] for w in e["writers_below"] if w in pos]
            e["standard_step"] = min(ps) if ps else None

    if problems:
        for pr in problems:
            print("ABORT:", pr)
        return 1

    OUT.mkdir(parents=True, exist_ok=True)
    first_level = [e for e in entries if e["depth"] == 0]
    stats = {
        "entries": len(entries),
        "first_level": len(first_level),
        "files": sum(1 for e in entries if e["kind"] == "file"),
        "folders": sum(1 for e in entries if e["kind"] == "folder"),
        "patterns": sum(1 for e in entries if e["kind"] == "pattern"),
        "skills": len(skills),
        "writing_skills": sum(1 for s in skills if s["produces"]),
        "flows": len(flows),
        "profiles": len(profiles),
        "contract_lines": len(CONTRACT.read_text().splitlines()),
    }
    for name, data in {"entries": entries, "first_level": first_level, "skills": skills,
                       "flows": flows, "profiles": profiles, "read_direction": readdir,
                       "unlisted": unlisted, "stats": [stats]}.items():
        (OUT / f"{name}.json").write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    print(" · ".join(f"{k} {v}" for k, v in stats.items()))
    print("no owner:", [e["path"] for e in entries if not e["owner"]])
    print("unlisted:", [(u["skill"], u["path"]) for u in unlisted])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
