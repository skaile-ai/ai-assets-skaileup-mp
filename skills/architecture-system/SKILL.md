---
name: architecture-system
description: "Use when the stack is chosen and the features need more than the stack ships with — records the custom modules, protocols and external integrations this project adds, and stops there. Triggers on 'architecture', 'system design', 'do we need a websocket', 'which modules', 'how does this talk to Stripe'."
version: "0.1.0"
metadata:
  artifacts:
    requires:
      - { id: brief }
      - { id: features }
      - { id: techstack }
  prerequisites:
    files:
      - { path: "_concept/brief.md", gate: hard }
      - { path: "_concept/05_features", gate: hard, min_entries: 1 }
      - { path: "_concept/10_blueprint/techstack.md", gate: hard }
      - { path: "_concept/06_behaviors", gate: soft, min_entries: 1 }
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
`contracts/artifact_frontmatter.md § blueprint/architecture.md`.

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
3. **Ask only what the features left open**, one question per message per
   `contracts/agent_patterns.md`: background or scheduled work, live updates, external
   services, streaming or instant communication, and any non-standard handling of data. A
   question the feature specs already answer spends the round you needed for a real one.
4. **Write each addition with the thing that makes it buildable.** A custom module names its
   purpose, what it depends on, and the feature that asked for it. A protocol names its
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
   `custom_services`, `custom_modules`, `protocols`, `external_integrations`, `last_updated` —
   and one body section per addition, in that order. Prose and diagrams, no code: this file is
   read by `architecture-datamodel` for the entities a module implies, by `build-plan` for the
   work a slice has to cross, and by `build-implement` for what to build against. An empty
   frontmatter list is a real result — say in the body that the stack covers this project as
   it stands, rather than inflating four sections to look complete.
7. **Approve it in plain language.** What the app's structure lets it do, which features get
   live updates and over what, what the custom logic is *for* in business terms, and which
   outside services it will depend on. The counts — apps, modules, protocols, integrations —
   go underneath for whoever wants them. Approve, or name what to change.

**Done when** `10_blueprint/architecture.md` exists, every entry in its frontmatter lists is
described in the body with its dependencies and its error behaviour, and the user has
approved it.
