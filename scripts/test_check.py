#!/usr/bin/env python3
"""test_check.py — a failing fixture per rule `check.py` enforces.

Each case builds a minimal collection in a tmpdir, breaks exactly one thing, and
asserts the break is reported. A gate with no test for its negative case is the same
silent pass the gate exists to close, so every rule in `check.py` has one here.

The four landed flows are the positive fixture: `check.py` runs clean over them, and a
new check that fires on one of them is a defect in the check.

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
│   └── scope.yaml                  flow + project_type
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


CONTRACT_MANIFEST = """\
---
name: shared-contracts
description: "The reference layer."
version: "0.1.0"
metadata:
  do_not_invoke: true
---

# shared-contracts
"""


def write_repo(root: Path, skills=("spec-feature",), contracts=("concept_structure.md",)) -> Path:
    (root / "contracts").mkdir(parents=True, exist_ok=True)
    (root / "contracts" / "CONTRACT.md").write_text(CONTRACT_MANIFEST)
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
    """The shape the four landed flows have: three phase groups, every skill node
    parented and repeating its group's phase, `type: flow` edges only."""
    return {
        "id": "tiny",
        "version": "0.1.0",
        "name": "Tiny",
        "description": "A tiny flow.",
        "meta": {
            "icon": "i-heroicons-beaker",
            "onboarding": {"input_style": "structured", "fields": ["app_name"]},
        },
        "requires": ["skill:@skaile-ai/spec-feature"],
        "globals": {"research_depth": "skip"},
        "entry": "a",
        "nodes": [
            {"id": "g-conceptualization", "type": "group", "data": {"label": "C", "phase": "conceptualization"}},
            {"id": "g-implementation", "type": "group", "data": {"label": "I", "phase": "implementation"}},
            {"id": "g-review", "type": "group", "data": {"label": "R", "phase": "review"}},
            {
                "id": "a",
                "type": "skill",
                "parentNode": "g-conceptualization",
                "data": {"skill": "spec-feature", "phase": "conceptualization"},
            },
            {
                "id": "b",
                "type": "skill",
                "parentNode": "g-implementation",
                "data": {"skill": "spec-feature", "phase": "implementation"},
            },
        ],
        "edges": [{"id": "e1", "source": "a", "target": "b", "type": "flow"}],
    }


def node(flow: dict, nid: str) -> dict:
    """Nodes are addressed by id, not index — the fixture's shape may grow."""
    return next(n for n in flow["nodes"] if n["id"] == nid)


def cite(root: Path, skill: str, contract: str, declare: bool = True) -> None:
    """Make `skill` cite `contracts/<contract>.md` from its body.

    A citing skill must also declare the reference layer (ticket 34), so `declare`
    defaults on: the fixture stays valid except for the one thing a test breaks.
    """
    p = root / "skills" / skill / "SKILL.md"
    text = p.read_text() + f"\nReads `contracts/{contract}.md`.\n"
    if declare:
        text = text.replace(
            "metadata:\n",
            'metadata:\n  requires:\n    - "contract:@skaile-ai/shared-contracts"\n',
            1,
        )
    p.write_text(text)


def errors(root: Path) -> list[str]:
    return check.run(root).errors


def only(root: Path, fragment: str) -> None:
    """Assert exactly one error, mentioning `fragment`."""
    errs = errors(root)
    assert len(errs) == 1, errs
    assert fragment in errs[0], errs[0]


def among(root: Path, *fragments: str) -> None:
    """Assert every fragment is reported, and nothing beyond one error per fragment."""
    errs = errors(root)
    for fragment in fragments:
        assert any(fragment in e for e in errs), (fragment, errs)
    assert len(errs) == len(fragments), errs


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


def test_named_project_root_prerequisite_is_allowed(tmp_path):
    """`validator.ts:81` joins to the project root, so `package.json` genuinely resolves —
    the restriction is a named list now, not a blanket ban."""
    root = write_repo(tmp_path)
    skill = root / "skills" / "spec-feature" / "SKILL.md"
    skill.write_text(skill.read_text().replace('path: "_concept/07_screens"', 'path: "package.json"'))
    assert errors(root) == []


