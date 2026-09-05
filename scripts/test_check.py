#!/usr/bin/env python3
"""test_check.py — the flow half of `check.py` has no live subject yet.

`flows/` is deliberately empty until the flow set is decided, so nothing in the
repo exercises the flow checks. These fixtures are that exercise. Each one
builds a minimal collection in a tmpdir, breaks exactly one thing, and asserts
the break is reported.

  $ pytest scripts/test_check.py -q
"""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

import check


CONCEPT_STRUCTURE = """\
# `_concept/` — the artifact tree

```
_concept/
├── brief.md                        elevator pitch
│
├── 01_meta/
│   └── scope.yaml                  tier + profile
│
├── 07_screens/
│   └── shell.md                    the app shell
```

## Numbering
"""

SKILL = """\
---
name: {name}
description: "A skill."
version: "0.1.0"
metadata:
  prerequisites:
    files:
      - {{ path: "_concept/07_screens", gate: hard }}
---

# {name}

Body.
"""


def write_repo(root: Path, skills=("spec-feature",), contracts=("concept_structure.md",)) -> Path:
    (root / "contracts").mkdir(parents=True, exist_ok=True)
    (root / "contracts" / "concept_structure.md").write_text(CONCEPT_STRUCTURE)
    for c in contracts:
        if c != "concept_structure.md":
            (root / "contracts" / c).write_text("# contract\n")
    for name in skills:
        d = root / "skills" / name
        d.mkdir(parents=True, exist_ok=True)
        (d / "SKILL.md").write_text(SKILL.format(name=name))
    (root / "flows").mkdir(exist_ok=True)
    return root


def write_flow(root: Path, flow: dict, flow_id: str | None = None) -> None:
    flow_id = flow_id or flow["id"]
    d = root / "flows" / flow_id
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{flow_id}.flow.yaml").write_text(yaml.safe_dump(flow, sort_keys=False))


def good_flow() -> dict:
    return {
        "id": "tiny",
        "name": "Tiny flow",
        "requires": ["skill:@skaile-ai/spec-feature"],
        "entry": "a",
        "nodes": [
            {"id": "a", "type": "skill", "data": {"skill": "spec-feature", "phase": "conceptualization"}},
            {"id": "b", "type": "skill", "data": {"skill": "spec-feature", "phase": "implementation"}},
        ],
        "edges": [{"id": "e1", "source": "a", "target": "b", "type": "flow"}],
    }


def errors(root: Path) -> list[str]:
    return check.run(root).errors


def only(root: Path, fragment: str) -> None:
    """Assert exactly one error, mentioning `fragment`."""
    errs = errors(root)
    assert len(errs) == 1, errs
    assert fragment in errs[0], errs[0]


# -- baseline ---------------------------------------------------------------

def test_clean_collection_has_no_errors(tmp_path):
    root = write_repo(tmp_path)
    write_flow(root, good_flow())
    assert errors(root) == []


def test_empty_flows_directory_is_fine(tmp_path):
    root = write_repo(tmp_path)
    assert errors(root) == []


# -- skills -----------------------------------------------------------------

def test_name_must_match_directory(tmp_path):
    root = write_repo(tmp_path)
    skill = root / "skills" / "spec-feature" / "SKILL.md"
    skill.write_text(skill.read_text().replace("name: spec-feature", "name: spec-features"))
    only(root, "must match character for character")


def test_missing_version_is_reported(tmp_path):
    root = write_repo(tmp_path)
    skill = root / "skills" / "spec-feature" / "SKILL.md"
    skill.write_text(skill.read_text().replace('version: "0.1.0"\n', ""))
    only(root, "no `version:`")


def test_line_budget(tmp_path):
    root = write_repo(tmp_path)
    skill = root / "skills" / "spec-feature" / "SKILL.md"
    skill.write_text(skill.read_text() + "\nfiller\n" * check.LINE_BUDGET)
    only(root, f"over the {check.LINE_BUDGET}-line ceiling")


def test_prerequisite_path_outside_the_tree(tmp_path):
    root = write_repo(tmp_path)
    skill = root / "skills" / "spec-feature" / "SKILL.md"
    skill.write_text(
        skill.read_text().replace('path: "_concept/07_screens"', 'path: "_concept/experience/screens"')
    )
    only(root, "not a top-level entry of the artifact tree")


