#!/usr/bin/env python3
"""Dump facts about the ai-assets-skaileup-mp collection for the skill-set critique report.

Run from anywhere; the repo root is this file's parents[2].
Writes .scratch/reports/skill-set-critique-2026-10-15.data/<collection>.json (JSON arrays).

Everything is read from files except two hand-held inputs, and both are asserted:
  * WRITES   - the writer map (skill -> _concept path), each row cites the line that says so
  * findings - every *.json in skill-set-critique-2026-10-15.findings/, each evidence row cited;
               a finding with `status: "closed"` (+ `closed_by`: the i-ssi ticket) is carried
               through but its evidence is not validated: the quoted problem text is gone
A citation is `path:N` or `path:A-B` whose lines must contain `quote` verbatim. Any failure
aborts the run before a single output file is written. The writer map is also cross-checked
against every skill's `metadata.artifacts.produces`; disagreements are printed, not fatal.
"""
from __future__ import annotations

import datetime
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
HOST = Path("/Users/matthias/devBench/SKAILEdev/forge/skaile-forge")
OUT = ROOT / ".scratch/reports/skill-set-critique-2026-10-15.data"
FINDINGS_DIR = ROOT / ".scratch/reports/skill-set-critique-2026-10-15.findings"

STAGES = ["concept", "design", "experience", "spec", "mockup", "architecture", "build", "quality", "ops", "collection"]
SEVS = ["critical", "high", "medium", "low"]
LENSES = ["dup", "alt", "order", "disk", "wayfinding"]
STATUSES = ["open", "closed"]

# artifact targets: id -> path (11 first-level folders + three root files: brief, goals, glossary)
ARTIFACTS = [
    ("a-brief", "_concept/brief.md"),
    ("a-goals", "_concept/goals.md"),
    ("a-glossary", "_concept/glossary.md"),
    ("a-01_meta", "_concept/01_meta"),
    ("a-02_grounding", "_concept/02_grounding"),
    ("a-03_brand", "_concept/03_brand"),
    ("a-04_journeys", "_concept/04_journeys"),
    ("a-05_features", "_concept/05_features"),
    ("a-06_behaviors", "_concept/06_behaviors"),
    ("a-07_screens", "_concept/07_screens"),
    ("a-08_dossiers", "_concept/08_dossiers"),
    ("a-09_mockup", "_concept/09_mockup"),
    ("a-10_blueprint", "_concept/10_blueprint"),
    ("a-11_build", "_concept/11_build"),
]

# project-root artifacts a skill may write outside the tree (mirrors check.py PROJECT_ROOT_ARTIFACTS, ADR 0015);
# every other project-root gate (package.json) is a fact about the scaffolded project, not a node's output.
PROJECT_ROOT_ARTIFACTS = {"APP-DESIGN.md"}

