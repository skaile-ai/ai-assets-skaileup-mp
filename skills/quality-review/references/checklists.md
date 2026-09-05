# Security and accessibility checks

The two axes `code-review` does not carry. Its Standards axis reads the diff against the
repo's documented conventions and the Fowler smell baseline, and its Spec axis reads it
against the feature spec — neither looks for an unauthorised route or an unlabelled input.

Walk each list against the review scope (the `commits[]` diffs plus the current contents of
`source_files[]`). A hit is a finding only with a file, a line and the specific change that
clears it; "consider reviewing auth here" is a note to nobody.

## Security and data integrity

Scope: every route, handler, query and form the diff touches.

- **Injection.** User input reaching a query, a shell command or a template without
  parameterisation or escaping.
- **Authorisation.** Every route the diff adds or changes, checked against the feature's
  `permissions:` table. A route with no check is a finding even when the UI never links to
  it — the UI is not the boundary.
- **Row-level scoping.** A query that filters by id but not by owner, tenant or workspace
  returns another user's data the moment an id is guessed.
- **Secrets.** Keys, tokens or connection strings in source, in fixtures, or in a committed
  `.env`.
- **Input validation at the boundary.** Types accepted from the network validated where they
  arrive, not three calls in.
- **XSS and unsafe deserialisation.** Raw HTML interpolation, `dangerouslySetInnerHTML`,
  `eval`, and object deserialisation from untrusted payloads.
- **CSRF.** State-changing requests that rely on a cookie with no token or same-site policy.

## Accessibility

Scope: every screen the diff renders or changes.

- **States.** Loading, error and empty each render something a user can read. A screen that
  shows nothing while it loads is indistinguishable from a broken one.
- **Keyboard.** Every interactive element reachable and operable without a mouse, in an order
  that matches the visual one.
- **Focus.** A visible focus indicator, and focus moved deliberately when a dialog opens or
  a route changes.
- **Labels.** Every input, button and icon-only control carries an accessible name.
- **Semantics.** Headings, landmarks and roles used for what they mean, so the structure
  survives without the styling.
- **Contrast.** Text and interactive elements against their real background, at WCAG AA.
