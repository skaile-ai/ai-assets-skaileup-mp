#!/usr/bin/env python3
"""check.py — the collection's self-check.

One script, one CI job. It answers a single question: would this collection
install and run, or does it contain a reference that silently resolves to
nothing?

Every check here exists because its failure mode is *quiet*. A skill whose
directory disagrees with its `name:` installs under the directory and the flow
node that names it runs with an empty prompt, reporting `satisfied: true`. A
prerequisite path that no skill writes is a gate that can never open. A cited
contract that was deleted reads as fine. None of these raise anywhere in the
toolchain, so they are raised here.

Usage:
  python scripts/check.py [--repo <path>]

Exit codes:
  0  no errors
  1  at least one error
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

# The published skill body ceiling (ADR 0003). A whole SKILL.md, frontmatter
# included — that is how a reader meets it.
LINE_BUDGET = 140

# Every declared prerequisite path is joined to the *project* root, never to the concept
# (`resolver/src/validator.ts:81`), so the prefix is part of the declaration.
ARTIFACT_ROOT = "_concept"

# forge-concept's lane vocabulary (`shared/flow-phases.ts`). An invalid value is
# silently swallowed there, which is why it is checked here.
PHASES = {"conceptualization", "implementation", "review"}

# The engine takes dependencies from `edges.filter(e => e.type === "flow")`.
# Any other type — or no type — draws an edge that orders nothing.
FLOW_EDGE = "flow"


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []

    def error(self, where: str, msg: str) -> None:
        self.errors.append(f"{where}: {msg}")

    def ok(self) -> bool:
        return not self.errors


# --------------------------------------------------------------------------
# frontmatter
# --------------------------------------------------------------------------

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def split_frontmatter(text: str) -> tuple[dict, str]:
    """Return (frontmatter dict, body). Missing or unparseable frontmatter is {}."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    try:
        data = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return {}, text[m.end():]
    return (data if isinstance(data, dict) else {}), text[m.end():]


# --------------------------------------------------------------------------
# the artifact tree — parsed from the contract, never restated here
# --------------------------------------------------------------------------

TREE_ENTRY_RE = re.compile(r"^[├└]── (\S+)")


def _fenced_tree(repo: Path) -> set[str]:
    """The set of legal first path segments under `_concept/`.

    Read out of `contracts/concept_structure.md`'s fenced tree so this check
    cannot drift from the contract it enforces: renaming a directory there
    renames it here.
    """
    contract = repo / "contracts" / "concept_structure.md"
    if not contract.is_file():
        return set()
    lines = contract.read_text().splitlines()
    entries: set[str] = set()
    inside = False
    for line in lines:
        if line.strip().startswith("```"):
            if inside:
                break
            inside = True
            continue
        if inside:
            m = TREE_ENTRY_RE.match(line)
            if m:
                entries.add(m.group(1).rstrip("/"))
    return entries


# --------------------------------------------------------------------------
# skills
# --------------------------------------------------------------------------

CONTRACT_REF_RE = re.compile(r"`?contracts/([A-Za-z0-9_./-]+)`?")