# The writer map: (skill, path, at, quote). `at` is the SKILL.md line that states the write;
# `quote` is a verbatim substring of that line. path None = writes nothing under _concept/.
# It is the body-cited cross-check of each skill's frontmatter `metadata.artifacts.produces`.
WRITES: list[tuple[str, str | None, str, str]] = [
    ("concept-scope", "_concept/01_meta/scope.yaml", "skills/concept-scope/SKILL.md:67", "write `01_meta/scope.yaml`"),
    ("concept-onboard", "_concept/02_grounding/onboarding/", "skills/concept-onboard/SKILL.md:27", "Fills `02_grounding/onboarding/`"),
    ("concept-brief", "_concept/brief.md", "skills/concept-brief/SKILL.md:57", "Write `brief.md`"),
    ("concept-brief", "_concept/goals.md", "skills/concept-brief/SKILL.md:59", "in `goals.md`"),
    ("concept-glossary", "_concept/glossary.md", "skills/concept-glossary/SKILL.md:56", "Write `glossary.md`."),
    ("concept-research", "_concept/02_grounding/research/", "skills/concept-research/SKILL.md:31", "Fills `02_grounding/research/`"),
    ("concept-research", "_concept/02_grounding/findings/", "skills/concept-research/SKILL.md:32", "`02_grounding/findings/` with the raw material"),
    ("concept-reverse", "_concept/02_grounding/findings/", "skills/concept-reverse/SKILL.md:56", "Write the seven findings into `02_grounding/findings/`"),
    ("design-brand", "_concept/03_brand/", "skills/design-brand/SKILL.md:31", "Writes `03_brand/`"),
    ("design-brand", "_concept/02_grounding/findings/", "skills/design-brand/SKILL.md:32", "go to `02_grounding/findings/`"),
    ("experience-journeys", "_concept/04_journeys/stories.yaml", "skills/experience-journeys/SKILL.md:73", "**Write `04_journeys/stories.yaml`**"),
    ("spec-featuresets", "_concept/05_features/featuresets.md", "skills/spec-featuresets/SKILL.md:71", "**Write `05_features/featuresets.md`.**"),
    ("experience-behaviors", "_concept/06_behaviors/", "skills/experience-behaviors/SKILL.md:52-53", "`06_behaviors/<featureset>.md`"),
    ("experience-shell", "_concept/07_screens/shell.md", "skills/experience-shell/SKILL.md:32", "Writes exactly one file: `07_screens/shell.md`"),
    ("spec-feature", "_concept/05_features/", "skills/spec-feature/SKILL.md:92-95", "**Write the feature spec** to `05_features/<featureset>/<feature_slug>.md`"),
    ("spec-feature", "_concept/07_screens/", "skills/spec-feature/SKILL.md:109-113", "`07_screens/<feature_slug>/<screen>.md`"),
    ("spec-feature", "_concept/08_dossiers/", "skills/spec-feature/SKILL.md:68-71", "write `08_dossiers/<feature_slug>/index.md`"),
    ("spec-feature", "_concept/10_blueprint/decisions.md", "skills/spec-feature/SKILL.md:80-83", "`10_blueprint/decisions.md`, cheap now"),
    ("mockup-walkthrough", "_concept/09_mockup/walkthrough/", "skills/mockup-walkthrough/SKILL.md:27", "`_concept/09_mockup/walkthrough/<renderer>/`"),
    ("mockup-storybook", "_concept/09_mockup/storybook/", "skills/mockup-storybook/SKILL.md:31", "`_concept/09_mockup/storybook/`"),
    ("mockup-annotate", "_concept/09_mockup/feedback/sessions/", "skills/mockup-annotate/SKILL.md:57", "create `sessions/`"),
    ("mockup-feedback", "_concept/09_mockup/feedback/", "skills/mockup-feedback/SKILL.md:101", "writes `applied/<sid>.json`"),
    ("mockup-feedback", "_concept/07_screens/", "skills/mockup-feedback/SKILL.md:22", "edited screen specs"),
    ("mockup-feedback", "_concept/05_features/", "skills/mockup-feedback/SKILL.md:66", "one target file"),
    ("architecture-techstack", "_concept/10_blueprint/techstack.md", "skills/architecture-techstack/SKILL.md:99", "`10_blueprint/techstack.md` exists"),
    ("architecture-system", "_concept/10_blueprint/architecture.md", "skills/architecture-system/SKILL.md:67", "**Write `10_blueprint/architecture.md`.**"),
    ("architecture-datamodel", "_concept/10_blueprint/datamodel/", "skills/architecture-datamodel/SKILL.md:26-27", "under `10_blueprint/datamodel/`"),
    ("experience-interaction", "APP-DESIGN.md", "skills/experience-interaction/SKILL.md:79", "**Write `APP-DESIGN.md` after every round**"),
    ("build-plan", "_concept/11_build/slices/", "skills/build-plan/SKILL.md:94", "`11_build/slices/<slice_id>/plan.md`"),
    ("build-plan", "_concept/11_build/acceptance-criteria/", "skills/build-plan/SKILL.md:106", "`11_build/acceptance-criteria/<featureset>/<feature_slug>.ac.md`"),
    ("build-implement", "_concept/11_build/slices/", "skills/build-implement/SKILL.md:93", "`11_build/slices/<slice_id>/index.md`"),
    ("build-implement", "_concept/11_build/acceptance-criteria/", "skills/build-implement/SKILL.md:80", "update the ledger at `11_build/acceptance-criteria/"),
    ("build-implement", "_concept/11_build/trace.yaml", "skills/build-implement/SKILL.md:75", "write the slice into `11_build/trace.yaml`"),
    ("quality-e2e", "_concept/11_build/acceptance-criteria/", "skills/quality-e2e/SKILL.md:53", "`11_build/acceptance-criteria/<featureset>/<feature_slug>.ac.md`"),
    ("quality-review", "_concept/11_build/acceptance-criteria/", "skills/quality-review/SKILL.md:62", "`11_build/acceptance-criteria/<featureset>/<feature_slug>.ac.md`"),
    ("quality-review", "_concept/11_build/reviews/", "skills/quality-review/SKILL.md:73", "to `11_build/reviews/<feature_slug>.yaml`"),
    ("quality-release", "_concept/11_build/release.yaml", "skills/quality-release/SKILL.md:74", "to `11_build/release.yaml`"),
    ("quality-interaction", "_concept/11_build/interaction.yaml", "skills/quality-interaction/SKILL.md:85", "**Write the verdict** to `_concept/11_build/interaction.yaml`"),
    ("quality-standards", "_concept/02_grounding/standards/", "skills/quality-standards/SKILL.md:30", "`02_grounding/standards/<domain>/<convention>.md`"),
    # no _concept target: the line shows what the skill produces instead
    ("ops-review", None, "skills/ops-review/SKILL.md:35", "never written to disk"),
    ("build-scaffold", None, "skills/build-scaffold/SKILL.md:89", "the app builds and runs"),
    ("build-database", None, "skills/build-database/SKILL.md:85", "the migration has applied"),
    ("build-branch", None, "skills/build-branch/SKILL.md:62", "the branch exists and is checked out"),
    ("quality-test", None, "skills/quality-test/SKILL.md:84", "has a test file at the levels"),
    ("skaileup", None, "skills/skaileup/SKILL.md:14", "It writes"),
]

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
CONTRACT_REF_RE = re.compile(r"(?<![A-Za-z0-9_./-])`?(?:\.\./)*contracts/([A-Za-z0-9_./-]+)`?")
STEP_RE = re.compile(r"^\d+\. \*\*", re.MULTILINE)
QUESTION_RE = re.compile(r"\b(ask|approve|approval|confirm|interview|grill|one question)\b", re.I)
CITE_RE = re.compile(r"^(.*):(\d+)(?:-(\d+))?$")


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def split_frontmatter(text: str) -> tuple[dict, str]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    try:
        data = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return {}, text[m.end():]
    return (data if isinstance(data, dict) else {}), text[m.end():]


