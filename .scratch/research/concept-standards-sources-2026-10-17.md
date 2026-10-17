# Standards and open formats for `_concept/` artifacts — verified sources

Research date: 2026-10-17. All versions and dates are "as of the cited source" on that date. This file records facts only; it makes no migration recommendations.

Conventions:
- **Stability** uses: `stable` (final / OASIS Standard / W3C Rec / ISO published), `candidate` (final report of a community body that is not a standards body), `draft`, `pre-1.0`, `de-facto` (widely used, no standards body).
- `UNVERIFIED` = not confirmed from a primary source in this session.
- "Primary" = spec site, spec owner's repo / registry, standards body page. Tool-support entries are taken from the owner's own docs or release notes unless marked.
- Where an owner's own site was the only source for a tool list, it is cited as such.

---

## 1. Design tokens

### 1.1 Design Tokens Format Module (DTCG)
| Field | Value |
|---|---|
| Owner | W3C Design Tokens Community Group (DTCG). A W3C **Community Group** report; the page says "It is not a W3C Standard nor is it on the W3C Standards Track." |
| Version / date | **Design Tokens Format Module 2025.10**, Final Community Group Report, **28 October 2025** |
| Stability | **candidate / stable (CG-level).** Published "as a Candidate Recommendation following the definitions provided by the W3C process"; "This specification is considered stable. Further updates will be provided in superseding specifications." Announced as "the first stable version" (W3C CG blog post, 2025-10-28). A newer *preview* draft exists at `/tr/drafts/format/` (dated 08 September 2026) and is marked "Do not attempt to implement this version" — it is not a release. |
| Format | JSON. File extensions: `.tokens` or `.tokens.json` ("recommended by this spec"). Media type: `application/design-tokens+json` (SHOULD); `application/json` MAY be used; tools MUST support both. |
| Shape | Tree of groups and tokens. Reserved properties are `$`-prefixed: `$value`, `$type`, `$description`, `$extensions`, `$deprecated`; aliases use `{group.token}` references; composite tokens (e.g. `shadow`) have object `$value`. Colors are structured objects in 2025.10 (`colorSpace`, `components`, `alpha`, optional `hex`). `$root` token path segment exists in 2025.10. |
| Companion modules (same date) | **Color Module 2025.10** and **Resolver Module 2025.10** (theming / multi-file resolution). Resolver documents: file extension `.resolver.json` (SHOULD). |
| Tool support | Style Dictionary (v5), Terrazzo, Tokens Studio; the W3C announcement also lists Penpot, Figma, Sketch, Framer, Knapsack, Supernova, zeroheight as "support or are implementing" (vendor claims in the CG's own announcement). |
| Primary URLs | Format: https://www.designtokens.org/tr/2025.10/format/ · Reports index: https://www.w3.org/community/design-tokens/ · Announcement: https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/ · Resolver: https://www.designtokens.org/tr/2025.10/resolver/ |

### 1.2 Style Dictionary (DTCG support)
| Field | Value |
|---|---|
| Owner | Style Dictionary project (`style-dictionary/style-dictionary`), npm `style-dictionary` |
| Versions | v4.0.0 published 2024-06-28, v5.0.0 2025-05-16 (npm registry timestamps); latest **v5.7.0, 2026-10-16** (GitHub releases). |
| DTCG status | Docs: "As of version 4, Style Dictionary has first-class support for the DTCG format. **Important note: the latest format 2025.10 does not have full support yet in Style Dictionary. This is a work in progress in v5.**" Release notes show incremental 2025.10 support: v5.3.0 (2026-02-09) structured color objects, 14 color spaces; v5.4.0 (2026-03-22) dimension object values; v5.7.0 (2026-10-16) `duration`, `$root`. v5.0.0 aligned reference syntax `{ref.foo}` with DTCG and requires Node ≥ 22. |
| Primary URLs | https://styledictionary.com/info/dtcg/ · https://styledictionary.com/versions/v5/migration/ · https://github.com/style-dictionary/style-dictionary/releases |

### 1.3 Figma Variables vs DTCG
| Field | Value |
|---|---|
| Owner | Figma (proprietary variables model) |
| Status | Figma Variables are a **proprietary** model with a REST API ("This API is available to full members of Enterprise orgs"). They are described by Figma as a way to "implement design tokens". |
| DTCG relation | DTCG announcement lists Figma as supporting/implementing the spec. **Native Figma import/export of DTCG JSON: UNVERIFIED** — the only source found is a third-party blog (figma.obra.studio, 2025-11-11) summarising a Figma conference talk; no Figma help-center or release-notes page confirming it was found. Figma's own resource page says the DTCG "is actively working to standardize this format". |
| Primary URLs | https://developers.figma.com/docs/rest-api/variables-endpoints/ · https://help.figma.com/hc/en-us/articles/15339657135383-Guide-to-variables-in-Figma · https://www.figma.com/resource-library/design-tokens/ |

---

## 2. Architecture decision records

### 2.1 MADR (Markdown Architectural Decision Records)
| Field | Value |
|---|---|
| Owner | `adr` GitHub org (Oliver Kopp, Olaf Zimmermann); dual MIT / CC0 |
| Version / date | **4.0.0, 2024-09-17** (also on npm `madr@4.0.0`); 4.0.0-beta 2024-09-02; 3.0.0 2022-10-09 |
| Stability | **de-facto** (community template; no standards body) |
| Format / name | Markdown. Decisions in `docs/decisions/`, file name `NNNN-title-with-dashes.md` (`NNNN` consecutive number, lowercase dashes, `.md`). Optional YAML front matter keys in the template: `status`, `date`, `decision-makers`, `consulted`, `informed`. |
| Shape | `# {title}` → `## Context and Problem Statement` → `## Decision Drivers` (opt.) → `## Considered Options` → `## Decision Outcome` (+ `### Consequences`, `### Confirmation` opt.) → `## Pros and Cons of the Options` (opt.) → `## More Information` (opt.). Templates shipped: full, minimal, bare, bare-minimal. |
| Tool support | `markdownlint` config shipped in template; Log4brains (default template); Structurizr (`madr` ADR importer). Site notes "There is currently no tooling supporting MADR 3.0.0" for an automatic create flow. |
| Primary URLs | https://adr.github.io/madr/ · https://github.com/adr/madr/releases/tag/4.0.0 |

### 2.2 Nygard ADR format
| Field | Value |
|---|---|
| Owner | Michael Nygard, blog post "Documenting Architecture Decisions", 2011-11-15 (Cognitect) |
| Stability | **de-facto** (blog post; no versioned spec) |
| Shape | Title (short noun phrase, e.g. "ADR 1: …"), Context, Decision ("We will …"), Status (proposed / accepted / superseded), Consequences. Stored as "a collection of records" in the repo. |
| Primary URL | https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions |

### 2.3 adr-tools
| Field | Value |
|---|---|
| Owner | Nat Pryce (`npryce/adr-tools`) |
| Version / date | **3.0.0, 2018-07-25** (latest release; no later release found) |
| Stability | **de-facto**; shell scripts |
| Convention | `adr init <dir>` (default `doc/adr`) creates `0001-record-architecture-decisions.md` (verified in repo tree: `doc/adr/0001-record-architecture-decisions.md`). `adr new -s N <title>` supersedes. Markdown, numbered file per decision. |
| Primary URLs | https://github.com/npryce/adr-tools · https://raw.githubusercontent.com/npryce/adr-tools/master/README.md |

### 2.4 Log4brains
| Field | Value |
|---|---|
| Owner | Thomas Vaillant (`thomvaill/log4brains`) |
| Version / date | **v1.1.0, 2024-12-17** (npm `log4brains`, `@log4brains/cli`) |
| Stability | **de-facto** |
| Convention | ADR folder configured by `adrFolder` (default `./docs/adr`); file names `YYYYMMDD-title.md` (README example tree), plus `index.md` and `template.md`; README states "No required file numbering schema (i.e. `adr-0001.md`)…". Default template is MADR. Monorepo: global ADRs in `docs/adr` and per-package ADRs in `packages/<name>/docs/adr`. |
| Primary URL | https://github.com/thomvaill/log4brains |

Cross-check: Structurizr's ADR importers are `adr-tools`, `madr`, `log4brains` (https://docs.structurizr.com/dsl/adrs). **Naming difference to note:** MADR uses `docs/decisions/NNNN-title.md`; adr-tools uses `doc/adr/NNNN-*.md`; Log4brains uses `docs/adr/YYYYMMDD-*.md`.

---

## 3. Architecture description

### 3.1 C4 model
| Field | Value |
|---|---|
| Owner | Simon Brown (c4model.com; site content CC BY 4.0) |
| Version | No version number or release date published on the site. **UNVERIFIED** as a versioned spec. |
| Stability | **de-facto** (an approach, not a file format) |
| Shape | Hierarchical abstractions: software system → container → component → code. Hierarchical diagrams: system context, container, component, code; supporting diagrams: system landscape, dynamic, deployment. "Notation independent" ("doesn't prescribe any particular notation") and "tooling independent". **No canonical file format or file name.** |
| Primary URLs | https://c4model.com/ · https://c4model.com/diagrams/notation |

### 3.2 Structurizr DSL
| Field | Value |
|---|---|
| Owner | Structurizr (Simon Brown). Repo `structurizr/structurizr`, Apache-2.0, "models as code tool designed for the C4 model" |
| Version / date | No separate DSL version. Tooling release **v2026.09.19** (2026-09-19, GitHub releases; docs "Binaries - v2026.09.19"). Separate `structurizr/cli` last release v2025.11.09 and `structurizr/lite` last v2025.11.08. |
| Stability | **de-facto** (tool-defined language) |
| Format / name | Text DSL. `workspace.dsl` is the workspace source ("Your workspace source, created using the Structurizr DSL"); the companion JSON file type is `workspace.json`. Quickstart: Structurizr "created a file named `workspace.dsl`" in the data directory. Workspace-level blocks: `model`, `views`, `configuration`, `!docs`, `!adrs`, `!identifiers`. |
| Tool support | Structurizr (server / local / Lite), Structurizr CLI, export to PlantUML and Mermaid (docs getting-started list), MCP server + DSL generation (docs "AI + MCP"). C4-PlantUML (`plantuml-stdlib/C4-PlantUML` v2.14.0, 2026-08-26) is a separate, notation-level library. |
| Primary URLs | https://docs.structurizr.com/dsl/language · https://docs.structurizr.com/workspaces/file-types · https://docs.structurizr.com/local/quickstart · https://github.com/structurizr/structurizr |

### 3.3 arc42
| Field | Value |
|---|---|
| Owner | Dr. Gernot Starke (arc42.org page author); template repo `arc42/arc42-template`. License CC BY-SA 4.0 (arc42.org/license). Other authors/maintainers: UNVERIFIED. |
| Version / date | Repo README table: **English 9.0 (July 2025)**; German 9.1 (December 2025); other languages 8.2–9.0. Repo CI tags like `2026.10.15.3` are build tags (2026-10-15), not template versions. |
| Stability | **de-facto** (open template; no standards body) |
| Shape | **12 sections**: 1 Introduction & Goals · 2 Constraints · 3 Context & Scope · 4 Solution Strategy · 5 Building Block View · 6 Runtime View · 7 Deployment View · 8 Crosscutting Concepts · 9 Architectural Decisions · 10 Quality Requirements · 11 Risks & Technical Debt · 12 Glossary. Section 9 lists "Important decisions, unless described elsewhere"; section 12 is the "ubiquitous language". |
| Format | Source is AsciiDoc; downloadable formats include docx, Markdown, DocBook "and others". No canonical single file name found (**UNVERIFIED**). |
| Primary URLs | https://arc42.org/overview · https://github.com/arc42/arc42-template · https://arc42.org/license |

### 3.4 ISO/IEC/IEEE 42010:2022
| Field | Value |
|---|---|
| Owner | ISO/IEC JTC 1/SC 7 with IEEE |
| Version / date | **Edition 2, 2022-11** (published 2022-11-07), stage 60.60; replaces 42010:2011 |
| Stability | **stable** (published International Standard) |
| Shape | Specifies requirements for the *structure and expression* of an architecture description (architecture description framework, ADL, viewpoints, model kinds). States: "This document does not specify any format or media for recording an AD." |
| Primary URL | https://www.iso.org/standard/74393.html |

---

## 4. Acceptance criteria and requirements

### 4.1 EARS
| Field | Value |
|---|---|
| Owner | Alistair Mavin (with Rolls-Royce co-authors, RE'09 paper) |
| Version | No version number. **UNVERIFIED** for a versioned spec. |
| Stability | **de-facto** (method / sentence templates) |
| Shape | Five patterns plus combinations, `The <system name> shall <system response>`: Ubiquitous (no keyword); Event-driven (`When`); State-driven (`While`); Unwanted behaviour (`If … then`); Optional feature (`Where`); Complex = combinations. Not a file format. |
| Primary URL | https://alistairmavin.com/ears/ |

### 4.2 Gherkin / Cucumber
| Field | Value |
|---|---|
| Owner | Cucumber open-source project (`cucumber/gherkin`) |
| Version / date | Gherkin parser **v42.0.1, 2026-08-05** (GitHub releases); `cucumber-jvm` v8.0.4 (2026-10-02); `cucumber-js` v13.3.0 (2026-10-05) |
| Stability | **de-facto** (project-defined language; no standards body) |
| Format | Plain text, extension **`.feature`**; "You can only have a single Feature in a `.feature` file". Keywords: Feature, Rule, Example/Scenario, Given/When/Then/And/But, Background, Scenario Outline + Examples. Comments `#`. |
| Primary URL | https://cucumber.io/docs/gherkin/reference/ |

### 4.3 ISO/IEC/IEEE 29148:2018
| Field | Value |
|---|---|
| Owner | ISO/IEC JTC 1/SC 7 with IEEE |
| Version / date | **Edition 2, 2018-11**; "last reviewed and confirmed in 2024"; stage **90.92 (to be revised)** since 2026-02-16; a draft replacement **ISO/IEC/IEEE DIS 29148** (Edition 1) is listed as "Next version under development" |
| Stability | **stable** (published; revision under way) |
| Shape | Requirements-engineering processes and required information items/content (e.g. StRS, SyRS, SRS). Gives format *guidelines*; not a file format. |
| Primary URL | https://www.iso.org/standard/72089.html |

### 4.4 OMG ReqIF
| Field | Value |
|---|---|
| Owner | OMG (Object Management Group) |
| Version / date | **ReqIF 1.2, formal/16-07-01, July 2016** ("Document Status: formal"). |
| Stability | **stable** (formal OMG spec) |
| Format | XML exchange document, normative `reqif.xsd` (XML schema) plus CMOF/XMI model, spec PDF has "Exchange Document Structure" and "Exchange Document Content" clauses. Exchange-process based (requirements tool → requirements tool). **Canonical file extension (`.reqif` / `.reqifz`): UNVERIFIED** — not stated in the spec PDF (text search of the 98-page PDF found no extension). |
| Primary URLs | https://www.omg.org/spec/ReqIF · https://www.omg.org/spec/ReqIF/1.2/PDF |

### 4.5 OSLC Requirements Management
| Field | Value |
|---|---|
| Owner | OSLC Open Project (OASIS) |
| Version / date | **OSLC Requirements Management Version 2.1, OASIS Standard, 21 June 2021** (Part 1: Specification). OSLC Core Version 3.0: **OASIS Standard, 26 August 2021**. OSLC spec index also lists RM 2.1 PS01 / PSD 02 follow-up drafts and RM 2.0 "Final (closed WG)". |
| Stability | **stable** (OASIS Standard); newer drafts exist |
| Shape | RESTful services + RDF vocabularies (linked data) for requirements and links to other lifecycle domains (CM, QM, Architecture Management). Not a file format; a server-protocol standard. |
| Primary URLs | https://docs.oasis-open-projects.org/oslc-op/rm/v2.1/os/requirements-management-spec.html · https://docs.oasis-open-projects.org/oslc-op/core/v3.0/oslc-core.html · https://open-services.net/specifications/ |

### 4.6 AI spec-driven conventions (not standards; tool conventions)

| Tool | Owner / version | Files and layout (verified) | Stability | Primary URL |
|---|---|---|---|---|
| **GitHub Spec Kit** | GitHub (`github/spec-kit`), MIT; **v1.2.1, 2026-10-16** | Per-feature dir `specs/NNN-name/` with `spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`, `tasks.md` (from `spec-driven.md`). Project-wide `.specify/memory/constitution.md` (repo tree). Active feature recorded in `.specify/feature.json` (quickstart doc). Templates in `templates/` (`spec-template.md`, `plan-template.md`, `tasks-template.md`, `constitution-template.md`). Slash commands `/speckit.*` / `/speckit-*`. | de-facto, fast-moving | https://github.com/github/spec-kit · https://raw.githubusercontent.com/github/spec-kit/main/spec-driven.md |
| **AWS Kiro specs** | AWS Kiro IDE | Three files per spec: `requirements.md` (or `bugfix.md`), `design.md`, `tasks.md`. `requirements.md` "uses EARS notation": `WHEN [condition/event] THE SYSTEM SHALL [expected behavior]`. Layout `.kiro/specs/<feature>/` (best-practices doc). | vendor-defined, de-facto | https://kiro.dev/docs/specs/ · https://kiro.dev/docs/specs/feature-specs/ · https://kiro.dev/docs/specs/best-practices/ |
| **OpenSpec** | Fission-AI (`Fission-AI/OpenSpec`), MIT; **v1.14.3, 2026-10-17** (npm `@fission-ai/openspec`) | `openspec/specs/<domain>/spec.md` (current behaviour; `### Requirement:` with `SHALL`/`MUST` + `#### Scenario:` GIVEN/WHEN/THEN) and `openspec/changes/<change-name>/` with `proposal.md`, `design.md`, `tasks.md`; archived to `openspec/changes/archive/<date>-<name>/`. | de-facto | https://github.com/Fission-AI/OpenSpec · https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md |

---

## 5. Test and verification results

### 5.1 JUnit XML
| Field | Value |
|---|---|
| Owner | No owner of a spec. Origin: Apache Ant `junit` / `junitreport` tasks (JUnit project). |
| Version | None. **De-facto schema, no official specification.** A community documentation project states: "There is no official specification for the JUnit XML file format and various tools generate and support different flavors" (Testmo, secondary source). |
| Stability | **de-facto** |
| Format / name | XML. Ant writes per-suite `TEST-<class>.xml` and merges to `TESTS-TestSuites.xml` (Ant `junitreport` docs). Elements `testsuites` / `testsuite` / `testcase` with `failure` / `error` / `skipped`. |
| Newer JUnit-team format | **Open Test Reporting** (`ota4j-team/open-test-reporting`, "Language-agnostic XML and HTML test reporting formats… Maintained by the JUnit team"); release **r0.2.7, 2026-07-25**; pre-1.0 style tags. Has an event-based XML format and a hierarchical XML format. |
| Primary URLs | https://ant.apache.org/manual/Tasks/junitreport.html · https://github.com/ota4j-team/open-test-reporting · (secondary) https://github.com/testmoapp/junitxml |

### 5.2 CTRF — Common Test Report Format
| Field | Value |
|---|---|
| Owner | CTRF community (`ctrf-io/ctrf`), MIT |
| Version / date | Spec tag **v0.2.0, 2026-10-10** (git tag date); v0.1.0 2026-10-03. Docs examples follow CTRF 0.1.0. |
| Stability | **pre-1.0** ("We are maintaining a pre-1.0 version to allow for community-driven refinements before locking the v1.0.0 standard.") |
| Format | JSON. Root requires `reportFormat: "CTRF"`, `specVersion` (SemVer), `results`; optional `reportId`, `timestamp`, `generatedBy`. JSON Schema at `schema/ctrf.schema.json`. Canonical file name: **UNVERIFIED**. |
| Shape | `results` → `tool`, `summary`, `tests[]` (each with status), optional `environment`, `insights`, `baseline`. |
| Tool support | Reporters/plugins for many frameworks (e.g. `jest-ctrf-reporter` named in root example), CLI, integrations list on site. |
| Primary URLs | https://ctrf.io/docs/specification/overview · https://ctrf.io/docs/specification/root · https://github.com/ctrf-io/ctrf |

### 5.3 SARIF (OASIS)
| Field | Value |
|---|---|
| Owner | OASIS SARIF TC |
| Version / date | **SARIF 2.1.0, OASIS Standard, 27 March 2020**; **Errata 01 approved 28 August 2023** (current OASIS Standard text: "Version 2.1.0 Plus Errata 01"). A **2.2** line exists only as Committee Specification Drafts: GitHub tags `sarif-2.2-csd-01-20261009` (2026-10-13) etc., marked prerelease. |
| Stability | **stable** (2.1.0 + Errata 01); 2.2 = **draft** |
| Format | JSON. File name "SHOULD end with the extension `.sarif`"; MAY also end `.json` (e.g. `output.sarif.json`). |
| Shape | Static-analysis result log: `runs[]` → `tool.driver.rules[]`, `results[]` (ruleId, level, message, locations[]), artifacts. Format is generic enough for any linter that emits findings. |
| Tool support | GitHub code scanning accepts SARIF uploads (GitHub docs page "SARIF support for code scanning"). Other consumers (CodeQL, VS Code SARIF viewer, linter formatters): UNVERIFIED in this session. |
| Primary URLs | https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html · https://www.oasis-open.org/committees/tc_home.php?wg_abbrev=sarif · https://github.com/oasis-tcs/sarif-spec · https://docs.github.com/en/code-security/code-scanning/integrating-with-code-scanning/sarif-support-for-code-scanning |

### 5.4 TAP — Test Anything Protocol
| Field | Value |
|---|---|
| Owner | testanything.org community |
| Version | **TAP version 14 specification — labelled "(Current)"** on the site; versions 13 and original TAP listed. Publication date of v14: **UNVERIFIED**. |
| Stability | **de-facto** (site: "Document the observed behavior of widely used TAP implementations. Add no features that are not already in wide usage") |
| Format | Line-oriented text. `ok` / `not ok` + test number + ` - ` description + optional directive (`# SKIP`, `# TODO`), `1..N` plan, `TAP version 14` header. No mandated extension (`.tap` common — UNVERIFIED). |
| Primary URLs | https://testanything.org/ · https://testanything.org/tap-version-14-specification.html |

---

## 6. Data model

### 6.1 DBML
| Field | Value |
|---|---|
| Owner | Holistics (`holistics/dbml`), Apache-2.0 |
| Version | No language version number published; npm `@dbml/core` and `@dbml/cli` **10.3.1, 2026-10-09**. |
| Stability | **de-facto** ("open-source DSL") |
| Format / name | Text DSL; docs: "Our recommended best practices is to have a `database.dbml` file in your root repository". Core constructs: `Project`, `Table`, columns with settings, `Ref`, `Enum`, `Index`, `TableGroup`, `Note`. |
| Tool support | dbdiagram.io (diagram as code), dbdocs (docs as code), `@dbml/cli` (DBML ⇄ SQL), `@dbml/core` module. |
| Primary URLs | https://dbml.dbdiagram.io/docs/ · https://dbml.dbdiagram.io/home/ · https://github.com/holistics/dbml |

### 6.2 JSON Schema
| Field | Value |
|---|---|
| Owner | JSON Schema organisation (`json-schema-org`) |
| Version | json-schema.org specification page: **"The current version is 2020-12! The previous version was 2019-09."** No newer published release on that page (a date-based "latest unreleased" draft is referenced). |
| Stability | **de-facto** (community-maintained spec; no standards body) |
| Format | JSON (also expressible in YAML). `$schema` URI `https://json-schema.org/draft/2020-12/schema`. |
| Primary URL | https://json-schema.org/specification |

### 6.3 Prisma schema (PSL)
| Field | Value |
|---|---|
| Owner | Prisma (vendor) |
| Version | Latest **non-prerelease GitHub release 7.10.0, 2026-08-25**. v7 docs: "typically a single file called `schema.prisma` (or multiple files with `.prisma` file extension)". **v8 release candidates** (`8.0.0-rc.23`, npm `prisma` 2026-10-15; GitHub `v8.0.0-rc.18` 2026-10-14) — current (v8-track) docs state "the **`contract.prisma` file that replaced `schema.prisma`**… `npx prisma contract emit`". |
| Stability | **de-facto, vendor-owned**; file name differs between v7 (`schema.prisma`) and v8 RC (`contract.prisma`) |
| Primary URLs | https://www.prisma.io/docs/orm/prisma-schema/overview (v8 track) · https://www.prisma.io/docs/orm/prisma-schema/overview.md (v7 text) · https://github.com/prisma/prisma/releases |

### 6.4 OpenAPI
| Field | Value |
|---|---|
| Owner | OpenAPI Initiative (spec.openapis.org) |
| Versions / dates (GitHub releases) | **3.2.1, 2026-09-10** (patch; "no significant changes"); **3.2.0, 2025-09-19**; 3.1.2 2025-09-19; 3.1.1, 3.1.0; 3.0.4 … 3.0.0; 2.0. spec.openapis.org lists v3.2.1, v3.2.0, v3.1.2, 3.1.1, 3.1.0, 3.0.4 … |
| Stability | **stable** (published specification versions) |
| Format | JSON or YAML (file names and 3.1 ⇄ JSON Schema 2020-12 alignment: UNVERIFIED — not re-read this session). |
| Primary URLs | https://spec.openapis.org/oas/ · https://github.com/OAI/OpenAPI-Specification/releases |

### 6.5 AsyncAPI
| Field | Value |
|---|---|
| Owner | AsyncAPI Initiative |
| Version / date | **3.1.0, 2026-01-31** (GitHub `asyncapi/spec` release); 3.0.1 2023-12-13; 3.0.0 2023-12-05 |
| Stability | **stable** |
| Format | JSON or YAML. "By convention, the AsyncAPI Specification (A2S) file is named `asyncapi.json` or `asyncapi.yaml`." |
| Tool support | `@asyncapi/parser` 3.6.6 (2026-10-16) |
| Primary URL | https://www.asyncapi.com/docs/reference/specification/v3.1.0 |

### 6.6 LinkML
| Field | Value |
|---|---|
| Owner | LinkML community project (`linkml/linkml`), Apache-2.0 |
| Version / date | **v1.12.1, 2026-10-13** (linkml); `linkml-model` v1.12.0 (2026-10-08) |
| Stability | **de-facto** (open-source modeling language) |
| Format | YAML schemas ("author schemas in YAML"). Generators documented for JSON Schema, SQL DDL, Pydantic, SHACL, OWL, JSON-LD context, GraphQL, ProtoBuf, OpenAPI, TypeScript, Rust, Go, Java, PlantUML/ER diagrams. |
| Primary URLs | https://linkml.io/linkml/ · https://linkml.io/linkml/generators/index.html |

---

## 7. Behaviour and state machines

### 7.1 W3C SCXML
| Field | Value |
|---|---|
| Owner | W3C |
| Version / date | **State Chart XML (SCXML): State Machine Notation for Control Abstraction, W3C Recommendation, 1 September 2015** |
| Stability | **stable** ("a stable document and may be used as reference material") |
| Format | XML. Media type **`application/scxml+xml`** (Appendix H). Spec examples are named `*.scxml` (e.g. `Main.scxml`). |
| Tool support | Apache Commons SCXML (docs page shows `Version: 2.0-SNAPSHOT`, last published 15 July 2015 — maintenance state unclear); `@xstate/scxml` is on release feed as `1.0.0-alpha.2` (2026-10-17, prerelease). |
| Primary URL | https://www.w3.org/TR/scxml/ |

### 7.2 XState v5 JSON (Stately)
| Field | Value |
|---|---|
| Owner | Stately (`statelyai/xstate`), MIT |
| Version / date | **xstate 5.33.3, 2026-10-17** (latest); **6.0.0-alpha.68** pre-release (2026-10-17); docs banner "XState v6 alpha" |
| Stability | **de-facto** (library-defined; vendor-owned) |
| Format | Machine configs are plain JSON-serializable objects (`id`, `initial`, `context`, `states`, `on`, `invoke`). Stately Studio "Export as code" offers "JSON code for use with XState", JavaScript, TypeScript, Markdown (beta), Mermaid. Stately SDK supports "XState `.json` and `.jsonc` sources" (one machine per file). No standard file extension beyond `.json`/`.jsonc`. |
| Primary URLs | https://stately.ai/docs/xstate · https://stately.ai/docs/machines · https://stately.ai/docs/export-as-code · https://stately.ai/docs/packages/sdk · https://github.com/statelyai/xstate/releases |

### 7.3 BPMN 2.0
| Field | Value |
|---|---|
| Owner | OMG; ISO adoption as **ISO/IEC 19510:2013** (Edition 1, 2013) |
| Version / date | OMG current: **BPMN 2.0.2, formal/13-12-09, January 2014**. ISO/IEC 19510:2013 published. |
| Stability | **stable** |
| Format | XML. Normative schema `BPMN20.xsd` (namespace `http://www.omg.org/spec/BPMN/20100501/BPMN20.xsd`); the spec's own interchange examples use `.bpmn` file names (`main.bpmn`, `semantic1.bpmn`, `diagram1.bpmn`). |
| Primary URLs | https://www.omg.org/spec/BPMN/ · https://www.iso.org/standard/62652.html |

### 7.4 Mermaid `stateDiagram`
| Field | Value |
|---|---|
| Owner | `mermaid-js/mermaid`, MIT |
| Version / date | npm `mermaid` **12.2.0, 2026-10-13** |
| Stability | **de-facto** (library syntax; no standard) |
| Shape | Keyword `stateDiagram-v2` (newer renderer) or `stateDiagram` (older renderer); `[*] --> State`, nested/composite states, notes. Syntax "tries to be compliant with the syntax used in plantUml". No dedicated extension (diagram text lives in Markdown code fences or `.mmd` — latter UNVERIFIED). |
| Primary URLs | https://mermaid.js.org/syntax/stateDiagram.html · https://github.com/mermaid-js/mermaid |

---

## 8. Glossary and vocabulary

### 8.1 W3C SKOS
| Field | Value |
|---|---|
| Owner | W3C (Semantic Web Deployment WG) |
| Version / date | **SKOS Simple Knowledge Organization System Reference, W3C Recommendation, 18 August 2009** |
| Stability | **stable** |
| Shape | RDF vocabulary: `skos:Concept`, `skos:ConceptScheme`, `prefLabel`, `altLabel`, `definition`, `broader`/`narrower`/`related`, mapping properties. Serialised as RDF (Turtle, RDF/XML, JSON-LD — serialisation list not re-verified here). |
| Primary URL | https://www.w3.org/TR/skos-reference/ |

### 8.2 Context Mapper CML (DDD)
| Field | Value |
|---|---|
| Owner | ContextMapper project (`ContextMapper/context-mapper-dsl`), Apache-2.0 |
| Version / date | Latest release **v6.12.0, 2024-08-30** (GitHub releases; no later release found) |
| Stability | **de-facto** (DSL for strategic DDD: context map, bounded contexts, aggregates, subdomains) |
| Format | `.cml` (owner's examples repo contains `*.cml` files, e.g. `src/main/cml/architectural-refactorings/AR-01-…/example-input.cml`). Shape: Context Map, Bounded Context, Domain/Subdomain, Aggregate; relationship patterns (Partnership, Shared Kernel, Customer/Supplier, Conformist, OHS, ACL, Published Language). It models bounded contexts/aggregates, not glossary term definitions. |
| Primary URLs | https://contextmapper.org/ · https://contextmapper.org/docs/language-model/ · https://github.com/ContextMapper/context-mapper-dsl |

(Schema.org `DefinedTerm` is item 12.3.)

---

## 9. UI components / screens

### 9.1 Storybook Component Story Format (CSF)
| Field | Value |
|---|---|
| Owner | Storybook (`ComponentDriven/csf`; docs on storybook.js.org) |
| Version | **CSF 3** is the documented stable format. **CSF Next (Preview)** — factory-function API ("CSF Factories"), marked "🧪 preview feature… API may change". Storybook **10.6.2, 2026-10-12** (npm `@storybook/react` latest; 11.0.0-alpha.6 on `next`). `ComponentDriven/csf` last tag v0.1.13 (2024-12-24). |
| Stability | **de-facto** ("an open standard based on ES6 modules that is portable beyond Storybook" per Storybook; no standards body) |
| Format | ES modules `*.stories.(js|ts|jsx|tsx|…)`; required default export (meta: `component`, `title`, `decorators`…), named exports are stories (`args`, `play`, `render`, `parameters`). |
| Primary URLs | https://storybook.js.org/docs/api/csf · https://storybook.js.org/docs/api/csf/csf-next · https://github.com/ComponentDriven/csf |

### 9.2 Figma Variables vs DTCG
See 1.3.

### 9.3 "OpenUI"
- **Open UI** (open-ui.org) is real: a **W3C Community Group** whose purpose is "to allow web developers to style and extend built-in web UI components and controls" (HTML form controls, `<select>` etc.). It standardises browser behaviour/proposals, **not** a screen/layout file format. Primary: https://open-ui.org/ · https://github.com/openui/open-ui
- A separate generative-UI project also called "OpenUI" exists; **UNVERIFIED** in this session and not investigated.

---

## 10. Traceability

- **OSLC**: see 4.5. OSLC links across RM / CM / QM / Architecture Management; OSLC Core 3.0 is an OASIS Standard (26 August 2021). Server protocol, not a file format.
- **SPDX 3.0.1** (https://spdx.github.io/spdx-spec/v3.0.1/conformance/): conformance profiles listed are Core, Software, Security, Licensing, Dataset, AI, Build, Lite, Extension. **No requirements-trace profile.**
- **CycloneDX 1.7** (release 2025-10-21; JSON/XML/Protobuf; ECMA-424 listed on site): https://cyclonedx.org/specification/overview/. I found no requirements-trace profile there; **not exhaustively checked**.
- **Git commit trailers**: `git interpret-trailers` defines trailers as "a key-value pair with a colon as a separator" in the last paragraph of a commit message (e.g. `Signed-off-by: Alice <alice@example.com>`). Primary: https://git-scm.com/docs/git-interpret-trailers. **Conventional Commits 1.0.0** footers "follow a convention similar to git trailer format" and define `BREAKING CHANGE:`; no standard trailer key for requirement/story/feature ids — that part is a project convention. Primary: https://www.conventionalcommits.org/en/v1.0.0/.

---

## 11. Product docs and agent-facing files

### 11.1 Methods (not file formats)
| Item | Owner | Verified statement | Primary URL |
|---|---|---|---|
| Lean Canvas | Ash Maurya (Leanstack) | "1-page business model template created by Ash Maurya in 2010. It adapts Alexander Osterwalder's Business Model Canvas". Leanstack's page lists **12 blocks** (Customer Segments, Problem, Existing Alternatives, UVP, Solution, Key Metrics, Channels, Early Adopters, Cost Structure, Revenue Streams, Unfair Advantage, High-Level Concept) — the classic version has 9 blocks (not re-verified; page count of 12 is what the owner's site now shows). No file format. | https://leanstack.com/lean-canvas |
| Opportunity Solution Tree | Teresa Torres (Product Talk) | "Visualize your discovery"; a visual/diagram method (outcome → opportunities → solutions → experiments). No file format. | https://www.producttalk.org/opportunity-solution-tree/ |
| OKR | Popularised by John Doerr / whatmatters.com | "a collaborative goal-setting methodology" (Objectives and Key Results). No file format. | https://www.whatmatters.com/faqs/okr-meaning-definition-example |
| Diátaxis | Daniele Procida | "A systematic approach to technical documentation": four documentation types — tutorials, how-to guides, reference, explanation. Framework; no file format. | https://diataxis.fr/ |

**Closest standardised goals format found:** **ISO 17469-1:2015 StratML Part 1 (Strategy Markup Language)**, ISO/TC 171/SC 2, Edition 1, 2015-02, "last reviewed and confirmed in 2025", XML vocabulary + XSD for strategic-plan core elements (goals/objectives/performance indicators). Primary: https://www.iso.org/standard/59859.html. Adoption in OKR tooling: UNVERIFIED.

### 11.2 `llms.txt`
| Field | Value |
|---|---|
| Owner | Jeremy Howard (llmstxt.org); "A proposal to standardise on using an `/llms.txt` file" |
| Version / date | **v2** of the proposal; published 2024-09-03, modified 2026-08-10 |
| Stability | **draft / proposal** (no standards body) |
| Format | Markdown file named `llms.txt` at the site root `/llms.txt` or any subpath (`/docs/llms.txt`); order: optional BOM, an H1 with the name, then (per spec) blockquote summary and H2 file lists; markdown "rather than a classic structured format such as XML". |
| Primary URL | https://llmstxt.org/ |

### 11.3 `AGENTS.md`
| Field | Value |
|---|---|
| Owner | **Agentic AI Foundation under the Linux Foundation** ("AGENTS.md is now stewarded by…" per agents.md); repo `agentsmd/agents.md`, MIT |
| Version | None. "Are there required fields? No. AGENTS.md is just standard Markdown." |
| Stability | **de-facto** convention ("used by over 60k open-source projects", per the site) |
| Format | Plain Markdown, root-level `AGENTS.md`; nested files allowed (site: "the main OpenAI repo has 88 AGENTS.md files"). Supported by Codex, Jules, Cursor, Factory, Aider, goose, opencode, Zed, Warp, VS Code, Devin, Junie (site list). |
| Primary URL | https://agents.md/ · https://github.com/agentsmd/agents.md |

---

## 12. Frontmatter and metadata

### 12.1 YAML front matter
- **De-facto convention, no standard.** Jekyll docs: "Any file that contains a YAML front matter block will be processed by Jekyll as a special file. The front matter must be the first thing in the file and must take the form of valid YAML set between triple-dashed lines." Primary: https://jekyllrb.com/docs/front-matter/. Pandoc has "YAML metadata blocks" (https://pandoc.org/MANUAL.html).
- **CommonMark**: the spec (version **0.31.2, 2024-01-28**) contains **no front-matter section** — a text search of the spec for "front matter" / "YAML" found nothing. Front matter is an extension handled by tools before Markdown parsing. Primary: https://spec.commonmark.org/0.31.2/
- **YAML 1.2.2** (revision of **2021-10-01**) is the current YAML spec; the 1.2 line made YAML a strict superset of JSON, which is why a JSON Schema can describe a parsed YAML document. Primary: https://yaml.org/spec/1.2.2/. I found **no primary statement that "JSON Schema for front matter" is a standard**; it is a practice (editors/tools validate parsed YAML against JSON Schema). **UNVERIFIED** as standardised.

### 12.2 JSON Schema
See 6.2.

### 12.3 Schema.org `DefinedTerm`
| Field | Value |
|---|---|
| Owner | Schema.org community |
| Version / date | Schema.org release **v30.1, 2026-09-15** (GitHub release; the page being read was the "development version" at fetch time) |
| Status | Core vocabulary type `Thing > Intangible > DefinedTerm`; "A word, name, acronym, phrase, etc. with a formal definition." Properties include `termCode`, `inDefinedTermSet` (DefinedTermSet or URL), `description`. Exact graduation date of `DefinedTerm` into core: **UNVERIFIED**. |
| Format | Vocabulary, serialised as JSON-LD / RDFa / Microdata. Not a file convention for glossaries. |
| Primary URL | https://schema.org/DefinedTerm |

---

## 13. Story maps and personas

- **No standard file format found.** Story-mapping method: Jeff Patton (https://www.jpattonassociates.com/user-story-mapping/ — "A user story map arranges user stories into a useful model…"). Persona: method only.
- Web search for a persona / story-map interchange standard surfaced only community or vendor items (e.g. a "storymap" PyPI package, `INTENT.md` format, StratML), none from a standards body. `StratML` (11.1) covers strategic goals, not personas or story maps.

## 14. Brand guidelines and tone of voice

- **No standards-body specification found.** Visual brand values can be carried by DTCG tokens (1.1), but DTCG's scope is design tokens; tone of voice/copy has no standard.
- Emerging **vendor/community JSON formats** (none from a standards body; all young):
  | Format | Owner | Version / status as read | Primary URL |
  |---|---|---|---|
  | BrandSpec | Whyso Ltd | "Open Standard BETA", **Brand Spec v0.1.0**; JSON with tokens, strategy, voice, assets, purpose | https://brandspec.org/ |
  | `brand.json` (AdCP Brand protocol) | Ad Context Protocol / AgenticAdvertising.org | Part of **AdCP 3.2** (docs: "generally available"); `$schema` `https://adcontextprotocol.org/schemas/3.2.3/brand.json`; carries logos, colors, tone, restrictions | https://docs.adcontextprotocol.org/docs/brand-protocol |
  | Brand Context Protocol (BCP) | BCP (brandcontextprotocol.com) | JSON, JSON Schema draft-07; sections identity, visual, verbal (voice/tone/vocabulary), positioning, governance | https://www.brandcontextprotocol.com/documentation |
  | `.grain` | Grain (grainhq.app) | **v1.0**, media type `application/vnd.grain+json`; voice, messaging, visual identity | https://grainhq.app/format/ |
  | MRBS (Machine-Readable Brand Specification) | BrandCodex | **v1.0.0, Apache-2.0**; `brand.manifest.json` with `mrbs_version`; directory structure | https://brandcodex.org/specification |
  Governance, adoption and long-term stewardship of each: **UNVERIFIED**.

---

## "No standard exists" list

| Item | Finding |
|---|---|
| Story maps (13) | No standard file format. Method only (Patton). |
| Personas (13) | No standard file format. |
| Brand guidelines / tone of voice (14) | No standards-body spec; only young vendor/community JSON formats (BrandSpec v0.1.0, AdCP `brand.json`, BCP, `.grain`, MRBS). |
| Lean Canvas, OST, OKR, Diátaxis (11) | Methods / frameworks; no file formats. (Only loosely related standard: ISO 17469-1 StratML for strategic plans.) |
| C4 model (3.1) | No file format and no version; notation-independent. Structurizr DSL is the de-facto text format. |
| EARS (4.1) | Sentence patterns only; no file format or version. |
| Requirements trace in SPDX / CycloneDX (10) | No requirements-trace profile found in SPDX 3.0.1; none found in CycloneDX 1.7 (not exhaustively checked). |
| Commit trailer key for feature/requirement id (10) | `git interpret-trailers` is a mechanism only; no standard key. |
| Front matter (12.1) | Not in CommonMark 0.31.2; Jekyll/Pandoc convention. |
| JSON Schema for YAML front matter (12.1) | Practice, not a published standard. |
| Glossary file format (8) | SKOS (RDF) is the W3C standard vocabulary; no standard *Markdown* glossary file. arc42 §12 and Schema.org `DefinedTerm` are structure/vocabulary, not file formats. |
| Screens / layout file (9) | No standard. CSF is a component-example format; Open UI standardises browser controls. |

## Items marked UNVERIFIED (summary)
1. Figma native DTCG import/export (only a third-party blog).
2. ReqIF file extension (`.reqif`/`.reqifz`) — not found in the OMG spec text.
3. CTRF canonical file name.
4. TAP v14 publication date; `.tap` extension.
5. arc42 canonical file name.
6. SARIF consumers other than GitHub code scanning, and SARIF use by non-code linters — not checked.
7. Schema.org `DefinedTerm` core-graduation date.
8. Governance/adoption of the brand JSON formats; second "OpenUI" project.
9. OpenAPI default file names (`openapi.json`/`openapi.yaml`) and 3.1 ⇄ JSON Schema 2020-12 alignment (not re-read here).
10. Whether `.mmd` is a Mermaid convention; CML file extension relied on owner's examples repo rather than a doc statement.