def check_skills(repo: Path, rep: Report) -> set[str]:
    """Check every skill. Returns the set of installable skill names."""
    skills_dir = repo / "skills"
    names: set[str] = set()
    if not skills_dir.is_dir():
        return names

    top_level = _fenced_tree(repo)

    for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
        directory = skill_md.parent.name
        where = f"skills/{directory}"
        text = skill_md.read_text()
        fm, _body = split_frontmatter(text)

        if not fm:
            rep.error(where, "SKILL.md has no parseable YAML frontmatter")
            continue

        # 1. identity. Three of the four roles a skill name plays resolve
        #    through the directory, and forge-concept never reads `name:` for
        #    identity at all — so a mismatch is invisible until a node runs
        #    with no skill body.
        name = fm.get("name")
        if not name:
            rep.error(where, "frontmatter has no `name:`")
        elif name != directory:
            rep.error(where, f"`name:` is {name!r} but the directory is {directory!r} — they must match character for character")
        else:
            names.add(name)

        # 2. the one frontmatter field with a live reader.
        if "version" not in fm:
            rep.error(where, "frontmatter has no `version:`")

        # 3. the body ceiling.
        line_count = len(text.splitlines())
        if line_count > LINE_BUDGET:
            rep.error(where, f"SKILL.md is {line_count} lines, over the {LINE_BUDGET}-line ceiling")

        # 4. the machine layer has to be where its readers look. `parseSkillRequirements`
        #    reads `fm.metadata.prerequisites` and `extractSkillRequires` returns early on a
        #    missing `metadata` — neither falls back to the root, and neither raises. A block
        #    at the root parses clean and reports `satisfied: true` on an unmet gate.
        for key in ("artifacts", "prerequisites"):
            if key in fm:
                rep.error(where, f"`{key}:` is at the frontmatter root — it must sit under `metadata:`, which is the only place its reader looks")

        # 5. declared prerequisites are joined to the *project* root (`validator.ts:81`),
        #    not to `_concept/`, so a path without the prefix resolves one level too high —
        #    and its first segment inside the tree has to be a real one.
        for entry in _prerequisite_paths(fm):
            if not entry.startswith(ARTIFACT_ROOT + "/"):
                rep.error(
                    where,
                    f"prerequisite path {entry!r} does not start with {ARTIFACT_ROOT + '/'!r} — "
                    f"the validator joins it to the project root, so it would resolve outside the concept",
                )
                continue
            if top_level:
                first = entry[len(ARTIFACT_ROOT) + 1:].split("/", 1)[0]
                if first not in top_level:
                    rep.error(
                        where,
                        f"prerequisite path {entry!r} starts at {first!r}, which is not a "
                        f"top-level entry of the artifact tree",
                    )

        # 6. cited contracts must exist.
        for ref in sorted(set(CONTRACT_REF_RE.findall(text))):
            ref = ref.rstrip(".,;:)")
            if not (repo / "contracts" / ref).exists():
                rep.error(where, f"cites `contracts/{ref}`, which does not exist")

    return names


def _prerequisite_paths(fm: dict) -> list[str]:
    """Declared file gates, read the way the resolver reads them — and also from the root,
    so a misplaced block is checked for its paths rather than silently skipped."""
    meta = fm.get("metadata") if isinstance(fm.get("metadata"), dict) else {}
    prereq = meta.get("prerequisites") or fm.get("prerequisites") or {}
    if not isinstance(prereq, dict):
        return []
    files = prereq.get("files") or []
    out = []
    for item in files:
        if isinstance(item, dict) and item.get("path"):
            out.append(str(item["path"]).lstrip("/"))
    return out


# --------------------------------------------------------------------------
# contracts
# --------------------------------------------------------------------------

def check_contracts(repo: Path, rep: Report) -> None:
    """Contracts cite each other too, and are pruned aggressively."""
    contracts_dir = repo / "contracts"
    if not contracts_dir.is_dir():
        return
    for path in sorted(contracts_dir.glob("*.md")):
        text = path.read_text()
        for ref in sorted(set(CONTRACT_REF_RE.findall(text))):
            ref = ref.rstrip(".,;:)")
            if not (contracts_dir / ref).exists():
                rep.error(f"contracts/{path.name}", f"cites `contracts/{ref}`, which does not exist")


# --------------------------------------------------------------------------
# flows
# --------------------------------------------------------------------------

def check_flows(repo: Path, skill_names: set[str], rep: Report) -> None:
    flows_dir = repo / "flows"
    if not flows_dir.is_dir():
        return

    for flow_file in sorted(flows_dir.glob("*/*.flow.yaml")):
        where = f"flows/{flow_file.parent.name}/{flow_file.name}"
        try:
            flow = yaml.safe_load(flow_file.read_text()) or {}
        except yaml.YAMLError as exc:
            rep.error(where, f"is not parseable YAML: {exc}")
            continue
        if not isinstance(flow, dict):
            rep.error(where, "does not contain a mapping")
            continue
        _check_one_flow(repo, flow, flow_file, where, skill_names, rep)