def norm(path: str) -> str:
    return path.strip().rstrip("/")


def paths_overlap(a: str, b: str) -> bool:
    """Equal, or one is under the other (trailing slashes ignored)."""
    a, b = norm(a), norm(b)
    return a == b or a.startswith(b + "/") or b.startswith(a + "/")


def under(path: str, base: str) -> bool:
    path, base = norm(path), norm(base)
    return path == base or path.startswith(base + "/")


def artifact_of(path: str | None) -> str | None:
    """Deepest artifact target containing the path."""
    if not path:
        return None
    best = None
    for aid, apath in ARTIFACTS:
        if under(path, apath) and (best is None or len(apath) > len(best[1])):
            best = (aid, apath)
    return best[0] if best else None


def dump_json(name: str, rows: list) -> None:
    (OUT / f"{name}.json").write_text(json.dumps(rows, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def iso(ts: float) -> str:
    return datetime.datetime.fromtimestamp(ts).isoformat(timespec="seconds")


_LINES: dict[Path, list[str] | None] = {}


def file_lines(p: Path) -> list[str] | None:
    if p not in _LINES:
        try:
            _LINES[p] = p.read_text(encoding="utf-8").split("\n")
        except (OSError, UnicodeDecodeError):
            _LINES[p] = None
    return _LINES[p]


def check_citation(collection: str, row_id: str, at: str, quote: str) -> str | None:
    """Return a failure message, or None when `quote` is on a line of `at`."""
    head = f"[{collection}] {row_id}: at={at!r} quote={quote!r}"
    if not isinstance(at, str) or not isinstance(quote, str) or not quote:
        return f"{head}\n    -> `at` and `quote` must be non-empty strings"
    m = CITE_RE.match(at)
    if not m:
        return f"{head}\n    -> `at` is not path:N or path:A-B"
    path_s, a, b = m.group(1), int(m.group(2)), m.group(3)
    b = int(b) if b else a
    p = Path(path_s)
    if not p.is_absolute():
        p = ROOT / p
    lines = file_lines(p)
    if lines is None:
        return f"{head}\n    -> file not found: {p}"
    if a < 1 or b < a or b > len(lines):
        return f"{head}\n    -> line range outside the file ({len(lines)} lines)"
    if b - a > 7:
        return f"{head}\n    -> range longer than 8 lines"
    if any(quote in lines[i - 1] for i in range(a, b + 1)):
        return None
    hint = ""
    near = [i for i in range(max(1, a - 6), min(len(lines), b + 6) + 1) if quote in lines[i - 1]]
    if near:
        best = min(near, key=lambda i: min(abs(i - a), abs(i - b)))
        hint = f"\n    -> hint: the quote is on line {best}"
    else:
        anywhere = [i for i, ln in enumerate(lines, 1) if quote in ln]
        if anywhere:
            hint = f"\n    -> hint: the quote is not within +-6 lines; it is on line {anywhere[0]}"
        else:
            hint = "\n    -> hint: the quote is nowhere in that file"
    return head + hint


def quote_is_whole_line(at: str, quote: str) -> bool:
    """True when `quote` equals the stripped content of a cited line (a short line cannot be quoted longer)."""
    m = CITE_RE.match(at)
    p = Path(m.group(1))
    lines = file_lines(p if p.is_absolute() else ROOT / p) or []
    a = int(m.group(2))
    b = int(m.group(3) or a)
    return any(lines[i - 1].strip() == quote for i in range(a, b + 1))


# --------------------------------------------------------------------------
# collections
# --------------------------------------------------------------------------
def load_flows() -> list[dict]:
    rows = []
    for f in sorted((ROOT / "flows").glob("*/*.flow.yaml")):
        text = f.read_text(encoding="utf-8")
        doc = yaml.safe_load(text) or {}
        text_lines = text.split("\n")
        edges_at = next((i for i, ln in enumerate(text_lines) if re.match(r"^edges:", ln)), len(text_lines))

        def node_line(node_id: str) -> int | None:
            pat = re.compile(r"^\s*(?:-\s*)?id:\s*%s\s*$|\{\s*id:\s*%s\s*[,}]" % (re.escape(node_id), re.escape(node_id)))
            for i in range(edges_at):
                if pat.search(text_lines[i]):
                    return i + 1
            return None

        nodes = {n["id"]: n for n in doc.get("nodes", []) if isinstance(n, dict) and "id" in n}
        skill_nodes = {i: n for i, n in nodes.items() if n.get("type") == "skill"}
        out_edges: dict[str, list[str]] = {}
        for e in doc.get("edges", []):
            if e.get("type") == "flow":
                out_edges.setdefault(e["source"], []).append(e["target"])
        order_nodes, seen, queue = [], set(), [doc.get("entry")]
        while queue:
            cur = queue.pop(0)
            if cur in seen or cur is None:
                continue
            seen.add(cur)
            if cur in skill_nodes:
                order_nodes.append(cur)
            queue.extend(out_edges.get(cur, []))
        order = [skill_nodes[i]["data"]["skill"] for i in order_nodes]

        def label_of(node_id: str) -> str:
            n = skill_nodes.get(node_id)
            return n["data"]["skill"] if n else node_id

        def edge_line(src: str, tgt: str) -> int | None:
            pat = re.compile(r"source:\s*%s\s*[,}\n]|source:\s*%s\s*$" % (re.escape(src), re.escape(src)))
            pat2 = re.compile(r"target:\s*%s\s*(?:[,}]|$)" % re.escape(tgt))
            for i in range(edges_at + 1, len(text_lines)):
                if pat.search(text_lines[i]) and pat2.search(text_lines[i]):
                    return i + 1
            return None

        edge_lines = []
        for e in doc.get("edges", []):
            if e.get("type") != "flow":
                continue
            ln = edge_line(e["source"], e["target"])
            if ln is None:
                raise SystemExit(f"ABORT: {f.name}: no single-line yaml entry found for edge {e.get('source')} -> {e.get('target')}")
            edge_lines.append({"source": label_of(e["source"]), "target": label_of(e["target"]), "line": ln})
        node_lines = {skill_nodes[i]["data"]["skill"]: node_line(i) for i in skill_nodes}
        phases = {skill_nodes[i]["data"]["skill"]: skill_nodes[i]["data"].get("phase") for i in skill_nodes}
        rows.append({
            "id": doc.get("id") or f.name[: -len(".flow.yaml")],
            "name": doc.get("name"),
            "file": str(f.relative_to(ROOT)),
            "nodes_n": len(skill_nodes),
            "order": order,
            "requires_n": len(doc.get("requires") or []),
            "research_depth": (doc.get("globals") or {}).get("research_depth"),
            "unmet_hard": 0,
            "node_lines": node_lines,
            "edge_lines": edge_lines,
            "_phases": phases,
        })
    return rows


def load_contract_files() -> list[Path]:
    return [p for p in sorted((ROOT / "contracts").glob("*.md")) if p.name not in ("README.md", "CONTRACT.md")]


def load_skills(contract_stems: set[str]) -> list[dict]:
    rows = []
    for d in sorted((ROOT / "skills").iterdir()):
        f = d / "SKILL.md"
        if not f.is_file():
            continue
        text = f.read_text(encoding="utf-8")
        fm, body = split_frontmatter(text)
        meta = fm.get("metadata") if isinstance(fm.get("metadata"), dict) else {}
        arts = (meta.get("artifacts") or {}).get("requires") or []
        produces = [
            {"id": p.get("id"), "path": p.get("path")}
            for p in ((meta.get("artifacts") or {}).get("produces") or [])
            if isinstance(p, dict)
        ]
        prereq = meta.get("prerequisites") or {}
        lines = text.split("\n")
        prereqs = []
        for item in prereq.get("files") or []:
            if not isinstance(item, dict) or not item.get("path"):
                continue
            p = str(item["path"])
            at_line = next((i for i, ln in enumerate(lines, 1) if re.search(r"path:\s*[\"']?%s[\"']?" % re.escape(p), ln)), None)
            prereqs.append({
                "path": p,
                "gate": item.get("gate", "soft"),
                "min_entries": item.get("min_entries"),
                "at": f"skills/{fm.get('name', d.name)}/SKILL.md:{at_line}" if at_line else None,
            })
        cited = set()
        for ref in CONTRACT_REF_RE.findall(body):
            stem = ref.rstrip(".,;:)").split("/")[0]
            stem = stem[:-3] if stem.endswith(".md") else stem
            if stem in contract_stems:
                cited.add(f"c-{stem}")
        # numbered steps: a step runs to the next step, heading or "Done when"
        qsteps = 0
        body_lines = body.split("\n")
        starts = [i for i, ln in enumerate(body_lines) if re.match(r"^\d+\. \*\*", ln)]
        for k, s in enumerate(starts):
            end = len(body_lines)
            for j in range(s + 1, len(body_lines)):
                if re.match(r"^\d+\. \*\*", body_lines[j]) or body_lines[j].startswith("#") or body_lines[j].startswith("**Done when"):
                    end = j
                    break
            if QUESTION_RE.search("\n".join(body_lines[s:end])):
                qsteps += 1
        sid = str(fm.get("name") or d.name)
        n_lines = len(text.rstrip("\n").split("\n")) if text else 0
        rows.append({
            "id": sid,
            "dir": d.name,
            "domain": "collection" if sid.split("-")[0] == "skaileup" else sid.split("-")[0],
            "lines": n_lines,
            "steps": len(STEP_RE.findall(body)),
            "description": fm.get("description", ""),
            "requires": [a.get("id") for a in arts if isinstance(a, dict)],
            "produces": produces,
            "prereqs": prereqs,
            "hard_n": sum(1 for p in prereqs if p["gate"] == "hard"),
            "soft_n": sum(1 for p in prereqs if p["gate"] != "hard"),
            "inputs_optional": [i.get("id") for i in (prereq.get("inputs_optional") or []) if isinstance(i, dict)],
            "contracts": sorted(cited),
            "contracts_n": len(cited),
            "question_steps": qsteps,
            "glossary_mentions": len(re.findall(r"glossary", body, re.I)),
            "flows": [],
            "phase": "none",
            "findings_n": 0,
            "findings": [],
            "_body": body,
        })
    return rows


def parse_tree_forms() -> dict[str, str]:
    """artifact path -> editor form, from the fenced tree in contracts/concept_structure.md."""
    lines = (ROOT / "contracts/concept_structure.md").read_text(encoding="utf-8").split("\n")
    start = next(i for i, ln in enumerate(lines) if ln.strip() == "_concept/")
    end = next(i for i in range(start, len(lines)) if lines[i].startswith("```"))
    groups: dict[str, set[str]] = {}
    cur = None
    for ln in lines[start + 1:end]:
        m = re.search(r"[├└]──\s+(\S+)", ln)
        if not m:
            continue
        token = m.group(1)
        is_top = re.match(r"^[├└]──", ln) is not None
        if is_top:
            cur = token.rstrip("/")
            groups[cur] = set()
            if token.endswith("/"):
                continue  # the folder line itself says nothing about its files
        if cur is None:
            continue
        ext = re.search(r"\.([A-Za-z0-9]+)$", token)
        e = ext.group(1).lower() if ext and not token.endswith("/") else None
        if e == "md":
            groups[cur].add("md")
        elif e in ("yaml", "yml", "json", "dbml", "txt"):
            groups[cur].add("code")
        elif e == "html":
            groups[cur].add("html")
        else:
            groups[cur].add("other")  # a folder entry or an image glob: no single editor form
    forms = {}
    for name, kinds in groups.items():
        if "other" in kinds or not kinds:
            form = "mixed"
        elif kinds == {"md"}:
            form = "prose (TipTap)"
        elif kinds <= {"code"}:
            form = "code editor"
        elif kinds == {"html"}:
            form = "preview"
        else:
            form = "mixed"
        forms[name] = form
    return forms


def main() -> int:
    failures: list[str] = []

    # ---- writer map ------------------------------------------------------
    writes = []
    skill_dirs = {p.name for p in (ROOT / "skills").iterdir() if (p / "SKILL.md").is_file()}
    for n, (skill, path, at, quote) in enumerate(WRITES, 1):
        rid = f"w-{n}"
        if skill not in skill_dirs:
            failures.append(f"[writes] {rid}: unknown skill {skill!r}")
        msg = check_citation("writes", f"{rid} ({skill} -> {path})", at, quote)
        if msg:
            failures.append(msg)
        if path is not None and path not in PROJECT_ROOT_ARTIFACTS and artifact_of(path) is None:
            failures.append(f"[writes] {rid}: path {path!r} is under no artifact target")
        writes.append({"id": rid, "skill": skill, "path": path, "artifact": artifact_of(path), "at": at, "quote": quote})

    # ---- contracts / skills / flows --------------------------------------
    contract_files = load_contract_files()
    stems = {p.stem for p in contract_files}
    skills = load_skills(stems)
    skill_ids = {s["id"] for s in skills}
    flows = load_flows()
    contract_ids = {f"c-{s}" for s in stems}
    flow_ids = {f["id"] for f in flows}
    artifact_ids = {a for a, _ in ARTIFACTS}

    by_skill = {s["id"]: s for s in skills}

    # ---- writer map vs the skills' own `produces` ------------------------------
    # WRITES is the independent, body-cited check of the frontmatter; the two must cover each other.
    produces_gaps: list[str] = []
    for s in skills:
        wpaths = sorted({w["path"] for w in writes if w["skill"] == s["id"] and w["path"]})
        ppaths = [p["path"] for p in s["produces"]]
        for wp in wpaths:
            if not any(paths_overlap(wp, pp) for pp in ppaths):
                produces_gaps.append(f"{s['id']}: WRITES row {wp} is covered by no `produces` path")
        for pp in ppaths:
            if not any(paths_overlap(wp, pp) for wp in wpaths):
                produces_gaps.append(f"{s['id']}: `produces` path {pp} has no WRITES row")
    for w in writes:
        sk = by_skill.get(w["skill"])
        w["in_produces"] = bool(w["path"] and sk and any(paths_overlap(w["path"], p["path"]) for p in sk["produces"]))
    for f in flows:
        phases = f.pop("_phases")
        for sk in f["order"]:
            if sk not in by_skill:
                failures.append(f"[flows] {f['id']}: node skill {sk!r} has no skills/ directory")
                continue
            by_skill[sk]["flows"].append(f["id"])
            ph = phases.get(sk)
            cur = by_skill[sk]["phase"]
            if ph and ph not in cur.split("/") and cur != "none":
                by_skill[sk]["phase"] = f"{cur}/{ph}"
            elif ph and cur == "none":
                by_skill[sk]["phase"] = ph

    contracts = []
    for p in contract_files:
        readers = sorted(s["id"] for s in skills if f"c-{p.stem}" in s["contracts"])
        contracts.append({
            "id": f"c-{p.stem}",
            "file": f"contracts/{p.name}",
            "lines": len(p.read_text(encoding="utf-8").rstrip("\n").split("\n")),
            "readers": readers,
            "readers_n": len(readers),
        })

    # ---- gates -----------------------------------------------------------
    writes_by_skill: dict[str, list[str]] = {}
    for w in writes:
        if w["path"]:
            writes_by_skill.setdefault(w["skill"], []).append(w["path"])
    gates = []
    for f in flows:
        for pos, sk in enumerate(f["order"], 1):
            if sk not in by_skill:
                continue
            for pr in by_skill[sk]["prereqs"]:
                producer = None
                for j in range(pos - 2, -1, -1):
                    up = f["order"][j]
                    if any(paths_overlap(wp, pr["path"]) for wp in writes_by_skill.get(up, [])):
                        producer = up
                        break
                project_gate = not pr["path"].startswith("_concept/") and pr["path"] not in PROJECT_ROOT_ARTIFACTS
                unmet = pr["gate"] == "hard" and producer is None and not project_gate
                if unmet:
                    f["unmet_hard"] += 1
                gates.append({
                    "id": f"{f['id']}:{sk}:{pr['path']}",
                    "flow": f["id"],
                    "position": pos,
                    "skill": sk,
                    "path": pr["path"],
                    "gate": pr["gate"],
                    "producer": producer,
                    "satisfied": producer is not None,
                    "unmet_hard": unmet,
                    "satisfied_s": "yes" if producer is not None else "no",
                    "prereq_at": pr["at"],
                })

    # ---- artifacts -------------------------------------------------------
    forms = parse_tree_forms()
    artifacts = []
    for aid, apath in ARTIFACTS:
        writers = sorted({w["skill"] for w in writes if w["artifact"] == aid})
        token = apath.split("/")[-1]
        readers = sorted(
            s["id"] for s in skills
            if any(under(pr["path"], apath) for pr in s["prereqs"]) or token in s["_body"]
        )
        form = forms.get(token)
        if form is None:
            failures.append(f"[artifacts] {aid}: no entry {token!r} in the tree of contracts/concept_structure.md")
            form = "mixed"
        artifacts.append({
            "id": aid,
            "path": apath,
            "writers": writers,
            "writers_n": len(writers),
            "multi_writer": len(writers) > 1,
            "readers": readers,
            "readers_n": len(readers),
            "editor_form": form,
            "kind": "artifact",
        })

    # ---- findings --------------------------------------------------------
    findings: list[dict] = []
    if FINDINGS_DIR.is_dir():
        for part in sorted(FINDINGS_DIR.glob("*.json")):
            try:
                data = json.loads(part.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                failures.append(f"[findings] {part.name}: invalid JSON: {exc}")
                continue
            if not isinstance(data, list):
                failures.append(f"[findings] {part.name}: top level is not an array")
                continue
            for row in data:
                if isinstance(row, dict):
                    row["_file"] = part.name
                findings.append(row)
    warnings: list[str] = []
    seen_ids: set[str] = set()
    required = ["id", "sev", "lens", "stage", "skills", "contracts", "flows", "artifacts", "title", "detail", "evidence", "recommendation"]
    for row in findings:
        if not isinstance(row, dict):
            failures.append(f"[findings] non-object row: {row!r}")
            continue
        fid = row.get("id", "?")
        tag = f"{fid} ({row.get('_file')})"
        for k in required:
            if k not in row:
                failures.append(f"[findings] {tag}: missing key {k!r}")
        if fid in seen_ids:
            failures.append(f"[findings] {tag}: duplicate id")
        seen_ids.add(fid)
        if not re.fullmatch(r"F\d\d", str(fid)):
            failures.append(f"[findings] {tag}: id is not F<2 digits>")
        if row.get("sev") not in SEVS:
            failures.append(f"[findings] {tag}: sev {row.get('sev')!r} not in {SEVS}")
        if row.get("lens") not in LENSES:
            failures.append(f"[findings] {tag}: lens {row.get('lens')!r} not in {LENSES}")
        if row.get("stage") not in [f"s-{s}" for s in STAGES]:
            failures.append(f"[findings] {tag}: stage {row.get('stage')!r} unknown")
        if len(str(row.get("title", ""))) > 80:
            failures.append(f"[findings] {tag}: title longer than 80 characters ({len(row['title'])})")
        for key, known in (("skills", skill_ids), ("contracts", contract_ids), ("flows", flow_ids), ("artifacts", artifact_ids)):
            for v in row.get(key) or []:
                if v not in known:
                    failures.append(f"[findings] {tag}: {key} entry {v!r} does not exist")
        status = row.get("status", "open")
        if status not in STATUSES:
            failures.append(f"[findings] {tag}: status {status!r} not in {STATUSES}")
        if status == "closed" and not re.fullmatch(r"i-ssi-[a-z0-9-]+", str(row.get("closed_by", ""))):
            failures.append(f"[findings] {tag}: a closed finding needs `closed_by`: an i-ssi-<ticket> id")
        if status == "open" and row.get("closed_by"):
            failures.append(f"[findings] {tag}: an open finding carries `closed_by`")
        ev = row.get("evidence")
        if not isinstance(ev, list) or not ev:
            failures.append(f"[findings] {tag}: evidence must be a non-empty array")
            continue
        if status == "closed":
            continue  # the quoted problem text is gone or changed: that is what closed means
        for k, e in enumerate(ev):
            if not isinstance(e, dict):
                failures.append(f"[findings] {tag}: evidence[{k}] is not an object")
                continue
            msg = check_citation("findings", f"{fid} evidence[{k}]", e.get("at"), e.get("quote"))
            if msg:
                failures.append(msg)
            elif not (10 <= len(e["quote"]) <= 80) and not (len(e["quote"]) < 10 and quote_is_whole_line(e["at"], e["quote"])):
                warnings.append(f"[findings] {fid} evidence[{k}]: quote is {len(e['quote'])} characters (10-80 wanted)")

    if failures:
        print(f"ABORT: {len(failures)} failure(s); nothing was written.\n", file=sys.stderr)
        for msg in failures:
            print(msg, file=sys.stderr)
        return 1

    for row in findings:
        row.pop("_file", None)
        row["first_at"] = row["evidence"][0]["at"]
        row["refs"] = list(dict.fromkeys(list(row["skills"]) + list(row["contracts"]) + list(row["flows"]) + list(row["artifacts"])))
        row["status"] = row.get("status", "open")
        row["closed_by"] = row.get("closed_by", "")
        row["closed_note"] = row.get("closed_note", "")
        row["open_reason"] = row.get("open_reason", "")
    for s in skills:
        named = [f["id"] for f in findings if s["id"] in f["skills"]]
        s["findings"] = named
        s["findings_n"] = len(named)
        s.pop("_body")

    # ---- stages ----------------------------------------------------------
    stages = []
    for i, dom in enumerate(STAGES, 1):
        in_stage = [s for s in skills if s["domain"] == dom]
        stages.append({
            "id": f"s-{dom}",
            "label": dom,
            "order": i,
            "skills_n": len(in_stage),
            "lines": sum(s["lines"] for s in in_stage),
            "findings_n": sum(1 for f in findings if f["stage"] == f"s-{dom}"),
            "open_n": sum(1 for f in findings if f["stage"] == f"s-{dom}" and f["status"] == "open"),
        })

    # ---- freshness input: read BEFORE writing ----------------------------
    old_out = [p.stat().st_mtime for p in OUT.glob("*.json")]
    prev_out = min(old_out) if old_out else None

    sources = [p for p in (ROOT / "skills").rglob("*") if p.is_file()]
    sources += list((ROOT / "contracts").glob("*.md"))
    sources += [p for p in (ROOT / "flows").rglob("*") if p.is_file()]
    sources += list((ROOT / "profiles").glob("*.yaml"))
    sources.append(ROOT / "scripts/check.py")
    sources += [p for p in FINDINGS_DIR.glob("*.json")]
    cited: set[Path] = set()
    for row in findings:
        if row["status"] == "closed":
            continue  # a closed finding's evidence is not validated, so it is not a freshness source
        for e in row["evidence"]:
            m = CITE_RE.match(e["at"])
            p = Path(m.group(1))
            cited.add(p if p.is_absolute() else ROOT / p)
    sources += sorted(cited)

    # ---- write -----------------------------------------------------------
    OUT.mkdir(parents=True, exist_ok=True)
    dump_json("skills", skills)
    dump_json("contracts", contracts)
    dump_json("flows", flows)
    dump_json("gates", gates)
    dump_json("artifacts", artifacts)
    dump_json("writes", writes)
    dump_json("findings", findings)
    dump_json("stages", stages)

    hard = sum(1 for g in gates if g["gate"] == "hard")
    unmet = sum(1 for g in gates if g["unmet_hard"])
    closed = sum(1 for f in findings if f["status"] == "closed")
    print(
        f"skills {len(skills)} · contracts {len(contracts)} · flows {len(flows)} · "
        f"gates {len(gates)} (hard {hard}, unmet hard {unmet}) · artifacts {len(artifacts)} · "
        f"writes {len(writes)} · findings {len(findings)} (closed {closed}, open {len(findings) - closed}) · stages {len(stages)}"
    )
    print("severity (open): " + ", ".join(f"{s} {sum(1 for f in findings if f['sev'] == s and f['status'] == 'open')}" for s in SEVS))
    print("lens (open): " + ", ".join(f"{l} {sum(1 for f in findings if f['lens'] == l and f['status'] == 'open')}" for l in LENSES))
    for f in findings:
        if f["status"] == "open":
            print(f"open: {f['id']} {f['title']}")
    print(f"writes vs produces: {len(produces_gaps)} disagreement(s)")
    for msg in produces_gaps:
        print("disagreement: " + msg)
    for w in warnings:
        print("warning: " + w)

    newest, newest_src = max(((p.stat().st_mtime, p) for p in sources if p.exists()), key=lambda t: t[0])
    prev = f"{iso(prev_out)}" if prev_out is not None else "none"
    print(f"newest source mtime: {iso(newest)} ({newest_src.relative_to(ROOT) if newest_src.is_relative_to(ROOT) else newest_src})  previous output: {prev}")
    if prev_out is not None and newest > prev_out:
        print("STALE: sources changed since the last dump")
    return 0


if __name__ == "__main__":
    sys.exit(main())
