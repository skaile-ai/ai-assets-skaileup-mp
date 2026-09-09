#!/usr/bin/env python3
"""check.py — the collection's self-check.

One script, one CI job. It answers a single question: would this collection
install and run, or does it contain a reference that silently resolves to
nothing?

Every check here exists because its failure mode is *quiet*. A skill whose
directory disagrees with its `name:` installs under the directory and the flow
node that names it runs with an empty prompt, reporting `satisfied: true`. A
prerequisite path that no skill writes is a gate that can never open. A cited
contract that was deleted reads as fine. A node whose `data.phase` contradicts
its group's renders in the group's lane and never says so. None of these raise
anywhere in the toolchain, so they are raised here.

This is the collection's only real gate. forge-concept validates no flow at all — it
loads them and drops the malformed ones silently — so anything not checked here is not
checked anywhere.

About a dozen rules here are copies of facts in forge-concept and @skaile/workspaces.
Each names its fact id and nothing else: `scripts/host_facts.py` owns the path, the
signature and the date, and `scripts/verify_host.py` greps them against real checkouts.
A `file:line` in a comment is not a citation — ticket 40 measured four of fourteen
rotting in two weeks while every underlying fact still held.

The rules are only as good as the fixtures behind them, so this script runs
`test_check.py` as its last phase. That is not tidiness: ticket 34 changed these
rules without updating those fixtures, `check.py` printed a confident `0 error(s)`
because it did not run them, and `main` was red for ~13 hours. One command has to
mean green, or half of the gate is optional in practice.

Usage:
  python scripts/check.py [--repo <path>] [--no-tests]

Exit codes:
  0  the collection checks out and the checker's own fixtures pass
  1  at least one error, or a failing fixture, or pytest is missing
"""
from __future__ import annotations

import argparse
import re
import subprocess
import unicodedata
import sys
from pathlib import Path

import yaml

import host_facts as hf

# The published skill body ceiling (ADR 0003). A whole SKILL.md, frontmatter
# included — that is how a reader meets it.
LINE_BUDGET = 140

# Every declared prerequisite path is joined to the *project* root, never to the concept
# (`host:prerequisite-project-root`), so the prefix is part of the declaration.
ARTIFACT_ROOT = "_concept"

# The named exceptions to "every prerequisite path lives under `_concept/`".
#
# `host:prerequisite-project-root` joins the declared path to the *project* root, so a project-root
# gate like `package.json` resolves correctly — the blanket ban this check used to carry
# was stricter than the reader it protects (found by ticket 23, which had to move
# `quality-test`'s source-exists gate into the step body to work around it).
#
# The ban still earns its keep for everything else, and the reason is drift, not the
# reader: the dominant defect class in this repo is a *concept* path written against a
# superseded tree (ADR 0007 renamed the whole first level; ticket 30 swept 32 files of
# it). Allowing arbitrary paths outside `_concept/` would let `experience/screens/foo.md`
# — a pre-0007 concept path — pass as "some project-root file". So the restriction stays,
# narrowed from a ban to this list: a path is legal if it is under `_concept/` (and its
# first segment is a real entry of the artifact tree) or if it is named here. Extend the
# list deliberately; a project-root path cannot be verified from inside this collection,
# because whether it exists is a fact about the scaffolded project, not about this repo.
PROJECT_ROOT_PREREQUISITES = {"package.json"}

# forge-concept's lane vocabulary (`host:phase-lane-vocabulary`). An invalid value is
# silently swallowed there, which is why it is checked here.
PHASES = {"conceptualization", "implementation", "review"}

# The engine takes dependencies from `edges.filter(e => e.type === "flow")`.
# Any other type — or no type — draws an edge that orders nothing.
FLOW_EDGE = "flow"

# Ticket 10: `-mp` ships `skill` and `group` nodes only. The `sub-flow` kind died with
# the shared building blocks (every loaded flow becomes an onboarding card, so a flow
# that is not a way to start a project has no business being one), and `router` died
# with the pick-one renderers.
NODE_KINDS = {"skill", "group"}

# `host:profile-onboarding` casts `meta.onboarding.input_style` to this union without
# checking it; the wizard then branches on it and renders nothing for a value outside
# the set.
INPUT_STYLES = {"freeform", "structured", "repo"}

# `host:research-depth-options` publishes exactly these as the selectable depths.
RESEARCH_DEPTHS = {"skip", "light", "moderate", "deep"}

# Keys ticket 10 deleted as decoration. `meta.category` and the globals fell through
# every reader, which makes their bans house style — a decision this map made, owned by
# nobody else. `data.parameters` and `data.writes` are different: both still have live
# reads (`host:sub-flow-parameters-read`, `host:node-writes-legacy-read`), so those two
# bans are host-derived and carry a fact id.
DEAD_META_KEYS = ("category",)
DEAD_GLOBALS = ("approval_mode", "subagent_mode", "verbosity", "concept_depth")
DEAD_NODE_DATA = ("parameters", "writes")

# Which fact each of those two bans rests on, and the clause it contributes. Hoisted out
# of the loop so the ids stay plain literals: `test_check.py` reconciles the table by
# walking this module's AST, and a fact id built at runtime would read as an orphan.
DEAD_NODE_DATA_FACTS = {
    "parameters": (
        "host:sub-flow-parameters-read",
        "node-data-parameters",
        " — and it is not inert: {host} reads `data.parameters.flow`",
    ),
    "writes": (
        "host:node-writes-legacy-read",
        "node-data-writes",
        " — {host} still reads it for legacy flows",
    ),
}

