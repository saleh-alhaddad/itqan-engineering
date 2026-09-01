# Discipline pack — Security

Load for any change touching untrusted input, authentication, authorization, secrets,
payments, personal data, or external integrations. Deepens the security axis of `inspect` and
backs the `harden` skill. Framework-neutral; adapt to the detected stack.

## Threat-model first
Map the **trust boundaries** (where untrusted data crosses into trusted code), then walk
**STRIDE** — Spoofing, Tampering, Repudiation, Information disclosure, Denial of service,
Elevation of privilege — and the concrete **abuse cases** for this change. Design the defense
before writing the feature.

## OWASP Top 10 (web/app) — prevention checklist
- **Broken access control:** enforce authz on every route/action (not just authn); deny by
  default; never trust client-supplied IDs/roles (IDOR).
- **Injection:** parameterize SQL/NoSQL/OS/LDAP; validate and normalize at the boundary.
- **Cryptographic failures:** TLS in transit, encrypt sensitive data at rest, no home-rolled
  crypto, strong password hashing (argon2/bcrypt).
- **Insecure design / misconfig:** secure defaults, least privilege, no debug endpoints in prod.
- **Vulnerable dependencies:** scan and patch; pin and review new deps (supply chain).
- **Auth failures:** rate-limit login, secure session/JWT handling, MFA where it matters.
- **SSRF / unsafe deserialization / logging of secrets:** validate outbound URLs, avoid
  untrusted deserialization, never log secrets or PII.

## LLM / AI features — OWASP LLM Top 10 (when applicable)
Prompt injection (treat retrieved/tool content as data, not instructions), insecure output
handling, unsafe tool/agent permissions, sensitive-data leakage in prompts/logs, model/data
supply-chain provenance.

## Ask First — building these needs explicit human approval

Some things are dangerous to *build*, not just to build wrong. Get the user's explicit OK
before adding or changing: an auth flow, a new category of sensitive data, a new external
integration, a CORS policy, a file-upload handler, a rate-limit change, or elevated
permissions. The gate is on the construction, before any finding could exist.

## Dependencies — audit triage & install safety

- Triage vulnerability-audit findings by **reachability**: is the vulnerable code on a
  runtime, build, or test-only path? Fix by real exposure, not by scanner count.
- **Never run a forced auto-fix** (e.g. a force-flagged audit fix) — it swaps breakage for
  breakage; upgrade deliberately (one dep per change, read the changelog).
- On a first install of untrusted dependencies, **block lifecycle/install scripts**, inspect,
  approve only the minimum, then verify with a frozen-lockfile install.

## Secrets
Never in code, config, or logs — use the platform secret store; rotate on exposure; scan the
diff for accidental keys before commit.

## Verify & review
- Test the **abuse cases**, not just the happy path (authz denied, malformed input, replay).
- A finding is real only with a violated boundary + demonstrated impact + a concrete fix.
