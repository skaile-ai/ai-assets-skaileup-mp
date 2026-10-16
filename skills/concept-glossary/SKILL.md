---
name: concept-glossary
description: "Use when the brief is approved and the product's words are not pinned yet, or when a later step meets a concept that has no term. Grills the user on the domain vocabulary and writes the glossary every journey, feature, screen, model and test then names things from. Triggers on 'pin the vocabulary', 'what do we call this', 'write the glossary', 'we use two words for the same thing'."
version: "0.1.0"
metadata:
  requires:
    - contract:@skaile-ai/shared-contracts
  artifacts:
    requires:
      - { id: scope }
      - { id: brief }
    produces:
      - { id: glossary, path: "_concept/glossary.md" }
  prerequisites:
    files:
      - { path: "_concept/brief.md", gate: hard }
      - { path: "_concept/01_meta/scope.yaml", gate: soft }
---

# concept-glossary

The one writer of `_concept/glossary.md`: the project's ubiquitous language, term to
definition, with the words each term beat listed under `_Avoid_`. It runs right after the
brief because everything after it names things — journeys, features, screens, entities,
tests — and each of them coins its own words when no glossary exists to read. It writes
words and nothing else: no fields, no types, no paths.

Format, rules and the opinionated-term stance are
`contracts/domain_model.md § Glossary format`'s; the path is
`contracts/concept_structure.md`'s and the frontmatter is
`contracts/artifact_frontmatter.md`'s. Interview conduct is
`contracts/agent_patterns.md § Questions Are Standalone Messages` and
`contracts/agent_patterns.md § Answers persist`.

## Steps

1. **Read the ground.** `brief.md` — pitch, audience, problem, hero flow and its
   `## Comparables` — and `02_grounding/research/{domain,competitors,audiences}.md` where
   research ran, since that is where the field's own words are. Where a repository was reverse
   engineered, `02_grounding/findings/` carries names the code already uses, each with its
   grade. `02_grounding/onboarding/answers.json` may already hold terms the user gave. If
   `glossary.md` exists this is a re-entry: go to step 6.
2. **List the candidates.** Every noun the product keeps, every role of a person, every
   event or state a user would name aloud, drawn from those files and marked with where it
   came from. Only terms unique to this domain belong; a general programming word (timeout,
   cache, retry) stays out however heavily the product uses it. A name taken from code
   findings goes in as a candidate, never as settled, because code names drift from what the
   people say.
3. **Grill the words.** Take the candidates one at a time, as a message of its own, with
   your recommended term and a one-line reason. Two words for one concept: ask which wins
   and list the loser under `_Avoid_`. One word for two concepts: split it and name both.
   An invented term is indistinguishable from the user's by the time a spec quotes it, so a
   word that came from neither the user nor a cited source goes in only on a yes. The depth
   follows `01_meta/scope.yaml`: `appbuilder-mvp` settles the ten or so terms the hero flow
   needs in one pass; `appbuilder-standard`, `skaileup-concept-only` and
   `skaileup-concept-reverse` work the list until the user stops correcting.
4. **Write `glossary.md`.** Frontmatter per the contract (`last_updated`, no `approved:`
   yet), a sentence on what the domain is, then the entries in `domain_model.md`'s format,
   grouped under a cluster heading where clusters are natural. Each definition says what the
   thing *is* in one or two sentences, and the `_Avoid_` line is the anti-drift mechanism, so
   it lists every word the sources used for the same concept.
5. **Show the glossary and wait for a yes in words.** Apply corrections, show it again, ask
   again. On the yes, write `approved: <date>` into the frontmatter in the same write; an
   edit after that clears the key until the user says yes again.
6. **Re-enter for a missing term.** A later step — `spec-feature`, `architecture-datamodel`,
   `experience-journeys` — never appends to this file. When it meets a concept with no term
   it stops, names the concept and hands back, and the flow re-enters this node with that
   concept as the input. Grill only that term, add it in place under the right cluster, and
   leave every existing entry alone unless the user asks to change it. A changed existing
   definition ripples into the artifacts that quote it, so say which ones and let the user
   decide before the edit. Stamp `approved:` again on the yes and return to the step that
   handed back.

**Done when** `glossary.md` is on disk, every entry has a definition and an `_Avoid_` line
(or says there is none), no entry carries implementation detail, and the user has said yes,
which `approved:` in the frontmatter records.