# No `${...}` resolver runs on forge-concept's node-run path (`host:prompt-is-verbatim`)
# — the string reaches the prompt verbatim. Scoped to that path deliberately: the flow
# *connector* in @skaile/workspaces does resolve `${}`, and forge-concept never calls it.
INTERPOLATION_RE = re.compile(r"\$\{[^}]*\}")


# The three kinds of rule this script mixes, kept apart in the *output* and nowhere
# else. A red gate is a red gate — there is no second exit code, because a distinct one
# invites a CI config that ignores it.
#
#   intrinsic     depends on nothing outside this repo. `name:` == directory, links
#                 resolve, edges reference real nodes, reachability. If one fails, the
#                 collection is wrong.
#   host-derived  a copy of a fact in someone else's repo, each owned by a row in
#                 `host_facts.py`. If one fails, either the collection is wrong or the
#                 fact expired — and until someone runs `verify_host.py` that is
#                 genuinely ambiguous, so the message says both.
#   house style   decisions this map made (ADR 0003's ceiling, ticket 10's deletions,
#                 the plural rule). They stay errors: a warning nobody is forced to read
#                 is how a deleted key comes back.
INTRINSIC = "intrinsic"
HOST_DERIVED = "host-derived"
HOUSE_STYLE = "house style"

TIERS = (INTRINSIC, HOST_DERIVED, HOUSE_STYLE)


class Problem:
    """One reported failure, with the tier that decides how it reads."""

    def __init__(
        self, where: str, msg: str, tier: str, facts: tuple[str, ...] = (), rule: str | None = None
    ) -> None:
        self.where = where
        self.msg = msg
        self.tier = tier
        self.facts = facts
        self.rule = rule

    def __str__(self) -> str:
        suffix = f" [{', '.join(self.facts)}]" if self.facts else ""
        return f"{self.where}: {self.msg}{suffix}"


class Report:
    def __init__(self) -> None:
        self.problems: list[Problem] = []

    def error(
        self,
        where: str,
        msg: str,
        *,
        fact: str | tuple[str, ...] | None = None,
        rule: str | None = None,
    ) -> None:
        """An intrinsic failure, or — with `fact=` — a host-derived one.

        `fact` names a row in `host_facts.py`, or several when one rule rests on more
        than one (an edge type governs both run ordering and readiness, in two files
        that can rot apart). An unknown id raises rather than printing: a citation that
        resolves to nothing is exactly the defect this table exists to make loud.

        `rule` names this rule, and must appear in every cited row's `rules`. It is what
        makes that column mean something: a rule id that lives only in the table is
        unfalsifiable bookkeeping — the defect the table was built to abolish, one field
        further in. `test_check.py` reconciles both directions.

        `{host}` in `msg` is replaced by the first row's host and path, so the message
        cannot drift out of step with the table.
        """
        if fact is None:
            if rule is not None:
                raise ValueError(f"rule {rule!r} given without a fact — only host-derived rules carry ids")
            self.problems.append(Problem(where, msg, INTRINSIC))
            return
        if rule is None:
            raise ValueError(f"fact {fact!r} cited with no rule id — the table's `rules` column would go unowned")
        ids = (fact,) if isinstance(fact, str) else tuple(fact)
        rows = [hf.fact(i) for i in ids]
        for row in rows:
            if rule not in row.rules:
                raise KeyError(f"rule {rule!r} is not listed in {row.id}'s `rules` — add it to scripts/host_facts.py")
        self.problems.append(
            Problem(where, msg.replace("{host}", rows[0].where), HOST_DERIVED, ids, rule)
        )

    def house(self, where: str, msg: str) -> None:
        """A rule this collection imposes on itself. Same severity, different reading."""
        self.problems.append(Problem(where, msg, HOUSE_STYLE))

    @property
    def errors(self) -> list[str]:
        return [str(p) for p in self.problems]

    def by_tier(self, tier: str) -> list[Problem]:
        return [p for p in self.problems if p.tier == tier]

    def facts_cited(self) -> set[str]:
        return {f for p in self.problems for f in p.facts}

    def ok(self) -> bool:
        return not self.problems


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


TREE_NODE_RE = re.compile(r"^(?P<indent>(?:[\u2502 ] {3})*)[\u251c\u2514]\u2500\u2500 (?P<name>\S+)")


def _tree_entry_stem(raw: str) -> str:
    """The comparable name of a tree entry: no extension, no path tail, no placeholder.

    `review.yaml` -> `review`, `reviews/` -> `reviews`, `slices/<slice_id>/` -> `slices`.
    """
    head = raw.split("/")[0].split("<")[0].strip()
    return head.rsplit(".", 1)[0] if "." in head else head


def _is_plural_of(a: str, b: str) -> bool:
    """Whether `a` is `b` under a naive English pluralisation."""
    a, b = a.lower(), b.lower()
    return a in (b + "s", b + "es") or (b.endswith("y") and a == b[:-1] + "ies")


def check_tree_names(repo: Path, rep: Report) -> None:
    """No two siblings in the concept tree differ only by singular and plural.

    `concept_structure.md`'s Naming section states the rule; this enforces it against
    the same fenced tree the rest of the contract declares, so a pair like
    `review.yaml` beside `reviews/` cannot be typed back in unnoticed.
    """
    contract = repo / "contracts" / "concept_structure.md"
    if not contract.is_file():
        return
    where = "contracts/concept_structure.md"

    # parent path -> the entry stems directly under it
    siblings: dict[str, list[str]] = {}
    stack: list[str] = []
    inside = False
    for line in contract.read_text().splitlines():
        if line.strip().startswith("```"):
            if inside:
                break
            inside = True
            continue
        if not inside:
            continue
        m = TREE_NODE_RE.match(line)
        if not m:
            continue
        depth = len(m.group("indent")) // 4
        stem = _tree_entry_stem(m.group("name"))
        if not stem:
            continue
        del stack[depth:]
        parent = "_concept/" + "/".join(stack)
        siblings.setdefault(parent, []).append(stem)
        stack.append(stem)

    for parent, names in siblings.items():
        for i, a in enumerate(names):
            for b in names[i + 1 :]:
                if _is_plural_of(a, b) or _is_plural_of(b, a):
                    rep.house(
                        where,
                        f"`{parent}` declares `{a}` and `{b}`, which differ only by plural",
                    )


