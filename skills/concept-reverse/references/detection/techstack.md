# Detection — the tech stack

Read, in this order, and stop reading a dimension once a manifest declares it: the root
manifest (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `pom.xml`,
`composer.json`, `Gemfile`) and its lock file; the framework config files; the Dockerfile
and `docker-compose.yml`; the CI workflow files; and `.env.example`.

A dependency in `dependencies` is a stronger signal than the same name in
`devDependencies`, which is a stronger signal than a mention in a config comment.

| dimension | where it is declared |
|---|---|
| `platform` | Dockerfile base image, CI runner image, deployment config |
| `frontend` | `nuxt`, `next`, `remix`, `astro`, `@sveltejs/kit`, or `vite` plus `react` / `vue` |
| `ui_library` | `@nuxt/ui`, `shadcn-ui`, `@radix-ui/*`, `primevue`, `vuetify`, `@mantine/core`, `@chakra-ui/react`, `tailwindcss` |
| `backend` | `express`, `fastify`, `hono`, `koa`, `@nestjs/core`, `django`, `fastapi`, `flask`, `rails`, `laravel` |
| `database` | `pg`, `mysql2`, `sqlite3`, `mongodb` — and the ORM below usually names it too |
| `orm` | `@prisma/client`, `drizzle-orm`, `typeorm`, `mongoose`, `sequelize`, `sqlalchemy` |
| `auth` | `next-auth`, `lucia`, `passport`, `@auth0/nextjs-auth0`, `better-auth`, `@supabase/supabase-js`, a Keycloak client |
| `hosting` | `vercel.json`, `netlify.toml`, `railway.json`, `fly.toml`, or the deploy step in CI |
| `package_manager` | `bun.lockb` → bun · `pnpm-lock.yaml` → pnpm · `yarn.lock` → yarn · `package-lock.json` → npm |

## Grading

`extracted` when a manifest or config names it. `inferred` when only an import or a
directory convention implies it — a `server/api/` tree with no server framework in the
manifest is a framework-provided server, which is worth saying rather than guessing at.
`needs_review` when the dimension has no signal at all; an empty field with a grade is more
useful than a plausible default, because a default gets built on.

## What belongs in the body rather than the frontmatter

Version constraints that will bite (a major pinned below current, a peer-dependency
conflict), combinations that are unusual enough to be deliberate (two ORMs, a second
frontend framework in one package), and anything the CI does that the manifests do not
explain. These are what a person reading the stack file needs and what no field holds.