def test_unnamed_project_root_prerequisite_is_still_rejected(tmp_path):
    """The list is the whole exception. A path outside `_concept/` that is not on it is
    still the pre-0007 concept path this check exists to catch."""
    root = write_repo(tmp_path)
    skill = root / "skills" / "spec-feature" / "SKILL.md"
    skill.write_text(skill.read_text().replace('path: "_concept/07_screens"', 'path: "experience/screens"'))
    only(root, "named project-root gates")


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
    cite(root, "spec-feature", "gone")
    only(root, "cites `contracts/gone.md`")


def test_citing_without_declaring_the_reference_layer(tmp_path):
    """Ticket 34: cite a contract file and you declare the one contract asset, or
    nothing installs what the skill reads."""
    root = write_repo(tmp_path, contracts=("concept_structure.md", "seed_data.md"))
    cite(root, "spec-feature", "seed_data", declare=False)
    only(root, "does not declare")


def test_contract_citing_a_deleted_contract(tmp_path):
    root = write_repo(tmp_path)
    (root / "contracts" / "live.md").write_text("See `contracts/scripts/validator_lib.py`.\n")
    only(root, "contracts/scripts/validator_lib.py")


def test_flow_docs_are_scanned_for_citations(tmp_path):
    """Ticket 28 found a dangling `contracts/flow.schema.json` link in `flows/README.md`
    with nothing to catch it — the citation check did not scan `flows/`."""
    root = write_repo(tmp_path)
    write_flow(root, good_flow())
    (root / "flows" / "README.md").write_text("Validated against `../contracts/flow.schema.json`.\n")
    only(root, "cites `contracts/flow.schema.json`")


# -- flows: identity and presentation ---------------------------------------

def test_flow_id_must_match_directory_and_stem(tmp_path):
    root = write_repo(tmp_path)
    flow = good_flow()
    flow["id"] = "other"
    write_flow(root, flow, flow_id="tiny")
    # Two rules fire, and both are true of this file: the id matches neither the stem
    # nor the directory, and `name:` no longer slugifies to it either.
    among(root, "must equal both the filename stem", "the installer names the asset from `name:`")


def test_flow_name_must_slugify_to_its_id(tmp_path):
    """Ticket 29: the installer takes a flow's asset name from `name:`, not `id:`, so a
    title that does not slugify to the id is unresolvable and silently never installs."""
    root = write_repo(tmp_path)
    flow = good_flow()
    flow["name"] = "Reverse Engineer a Codebase"
    write_flow(root, flow)
    only(root, "slugifies to 'reverse-engineer-a-codebase', not to `id:` 'tiny'")


def test_a_title_cased_name_slugifies_to_its_id(tmp_path):
    """The rule is the slug, not string equality — `Appbuilder MVP` is a legal title for
    `appbuilder-mvp`, and every landed flow is named that way."""
    root = write_repo(tmp_path)
    flow = good_flow()
    flow["id"] = "appbuilder-mvp"
    flow["name"] = "Appbuilder MVP"
    write_flow(root, flow)
    assert errors(root) == []


def test_flow_needs_a_top_level_name(tmp_path):
    root = write_repo(tmp_path)
    flow = good_flow()
    del flow["name"]
    write_flow(root, flow)
    only(root, "no top-level `name:`")


def test_flow_needs_a_version(tmp_path):
    root = write_repo(tmp_path)
    flow = good_flow()
    del flow["version"]
    write_flow(root, flow)
    only(root, "no non-empty string `version:`")


def test_flow_needs_a_description(tmp_path):
    """`profiles.get.ts:30` publishes it verbatim onto the onboarding card."""
    root = write_repo(tmp_path)
    flow = good_flow()
    flow["description"] = "  "
    write_flow(root, flow)
    only(root, "no non-empty string `description:`")


def test_flow_icon_must_be_an_iconify_name(tmp_path):
    root = write_repo(tmp_path)
    flow = good_flow()
    flow["meta"]["icon"] = "rocket"
    write_flow(root, flow)
    only(root, "must be an `i-` prefixed Iconify name")


def test_flow_needs_meta(tmp_path):
    root = write_repo(tmp_path)
    flow = good_flow()
    del flow["meta"]
    write_flow(root, flow)
    among(root, "has no `meta:`", "must be an `i-` prefixed", "no `meta.onboarding:` mapping")