# --------------------------------------------------------------------------
# citations — every asset kind cites contracts, and contracts are pruned hard
# --------------------------------------------------------------------------

# The lookbehind keeps a *deployed* path out of the citation set: a skill cites
# `contracts/x.md` repo-relatively, while `.claude/contracts/shared-contracts/` names
# where the asset lands and is not a file in this repo.
CONTRACT_REF_RE = re.compile(r"(?<![A-Za-z0-9_./-])`?(?:\.\./)*contracts/([A-Za-z0-9_./-]+)`?")
# The `../` run is matched explicitly because prose one directory down cites the layer
# relatively — `flows/README.md` says `../contracts/<file>`. Without it the lookbehind
# sees the slash and skips the citation, which is how ticket 28's `flows/` gate went
# quiet the moment the lookbehind landed: the deployed-path exclusion below is meant to
# drop `.claude/contracts/...`, not every path with a parent segment.

# The whole reference layer installs as one dir-scoped asset: `contracts/CONTRACT.md`
# names it, and `contract` is a dir-scoped kind, so the directory deploys whole. A
# per-file `contract:` ref could never resolve — `_` is not a legal asset-name
# character, so `acceptance_criteria` would index as `acceptance-criteria` even with a
# manifest of its own.
CONTRACT_ASSET = "shared-contracts"


def _cited_contracts(text: str) -> list[str]:
    """Every `contracts/<path>` this text names, trailing punctuation trimmed."""
    return sorted({ref.rstrip(".,;:)") for ref in CONTRACT_REF_RE.findall(text)})


def _check_citations(text: str, where: str, repo: Path, rep: Report) -> None:
    for ref in _cited_contracts(text):
        if not (repo / "contracts" / ref).exists():
            rep.error(where, f"cites `contracts/{ref}`, which does not exist")


def _contract_names(text: str) -> set[str]:
    """The stems of the top-level contract *documents* this text cites.

    A flow's `requires:` names contracts as `contract:@publisher/<stem>` resolving to
    `contracts/<stem>.md`, so only top-level `.md` files can appear there. `README.md`
    is the index, never a dependency.
    """
    out: set[str] = set()
    for ref in _cited_contracts(text):
        if "/" in ref or not ref.endswith(".md") or ref == "README.md":
            continue
        out.add(ref[: -len(".md")])
    return out


# --------------------------------------------------------------------------
# skills
# --------------------------------------------------------------------------

def _declared_contract_assets(fm: dict) -> set[str]:
    """The contract assets this skill's `metadata.requires` names."""
    metadata = fm.get("metadata")
    if not isinstance(metadata, dict):
        return set()
    requires = metadata.get("requires")
    if not isinstance(requires, list):
        return set()
    out: set[str] = set()
    for ref in requires:
        m = REF_RE.match(str(ref))
        if m and m.group(1) == "contract":
            out.add(m.group(3))
    return out


def _check_skill_contract_dep(fm: dict, cited: set[str], where: str, rep: Report) -> None:
    """Cite a contract file and you declare the contract asset — and vice versa."""
    declared = _declared_contract_assets(fm)
    for wrong in sorted(declared - {CONTRACT_ASSET}):
        rep.error(
            where,
            f"declares contract {wrong!r}, but the only contract asset is {CONTRACT_ASSET!r} — "
            f"{{host}} indexes an asset under its slugified `name:`, so a per-file ref names nothing",
            fact="host:asset-name-slug",
            rule="contract-asset-is-one",
        )
    if cited and CONTRACT_ASSET not in declared:
        rep.error(
            where,
            f"cites {len(cited)} contract file(s) but does not declare "
            f"`contract:@skaile-ai/{CONTRACT_ASSET}` in `metadata.requires` — "
            f"nothing would install what it reads, and {{host}} is what reports the gap",
            fact="host:doctor-walks-requires",
            rule="skill-declares-what-it-reads",
        )
    if not cited and CONTRACT_ASSET in declared:
        rep.error(
            where,
            f"declares {CONTRACT_ASSET!r} but cites no contract file — {{host}} would "
            f"report a dependency that reached no reader",
            fact="host:doctor-walks-requires",
            rule="skill-declares-what-it-reads",
        )


