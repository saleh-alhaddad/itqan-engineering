---
name: learn
description: >-
  Builds and tracks a personalized learning roadmap, or onboards you onto an existing
  codebase. A user-invoked entry point; the lifecycle never routes here.
disable-model-invocation: true
---

# learn — a personalized software-engineering roadmap you can follow and track

Turn "I want to learn X" into a clear, level-appropriate path the learner can actually
follow — ordered, with milestones and hands-on projects — and track their progress over time.
You meet them where they are: a total beginner and a senior dev pivoting to a new domain get
very different maps from the same skill.

Read [CONVENTIONS.md](../../CONVENTIONS.md) for the workspace (§1), the intake schema (§3),
the close-out summary (§13), and **grounding — no guessing (§14)**: cite *real* resources (docs, courses, books) and never invent a title or
URL. If you're unsure a resource exists, say "search for …" or label it a suggestion.

## Step 1 — Intake (one question at a time, each with a guess)

Ask only what you need, one at a time (§3), and infer what you can from how they phrase it.
Cover:

1. **Level** — new to programming · some basics · intermediate (ship features) · advanced
   (pivoting/deepening). Offer a quick self-check if unsure.
2. **Goal** — the outcome: get a first job, become a backend/frontend/mobile/AI engineer,
   learn a specific language, master a topic (system design, testing, security…), or build a
   specific project. The goal shapes the whole map.
3. **Target languages / stack / topics** — if they named them, use them. If not, **suggest**
   a sensible path for the goal and confirm (e.g. for "backend": one language + HTTP/APIs +
   databases + testing + deployment) — as a proposal, not a decree.
4. **Time & pace** — hours/week and any deadline; this sizes the milestones.
5. **Delivery mode** — **proactive** (a guided tutor: explains each topic, gives exercises
   and quizzes, checks in, tracks completion) or **text-only** (generate the full roadmap +
   resources and let them self-drive). Ask this explicitly.
6. **Content language** — which natural language to generate topics and explanations in
   (English, Arabic, …). Default to the language they're writing in; confirm.

Save every answer to `learning/profile.md`.

## Step 2 — Set up the learning folder (to monitor progress)

Create a `learning/` workspace so progress is trackable, not a one-off message:

```
learning/
├── profile.md      # level, goal, stack, pace, delivery mode, content language
├── roadmap.md      # the ordered path (phases → modules → milestones → projects)
├── progress.md     # the ledger: each module todo | in-progress | done, + current position
└── modules/
    ├── 01-<topic>/notes.md      # explanations, examples (in the chosen language)
    └── 02-<topic>/exercises.md  # tasks/quizzes, for proactive mode
```

## Step 3 — Build the map (ordered, level-appropriate)

Design the roadmap for the learner's level and goal. A sound general shape (adapt, don't
force it):

```
Fundamentals → Core language → Tooling (git, editor, CLI) → Data & the domain
(backend: APIs+DB · frontend: UI+state · mobile: platform · AI: math+ML) →
Quality (testing, debugging) → Advanced (system design, security, performance) →
Capstone project
```

For each **module** give: what it covers, why it matters, prerequisites, a concrete
**hands-on task/project** (people learn by building), a **milestone** ("you can now …"), and
**1–3 cited real resources**. Order by prerequisite so nothing depends on something later.
Render the flow as a simple tree or a mermaid diagram in `roadmap.md` so the path is visual.
Scale depth to level: a beginner gets more fundamentals and smaller steps; an advanced
learner gets a compressed path that skips what they know (verify with a quick check, don't
assume).

## Step 4 — Deliver by the chosen mode

- **Proactive:** walk module by module — explain in the chosen language, give an exercise or
  quiz, check their answer, and only advance when the milestone is met. Update `progress.md`
  as each module completes. Check in and adapt if they're stuck or moving fast.
- **Text-only:** output the full roadmap + resources, mark where to start, and let them
  self-drive. Still write `progress.md` so they (or a later session) can track and resume.

## Step 5 — Track & adapt

Treat `progress.md` like a ledger: mark modules done, keep a "current position," and on a
return visit **resume from there**. Re-assess periodically — if the goal or pace changes, or a
topic proves too easy/hard, adjust the remaining path. Suggest the next module and the next
project.

## Mode: onboard onto an existing app (new-employee ramp-up)

When the goal is "understand *this* codebase/app", the roadmap's subject is the repo itself.
Scan the code, the `engineering/` workspace if present — `profile.md`, `decisions.md`, and
the **feature changelog (§13.1), which is the app's memory of why things are the way they
are** — plus README/docs. Write/refresh the **shared, team-wide `engineering/onboarding.md`** in the repo (§1) — one
doc every new hire improves rather than each regenerating their own — and keep only the
**personalized path** (level-scaled first tasks, progress) in `learning/`. The onboarding map
covers: architecture overview,
the key features and how they connect, where things live, the main flows traced end-to-end,
conventions to follow (`standards.md`), and a guided path of first small tasks scaled to the
learner's level. Cite files/entries, don't guess intent (§14); what the changelog can't
answer, list as questions for the team.

## Grounding (§14)

Cite real, checkable resources — never fabricate a course, book, or link. If you're not sure
something current exists (a library version, a specific tutorial), say so and point to how to
find it (official docs, a search) rather than inventing it. Distinguish "this is the
established path" from "this is my suggestion."

## Composition

- **Consumes:** the learner's answers, optionally their current repo/skills to gauge level.
- **Produces:** the `learning/` folder — `roadmap.md`, `progress.md`, per-module notes — and
  in repo-onboarding mode the **shared, team-wide `engineering/onboarding.md`** (§1), which
  lives with the project rather than in the learner's personal folder.
- **Receives from:** the user directly — `engineer` never routes here.
- **Relates to:** the lifecycle skills — a capstone or practice project can be built with
  `engineer`/`construct`; a learner exploring "what to build" can use `discover`.
- A user-invoked entry point; `engineer` never routes here.

## Self-review (author's notes)

- *Mis-routed?* `engineer` never routes here — it is a user-chosen entry point. Pick this over
  `discover` when the goal is understanding, not shipping.
- *Single-agent safe?* Yes — dialogue, web/doc lookups, and file writes; no worker agents.
- *Leaks specifics?* No — languages, stacks, and resources come from the learner and the web,
  not hard-coded; content language is whatever they choose.
- *Grounding?* Central — real cited resources only; suggestions are labeled (§14).
