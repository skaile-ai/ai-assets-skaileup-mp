# flows/

One directory per flow: `flows/<id>/<id>.flow.yaml`, with `id: <id>` inside. The loader
keeps a flow only if it has `id`, `nodes` and `edges`; the top-level `requires:` block is
the flow's own install manifest and drives transitive install.

Every skill node (or its group container) declares `data.phase` —
`conceptualization` | `implementation` | `review`. `-mp` does not rely on the name-prefix
fallback in forge-concept's `phaseForNode`, which is why the domain names were free to
change.

Machine form of the contract: [`../contracts/flow.schema.json`](../contracts/flow.schema.json).

**Empty on purpose.** The flow set is being decided; flows are authored once the domains
they order exist.