def check_skills(repo: Path, rep: Report) -> tuple[set[str], dict[str, set[str]]]:
    """Check every skill.

    Returns `(installable skill names, contracts cited per skill directory)`. The
    second is what makes a flow's `contract:` manifest checkable for exactness rather
    than only for existence.
    """
    skills_dir = repo / "skills"
    names: set[str] = set()
    contracts: dict[str, set[str]] = {}
    if not skills_dir.is_dir():
        return names, contracts

    top_level = _fenced_tree(repo)

    for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
        directory = skill_md.parent.name
        where = f"skills/{directory}"
        text = skill_md.read_text()
        fm, _body = split_frontmatter(text)

        # Keyed by directory, because that is what a flow node resolves against —
        # `name:` may be wrong, and the mismatch is reported separately below.
        contracts[directory] = _contract_names(text)

        if not fm:
            rep.error(where, "SKILL.md has no parseable YAML frontmatter")
            continue

        # The reader declares its own dependency. A skill's `metadata.requires` is the
        # one list with a live reader in the shipped installer (`host:doctor-walks-requires`,
        # which reports a dependency that reached no workspace), while a flow's dependency
        # edges are built from its nodes' `run.assets`, never from its top-level `requires:`
        # (`extractFlowRequires`, @skaile/workspaces discovery/src/requires-graph.ts).
        _check_skill_contract_dep(fm, contracts[directory], where, rep)

        # 1. identity. Three of the four roles a skill name plays resolve through the
        #    directory, and forge-concept never reads `name:` for identity at all
        #    (`host:skill-identity-is-the-directory`) — so a mismatch is invisible until
        #    a node runs with no skill body.
        name = fm.get("name")
        if not name:
            rep.error(where, "frontmatter has no `name:`")
        elif name != directory:
            rep.error(
                where,
                f"`name:` is {name!r} but the directory is {directory!r} — they must match "
                f"character for character; {{host}} resolves a node's skill through the directory",
                fact="host:skill-identity-is-the-directory",
                rule="skill-name-matches-directory",
            )
        else:
            names.add(name)

        # 2. the one frontmatter field with a live reader.
        if "version" not in fm:
            rep.error(where, "frontmatter has no `version:`")

        # 3. the body ceiling.
        line_count = len(text.splitlines())
        if line_count > LINE_BUDGET:
            rep.house(where, f"SKILL.md is {line_count} lines, over the {LINE_BUDGET}-line ceiling")

        # 4. the machine layer has to be where its readers look — neither reader falls
        #    back to the frontmatter root, and neither raises. A block at the root parses
        #    clean and reports `satisfied: true` on an unmet gate.
        for key in ("artifacts", "prerequisites"):
            if key in fm:
                rep.error(
                    where,
                    f"`{key}:` is at the frontmatter root — it must sit under `metadata:`, "
                    f"which is the only place its reader looks ({{host}})",
                    fact="host:skill-metadata-nesting",
                    rule="machine-layer-nesting",
                )

        # 5. declared prerequisites are joined to the *project* root, not to `_concept/`
        #    (`host:prerequisite-project-root`). A concept path without the prefix resolves
        #    one level too high, and its first segment inside the tree has to be a real one. Paths
        #    outside the concept are legal only when named in PROJECT_ROOT_PREREQUISITES —
        #    see that constant for why the restriction survives ticket 23's finding.
        for entry in _prerequisite_paths(fm):
            if not entry.startswith(ARTIFACT_ROOT + "/"):
                if entry in PROJECT_ROOT_PREREQUISITES:
                    continue
                rep.error(
                    where,
                    f"prerequisite path {entry!r} does not start with {ARTIFACT_ROOT + '/'!r} and is not "
                    f"one of the named project-root gates ({', '.join(sorted(PROJECT_ROOT_PREREQUISITES))}) — "
                    f"{{host}} joins it to the project root, so a concept path without the prefix "
                    f"resolves outside the concept",
                    fact="host:prerequisite-project-root",
                    rule="prerequisite-prefix",
                )
                continue
            if top_level:
                first = entry[len(ARTIFACT_ROOT) + 1:].split("/", 1)[0]
                if first not in top_level:
                    rep.error(
                        where,
                        f"prerequisite path {entry!r} starts at {first!r}, which is not a "
                        f"top-level entry of the artifact tree — {{host}} would resolve it "
                        f"against the project root and find nothing",
                        fact="host:prerequisite-project-root",
                        rule="prerequisite-tree-segment",
                    )

        # 6. cited contracts must exist.
        _check_citations(text, where, repo, rep)

    return names, contracts


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

def check_contract_manifest(repo: Path, rep: Report) -> None:
    """Without `contracts/CONTRACT.md`, discovery finds no contract at all.

    Same failure ticket 29 gated for flows, from the other side: the installer indexes
    the asset under its slugified `name:`, so a name that does not slugify to what every
    `contract:` ref says leaves those refs naming nothing.
    """
    where = "contracts/CONTRACT.md"
    manifest = repo / "contracts" / "CONTRACT.md"
    if not manifest.is_file():
        rep.error("contracts/", "has no `CONTRACT.md` — discovery finds no contract asset and every `contract:` ref names nothing")
        return
    fm, _body = split_frontmatter(manifest.read_text())
    if not fm:
        rep.error(where, "has no parseable YAML frontmatter — the manifest is the frontmatter")
        return
    name = fm.get("name")
    if not name:
        rep.error(where, "frontmatter has no `name:`")
    elif _slugify_asset_name(str(name)) != CONTRACT_ASSET:
        rep.error(
            where,
            f"`name:` {name!r} installs as {_slugify_asset_name(str(name))!r}, but every "
            f"`contract:` ref names {CONTRACT_ASSET!r} — {{host}} takes the asset's identity "
            f"from the slugified name",
            fact="host:asset-name-slug",
            rule="contract-manifest-slug",
        )


def check_contracts(repo: Path, rep: Report) -> None:
    """Contracts cite each other too, and are pruned aggressively."""
    contracts_dir = repo / "contracts"
    if not contracts_dir.is_dir():
        return
    for path in sorted(contracts_dir.glob("*.md")):
        _check_citations(path.read_text(), f"contracts/{path.name}", repo, rep)


# --------------------------------------------------------------------------
# flows
# --------------------------------------------------------------------------

