---
name: harden
description: >-
  Security audit: threat model, OWASP Top 10 (and LLM Top 10), abuse cases, dependency and
  secret scan, with ranked findings and concrete fixes. Read-only.
disable-model-invocation: true
context: fork
---

# harden — dedicated security review

Look at the system the way an attacker would, then report what a defender must fix. This is
the focused security pass; `inspect` covers general quality with a security *axis*, but a
real hardening review deserves its own depth.

Read [references/disciplines/security.md](../../references/disciplines/security.md) — the
shared security reference (STRIDE, OWASP Top 10 + LLM Top 10, secrets, abuse cases). Read
[CONVENTIONS.md](../../CONVENTIONS.md) for the workspace (§1), the ledger (§2), the resume sweep (§5), git isolation (§11), multi-agent
rules (§8), grounding (§14), and freshness (§17 — check current CVEs/advisories against
today's date), and workspace integrity (§20).

## Step 1 — Scope & threat model

**The iron rule: no finding without a reachable path from an attacker to an asset.** A
checklist item that fails in the abstract is not a finding until you can name who reaches it
and what they get. Build the model before auditing, in this order:

1. **Assets** — what is actually worth stealing or breaking here? Credentials, personal data,
   money movement, the ability to act as another user, availability. Rank them; the audit's
   attention follows this list, not the checklist's order.
2. **Entry points** — every place untrusted input enters: routes and handlers, webhooks,
   queue consumers, file/image uploads, third-party callbacks, admin surfaces, CLI flags,
   environment and config. **The API is the surface, not the UI** — enumerate endpoints from
   the router, never from the screens.
3. **Actors and their starting privilege** — anonymous · self-registered user · another
   tenant's user · low-privilege staff · compromised dependency · someone with a stolen
   session. For each finding later, you will name which of these can reach it.
4. **Trust boundaries** — draw the lines where data crosses from one privilege level to
   another. Every boundary is a place validation and authorization must exist; missing checks
   cluster there.
5. **STRIDE per boundary** — spoofing · tampering · repudiation · information disclosure ·
   denial of service · elevation of privilege. Walk the six against each boundary and keep
   what is concrete for *this* system.

Load `security.md` for the checklist that the audit works through.

## Step 2 — Audit (read-only)
Work the checklist against the code and config:
- **Access control** — authz on every route/action, deny-by-default, no IDOR.
- **Injection & input** — parameterized queries, boundary validation.
- **Crypto & secrets** — TLS, encryption at rest, strong hashing; no secrets in code/logs
  (scan the diff).
- **Auth & sessions** — rate-limited login, safe session/JWT handling.
- **Dependencies/supply chain** — known-vulnerable packages (web-check current advisories, §17).
- **SSRF, deserialization, misconfig, debug endpoints.**
- **LLM features** — prompt injection, unsafe tool permissions, data leakage.

In multi-agent mode, dispatch parallel auditors by category and merge; the orchestrator owns
writes (§8). Single-agent: work the checklist inline with fresh eyes.

**These thoughts mean stop — you are about to dismiss a real finding:**

| The thought | The reality |
|---|---|
| "It's internal-only, not exposed" | Internal networks get breached. Assume the attacker is already inside. |
| "You'd have to be logged in to hit it" | Registration is usually free. Authenticated ≠ trusted. |
| "Another tenant couldn't reach this" | That is the claim to *test*, not assume — it is the definition of IDOR. |
| "No one would think to try that" | Attackers do this full-time and share notes. |
| "It's validated on the client" | Client validation is UX. The server is the boundary. |
| "That endpoint is old, nobody uses it" | Unused, reachable, and unmaintained is the ideal target. |
| "The framework probably handles it" | Probably is not a control. Read the config and confirm. |

Dismissing a finding is a decision with the same weight as raising one — it needs the same
evidence.

## Step 3 — Report
Write `security-review.md` in the task folder (bootstrap per §1), ranked by severity:

```
# Security review — <target> · <date>
### Critical  — exploitable now: <boundary violated> → <impact> → <fix>
### High      — likely exploitable / sensitive-data exposure
### Medium    — defense-in-depth gaps
### Info      — hardening suggestions
```

**Calibrate severity by reachability × impact, not by how alarming the category sounds:**

| Rank | Who can reach it | What they get |
|---|---|---|
| **Critical** | anonymous, or any self-registered user | auth bypass · RCE · another tenant's data · money movement · mass data exposure |
| **High** | authenticated, or a plausible precondition | a single user's sensitive data · privilege escalation within a tenant · destructive action |
| **Medium** | needs an unlikely chain, or is a missing layer behind a working control | defense-in-depth gap · information leak that aids a bigger attack |
| **Info** | not reachable today | hardening that prevents a future mistake |

A category does not set the rank — a hardcoded key in a repo nobody can read is not Critical,
and a missing authorization check on one route is not Info.

A finding is valid only with a **violated boundary + demonstrated impact + a concrete fix**,
and each one names **which actor reaches it** (Step 1) — no speculative "could be risky".
Never invent a CVE or a vulnerability — verify and cite, or label it a hypothesis to confirm
(§14). **No secret is ever written into the report**: name the file and line, never the
value, and if a live credential is found say so plainly and treat rotation as part of the
fix — a leaked secret that was committed is already public to anyone with repo history.

## Step 3b — Variant analysis (report the class, not the instance)

Every confirmed finding triggers a hunt: search the whole codebase for the **same pattern**
(same sink, same missing check, same unsafe construct) before closing. One SQL-injection
finding usually means several; fixing the instance while its siblings ship is a false
sense of security. Report the class with all its locations.

## Step 4 — Close the loop
Write `security-review.md` to disk and confirm it is non-empty (§20.2) **before** touching the
ledger — then record a `harden` entry in `state.json.phases` — `approved: true` on a clean pass, or
`waived: true` only on the user's explicit acceptance of open findings (§2) — so a resumed
run re-proves the security gate instead of trusting it. Critical/High must be fixed (or
defensibly, explicitly accepted by the user) before ship.
Route fixes through `construct` → `verify`, then re-audit the changed part. Record accepted
risks in `decisions.md`.

## Composition
- **Consumes:** the code/diff/config, `security.md`, project memory, current advisories (web).
- **Produces:** `security-review.md`; fixes routed to construct/verify.
- **Receives from:** `engineer` (auto-scheduled when a change touches auth, PII, payments,
  secrets, or a new public surface — a rule, not luck) or a direct user request.
- **Hands off to:** `construct` (fixes), `release` (blocks ship on unresolved Critical).
  Distinct from `inspect` (general code review) and `assess` (whole-app feature health).

## Self-review (author's notes)
- *Mis-routed?* `engineer` routes here when a change touches auth, secrets, payments, or
  untrusted input; wrong for general quality review (`inspect`) or app health (`assess`). Pick
  this over `inspect` when the threat model, not the diff, is the question.
- *Single-agent safe?* Yes — the checklist runs inline; parallel auditors are optional.
- *Leaks specifics?* No — checklist is framework-neutral; findings cite real boundaries.
- *Grounded?* CVEs/advisories web-checked with today's date; nothing invented (§14, §17).
