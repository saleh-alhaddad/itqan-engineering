# Discipline pack — Database

Load when the repo shows a database: an ORM/query builder, migration folders, SQL files, a
schema, or a DB driver in the manifest. Adds data-layer concerns. Engine (Postgres/MySQL/
SQLite/Mongo/…) is detected, never assumed.

## In DEFINE (spec / data-model design)
- Model the **entities, relationships, ownership, and invariants**; state what must be
  transactional and what may be eventually consistent. The schema is a contract — hard to
  change later (Hyrum's Law), so design it deliberately.
- Capture retention, PII, and access constraints up front.

## In BUILD (construct)
- **Migrations are expand → backfill → contract.** Never rename/drop a column in place under
  live traffic: add the new, backfill, switch reads/writes, then remove the old — each step
  shippable and reversible.
- **Every migration has a tested down/rollback**, not just up.
- **Lock safety — a correct migration can still take prod down.** Use the engine's online
  DDL (e.g. create indexes concurrently); set a `lock_timeout` and `statement_timeout` on
  every migration; never in-place `ALTER` a hot table; run backfills **chunked and
  throttled**, watching replication lag between chunks.
- Enforce integrity in the schema (constraints, FKs, NOT NULL, unique) — don't rely only on
  app code. Add the indexes the query patterns need; don't over-index writes.
- Keep queries parameterized (never string-concatenated) and I/O at the edges.

## In VERIFY
- Run the migration **up and down** against a real (test) database; confirm data survives.
  **Record the migration's runtime and the locks it took** — a pass that held an exclusive
  lock for minutes is a finding, not a green.
- Exercise the queries with **prod-shaped, anonymized data volume** (state the source), not
  a 3-row fixture.

## In REVIEW (inspect)
- **Performance:** N+1 queries, missing indexes, unbounded result sets (no pagination), full
  table scans, chatty per-row calls, missing query timeouts.
- **Correctness/safety:** unparameterized SQL (injection), missing transaction boundaries on
  multi-write operations, race conditions on read-modify-write, non-reversible migrations.
- **Data loss:** destructive migrations without a backup/rollback path.

## In SHIP (release)
- Backward-compatible migration order (expand before deploy, contract after); the **contract
  step waits until the old code is fully drained**, never same-deploy; a rollback plan for
  the schema, not just the code; backup/PITR **verified by an actual restore check**, not a
  checkbox, before any destructive change.