def test_prerequisite_path_without_the_concept_prefix(tmp_path):
    """The path the validator joins is the project root's, so the prefix is load-bearing."""
    root = write_repo(tmp_path)
    skill = root / "skills" / "spec-feature" / "SKILL.md"
    skill.write_text(skill.read_text().replace('path: "_concept/07_screens"', 'path: "07_screens"'))
    only(root, "does not start with '_concept/'")


def test_prerequisites_at_the_frontmatter_root(tmp_path):
    """The failure this catches is silent: the block parses and the gate never fires."""
    root = write_repo(tmp_path)
    skill = root / "skills" / "spec-feature" / "SKILL.md"
    skill.write_text(
        skill.read_text().replace(
            "metadata:\n  prerequisites:\n    files:\n      - ", "prerequisites:\n  files:\n    - "
        )
    )
    only(root, "must sit under `metadata:`")


def test_artifacts_at_the_frontmatter_root(tmp_path):
    root = write_repo(tmp_path)
    skill = root / "skills" / "spec-feature" / "SKILL.md"
    skill.write_text(
        skill.read_text().replace("metadata:\n", "artifacts:\n  requires:\n    - { id: screens }\nmetadata:\n")
    )
    only(root, "must sit under `metadata:`")


def test_top_level_set_comes_from_the_contract(tmp_path):
    """Rename a directory in the contract and the check follows it."""
    root = write_repo(tmp_path)
    contract = root / "contracts" / "concept_structure.md"
    contract.write_text(contract.read_text().replace("07_screens/", "08_screens/"))
    only(root, "not a top-level entry")


def test_missing_cited_contract(tmp_path):
    root = write_repo(tmp_path)
    skill = root / "skills" / "spec-feature" / "SKILL.md"
    skill.write_text(skill.read_text() + "\nSee `contracts/gone.md`.\n")
    only(root, "cites `contracts/gone.md`")


def test_contract_citing_a_deleted_contract(tmp_path):
    root = write_repo(tmp_path)
    (root / "contracts" / "live.md").write_text("See `contracts/scripts/validator_lib.py`.\n")
    only(root, "contracts/scripts/validator_lib.py")


# -- flows ------------------------------------------------------------------

def test_flow_id_must_match_directory_and_stem(tmp_path):
    root = write_repo(tmp_path)
    flow = good_flow()
    flow["id"] = "other"
    write_flow(root, flow, flow_id="tiny")
    only(root, "must equal both the filename stem")


def test_flow_needs_a_top_level_name(tmp_path):
    root = write_repo(tmp_path)
    flow = good_flow()
    del flow["name"]
    write_flow(root, flow)
    only(root, "no top-level `name:`")


def test_duplicate_node_ids(tmp_path):
    root = write_repo(tmp_path)
    flow = good_flow()
    flow["nodes"][1]["id"] = "a"
    flow["edges"] = [{"id": "e1", "source": "a", "target": "a", "type": "flow"}]
    write_flow(root, flow)
    errs = errors(root)
    assert any("duplicate node id" in e for e in errs), errs
    assert any("self-loop" in e for e in errs), errs


def test_dangling_edge_endpoint(tmp_path):
    root = write_repo(tmp_path)
    flow = good_flow()
    flow["edges"][0]["target"] = "nope"
    write_flow(root, flow)
    errs = errors(root)
    assert any("is not a node id" in e for e in errs), errs
    assert any("unreachable from `entry`" in e for e in errs), errs


def test_node_without_phase(tmp_path):
    root = write_repo(tmp_path)
    flow = good_flow()
    del flow["nodes"][1]["data"]["phase"]
    write_flow(root, flow)
    only(root, "declares no `data.phase`")


def test_node_with_invalid_phase(tmp_path):
    root = write_repo(tmp_path)
    flow = good_flow()
    flow["nodes"][1]["data"]["phase"] = "banana"
    write_flow(root, flow)
    only(root, "not one of")


