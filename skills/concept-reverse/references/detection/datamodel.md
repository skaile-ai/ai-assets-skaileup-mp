# Detection — the data model

Eight sources, in priority order. The first one present is authoritative; the rest are read
only to fill gaps it leaves, and a disagreement between two of them is a finding worth
reporting rather than silently resolving.

1. **Prisma** — `prisma/schema.prisma`
2. **Drizzle** — `db/schema.ts`, `src/db/*.ts`
3. **TypeORM** — decorated classes under `src/entities/`, `src/models/`
4. **Mongoose** — `models/*.ts`, `src/models/*.ts` with `new Schema({…})`
5. **SQL migrations** — `migrations/`, `db/migrations/`; take the most recent migration per
   table, since earlier ones describe columns that no longer exist
6. **SQLAlchemy** — `models.py`, `app/models/*.py`
7. **TypeScript interfaces** — `src/types/`, `shared/types/`, only when no ORM is present
8. **GraphQL schema** — `schema.graphql`, `src/schema.ts`

## What to record per entity

Field names and types, relations (foreign keys, `@relation`, `hasMany` / `belongsTo`),
unique constraints, nullability, defaults, and enum values. Record the file and line the
entity came from — the evidence is what makes the model checkable later.

## Type mapping

Framework types are translated to `contracts/semantic_types.md` types, never carried over
raw; a stack-specific type in the semantic layer is a translation the model then cannot be
retargeted from.

| framework | semantic |
|---|---|
| `String`, `varchar`, `text` | `string` — `text` / `@db.Text` on a long field is `richtext` |
| `Int`, `Float`, `Decimal`, `numeric` | `number` |
| `Boolean`, `bool` | `boolean` |
| `DateTime`, `timestamp`, `date` | `datetime` |
| `Json`, `jsonb` | `json` |
| an `@id` / primary key column | `uuid` |
| a relation field or foreign key | `relation` |
| a column holding a path or URL to an upload | `image` or `file` |
| an enum type or a checked string column | `enum`, with its values |

## Seed evidence

Fixture, factory and seed files in the repository are real example data for this schema.
Record where they are and what they cover; they are the `populated` scenario the seed
scenarios are built from, and they beat invented rows because they already satisfy the
constraints.
