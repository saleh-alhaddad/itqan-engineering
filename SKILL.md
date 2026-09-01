---
name: itqan
description: >-
  The full software-engineering lifecycle as one suite — DISCOVER, DEFINE, PLAN, BUILD,
  VERIFY, REVIEW, SHIP — with approval gates before code, test-first builds, evidence before
  "done", and resumable multi-session work. Routes to 12 sub-skills covering any stack, plus
  feature discovery, security audit, UI/UX craft, and learning roadmaps.
---

# itqan — engineering skills suite router

This repository is a **suite of 12 skills** sharing one backbone. When installed as a single
skill (e.g. via `npx skills add`), this file is your map; everything referenced below ships
inside this folder.

**This suite is invoked explicitly — it never fires on its own.** The user names it; nothing
here triggers from a matched description or keyword. `engineer` is the entry point for
lifecycle work and routes to the phases itself, but every sub-skill is also a valid door in
and bootstraps its own workspace (§1). If you are reading this file, you have been invoked:
route and proceed.

## How to work

1. **Read [CONVENTIONS.md](CONVENTIONS.md) first** — the shared rules every sub-skill
   depends on (§1 workspace · §2 phase ledger · §5 resume sweep · §6 role dial · §7 gates ·
   §8 multi-agent · §12 commit policy · §14 grounding · §15–17 session/big-change/freshness ·
   §18 closing output · §19 data-driven decisions · §20 filesystem access & integrity).
2. **Route the task to the right sub-skill** and follow its `SKILL.md` exactly:

| The user wants… | Follow |
|---|---|
| Something built/implemented/shipped end-to-end, or to "continue" prior work | [skills/engineer/SKILL.md](skills/engineer/SKILL.md) — the orchestrator |
| Feature ideas / "what should we build next" | [skills/discover/SKILL.md](skills/discover/SKILL.md) |
| A spec/PRD, or schema / data-model / API-contract design | [skills/define/SKILL.md](skills/define/SKILL.md) |
| An approved spec broken into an ordered task plan | [skills/blueprint/SKILL.md](skills/blueprint/SKILL.md) |
| Code written for an already-defined task (test-first), incl. scoped fixes/optimizations | [skills/construct/SKILL.md](skills/construct/SKILL.md) |
| Proof it works / a bug root-caused | [skills/verify/SKILL.md](skills/verify/SKILL.md) |
| A senior-depth read-only code review | [skills/inspect/SKILL.md](skills/inspect/SKILL.md) |
| A security audit / threat model / hardening pass | [skills/harden/SKILL.md](skills/harden/SKILL.md) |
| A safe release with rollback + GO/NO-GO | [skills/release/SKILL.md](skills/release/SKILL.md) |
| UI/UX design or a UI audit (web/mobile) | [skills/design/SKILL.md](skills/design/SKILL.md) |
| A learning roadmap, or onboarding onto this codebase | [skills/learn/SKILL.md](skills/learn/SKILL.md) |
| A whole-app health analysis / feature audit by an expert panel | [skills/assess/SKILL.md](skills/assess/SKILL.md) |

3. **Discipline packs** (auto-selected by detected stack) live in
   [references/disciplines/](references/disciplines/README.md) — stack packs (backend,
   frontend, mobile, ai-ml, any-language), the shared
   [ui-craft.md](references/disciplines/ui-craft.md), and concern packs (database, security,
   devops).

## Non-negotiables (from CONVENTIONS)

- Two user-approval gates before code (spec, plan) and GO/NO-GO before ship — recorded in
  the ledger; a resumed run re-proves them (§2, §5, §7).
- Evidence before claims: run it fresh and read the output before saying "done" (§14).
- Never commit or push without the user's approval; commit messages never mention the AI (§12).
- Don't guess — verify (cited), ask, or label a suggestion (§14); check the web with today's
  date for time-sensitive facts (§17).
