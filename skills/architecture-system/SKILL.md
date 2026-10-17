---
name: architecture-system
description: "Use when the stack is chosen and the features need more than the stack ships with — records the custom modules, protocols and external integrations this project adds, and stops there. Triggers on 'architecture', 'system design', 'do we need a websocket', 'which modules', 'how does this talk to Stripe'."
version: "0.1.0"
metadata:
  requires:
    - contract:@skaile-ai/shared-contracts
  artifacts:
    requires:
      - { id: brief }
      - { id: features }
      - { id: techstack }
    produces:
      - { id: architecture, path: "_concept/10_blueprint/architecture.md" }
  prerequisites:
    files:
      - { path: "_concept/brief.md", gate: hard }
      - { path: "_concept/05_features", gate: hard, min_entries: 1 }
      - { path: "_concept/10_blueprint/techstack.md", gate: hard }
      - { path: "_concept/06_behaviors", gate: soft, min_entries: 1 }
      - { path: "_concept/10_blueprint/datamodel", gate: soft }
---

# architecture-system

Writes `10_blueprint/architecture.md`: the apps, custom modules, communication protocols and
external integrations **this project adds beyond its template**, and nothing else. What the
chosen stack already provides is written down once, in
`templates/<tech_stack_skill>/TEMPLATE.md`, and read there by everyone who needs it —
restating it here produces a second copy that says the same thing until the day it does not.
The artifact is optional by design: a project whose features need nothing beyond its stack
gets a short document saying exactly that, which is the answer `build-plan` needs.

Paths are `contracts/concept_structure.md`'s; the frontmatter is
`contracts/artifact_frontmatter.md § 10_blueprint/architecture.md`.

## Steps

1. **Read the stack first, so what you write is the delta.** `10_blueprint/techstack.md`
   names `tech_stack_skill`; that template's `## Identity` and `## Scaffold Recipe` say what
   the project already gets — server runtime, ORM, auth provider, directory structure. Then
   read `brief.md` and every feature under `05_features/`.
2. **Read the features for architecture signals.** Real-time behaviour (chat, live updates,
   collaborative editing), background work (scheduling, long jobs, file processing), outside
   systems (payments, mail, third-party APIs), and data flows the stack has no shape for
   (event logs, multi-step workflows, pipelines). Where `06_behaviors/<featureset>.md` exists,
   its state tables sharpen all three: a transition on a timer is background work, one that
   two actors race for is real-time, and one that waits on an outside system names an adapter.
3. **Ask only what the features left open**, per
   `contracts/agent_patterns.md § Questions Are Standalone Messages`: background or
   scheduled work, live updates, external services, streaming or instant communication, and
   any non-standard handling of data. A question the feature specs already answer spends the
   round you needed for a real one.
4. **Write each addition with the thing that makes it buildable.** Screen each addition
   against `references/design-red-flags.md` first; a module that fails the shallow-module
   question is usually a feature's helper, not an architecture entry. A custom module names
   its purpose, what it depends on, and the feature that asked for it. A protocol names its
   endpoints, its message types, its connection lifecycle and what happens on error. An
   external integration names the API or SDK, what data crosses the boundary, the retry and
   fallback behaviour, and where the credentials live. Those last two are the ones that get
   invented at implementation time when they are missing here, and invented differently in
   every slice that touches the integration.
5. **Give every outside dependency a seam.** A module the app does not own — a payment
   gateway, a mail sender, a model provider — is declared as an interface with a real
   implementation and an in-memory stand-in behind it, chosen by configuration. That is what
   lets a slice be built and tested before anyone has credentials, and it is the one shape
   worth fixing here rather than per slice.
6. **Write `10_blueprint/architecture.md`.** Frontmatter per the contract — `apps`,
   `custom_services`, `custom_modules`, `protocols`, `external_integrations`, `last_updated`.
   The body follows the [C4 model](https://c4model.com/)'s levels, in this order, each
   section holding only what it says:
   - `## System context` — who uses the system and which outside systems it talks to. Its
     `### External Integrations` subsection is the only place in `_concept/` that records
     third-party services — payments, mail and SMS, file storage, analytics, error tracking,
     auth providers beyond the template's own — and `techstack.md` carries none of them.
   - `## Containers` — the `apps`, `custom_services` and `protocols`: what runs separately
     and how the parts talk.
   - `## Components` — the `custom_modules`, written only where a container's insides
     matter; leave the section out when no module earns one.
   - `## Deployment` — where each container runs, as far as the stack and the features fix it.
   - `## Risks and technical debt` — what is known to be weak or deferred, each with the
     feature or integration it touches.

   Prose and diagrams, no code: this file is read by `architecture-datamodel` for the entities
   a module implies, by `build-plan` for the work a slice has to cross, and by
   `build-implement` for what to build against. An empty frontmatter list is a real result —
   say in the body that the stack covers this project as it stands, rather than inflating
   sections to look complete.
7. **Write the API and event contracts where the project has them.** An HTTP API served to
   clients other than the project's own UI — always for project type `api-service` — gets
   `10_blueprint/openapi.yaml`, an OpenAPI 3.2.0 document with one path per endpoint the
   `protocols` and the features name. A project that publishes or consumes messages on a
   channel — a broker, a websocket, a webhook stream — gets `10_blueprint/asyncapi.yaml`, an
   AsyncAPI 3.1.0 document with its channels, messages and the operations that send or
   receive them. A project with neither writes neither file; the stack already covers it, and
   the body of `architecture.md` says so. Request, response and message payload schemas
   name entities from `10_blueprint/datamodel/model.json`, read and never coined; where that
   file does not exist, they come from `glossary.md`, and a payload concept with neither
   stops the step: name it and hand back to `concept-glossary`. Each error response and each
   failed message names what the caller sees, which is the behaviour step 4 wrote in prose.
8. **Approve it in plain language.** What the app's structure lets it do, which features get
   live updates and over what, what the custom logic is *for* in business terms, and which
   outside services it will depend on; where step 7 wrote a contract, which endpoints or
   channels outside parties can rely on. The counts — apps, modules, protocols, integrations,
   endpoints, channels — go underneath for whoever wants them. Approve, or name what to
   change. The contracts are approved with `architecture.md`, not separately.

## Re-entry

`quality-e2e` reads `openapi.yaml`; `build-scaffold` and `build-implement` read both files.
All three gate on them softly. A reader that needs an endpoint, a channel or a payload
changed hands back to this skill with the change named; steps 6–8 re-run for the affected
parts, and the reader does not edit `openapi.yaml` or `asyncapi.yaml` itself.

## What sits in `references/`

`design-red-flags.md` — four questions to ask of each candidate module, protocol and
integration before step 4 writes it down, and the rule for a module with two plausible
interfaces: write both, keep the deeper one.

**Done when** `10_blueprint/architecture.md` exists, every entry in its frontmatter lists is
described in the body with its dependencies and its error behaviour, `openapi.yaml` and
`asyncapi.yaml` exist exactly where step 7 says they are due, and the user has approved
all of them together.
