# Design red flags

Ask each question of every candidate custom module, protocol and external integration
before it goes into `10_blueprint/architecture.md`. A yes is a reason to reshape the
addition, or to drop it, before anyone builds against it.

## The four questions

1. **Shallow module** — is the interface about as big as what it hides? A module whose
   callers have to know as much as its body does buys a name and nothing else.
   *Fix:* merge it into its caller, or widen what it hides until the interface is small
   next to it.
2. **Information leakage** — is the same representation decision known in two places — a
   message format, a file layout, a retry policy, a provider's ID scheme? A change to it then
   has to land in both, in step.
   *Fix:* give the decision one owner and let everyone else go through that owner.
3. **Temporal decomposition** — is the split drawn by *when* things run (read, then
   transform, then write) rather than by *what* each piece hides? Steps in a sequence tend to
   share the knowledge the sequence needs, which is leakage across the step boundary.
   *Fix:* draw the boundary around a piece of knowledge, and let one module run every step
   that needs it.
4. **Pass-through** — does a layer forward calls with the same shape it received, adding no
   decision, translation or protection of its own?
   *Fix:* remove the layer, or give it the job that justified it — usually the seam to an
   outside dependency, where the in-memory stand-in lives.

## Design it twice

When a module admits two plausible interfaces, write both down as signatures — the
operations, their inputs and what they return — before choosing. Keep the deeper one: the
one whose callers need to know less to use it. The first interface that comes to mind is
rarely the deeper one, and comparing two on paper costs minutes where rebuilding the
seam later costs a slice.

---

Sources: pstack `architect/references/design-red-flags.md`; Pocock
`codebase-design/DESIGN-IT-TWICE.md`. Both draw on Ousterhout, *A Philosophy of Software
Design*.
