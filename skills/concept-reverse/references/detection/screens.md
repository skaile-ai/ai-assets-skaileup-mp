# Detection — routes and screens

Two passes. The first finds the routes; the second reads what is behind each one.

## Pass 1 — route discovery

In priority order:

1. **Router definitions** — `src/router/`, `app/router.ts`, Next.js `app/**/page.tsx` or
   `pages/**/*.tsx`, Nuxt `pages/**/*.vue`, SvelteKit `src/routes/**/+page.svelte`,
   Rails `config/routes.rb`, Django `urls.py`, FastAPI router registrations
2. **API route handlers** — `server/api/`, `api/`, `routes/`, `controllers/`, and
   `app.get(…)` / `router.post(…)` call sites
3. **Navigation components** — sidebar, navbar and breadcrumb components, which name the
   destinations a user is actually offered and so distinguish a real screen from a route
   nothing links to

File-system routers give the route from the path; explicit routers give it from the
registration. Where neither exists, routes recovered from component names are `inferred`,
and the report says so.

## Pass 2 — what is behind each route

| framework | where the page component lives |
|---|---|
| Nuxt | `pages/**/*.vue`, with `layouts/` for the frame |
| Next.js | `app/**/page.tsx`, `pages/**/*.tsx` |
| Vue Router | `views/`, `src/pages/` |
| React Router | `src/routes/`, `src/pages/` |
| SvelteKit | `src/routes/**/+page.svelte` |
| Django | `templates/**/*.html` |
| Rails | `app/views/**/*.erb` |

For each, record: the layout or template it wraps in; the entities it fetches or submits;
the interactions a user has (buttons, forms, links, and where each leads); the states the
component renders conditionally (loading, empty, error, populated); and the guard or
middleware protecting it, which is the evidence for who is allowed there.

## What this produces

`02_grounding/findings/routes.md` and `screens.md` — evidence, with the defining file cited
for every entry. Feature specs and screen specs are written from this by the skills that own
those trees. Keep the record in user terms where you can: the route is the citation, and what
the user can do there is the finding.
