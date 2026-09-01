# 3 · Getting started — your first run

[← Installation](02-installation.md) · [Book index](README.md) · [Next: the skills →](README.md)

## Your first command

From inside any project (or an empty folder for greenfield) — you name the skill; it never
fires on its own ([how you invoke it](02-installation.md#how-you-invoke-it)):

```
itqan:engineer "add password reset to the auth service"
```

Here's everything that happens, and why.

## Step 0 — First-run setup (asked once, ever)

On a project the suite hasn't seen, it captures the **project profile** — and never asks again:

- Your role (backend / frontend / mobile / AI / full-stack) — shapes defaults
- Multi-repo? Which repos it may **implement** in vs **review-only** (a hard write-boundary)
- Branch + commit format (checked against your CI's rules)
- **Where the `engineering/` workspace lives** — inside this repo, outside it in a central
  folder spanning several repos, or a path you name
- **Who can see it** — if it sits inside a repo: committed (your team reads your specs,
  intake, and decisions through git) or gitignored (private to this machine)
- Your **platform** — OS and shell, detected rather than asked, so every command it runs is
  correct on Windows, macOS, Linux, or a cloud shell

How the suite operates here is saved to `engineering/profile.md`; how your codebase is
written goes to `engineering/standards.md`. One minute, once.

## Step 1 — The detection report

Before asking you anything, it scans and *shows you what it thinks*:

```
Detection
• Mode:        existing project (first run)
• Stack:       Node 22 / Express · Jest
• Discipline:  backend
• Services:    single
• UI surface:  none detected
• Standards:   detected (following them)
• Patterns:    repository pattern · zod validation at routes
• Integrations: GitHub connected
```

Wrong on any line? Correct it with a word. This report is why the suite adapts to *your*
stack instead of assuming one.

## Step 2 — Triage: how much ceremony?

- **Small** (typo, config, isolated fix) → skips spec/plan, goes straight to a test-first
  fix. Still on its own branch, still verified, still your commit approval.
- **Big** (feature, several files, architecture) → full pipeline with both gates.
- It also states the inferred **role** ("Treating this as Lead-level — say 'senior' to
  change") and, for fixes on running systems, pulls **production evidence first**.

## Step 3 — Questions, then the two gates

First, one combined exchange sets up the run — build ambition (MVP or production?) together
with the three orchestration questions: worker agents `[multi/single]`, task flow
`[loop/step]`, and commit consent `[gate/pre-approved]`. One interruption, answered once,
recorded in the ledger. Then intake is one question at a time, each with a best guess so you
can answer in a word:

```
Q: Reset links expire after — 15 min, 1 hour, or 24 hours? (my guess: 1 hour)
```

Then: **`spec.md` → you approve ⛔ → `plan.md` → you approve ⛔.** Approvals are recorded
in the ledger — a resumed run cannot pretend a gate happened.

## Step 4 — Build, prove, review, ship

- **construct**: for each planned task — failing test first (watched to fail for the right
  reason), smallest code to green, refactor. Modern idioms for your installed versions.
- **verify**: full suite fresh + the real flow exercised; an independent pass attacks the
  spec's criteria; any bug becomes a pinned failing test before its fix.
- **inspect** (+ **harden** automatically if auth/PII/payments): ranked findings with fixes;
  Criticals must be resolved.
- **release**: rollback written first, staged rollout with numeric thresholds, GO/NO-GO.

## Step 5 — Your commit

Nothing was committed along the way. At the end:

```
## Changes — 0001-password-reset
Per file:   src/auth/reset.ts — token issue/verify endpoints …
Risks:      email delivery not covered by tests (external)
Not touched (intentionally): session refresh logic
Suggested commit: "Add password reset with expiring email tokens"
→ Approve this commit, adjust the message, or leave it uncommitted.
```

You approve. Push always asks separately.

## What's now in your repo

```
engineering/
├── profile.md        ← how the suite operates here: role, paths, exposure, platform
├── standards.md      ← how your codebase is written: stack, conventions, branch format
├── index.md          ← ordered registry of every task + live status
├── decisions.md      ← why token-expiry = 1h (the ADR)
├── changelog/password-reset/…  ← the dated change entry
└── tasks/0001-password-reset/  ← intake · spec · plan · review · summary · state.json
```

`summary.md` ends with an **Operate** runbook (what to watch, how to roll back) and an
**Outcome** line to fill after the rollout bakes.

## Resuming — the party trick

Close the laptop mid-build. Next week:

```
itqan:engineer "continue"
```

It reads the ledger, **re-proves** every phase marked done (tests run again; approvals
checked as real), repairs anything invalid, and resumes at the first unproven step —
announcing exactly what it re-proved and where it picked up.

**Next:** deep-dive any skill in [Part II](README.md), or see full
scenarios in the [Playbooks](04-playbooks.md).