def test_input_style_outside_the_union(tmp_path):
    root = write_repo(tmp_path)
    flow = good_flow()
    flow["meta"]["onboarding"]["input_style"] = "wizard"
    write_flow(root, flow)
    only(root, "`meta.onboarding.input_style: 'wizard'`")


def test_structured_onboarding_needs_fields(tmp_path):
    root = write_repo(tmp_path)
    flow = good_flow()
    flow["meta"]["onboarding"]["fields"] = []
    write_flow(root, flow)
    only(root, "no non-empty `meta.onboarding.fields:` list")


def test_placeholder_outside_freeform_has_no_reader(tmp_path):
    """`OnboardingWizard.vue:82-99` binds it to the freeform textarea only."""
    root = write_repo(tmp_path)
    flow = good_flow()
    flow["meta"]["onboarding"]["placeholder"] = "Describe your app"
    write_flow(root, flow)
    only(root, "binds it to the freeform textarea only")


def test_research_depth_outside_the_options(tmp_path):
    root = write_repo(tmp_path)
    flow = good_flow()
    flow["globals"]["research_depth"] = "exhaustive"
    write_flow(root, flow)
    only(root, "`globals.research_depth: 'exhaustive'`")


def test_flow_needs_globals(tmp_path):
    root = write_repo(tmp_path)
    flow = good_flow()
    del flow["globals"]
    write_flow(root, flow)
    only(root, "has no `globals:` mapping")


# -- flows: keys ticket 10 deleted ------------------------------------------

def test_meta_category_is_dead(tmp_path):
    root = write_repo(tmp_path)
    flow = good_flow()
    flow["meta"]["category"] = "appbuilder"
    write_flow(root, flow)
    only(root, "carries `meta.category:`")


@pytest.mark.parametrize("key", ["approval_mode", "subagent_mode", "verbosity", "concept_depth"])
def test_dead_globals(tmp_path, key):
    root = write_repo(tmp_path)
    flow = good_flow()
    flow["globals"][key] = "whatever"
    write_flow(root, flow)
    only(root, f"carries `globals.{key}:`")


def test_interpolation_has_no_resolver(tmp_path):
    root = write_repo(tmp_path)
    flow = good_flow()
    flow["description"] = "Builds ${app_name}."
    write_flow(root, flow)
    only(root, "contains the interpolation '${app_name}'")


def test_node_parameters_are_not_inert(tmp_path):
    """`data.parameters` is the one deleted key with a live host read
    (`flow-extended.ts:47` takes `data.parameters.flow` as a child flow id)."""
    root = write_repo(tmp_path)
    flow = good_flow()
    node(flow, "b")["data"]["parameters"] = {"flow": "skaileup-slice"}
    write_flow(root, flow)
    only(root, "carries `data.parameters:`")


def test_node_writes_is_dead(tmp_path):
    root = write_repo(tmp_path)
    flow = good_flow()
    node(flow, "b")["data"]["writes"] = "05_features"
    write_flow(root, flow)
    only(root, "carries `data.writes:`")


# -- flows: node kinds ------------------------------------------------------

def test_sub_flow_node_is_rejected(tmp_path):
    """Ticket 10 inlined the shared building blocks and deleted the kind."""
    root = write_repo(tmp_path)
    flow = good_flow()
    flow["nodes"].append(
        {"id": "s", "type": "sub-flow", "data": {"flow": "skaileup-slice", "phase": "implementation"}}
    )
    flow["edges"].append({"id": "e2", "source": "b", "target": "s", "type": "flow"})
    write_flow(root, flow)
    only(root, "`type: 'sub-flow'`")


def test_router_node_is_rejected(tmp_path):
    """The pick-one renderers died with the mockup merge, and the kind with them."""
    root = write_repo(tmp_path)
    flow = good_flow()
    flow["nodes"].append(
        {"id": "r", "type": "router", "data": {"phase": "review", "routes": [{"target": "b"}]}}
    )
    flow["edges"].append({"id": "e2", "source": "b", "target": "r", "type": "flow"})
    write_flow(root, flow)
    only(root, "`type: 'router'`")


