# Discipline pack — Backend

Load when the repo shows a server framework, route/controller layers, database or migration
folders, a Dockerfile, or an API schema. Adds server-side concerns to each phase. Framework
is detected, never assumed.

## In DEFINE (spec)
- Nail the **contract**: endpoints/messages, request/response shapes, status/error semantics,
  idempotency, versioning. The contract is the hardest thing to change later (Hyrum's Law —
  every observable behavior becomes something a caller depends on).
- Fix ONE **error envelope** for the whole API — e.g. `{code, message, details}` — with a
  consistent HTTP status mapping (400 validation · 401 unauthenticated · 403 forbidden ·
  404 missing · 409 conflict · 422 semantic · 500 unexpected), and **every list endpoint is
  paginated from day one** (retrofitting pagination is a breaking change). Treat third-party
  API responses as untrusted input: schema-validate before they touch logic or rendering.
- Nail the **data model**: entities, relationships, ownership, invariants, and what must be
  transactional.

## In BUILD (construct)
- **Validate at the boundary** — never trust input; validate and normalize at the edge, keep
  the core clean.
- Design interfaces to be **hard to misuse**: consistent error shapes, explicit nullability,
  additive-over-breaking evolution.
- Schema changes follow **expand → backfill → contract** — never rename a column in place
  under live traffic.
- Keep I/O at the edges; keep business logic pure and unit-testable.
- **Keep the API spec in sync** — when a route or contract changes, update the OpenAPI/Swagger
  doc or GraphQL schema in the same change; if the API has no spec, suggest adding one.

## In VERIFY
- Exercise the real endpoints/handlers with real input, including the error and auth paths —
  not just the happy path units.
- Test transactional behavior and failure/rollback.

## In REVIEW (inspect) — surface-specific security & perf
- **Security:** authn vs. authz on every route, injection (SQL/NoSQL/command), unsafe
  deserialization, secrets in code/logs, over-broad permissions, rate-limiting on public
  surfaces, SSRF on outbound calls.
- **Performance:** N+1 queries, missing indexes, unbounded result sets, work that should be
  batched or paginated, chatty cross-service calls, missing timeouts on external calls.

## In SHIP (release)
- Backward-compatible migrations; roll out schema and code in the safe order.
- Health/readiness signals and an alert on the symptom users would feel.