def _check_one_flow(
    repo: Path, flow: dict, flow_file: Path, where: str, skill_names: set[str], rep: Report
) -> None:
    stem = flow_file.name[: -len(".flow.yaml")]
    directory = flow_file.parent.name
    flow_id = flow.get("id")

    # identity — the loader finds a flow by directory, the manifest names it by id.
    if not flow_id:
        rep.error(where, "has no `id:`")
    elif flow_id != stem or flow_id != directory:
        rep.error(where, f"`id:` {flow_id!r} must equal both the filename stem {stem!r} and the directory {directory!r}")

    # platform's validateFlow requires `name`; forge-concept's loader does not.
    # Carrying it satisfies both, at the cost of one line.
    if not flow.get("name"):
        rep.error(where, "has no top-level `name:` (platform's validateFlow requires it)")

    nodes = flow.get("nodes") or []
    edges = flow.get("edges") or []
    if not isinstance(nodes, list) or not nodes:
        rep.error(where, "has no `nodes:` — the loader discards a flow missing id/nodes/edges")
        return
    if not isinstance(edges, list):
        rep.error(where, "`edges:` is not a list")
        return

    # node ids
    ids: list[str] = []
    for node in nodes:
        if not isinstance(node, dict) or not node.get("id"):
            rep.error(where, "a node has no `id`")
            continue
        ids.append(node["id"])
    seen: set[str] = set()
    for nid in ids:
        if nid in seen:
            rep.error(where, f"duplicate node id {nid!r}")
        seen.add(nid)

    by_id = {n["id"]: n for n in nodes if isinstance(n, dict) and n.get("id")}

    # phase, skill resolution, parentNode
    node_skills: set[str] = set()
    subflow_targets: set[str] = set()
    for node in nodes:
        if not isinstance(node, dict) or not node.get("id"):
            continue
        nid = node["id"]
        data = node.get("data") or {}
        kind = node.get("type")

        phase = data.get("phase")
        if phase is None:
            rep.error(where, f"node {nid!r} declares no `data.phase` — forge-concept then guesses from the skill name")
        elif phase not in PHASES:
            rep.error(where, f"node {nid!r} has `data.phase: {phase!r}`, not one of {sorted(PHASES)}")

        if kind == "skill" or (kind is None and data.get("skill")):
            skill = data.get("skill")
            if not skill:
                rep.error(where, f"skill node {nid!r} has no `data.skill`")
            else:
                node_skills.add(skill)
                if skill_names and skill not in skill_names:
                    rep.error(where, f"node {nid!r} names skill {skill!r}, which has no `skills/{skill}/` directory")
        elif kind == "sub-flow":
            target = data.get("flow") or data.get("target")
            if not target:
                rep.error(where, f"sub-flow node {nid!r} names no flow")
            else:
                subflow_targets.add(target)
        elif kind == "router":
            for route in data.get("routes") or []:
                tgt = route.get("target") if isinstance(route, dict) else None
                if tgt is not None and tgt not in by_id:
                    rep.error(where, f"router {nid!r} routes to {tgt!r}, which is not a node id")
            default = data.get("default")
            if default is not None and default not in by_id:
                rep.error(where, f"router {nid!r} has default {default!r}, which is not a node id")

        parent = node.get("parentNode")
        if parent is not None:
            if parent not in by_id:
                rep.error(where, f"node {nid!r} has parentNode {parent!r}, which is not a node id")
            elif by_id[parent].get("type") != "group":
                rep.error(where, f"node {nid!r} has parentNode {parent!r}, which is not a group node")

    # edges
    for edge in edges:
        if not isinstance(edge, dict):
            rep.error(where, "an edge is not a mapping")
            continue
        src, tgt = edge.get("source"), edge.get("target")
        eid = edge.get("id", f"{src}->{tgt}")
        if src not in by_id:
            rep.error(where, f"edge {eid!r} has source {src!r}, which is not a node id")
        if tgt not in by_id:
            rep.error(where, f"edge {eid!r} has target {tgt!r}, which is not a node id")
        if src is not None and src == tgt:
            rep.error(where, f"edge {eid!r} is a self-loop on {src!r}")

    # reachability under flow-typed edges. This is the check that catches the
    # untyped edge: `type` is optional in every schema in play, so an edge
    # without it validates green, draws on the canvas, and orders nothing.
    _check_reachability(flow, by_id, edges, where, rep)

    # requires: exactness. A missing entry is not a house-rule violation — the
    # skill is then never installed, and the node runs with an empty prompt.
    _check_requires(flow, node_skills, subflow_targets, repo, where, rep)