def test_unresolvable_skill(tmp_path):
    root = write_repo(tmp_path)
    flow = good_flow()
    flow["nodes"][1]["data"]["skill"] = "ghost"
    flow["requires"].append("skill:@skaile-ai/ghost")
    write_flow(root, flow)
    only(root, "has no `skills/ghost/` directory")


def test_untyped_edge_orders_nothing(tmp_path):
    """The check the whole flow half exists for: an untyped edge validates
    green everywhere else and creates zero dependency."""
    root = write_repo(tmp_path)
    flow = good_flow()
    del flow["edges"][0]["type"]
    write_flow(root, flow)
    only(root, "unreachable from `entry` along `type: flow` edges")


def test_review_loop_edge_is_a_no_op(tmp_path):
    root = write_repo(tmp_path)
    flow = good_flow()
    flow["edges"][0]["type"] = "review-loop"
    write_flow(root, flow)
    only(root, "unreachable from `entry`")


def test_optional_edge_does_not_confer_reachability(tmp_path):
    root = write_repo(tmp_path)
    flow = good_flow()
    flow["edges"][0]["type"] = "optional"
    write_flow(root, flow)
    only(root, "unreachable from `entry`")


def test_requires_missing_a_skill_a_node_runs(tmp_path):
    root = write_repo(tmp_path)
    flow = good_flow()
    flow["requires"] = []
    write_flow(root, flow)
    only(root, "does not list it in `requires:`")


def test_requires_listing_a_skill_no_node_runs(tmp_path):
    root = write_repo(tmp_path, skills=("spec-feature", "build-plan"))
    flow = good_flow()
    flow["requires"].append("skill:@skaile-ai/build-plan")
    write_flow(root, flow)
    only(root, "which no node in this flow runs")


def test_requires_names_a_missing_contract(tmp_path):
    root = write_repo(tmp_path)
    flow = good_flow()
    flow["requires"].append("contract:@skaile-ai/gone")
    write_flow(root, flow)
    only(root, "`contracts/gone.md` does not exist")


def test_requires_ref_grammar(tmp_path):
    root = write_repo(tmp_path)
    flow = good_flow()
    flow["requires"] = ["spec-feature"]
    write_flow(root, flow)
    errs = errors(root)
    assert any("is not a `kind:@publisher/name` ref" in e for e in errs), errs


def test_sub_flow_target_must_be_declared(tmp_path):
    root = write_repo(tmp_path)
    flow = good_flow()
    flow["nodes"][1] = {
        "id": "b",
        "type": "sub-flow",
        "data": {"flow": "skaileup-slice", "phase": "implementation"},
    }
    write_flow(root, flow)
    only(root, "delegates to flow 'skaileup-slice' but does not list it in `requires:`")


def test_router_target_must_resolve(tmp_path):
    root = write_repo(tmp_path)
    flow = good_flow()
    flow["nodes"].append(
        {"id": "r", "type": "router", "data": {"phase": "review", "routes": [{"target": "nope"}]}}
    )
    flow["edges"].append({"id": "e2", "source": "b", "target": "r", "type": "flow"})
    write_flow(root, flow)
    only(root, "routes to 'nope', which is not a node id")


def test_router_hands_control_on_without_an_edge(tmp_path):
    """A node reached only through a router's route is still reachable."""
    root = write_repo(tmp_path)
    flow = good_flow()
    flow["nodes"].append(
        {"id": "r", "type": "router", "data": {"phase": "review", "routes": [{"target": "b"}]}}
    )
    flow["edges"] = [{"id": "e1", "source": "a", "target": "r", "type": "flow"}]
    write_flow(root, flow)
    assert errors(root) == []


def test_group_nodes_are_containers_not_steps(tmp_path):
    root = write_repo(tmp_path)
    flow = good_flow()
    flow["nodes"].append({"id": "g", "type": "group", "data": {"phase": "conceptualization"}})
    flow["nodes"][0]["parentNode"] = "g"
    write_flow(root, flow)
    assert errors(root) == []


def test_parent_node_must_be_a_group(tmp_path):
    root = write_repo(tmp_path)
    flow = good_flow()
    flow["nodes"][1]["parentNode"] = "a"
    write_flow(root, flow)
    only(root, "which is not a group node")


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
