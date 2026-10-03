# Agent Patterns

The behaviours every skill shares at run time, read at the step that cites them rather than
restated in each body. Where a thing lives is `contracts/concept_structure.md`'s job; how a
skill writes back into an upstream file is `contracts/feedback_loop.md`'s.

## Pattern: Read the tree first

Before any output, check the `metadata.prerequisites.files` gates and stop, naming the missing
path, if one fails. Then read every required input, and the optional ones where present. The
`_concept/` artifacts outrank the conversation: where they disagree, the difference is a question.

## Pattern: Steps are the todo list

On entry, the skill's numbered steps become the first todo items, verbatim and in order, before
any task-specific item. A step that does not apply stays listed with `skip: <reason>` rather
than being dropped. The **Done when** line is the last item.

Where the harness has no todo tool, the first message lists the steps the same way and each
later message names the step it is on — the point is that the sequence survives, not the tool.

## Pattern: Questions Are Standalone Messages

Send a question to the user as its own message, one question per message; a status update or
explanation goes in the message before it. A technical term is explained in parentheses.

**Wrong:**
> I've analyzed the brief and identified 6 feature groups covering auth, dashboard,
> settings, notifications, billing, and reporting. I've also cross-referenced with
> the competitor analysis. Now I need one thing from you — do you want social login
> or just email+password?

**Right:**
> _(first message — status update, no question)_
> I've analyzed the brief and identified 6 feature groups covering auth, dashboard,
> settings, notifications, billing, and reporting.

> _(second message — question only)_
> Do you want social login or just email+password?

**Why:** a question at the end of a long message gets overlooked; alone, it is plain and easy to answer.

## Pattern: Answers persist

`concept-onboard` keeps every answer a dialog collected in
`_concept/02_grounding/onboarding/answers.json`, so a later skill can skip a question the user
has already answered. The host writes its own per-skill dialog file at a path it hardcodes; no
skill in this collection names that path.

1. Before asking anything, read `answers.json` if it exists, and what the host's dialog handed in.
2. Keys are the `id` values of the `inputs_optional` fields the dialog rendered.
3. Use a saved value as the default, or skip the question when it is already answered.
4. New answers merge into the file rather than replacing it.
5. An existing value changes only after the user confirms the change.

## Pattern: Standalone Mode

A skill runs without a flow as well as inside one:
1. Read the skill's own frontmatter gates under `metadata.prerequisites`.
2. Check each required path exists in `_concept/`.
3. If all pass: read the inputs, run the workflow, report per Completion Summary, suggest next steps.
4. If any fail: name the missing prerequisites and tell the user which skill to run first.

Next steps come from the edges leaving this skill's node in the relevant flow file, or from
what the skill knows it unblocks.

## Pattern: Next-Step Suggestion

After a skill completes, standalone or inside a flow:
1. Identify which skills now have all their required paths satisfied.
2. Present them as suggestions — the successors are the edges leaving this skill's node in
   the active flow.
3. If none is unblocked, show what is still missing and which skill would produce it.
4. When a flow is running, the host handles next-step dispatch itself.

## Pattern: Completion Summary

After producing artifacts, present the files created or modified, each with a brief
description, the key decisions made and the cross-references established; then the next steps.

Every claim in the summary says in the same sentence how it is known — **measured** (seen in a
file, a command's output, the running app) or **inferred** (follows from something measured,
and names it). A claim that is neither, such as a prediction or an unseen cause, is a
**guess** and goes under its own `Unverified:` line, apart from the results. A check the agent
could have run is run, not handed to the user.

## Pattern: Subagent Dispatch

When a flow node has `"subagent": true`:
1. The dispatching skill creates a fresh agent context.
2. That context holds only the skill's SKILL.md, the `contracts/` it cites and the input `_concept/` folders.
3. A subagent gets the task text verbatim and nothing of the conversation — paste the full
   task into its prompt rather than pointing it at the plan file.
4. The subagent runs to completion and ends with one of four statuses (below).
5. The dispatching skill acts on the status and collects the output artifacts. The block:

```
STATUS: DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED

[If DONE_WITH_CONCERNS]  Concerns: <trade-offs, deviations, debt incurred>
[If NEEDS_CONTEXT]       Missing:  <what is absent>
                         Question: <single specific question for the user or the dispatching skill>
[If BLOCKED]             Reason:   <what cannot be resolved>
                         Route:    context | escalate-model | decompose
```

| Status | Meaning | Dispatching skill's action |
|---|---|---|
| `DONE` | All requirements met, tests pass | Accept output, advance flow |
| `DONE_WITH_CONCERNS` | Implemented but with trade-offs or notes | Accept, log concerns in `decisions.md`, advance |
| `NEEDS_CONTEXT` | Missing information or ambiguous requirement | Put the question to the user; resume when answered |
| `BLOCKED` | Cannot proceed — see route | Follow the route below |

| Route | When to use | Dispatching skill's response |
|---|---|---|
| `context` | A specific question can unblock the task | Put the question to the user; re-dispatch with the answer |
| `escalate-model` | Task exceeded model capability | Note in `decisions.md`; re-dispatch on a higher-tier model |
| `decompose` | Task is too large to execute atomically | Break into smaller tasks; re-dispatch each |

A partial output with no status leaves the dispatching skill guessing; a code makes it act.