def check_flows(
    repo: Path, skill_names: set[str], skill_contracts: dict[str, set[str]], rep: Report
) -> None:
    flows_dir = repo / "flows"
    if not flows_dir.is_dir():
        return

    # The flow directory's prose cites contracts like everything else, and until now
    # nothing scanned it: ticket 28 found a dangling `contracts/flow.schema.json` link
    # in `flows/README.md`, deleted by ticket 16, that no check could see.
    for doc in sorted(flows_dir.rglob("*")):
        if doc.is_file() and doc.suffix in (".md", ".yaml", ".yml"):
            _check_citations(doc.read_text(), str(doc.relative_to(repo)), repo, rep)

    for flow_file in sorted(flows_dir.glob("*/*.flow.yaml")):
        where = f"flows/{flow_file.parent.name}/{flow_file.name}"
        text = flow_file.read_text()
        try:
            flow = yaml.safe_load(text) or {}
        except yaml.YAMLError as exc:
            rep.error(where, f"is not parseable YAML: {exc}")
            continue
        if not isinstance(flow, dict):
            rep.error(where, "does not contain a mapping")
            continue
        _check_one_flow(repo, flow, text, flow_file, where, skill_names, skill_contracts, rep)


def _slugify_asset_name(raw: str) -> str:
    """The installer's canonical asset name for `raw`.

    Mirrors `slugifyAssetName` (`host:asset-name-slug`): NFKD, drop
    combining accents, lowercase, every other run of non-alphanumerics to `-`, trim.
    """
    decomposed = unicodedata.normalize("NFKD", raw)
    stripped = "".join(c for c in decomposed if not unicodedata.combining(c))
    return re.sub(r"^-+|-+$", "", re.sub(r"[^a-z0-9]+", "-", stripped.lower()))


def _check_one_flow(
    repo: Path,
    flow: dict,
    text: str,
    flow_file: Path,
    where: str,
    skill_names: set[str],
    skill_contracts: dict[str, set[str]],
    rep: Report,
) -> None:
    stem = flow_file.name[: -len(".flow.yaml")]
    directory = flow_file.parent.name
    flow_id = flow.get("id")

    # identity — the loader finds a flow by directory, the manifest names it by id.
    if not flow_id:
        rep.error(where, "has no `id:`")
    elif flow_id != stem or flow_id != directory:
        rep.error(where, f"`id:` {flow_id!r} must equal both the filename stem {stem!r} and the directory {directory!r}")

    # `validateFlow` requires `name`; forge-concept's loader does not. Carrying it
    # satisfies both, at the cost of one line. (The claim used to read "platform's
    # validateFlow" — the schema lives in @skaile/workspaces, which platform calls.)
    flow_name = flow.get("name")
    if not flow_name:
        rep.error(
            where,
            "has no top-level `name:` — {host} requires a non-empty one",
            fact="host:flow-manifest-requires-name",
            rule="flow-name-present",
        )
    elif flow_id and _slugify_asset_name(flow_name) != flow_id:
        # `name:` is not decoration: the installer takes a flow's asset identity from it,
        # not from `id:` (`host:flow-asset-named-from-name`). A title that does not slugify
        # to the id makes the flow unresolvable as `flow:@<publisher>/<id>` and it silently
        # never installs, while the deployed directory the loader matches on is named from
        # the same slug.
        rep.error(
            where,
            f"`name:` {flow_name!r} slugifies to {_slugify_asset_name(flow_name)!r}, not to `id:` "
            f"{flow_id!r} — {{host}} names the asset from `name:`, so this flow cannot be "
            f"installed as `flow:@skaile-ai/{flow_id}`",
            fact="host:flow-asset-named-from-name",
            rule="flow-name-slugifies-to-id",
        )

    _check_presentation(flow, text, where, rep)

    nodes = flow.get("nodes") or []
    edges = flow.get("edges") or []
    if not isinstance(nodes, list) or not nodes:
        rep.error(
            where,
            "has no `nodes:` — {host} discards a flow missing id/nodes/edges, without an error",
            fact="host:loader-discards-incomplete-flow",
            rule="flow-has-nodes",
        )
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

    node_skills = _check_nodes(nodes, by_id, where, skill_names, rep)

    # edges. The host orders nodes along `type: flow` and nothing else
    # (`host:flow-edge-orders-run`, `host:flow-edge-gates-state`), so a differently-typed
    # edge draws on the canvas and orders nothing. Reachability below catches it when it is
    # the only path to a node; this catches it when it runs *parallel* to a flow edge,
    # where reachability stays green and the edge is pure decoration.
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
        etype = edge.get("type")
        if etype != FLOW_EDGE:
            rep.error(
                where,
                f"edge {eid!r} has `type: {etype!r}`, but {{host}} reads only `type: {FLOW_EDGE}` — "
                f"it would draw an edge that orders nothing, and gates no node's readiness either",
                fact=("host:flow-edge-orders-run", "host:flow-edge-gates-state"),
                rule="edge-type-flow",
            )

    # reachability under flow-typed edges — a disconnected subgraph is still possible
    # with every edge correctly typed.
    _check_reachability(flow, by_id, edges, where, rep)

    # requires: exactness. A missing entry is not a house-rule violation — the
    # skill is then never installed, and the node runs with an empty prompt.
    _check_requires(flow, node_skills, skill_contracts, repo, where, rep)


