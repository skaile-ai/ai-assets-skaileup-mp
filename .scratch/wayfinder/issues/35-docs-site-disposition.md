# 35: The docs site is generated from a tree that no longer exists

**Type:** grilling
**Blocked by:** None — graduated from the map's fog 2026-09-06
**Status:** resolved

## Question

Graduated from the **docs site** fog patch, narrowed twice already (ticket 18 cut the
second Starlight site out of it, ticket 33 supplied the reason to decide rather than defer).

The old repo carries a full Starlight site at `docs/` — **60 hand-written source files**, a
**470-line generator** (`docs/scripts/generate-skill-pages.mjs`), Astro + Starlight + mermaid
deps, and a `prebuild` hook that regenerates before every build. `-mp`'s `docs/` is **not a
site**: 14 plain markdown files (11 ADRs, the skill template, `examples/WHY.md`, the ADR
README).

Measured against `-mp` as it stands, the generator's inputs are mostly gone:

- **It emits a page per `DOMAIN.md`** (`:11`, `:345-348`, `:408`) and keys domains off a
  hardcoded `SKAILEUP_DOMAINS` set (`:98`, `:339`). **Ticket 05 deleted all 16 `DOMAIN.md`
  files** and ticket 04 made the tree flat — so the domain half of the generator has no input
  at all, and the synthesised fallback (`:427`, "_No DOMAIN.md authored yet._") would fire for
  every domain.
- **It hardcodes six contract paths** (`:35-40`); ticket 09 deleted **four** of them —
  `skill_grammar.md`, `asset_frontmatter.md`, `iron_laws.md`, `flows.md`. Only
  `golden_principles.md` and `semantic_types.md` survive, and `-mp` has eleven more contract
  files the list never names.
- **Three hand-written pages** (`docs/src/content/docs/domains/{meta,concept,impl}-group.md`)
  describe the old domain grouping, which ticket 04 replaced with nine name-carried domains.

Ticket 33 gave the reason this cannot just be deferred: **`check.py` globs `skills/` and
`contracts/` and never looks at `docs/`**, so anything skill-shaped living there has no gate
behind it — which is exactly how two worked examples drifted onto a dead tree and three dead
skill names went unnoticed until 33 found them.

So: **does `-mp` have a documentation site, and if so what generates it?**

1. **Port and rewrite** — carry the site over and rewrite the generator for a flat tree with
   no `DOMAIN.md`, thirteen contract files, and four flows. The generator is the bulk of the
   work; the 60 source pages are prose that has to be re-checked against a collection that
   changed shape in every dimension the site describes.
2. **Regenerate small** — drop the hand-written pages, keep a generated index over
   `skills/`, `flows/` and `contracts/` and nothing else. The site becomes a rendering of the
   collection rather than a document about it.
3. **Drop it** — `README.md`, `CONTEXT.md`, `contracts/README.md` and eleven ADRs already
   carry what the site's prose carried, and `-mp` is one third the size. The old repo keeps
   its site for as long as it runs.

Whatever the answer, it decides whether `docs/` needs a gate: today nothing checks it, and
`-mp` already ships `docs/examples/` that ticket 33 had to correct by hand.

## Answer

**No site. Option 3 — drop it.** `-mp` ships `docs/` as what it already is: 11 ADRs, the skill
template, `examples/WHY.md`. The old repo keeps its Starlight site with the tree that site
describes.

### Why the port was never a port

The measured case against carrying it over is not "it needs updating", it is that the site was
**already dead before the migration started**:

- **Never deployed.** No netlify/vercel/pages config anywhere in the old repo, no `site:` in
  `astro.config.mjs`, `dist/` untracked. Its README line reads "`npm run docs` to read it
  locally" — the site's entire audience was one machine.
- **Never built by CI.** `collection-ci.yml` runs `audit.py`, `verify_flows.py` and
  `verify_artifacts.py`; `docs:build` appears in no job. Nothing has ever proven the site
  compiles, let alone that it is accurate.
- **Two months stale by its own history.** `docs/src` was last touched **2026-06-30**, in the
  same commit that renamed the flows it documents. The collection kept moving until September;
  the site did not follow.