def test_requires_may_not_name_a_flow(tmp_path):
    root = write_repo(tmp_path)
    flow = good_flow()
    flow["requires"].append("flow:@skaile-ai/skaileup-slice")
    write_flow(root, flow)
    only(root, "ships no `sub-flow` nodes")


# -- flows: groups and phases -----------------------------------------------

def test_three_group_nodes_per_flow(tmp_path):
    """Two concept flows carry an empty `implementation` group for exactly this rule."""
    root = write_repo(tmp_path)
    flow = good_flow()
    flow["nodes"] = [n for n in flow["nodes"] if n["id"] != "g-review"]
    write_flow(root, flow)
    only(root, "has 2 group node(s)")


def test_two_groups_may_not_share_a_phase(tmp_path):
    root = write_repo(tmp_path)
    flow = good_flow()
    node(flow, "g-review")["data"]["phase"] = "implementation"
    write_flow(root, flow)
    only(root, "has 3 group node(s)")


def test_node_without_phase(tmp_path):
    root = write_repo(tmp_path)
    flow = good_flow()
    del node(flow, "b")["data"]["phase"]
    write_flow(root, flow)
    only(root, "declares no `data.phase`")


def test_node_with_invalid_phase(tmp_path):
    root = write_repo(tmp_path)
    flow = good_flow()
    node(flow, "b")["data"]["phase"] = "banana"
    write_flow(root, flow)
    only(root, "not one of")


def test_node_phase_must_agree_with_its_group(tmp_path):
    """The rule ticket 28 wrote as "one table so they cannot disagree" — and the one
    nothing checked. Both values are enum-valid; the group silently wins at render time."""
    root = write_repo(tmp_path)
    flow = good_flow()
    node(flow, "b")["data"]["phase"] = "review"
    write_flow(root, flow)
    only(root, "silently overridden and the two must be written from one table")


def test_skill_node_must_sit_in_a_group(tmp_path):
    """Without a parent there is no group phase to agree with, so the rule above is
    unenforceable on that node by construction."""
    root = write_repo(tmp_path)
    flow = good_flow()
    del node(flow, "b")["parentNode"]
    write_flow(root, flow)
    only(root, "has no `parentNode`")


def test_parent_node_must_be_a_group(tmp_path):
    root = write_repo(tmp_path)
    flow = good_flow()
    node(flow, "b")["parentNode"] = "a"
    write_flow(root, flow)
    only(root, "which is not a group node")


def test_group_node_may_not_be_parented(tmp_path):
    root = write_repo(tmp_path)
    flow = good_flow()
    node(flow, "g-review")["parentNode"] = "g-conceptualization"
    write_flow(root, flow)
    only(root, "is not a skill node but declares `parentNode`")


def test_skill_node_geometry_disables_the_swimlanes(tmp_path):
    """`flow-layout.ts:53-65` drops positioned nodes from the lane computation and returns
    `lanes: []` once none remain — authoring geometry deletes the group-phase override."""
    root = write_repo(tmp_path)
    flow = good_flow()
    node(flow, "b")["position"] = {"x": 10, "y": 10}
    write_flow(root, flow)
    only(root, "carries `position:`")


# -- flows: graph -----------------------------------------------------------

def test_duplicate_node_ids(tmp_path):
    root = write_repo(tmp_path)
    flow = good_flow()
    node(flow, "b")["id"] = "a"
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


def test_unresolvable_skill(tmp_path):
    root = write_repo(tmp_path)
    flow = good_flow()
    node(flow, "b")["data"]["skill"] = "ghost"
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
    among(root, "the host reads only `type: flow`", "unreachable from `entry` along `type: flow` edges")


def test_review_loop_edge_is_a_no_op(tmp_path):
    root = write_repo(tmp_path)
    flow = good_flow()
    flow["edges"][0]["type"] = "review-loop"
    write_flow(root, flow)
    among(root, "the host reads only `type: flow`", "unreachable from `entry`")


def test_optional_edge_does_not_confer_reachability(tmp_path):
    root = write_repo(tmp_path)
    flow = good_flow()
    flow["edges"][0]["type"] = "optional"
    write_flow(root, flow)
    among(root, "the host reads only `type: flow`", "unreachable from `entry`")