def _check_presentation(flow: dict, text: str, where: str, rep: Report) -> None:
    """The keys the onboarding endpoint turns into a card, and the keys ticket 10
    deleted. Every field here is read without validation on the far side: a missing
    `description` renders an empty card, an `input_style` outside the union is cast to
    it and branches to nothing, and a `research_depth` outside the published options is
    offered as a selected value the picker cannot show."""
    for key in ("version", "description"):
        value = flow.get(key)
        if not isinstance(value, str) or not value.strip():
            rep.error(
                where,
                f"has no non-empty string `{key}:` — {{host}} publishes `description` verbatim",
                fact="host:profile-description",
                rule="flow-description",
            )

    meta = flow.get("meta")
    if meta is None:
        rep.error(
            where,
            "has no `meta:` — {host} reads `meta.icon` and `meta.onboarding` from it",
            fact="host:profile-onboarding",
            rule="flow-meta",
        )
        meta = {}
    elif not isinstance(meta, dict):
        rep.error(where, "`meta:` is not a mapping")
        meta = {}

    for dead in DEAD_META_KEYS:
        if dead in meta:
            rep.house(where, f"carries `meta.{dead}:`, deleted by ticket 10 — every value fell through every reader")

    icon = meta.get("icon")
    if not isinstance(icon, str) or not icon.startswith("i-"):
        rep.error(
            where,
            f"has `meta.icon: {icon!r}` — it must be an `i-` prefixed Iconify name; "
            f"{{host}} passes it straight to the icon component, which renders nothing for anything else",
            fact="host:profile-icon",
            rule="flow-icon",
        )

    onboarding = meta.get("onboarding")
    if not isinstance(onboarding, dict):
        rep.error(
            where,
            "has no `meta.onboarding:` mapping — {host} then falls back to a structured "
            "form with no fields",
            fact="host:profile-onboarding",
            rule="onboarding-present",
        )
    else:
        style = onboarding.get("input_style")
        if style not in INPUT_STYLES:
            rep.error(
                where,
                f"has `meta.onboarding.input_style: {style!r}`, not one of {sorted(INPUT_STYLES)} "
                f"— {{host}} casts it to the union without checking it",
                fact="host:profile-onboarding",
                rule="onboarding-input-style",
            )
        fields = onboarding.get("fields")
        if style in ("structured", "repo"):
            if not isinstance(fields, list) or not fields or not all(isinstance(f, str) and f.strip() for f in fields):
                rep.error(
                    where,
                    f"has `input_style: {style!r}` but no non-empty `meta.onboarding.fields:` "
                    f"list — {{host}} would render a form with no questions",
                    fact="host:profile-onboarding",
                    rule="onboarding-fields",
                )
        if "placeholder" in onboarding and style != "freeform":
            rep.error(
                where,
                f"carries `meta.onboarding.placeholder:` with `input_style: {style!r}` — "
                f"{{host}} binds it to the freeform textarea only, so it has no reader here",
                fact="host:onboarding-placeholder-freeform",
                rule="onboarding-placeholder",
            )

    globals_ = flow.get("globals")
    if not isinstance(globals_, dict):
        rep.error(
            where,
            "has no `globals:` mapping — {host} seeds the onboarding depth picker from "
            "`globals.research_depth`",
            fact="host:research-depth-seed",
            rule="flow-globals",
        )
    else:
        for dead in DEAD_GLOBALS:
            if dead in globals_:
                rep.house(where, f"carries `globals.{dead}:`, deleted by ticket 10 — it has no reader in either host")
        depth = globals_.get("research_depth")
        if depth not in RESEARCH_DEPTHS:
            rep.error(
                where,
                f"has `globals.research_depth: {depth!r}`, not one of {sorted(RESEARCH_DEPTHS)} "
                f"— {{host}} publishes exactly those as selectable",
                fact="host:research-depth-options",
                rule="research-depth",
            )

    for found in sorted(set(INTERPOLATION_RE.findall(text))):
        rep.error(
            where,
            f"contains the interpolation {found!r} — {{host}} resolves nothing, so the "
            f"literal string reaches the prompt",
            fact="host:prompt-is-verbatim",
            rule="no-interpolation",
        )