def _check_reachability(flow: dict, by_id: dict, edges: list, where: str, rep: Report) -> None:
    entry = flow.get("entry")
    if not entry:
        rep.error(where, "has no `entry:`")
        return
    if entry not in by_id:
        rep.error(where, f"`entry: {entry!r}` is not a node id")
        return

    adjacency: dict[str, list[str]] = {}
    for edge in edges:
        if not isinstance(edge, dict):
            continue
        if edge.get("type") == FLOW_EDGE:
            adjacency.setdefault(edge.get("source"), []).append(edge.get("target"))
    # a router hands control on without an edge
    for nid, node in by_id.items():
        if node.get("type") == "router":
            data = node.get("data") or {}
            targets = [r.get("target") for r in (data.get("routes") or []) if isinstance(r, dict)]
            targets.append(data.get("default"))
            adjacency.setdefault(nid, []).extend(t for t in targets if t)

    reached = {entry}
    stack = [entry]
    while stack:
        cur = stack.pop()
        for nxt in adjacency.get(cur, []):
            if nxt and nxt not in reached:
                reached.add(nxt)
                stack.append(nxt)

    # group nodes are containers, not steps — they carry no flow edges.
    for nid, node in sorted(by_id.items()):
        if node.get("type") == "group":
            continue
        if nid not in reached:
            rep.error(
                where,
                f"node {nid!r} is unreachable from `entry` along `type: flow` edges — "
                f"it will never run, whatever else connects it",
            )


REF_RE = re.compile(r"^(skill|flow|contract):@([A-Za-z0-9_-]+)/([A-Za-z0-9_.-]+)(?:#(.+))?$")


def _check_requires(
    flow: dict, node_skills: set[str], subflow_targets: set[str], repo: Path, where: str, rep: Report
) -> None:
    requires = flow.get("requires")
    if requires is None:
        rep.error(where, "has no `requires:` manifest — installing the flow would install none of its skills")
        return

    declared_skills: set[str] = set()
    declared_flows: set[str] = set()
    for ref in requires:
        m = REF_RE.match(str(ref))
        if not m:
            rep.error(where, f"`requires:` entry {ref!r} is not a `kind:@publisher/name` ref")
            continue
        kind, _publisher, name, _version = m.groups()
        if kind == "skill":
            declared_skills.add(name)
        elif kind == "flow":
            declared_flows.add(name)
        elif kind == "contract":
            if not (repo / "contracts" / f"{name}.md").is_file():
                rep.error(where, f"`requires:` names contract {name!r}, but `contracts/{name}.md` does not exist")

    for missing in sorted(node_skills - declared_skills):
        rep.error(where, f"runs skill {missing!r} but does not list it in `requires:` — it would not be installed")
    for extra in sorted(declared_skills - node_skills):
        rep.error(where, f"`requires:` lists skill {extra!r}, which no node in this flow runs")
    for missing in sorted(subflow_targets - declared_flows):
        rep.error(where, f"delegates to flow {missing!r} but does not list it in `requires:`")
    for extra in sorted(declared_flows - subflow_targets):
        rep.error(where, f"`requires:` lists flow {extra!r}, which no sub-flow node delegates to")


# --------------------------------------------------------------------------

def run(repo: Path) -> Report:
    rep = Report()
    skill_names = check_skills(repo, rep)
    check_contracts(repo, rep)
    check_flows(repo, skill_names, rep)
    return rep


def main() -> int:
    parser = argparse.ArgumentParser(description="Check the collection for references that resolve to nothing.")
    parser.add_argument("--repo", default=None, help="repo root (default: the parent of this script's directory)")
    args = parser.parse_args()

    repo = Path(args.repo).resolve() if args.repo else Path(__file__).resolve().parent.parent
    rep = run(repo)

    skills = len(list((repo / "skills").glob("*/SKILL.md"))) if (repo / "skills").is_dir() else 0
    flows = len(list((repo / "flows").glob("*/*.flow.yaml"))) if (repo / "flows").is_dir() else 0

    for err in rep.errors:
        print(f"ERROR {err}")

    print(f"\n{skills} skill(s) · {flows} flow(s) · {len(rep.errors)} error(s)")
    return 0 if rep.ok() else 1


if __name__ == "__main__":
    sys.exit(main())