Against a dead site, "port and rewrite" is re-authoring: the generator's domain half has zero
input (ticket 05 deleted all 16 `DOMAIN.md`), four of its six hardcoded contract paths were
deleted by ticket 09, and the 8 intro pages (1,110 lines) all describe the pre-migration shape —
`mental-model.mdx` opens on `skaileup-base`, five tiers and the two slice clusters, none of which
exist. **Option 2 (regenerate small) was rejected too**, for a reason worth writing down: a
generated index over `skills/`, `flows/` and `contracts/` renders what `check.py` already
verifies and what forge-concept already draws, so it adds an Astro toolchain to restate two
things that are correct by construction.

### The gate: `docs/` is checked, on paths only

`check.py` gained **`check_docs`**, run over `docs/**/*.md` and the root markdown — the files no
other check reads (`skills/` and `contracts/` have their own; `flows/` is YAML). Two rules:

1. every **relative markdown link** resolves;
2. every **`skills/<name>` path** names a skill that exists.

It is deliberately a check on *paths*, not on *mentions*, and the probe that set that boundary is
the finding here. A dead-**name** sweep over prose fires on exactly the two artifacts that are
*supposed* to name dead things: an ADR recording a deletion cites the file it deleted
(`0004-contracts-earn-their-place.md` → `contracts/iron_laws.md`, `0010` → `contracts/plans.md`),
and `examples/WHY.md` quotes pre-port skill bodies verbatim — which ticket 33 kept on purpose.
Extending the existing contract-citation check to prose would have turned four correct historical
records into CI failures. The bar ticket 33 set is "a reader must not be able to copy a path that
resolves to nothing", and links carry that bar without touching what prose may *mention*.

Run over the repo as it stands: **zero** dead links and **zero** dead `skills/<name>` paths across
all 14 `docs/` files and the root markdown, so the gate lands green and locks ticket 33's cleanup
in place. Seven fixtures cover it, including the two exemptions as positive cases.

### `docs/` needs no narrative to replace the site

The site's intro pages were the only end-to-end prose, and they are also the only part of the old
repo that measurably rotted — because they restated the flow graph. `-mp` does not rewrite them.
Instead README grew a **How a project moves through it** table naming the four landed flows and
pointing at `contracts/concept_structure.md`, and its Status section now states outright that
there is no docs site and where the old one lives. The stale pointer it carried
(`.scratch/skaileup-mp/map.md`, in the old repo) is repaired to `.scratch/wayfinder/map.md`.

### Found on the way: `main` was red in CI

Not this ticket's question, but this ticket's file. `scripts/test_check.py` was **green at ticket
31 (61 passed) and 58-failed at ticket 34**, one commit later — so CI has been failing on `main`
since. Ticket 34 changed three things and updated no fixture:

- `write_repo` never wrote `contracts/CONTRACT.md`, which 34 made mandatory, so *every* test
  carried that one error and every `only(...)` assertion broke;
- three tests still asserted the per-file `requires:` contract rules 34 replaced with the single
  `shared-contracts` asset;
- the new lookbehind on `CONTRACT_REF_RE` — meant to keep deployed `.claude/contracts/...` paths
  out of the citation set — also stopped matching **`../contracts/<file>`**, silently disabling
  ticket 28's `flows/README.md` gate. That one was a real lost check, not a stale test: the
  regex now matches an explicit `../` run, and ticket 28's fixture passes again.

Repaired here because a new gate in that file cannot be verified against a red suite:
**69 passed**, `check.py` → `29 skill(s) · 4 flow(s) · 0 error(s)`.

### Consequences for ticket 37

[37: What carries over from the old repo besides skills](37-old-repo-carry-over.md) is unblocked.
Two of its three items are decided in shape: `improvements.mdx` was a page *inside* the dropped
site, and reading it settles the rest of the question — it is headed "The collection
reorganization history — Phases 0–3, all complete", a historical record of the **old** repo's
reorg, not a live backlog. `docs/devlog/` (31 files) is untouched by this ticket and is 37's real
question.