def _check_nodes(nodes: list, by_id: dict, where: str, skill_names: set[str], rep: Report) -> set[str]:
    """Node kinds, phases, group containment. Returns the set of skills the flow runs."""
    node_skills: set[str] = set()
    group_phases: dict[str, str] = {}

    for node in nodes:
        if not isinstance(node, dict) or not node.get("id"):
            continue
        nid = node["id"]
        data = node.get("data") if isinstance(node.get("data"), dict) else {}
        kind = node.get("type")

        if kind not in NODE_KINDS:
            rep.house(
                where,
                f"node {nid!r} has `type: {kind!r}` — `-mp` ships `skill` and `group` nodes only "
                f"(ticket 10 deleted the `sub-flow` and `router` kinds)",
            )

        # Both bans are host-derived rather than house style: each key still has a live
        # reader, so the ban would change meaning if the host stopped reading it.
        for dead in DEAD_NODE_DATA:
            if dead in data:
                fact_id, rule_id, extra = DEAD_NODE_DATA_FACTS[dead]
                rep.error(
                    where,
                    f"node {nid!r} carries `data.{dead}:`, deleted by ticket 10{extra}",
                    fact=fact_id,
                    rule=rule_id,
                )

        phase = data.get("phase")
        if phase is None:
            rep.error(
                where,
                f"node {nid!r} declares no `data.phase` — {{host}} then guesses one from the skill name",
                fact="host:phase-guessed-from-skill",
                rule="node-phase-present",
            )
        elif phase not in PHASES:
            rep.error(
                where,
                f"node {nid!r} has `data.phase: {phase!r}`, not one of {sorted(PHASES)} — "
                f"{{host}} is the whole lane vocabulary, and swallows anything else",
                fact="host:phase-lane-vocabulary",
                rule="node-phase-enum",
            )

        if kind == "group":
            if isinstance(phase, str):
                group_phases[nid] = phase
            continue

        if kind == "skill":
            skill = data.get("skill")
            if not skill:
                rep.error(where, f"skill node {nid!r} has no `data.skill`")
            else:
                node_skills.add(skill)
                if skill_names and skill not in skill_names:
                    rep.error(where, f"node {nid!r} names skill {skill!r}, which has no `skills/{skill}/` directory")

            # Authored geometry on a skill node is not cosmetic
            # (`host:positioned-nodes-lose-lanes`): every positioned node drops out of the
            # lane computation and the layout returns early with `lanes: []` once none are
            # left, so a fully-positioned flow loses the swimlanes *and* the group-phase
            # override that makes group nodes worth carrying. The collection has to
            # withhold geometry to get the feature.
            if node.get("position") is not None:
                rep.error(
                    where,
                    f"skill node {nid!r} carries `position:` — {{host}} removes positioned "
                    f"nodes from the lane computation, so authoring geometry here disables the phase swimlanes",
                    fact="host:positioned-nodes-lose-lanes",
                    rule="node-position",
                )

    # Three group nodes per flow, one per phase. Ticket 10 kept group nodes for one
    # reason — `host:group-phase-wins` — so a flow missing a lane loses the mechanism for
    # the nodes that would have sat in it.
    if len(group_phases) != 3 or set(group_phases.values()) != PHASES:
        rep.error(
            where,
            f"has {len(group_phases)} group node(s) with phases {sorted(group_phases.values())} — "
            f"every flow carries exactly three, one per phase {sorted(PHASES)}, because {{host}} "
            f"lets a group override its children's",
            fact="host:group-phase-wins",
            rule="group-nodes-per-phase",
        )

    # parentNode, and the agreement that makes the two phase declarations one table.
    for node in nodes:
        if not isinstance(node, dict) or not node.get("id"):
            continue
        nid = node["id"]
        if node.get("type") != "skill":
            if node.get("parentNode") is not None:
                rep.error(where, f"node {nid!r} is not a skill node but declares `parentNode` — only skill nodes sit in a group")
            continue
        parent = node.get("parentNode")
        if parent is None:
            rep.error(
                where,
                f"skill node {nid!r} has no `parentNode` — it sits in no phase group, so nothing can "
                f"hold its `data.phase` to the lane it renders in ({{host}})",
                fact="host:group-phase-wins",
                rule="skill-node-parent",
            )
            continue
        if parent not in by_id:
            rep.error(where, f"node {nid!r} has parentNode {parent!r}, which is not a node id")
            continue
        if by_id[parent].get("type") != "group":
            rep.error(where, f"node {nid!r} has parentNode {parent!r}, which is not a group node")
            continue
        data = node.get("data") if isinstance(node.get("data"), dict) else {}
        own = data.get("phase")
        group = group_phases.get(parent)
        # Only compare enum-valid values: a phase outside the enum is already reported
        # above, and reporting it twice hides that it is one defect.
        if own in PHASES and group is not None and own != group:
            rep.error(
                where,
                f"node {nid!r} declares `data.phase: {own!r}` but sits in group {parent!r}, whose phase is "
                f"{group!r} — {{host}} takes the group's, so the node's declaration is "
                f"silently overridden and the two must be written from one table",
                fact="host:group-phase-wins",
                rule="node-phase-agrees-with-group",
            )

    return node_skills


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
    flow: dict,
    node_skills: set[str],
    skill_contracts: dict[str, set[str]],
    repo: Path,
    where: str,
    rep: Report,
) -> None:
    requires = flow.get("requires")
    if requires is None:
        rep.error(where, "has no `requires:` manifest — installing the flow would install none of its skills")
        return

    declared_skills: set[str] = set()
    declared_contracts: set[str] = set()
    unresolvable_contracts: set[str] = set()
    for ref in requires:
        m = REF_RE.match(str(ref))
        if not m:
            rep.error(where, f"`requires:` entry {ref!r} is not a `kind:@publisher/name` ref")
            continue
        kind, _publisher, name, _version = m.groups()
        if kind == "skill":
            declared_skills.add(name)
        elif kind == "flow":
            # A `flow:` ref only makes sense for a sub-flow node, a kind `-mp` no
            # longer ships — so it can only install a flow nothing here delegates to.
            rep.error(where, f"`requires:` lists flow {name!r}, but `-mp` ships no `sub-flow` nodes — nothing can delegate to it")
        elif kind == "contract":
            declared_contracts.add(name)
            if name != CONTRACT_ASSET:
                unresolvable_contracts.add(name)
                rep.error(
                    where,
                    f"`requires:` names contract {name!r}, but the only contract asset is "
                    f"{CONTRACT_ASSET!r} — {{host}} indexes by slugified name, so a per-file "
                    f"ref resolves to nothing",
                    fact="host:asset-name-slug",
                    rule="requires-contract-per-file",
                )

    for missing in sorted(node_skills - declared_skills):
        rep.error(where, f"runs skill {missing!r} but does not list it in `requires:` — it would not be installed")
    for extra in sorted(declared_skills - node_skills):
        rep.error(where, f"`requires:` lists skill {extra!r}, which no node in this flow runs")

    # The reference layer is one asset, so a flow's contract manifest is one ref or none:
    # present when any of its own node skills reads a contract file, absent when none
    # does. Per-file exactness is not expressible here and is gated on the skills, which
    # is where the reading happens — `skill:` refs keep the "no inheritance, no extras"
    # rule because a skill really is per-node.
    if node_skills and all(s in skill_contracts for s in node_skills):
        needed = any(skill_contracts[skill] for skill in node_skills)
        if needed and CONTRACT_ASSET not in declared_contracts:
            rep.error(where, f"its skills read contract files, but `requires:` does not list `contract:@skaile-ai/{CONTRACT_ASSET}` — the reference layer would not be installed")
        if not needed and CONTRACT_ASSET in declared_contracts:
            rep.error(where, f"`requires:` lists {CONTRACT_ASSET!r}, which none of this flow's skills read")


# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# prose
# --------------------------------------------------------------------------

# `docs/` and the root markdown are the one part of the collection no gate looked at:
# `check.py` globs `skills/`, `contracts/` and `flows/` and stopped there. That is how two
# worked examples drifted onto the tree ADR 0007 replaced and three deleted skill names sat
# unread until ticket 33 found them by hand — the same quiet failure every other check here
# exists to raise, in the files a *human* reads first.
#
# The bar is ticket 33's: a reader must not be able to copy a path that resolves to nothing.
# It is deliberately a check on **paths**, not on prose. Two artifacts in this repo are
# supposed to name things that no longer exist — an ADR recording a deletion cites the
# contract it deleted (`0004` → `iron_laws.md`, `0010` → `plans.md`), and `examples/WHY.md`
# quotes pre-port skill bodies verbatim. A dead-*name* check would fire on exactly the two
# places where naming a dead thing is correct, so mentions are free and only links and
# `skills/<name>` paths are gated.
MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)")
SKILL_PATH_RE = re.compile(r"(?<![A-Za-z0-9_./-])`?skills/([a-z0-9][a-z0-9-]*)")


def _prose_files(repo: Path) -> list[Path]:
    """Every markdown file no other check reads: `docs/` and the repo root.

    `skills/` and `contracts/` are gated by their own checks, which know far more about
    what those files are; `flows/` holds YAML. What is left is prose.
    """
    return sorted([*(repo / "docs").rglob("*.md")] if (repo / "docs").is_dir() else []) + sorted(repo.glob("*.md"))


def check_docs(repo: Path, skill_names: set[str], rep: Report) -> None:
    for path in _prose_files(repo):
        where = path.relative_to(repo).as_posix()
        text = path.read_text(encoding="utf-8")

        for target in MD_LINK_RE.findall(text):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            rel = target.split("#", 1)[0]
            if not rel:
                continue
            if not (path.parent / rel).exists():
                rep.error(where, f"links to `{target}`, which does not exist")

        for name in sorted(set(SKILL_PATH_RE.findall(text))):
            if name not in skill_names:
                rep.error(where, f"names the path `skills/{name}`, which is not a skill in this collection")


def run(repo: Path) -> Report:
    rep = Report()
    skill_names, skill_contracts = check_skills(repo, rep)
    check_contracts(repo, rep)
    check_contract_manifest(repo, rep)
    check_tree_names(repo, rep)
    check_flows(repo, skill_names, skill_contracts, rep)
    check_docs(repo, skill_names, rep)
    return rep


def run_own_tests() -> int:
    """Run `test_check.py`, the failing fixture behind every rule above.

    A missing pytest is an error, not a skip: a skipped test phase reports the same
    confident green as the defect this phase exists to catch.
    """
    tests = Path(__file__).resolve().parent / "test_check.py"
    if not tests.is_file():
        print(f"ERROR {tests.name} is missing — the rules above have no fixtures behind them")
        return 1

    sys.stdout.flush()
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", str(tests), "-q"],
        cwd=tests.parent,
    )
    sys.stdout.flush()
    if proc.returncode == 4:  # pytest's usage error, which includes "no module named pytest"
        print("ERROR pytest could not run — install it (`pip install pytest`); a skipped test phase is not a pass")
    return proc.returncode


TIER_HEADINGS = {
    INTRINSIC: "intrinsic — this collection is wrong",
    HOST_DERIVED: "host-derived — this collection is wrong, or the fact expired",
    HOUSE_STYLE: "house style — a rule this collection imposes on itself",
}


def print_report(rep: Report) -> None:
    """Print failures grouped by tier.

    The tiering is output only: every tier is an error and the exit code stays one bit,
    because a distinct code invites a CI config that ignores it. It exists because the
    three read differently. An intrinsic failure has one meaning. A host-derived one has
    two, and which it is cannot be settled from inside this repo — so it names its fact
    and the tool that can.
    """
    for tier in TIERS:
        problems = rep.by_tier(tier)
        if not problems:
            continue
        print(f"-- {TIER_HEADINGS[tier]} ({len(problems)})")
        for problem in problems:
            print(f"ERROR {problem}")
        print()

    cited = sorted(rep.facts_cited())
    if cited:
        print(
            "Each host-derived failure above has two readings: this collection is wrong,\n"
            "or the fact it rests on expired. Only the verifier can tell them apart:\n"
            f"    python scripts/verify_host.py --fact {cited[0]}\n"
            f"    python scripts/verify_host.py            # all {len(hf.FACTS)} facts\n"
            f"facts cited by this run: {', '.join(cited)}\n"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Check the collection for references that resolve to nothing.")
    parser.add_argument("--repo", default=None, help="repo root (default: the parent of this script's directory)")
    parser.add_argument(
        "--no-tests",
        action="store_true",
        help="skip `test_check.py`. For CI, which runs it as its own step, and for iterating on one rule.",
    )
    args = parser.parse_args()

    repo = Path(args.repo).resolve() if args.repo else Path(__file__).resolve().parent.parent
    rep = run(repo)

    skills = len(list((repo / "skills").glob("*/SKILL.md"))) if (repo / "skills").is_dir() else 0
    flows = len(list((repo / "flows").glob("*/*.flow.yaml"))) if (repo / "flows").is_dir() else 0

    print_report(rep)

    print(f"\n{skills} skill(s) · {flows} flow(s) · {len(rep.errors)} error(s)")

    if args.no_tests:
        print("fixtures: skipped (--no-tests) — this run does not mean green")
        return 0 if rep.ok() else 1

    print("\nrunning the checker's own fixtures…", flush=True)
    tests_rc = run_own_tests()
    return 0 if (rep.ok() and tests_rc == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