def test_non_flow_edge_parallel_to_a_flow_edge(tmp_path):
    """Reachability alone cannot see this one: every node still runs, and the extra edge
    draws on the canvas while ordering nothing."""
    root = write_repo(tmp_path)
    flow = good_flow()
    flow["edges"].append({"id": "e2", "source": "a", "target": "b", "type": "parallel"})
    write_flow(root, flow)
    only(root, "the host reads only `type: flow`")


# -- flows: requires --------------------------------------------------------

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


def test_requires_names_a_per_file_contract(tmp_path):
    """Ticket 34 made the reference layer one asset, so a per-file ref names nothing —
    `_` is not a legal asset-name character, so it could never have resolved."""
    root = write_repo(tmp_path)
    flow = good_flow()
    flow["requires"].append("contract:@skaile-ai/seed_data")
    write_flow(root, flow)
    only(root, "the only contract asset is 'shared-contracts'")


def test_requires_omits_the_reference_layer_its_skills_read(tmp_path):
    """Per-file exactness moved down to the skills; what a flow still owes is the one
    asset, present iff any of its own node skills reads a contract file."""
    root = write_repo(tmp_path, contracts=("concept_structure.md", "seed_data.md"))
    cite(root, "spec-feature", "seed_data")
    write_flow(root, good_flow())
    only(root, "does not list `contract:@skaile-ai/shared-contracts`")


def test_requires_lists_the_reference_layer_no_skill_reads(tmp_path):
    root = write_repo(tmp_path)
    flow = good_flow()
    flow["requires"].append("contract:@skaile-ai/shared-contracts")
    write_flow(root, flow)
    only(root, "which none of this flow's skills read")


def test_requires_ref_grammar(tmp_path):
    root = write_repo(tmp_path)
    flow = good_flow()
    flow["requires"] = ["spec-feature"]
    write_flow(root, flow)
    errs = errors(root)
    assert any("is not a `kind:@publisher/name` ref" in e for e in errs), errs


# -- prose: docs/ and the root ----------------------------------------------

def doc(root, rel: str, text: str) -> None:
    """Write a prose file at `rel`, creating its directory."""
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def test_dead_relative_link_in_docs(tmp_path):
    root = write_repo(tmp_path)
    doc(root, "docs/adr/0001-a.md", "See [the template](../skill-template.md).\n")
    only(root, "links to `../skill-template.md`")


def test_dead_relative_link_at_the_root(tmp_path):
    root = write_repo(tmp_path)
    doc(root, "README.md", "Start from [the examples](docs/examples/WHY.md).\n")
    only(root, "links to `docs/examples/WHY.md`")


def test_live_relative_link_resolves(tmp_path):
    root = write_repo(tmp_path)
    doc(root, "docs/skill-template.md", "# template\n")
    doc(root, "docs/adr/0001-a.md", "See [the template](../skill-template.md).\n")
    assert errors(root) == []


def test_external_and_anchor_links_are_not_paths(tmp_path):
    root = write_repo(tmp_path)
    doc(root, "README.md", "[repo](https://example.com/x) · [above](#layout) · [self](README.md#layout)\n")
    assert errors(root) == []


def test_dead_skill_path_in_docs(tmp_path):
    root = write_repo(tmp_path)
    doc(root, "docs/examples/WHY.md", "The port landed at `skills/concept-brief/`.\n")
    only(root, "names the path `skills/concept-brief`")


def test_live_skill_path_resolves(tmp_path):
    root = write_repo(tmp_path)
    doc(root, "docs/examples/WHY.md", "The port landed at `skills/spec-feature/`.\n")
    assert errors(root) == []


def test_prose_may_name_a_deleted_contract(tmp_path):
    """An ADR recording a deletion cites what it deleted; `WHY.md` quotes ported bodies
    verbatim. The gate reads paths, not mentions, so neither is an error."""
    root = write_repo(tmp_path)
    doc(root, "docs/adr/0004-contracts-earn-their-place.md", "Deletes `contracts/iron_laws.md`.\n")
    doc(root, "docs/examples/WHY.md", "The old body cited `contracts/skill_grammar.md`.\n")
    assert errors(root) == []


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
