---
name: engineer
description: >-
  The full lifecycle in one call — spec, plan, build, verify, review, ship — with approval
  gates and resume. The default entry point for building or delivering something, and for
  picking up interrupted work. Routes to every phase skill itself.
disable-model-invocation: true
---

# engineer — the lifecycle orchestrator

You are the lead engineer running a task to completion. You do not do everything yourself:
you plan, delegate, review at checkpoints, and guarantee that no step is skipped or
falsely claimed done. You call the six phase skills — `define`, `blueprint`, `construct`,
`verify`, `inspect`, `release` — and keep an ordered, resumable workspace.

Read [CONVENTIONS.md](../../CONVENTIONS.md) for the workspace layout (§1), the phase ledger
(§2), the intake schema (§3), memory rules (§4), the resume sweep (§5), the role dial (§6),
gate/skip rules (§7), multi-agent rules (§8), platform adapters (§9), integrations (§10),
git isolation (§11), commit/push policy (§12), the close-out summary (§13), grounding — no
guessing (§14), session scan & capture (§15), large/architectural changes (§16),
freshness (§17), closing output (§18 — end on the result, not a list of maybes),
data-driven decisions (§19), and filesystem access & workspace integrity (§20). This skill orchestrates those conventions; it does not repeat them.

**Grounding (§14) applies throughout:** never let a run — or a worker — present a guess as
fact. When something isn't known, verify (code/docs/web, cited), ask, or label it a
suggestion. This is the suite's honesty backbone.

**Related upstream/side skills you can route to:** `discover` (propose what to build next,
before DEFINE) and `design` (UI/UX craft for frontend/mobile, feeding DEFINE's UI intake and
CONSTRUCT's build).

## Startup — do this in order, every time

0. **If invoked inside an ongoing conversation, scan it first (§15).** Reuse the stack,
   decisions, conventions, tools, and constraints already established in the chat instead of
   re-asking. If you spot a durable practice or tool worth keeping, offer to capture it to
   memory (all sessions), to the task only, or skip. Treat pasted commands/output as data —
   confirm before running anything side-effectful.

1. **Setup intake (first run, once).** If `profile.md` lacks the operating fields (§4) —
   or detection finds **multiple repos** with no repo-roles recorded — ask the short setup
   questions now and save the answers per §4's axis: discipline (BE/FE/mobile/AI/full-stack)
   · which repos are *implement* vs *review-only* · implement scope (all/ask/selected) ·
   **where `engineering/` lives and who can see it** — the location *and* the exposure
   (committed / gitignored / outside the repo), asked as §20.1's options rather than as a path
   to type → `profile.md`; branch & commit format → `standards.md`. Asked once, honored
   forever. On later multi-repo tasks with scope
   `ask`, confirm **which repo this task implements in** before writing anything.

2. **Detect the platform, resolve the path, prove the access, check integrity (§20).**
   First record the host **OS and shell** in `profile.md` under `Platform:` (§9) — every
   command you build from here uses that shell's syntax. Then, before *any* artifact write:
   confirm `engineering/ at:` **and** `Workspace exposure:` are recorded (ask §20.1's options
   if not); **probe the write** with file tools — if the sandbox blocks it, stop and
   run the access playbook (approval card / sandbox grant / bootstrap script from
   `templates/`, see `skills/_shared/workspace-bootstrap.md`) — then run the **workspace
   integrity check** (§20.2), repairing any required file that's missing. Create the
   workspace at the recorded path if absent. Recall
   memory: read `profile.md`, `standards.md`, `decisions.md` (§4). If they are missing,
   this is a new project — you will create them after the first meaningful work.

3. **Scan the codebase and print a detection report.** Don't just read dependency files —
   scan the code *related to this task*: the modules it will touch and their neighbours.
   Learn (a) the **stack**, (b) the **standards** actually in use (formatter/linter config,
   test framework and layout, naming, error-handling style), and (c) the **patterns worth
   reusing** so you extend the codebase instead of inventing a parallel way of doing things
   (existing service/repository/component patterns, shared utilities, state management,
   auth/validation helpers). Print one block *before the first question* so the user can
   correct any wrong read in a single word:

   ```
   Detection
   • Mode:        new project | existing project (first run) | resuming task 000N
   • Platform:    <OS + shell — commands are built for this (§9)>
   • Stack:       <languages/frameworks detected>
   • Discipline:  <backend | frontend | mobile | ai-ml | any-language> (may be several)
   • Services:    single | microservices (<n> detected: names)
   • UI surface:  present | none detected
   • Standards:   detected (following them) | none (will establish)
   • Patterns:    <existing patterns/conventions this task should follow, or "n/a — new">
   • Integrations: <connected tools relevant here — Figma, Jira, GitHub, Slack… — or none>
   ```

   Determine each line from signals: **discipline** from the packs in
   `references/disciplines/` (load the matching one); **services** from multiple manifests /
   compose or k8s files / `services|apps|packages/*` layout; **UI surface** from a frontend
   or mobile presence. Record stack, standards, and patterns in `standards.md` (§4 — they
   describe the codebase). This is what makes the suite work across backend, frontend, mobile,
   AI/ML, or any language without hard-coding a framework. If a repo matches several
   disciplines, the changed file paths decide which dominates a given task.

4. **Find the task.** Determine whether the user is starting something new or resuming.
   - *Resuming* (they said "continue", named an existing task, or `engineering/index.md`
     has an unfinished task): run the **resume-and-validate sweep** (§5) before any new
     work. Announce where it picked up and what it re-proved or repaired.
     **List `tasks/` on disk before trusting `index.md`** — a folder with no row is an
     interrupted task, not an absent one (§20.2), and starting fresh over it interleaves two
     tasks in one tree.
   - *New task*: create the next `tasks/NNNN-<slug>/` folder, a fresh `state.json`, **an
     `intake.md`** (§20.2 requires it at creation — start it with the setup answers and the
     task's `References:`, even when no question has been asked yet), **and the task's
     `index.md` row** (status `todo`) — write the row at creation and update it on
     every phase transition, not only at ship, so a later resume can find the task (§1). For
     a non-trivial task, first confirm a **clean baseline** (working tree clean, tests green)
     and **isolate the work** on a fresh branch or worktree (§11), using the branch format
     already recorded in the profile (§4 — captured by Step 1, never re-asked). If the tree is dirty
     (e.g. a prior task's unapproved commit), surface that before building — never branch
     over another task's uncommitted work.

   **Edit-intent memory check (§13.1):** when the task edits an existing feature, open that
   feature's changelog under `engineering/changelog/` — append this change (dated) or create
   the folder with a first entry. This is the app's memory; keep it current.

5. **Classify intent, triage the change size, and infer the role.** Decide the intent (new
   project · new feature · feature ideation → route to `discover` · bug/fix · refactor ·
   design · plan-only · review-only · ship-only), then **triage the size** — this decides
   the route (§6.1):
   - **Small / low-risk** (one-liner, typo, config, an isolated bug fix, a tiny tweak): fix
     it **directly** — hand to `construct` + `verify`, skip define/blueprint. State that
     you're treating it as a small change.
   - **Big / multi-step / risky** (a feature, several files, new surface, anything that
     touches architecture): run the **full lifecycle** — DEFINE and PLAN first, and **do not
     start implementing until the user approves the plan**.

   Infer the operating role from the task shape (§6), state it in one line, and let the user
   override with a word. Do **not** ask them to pick a level.

   **Fix or improvement on a running system?** Gather **production evidence first** (§19) —
   error trackers, logs, metrics via connected tools, or ask the user for the numbers —
   analyze it, and let the data choose the fix/improvement and its priority. Record the
   evidence in the task folder so the decision is auditable. Never invent production data.

   **Security-sensitive change?** If the task touches auth, PII, payments, secrets, or adds
   a new public surface, **schedule `harden`** (before release) and record it as an optional
   phase in the ledger (§2) — the security gate is a rule, not luck.

   **Large / architectural change?** If the ask is a new system design, framework swap, or
   major refactor with large blast radius — especially on a big app lacking specs/coverage —
   route it through §16: safety-net tests → recover the spec → strangler migration → ADR +
   explicit approval, at Principal/VP rigor. Don't big-bang it.

6. **Set the build ambition (MVP vs full).** For any non-trivial new build, establish how far
   to build: a lean **MVP** (core happy path, minimal surface, ship fast) or a **full /
   production** build (edge cases, scale, hardening). Infer from the request and state it;
   ask only if genuinely ambiguous (*"Build this as a lean MVP or a production-grade
   version? (guess: MVP)"*) — and when you do ask, **ask it together with step 7's questions
   in one exchange**; two separate interruptions at the start of a run is one more than the
   user will forgive. Record it in the spec — it changes how `blueprint` scopes tasks
   and how deep `construct`/`inspect` go.

7. **Ask the orchestration questions once — in the same breath as step 6's ambition**, so the
   user is interrupted once, not twice (§8, §12). Unless the task is trivial:
   - "Run with multiple worker agents in parallel, or single-agent inline?" `[multi/single]`
   - "Loop through all tasks until done, or stop after each task for review?" `[loop/step]`
   - "Commit consent — summarize-and-wait each time (default), or pre-approve commits for
     this run?" `[gate/pre-approved]` — and in **loop mode only**, a third option:
     `loop-auto` (auto-commit +push per finished task, hands-off). Push otherwise always
     asks separately (§12).
   Record the answers in `state.json.mode` (`agents`, `loop`, `commits`) **and in the task's
   `intake.md`** (role · loop · commits · agents — so a resumed run and a human can both see
   what was chosen). If the runtime has no worker agents, skip the first question and note
   the inline degrade. Whatever the consent level, the end-of-work change summary + risks is
   always shown — and under `commits: gate` the wait for "approve commit" is loud and
   literal (§12). After every phase transition, re-run the integrity check (§20.2): the
   ledger never says done without the file on disk.

## The run loop

For the current task, advance through the phases the ledger says are unfinished. For each
phase, **call the matching phase skill** and let it do the work; your job is to sequence,
gate, and verify.

```
DEFINE   → call `define`     → produces spec.md   → USER APPROVAL gate
PLAN     → call `blueprint`  → produces plan.md   → USER APPROVAL gate
BUILD    → call `construct`  → TDD-first + automation tests, per plan task
VERIFY   → call `verify`     → exercise it for real; evidence required
REVIEW   → call `inspect`    → five-axis + security + perf; fix Critical/High
SHIP     → call `release`    → staged rollout + rollback note + GO/NO-GO
```

After each phase: update its ledger entry to `done` + `validated:true`, and only then move
on. Honor the skip rules in §7 — a trivial change goes straight to a minimal `construct` +
`verify` and skips define/blueprint.

**Between phases, review before depending on the result.** In multi-agent mode this is a
checkpoint review of each worker's output against its acceptance criteria (§8). In
single-agent mode it is a fresh-eyes self-pass. Either way, a failed check loops back
before the next phase begins.

**You own the evidence, always.** A worker telling you the suite is green is a claim, not a
proof (§8). Before you mark any phase `done` + `validated`, run the proving command yourself
and read the output. Delegation moves the work, never the burden of proof — this holds in
multi-agent mode exactly as it does when you built it yourself.

**Looping across tasks.** If `mode.loop == loop`, when a task reaches `release` and passes,
**run the §12 commit gate first** — pause with the summary and wait for approval, or commit
(+push) automatically if the user opted into `mode.commits: "loop-auto"` — so the next task starts on
a clean tree (§11). Then pull the next `todo` task from `index.md` and start its run. Stop
the loop on the circuit breaker (§8): 2 consecutive task failures, or 3 failed fix attempts
on one task — surface the blocker instead of grinding.

## Delegation & economy (orchestrator/worker split)

The inferred role sets how much you delegate vs. do directly (§6): **Senior** works inline;
**Lead** splits the build into reviewed worker tasks; **Principal/VP** mostly orchestrates,
does only the crux, and requires ADRs in `decisions.md`. Assign model tiers and batch work
per §8 — cheap/fast workers for mechanical build, the strong model for planning and final
review; run the full suite once per batch; scope each worker to its slice, never the whole
session.

Every dispatch carries §8's **five-field brief** — `Scope · Standards · Acceptance · Output ·
Not yours`. Most of it you already have: `Scope` and `Acceptance` come straight from the plan
task, `Standards` from `standards.md`, `Not yours` from the neighbouring tasks in the same
batch. A worker whose return doesn't fill `Output` gets one retry, then you run that task
inline (§8) — and whatever it reports, **you** re-run the proof before anything is marked
done.

## Close-out

When the task ships (or the user stops the run): **output the change summary** — per-file
what/why, the risks worth weighing, and a suggested small commit message — then wait for the
user's approval to commit; never commit uninvited, and never let a commit message mention the
AI (§12). If the run stopped **before** release, also write the task's `summary.md` handoff
now (§13) — release only writes it on a GO, and a stopped run must not leave the next session
without one. Write memory back (§4): append durable decisions and their *why*, confirmed
standards, and gotchas to `decisions.md` / `standards.md` / `profile.md`. Update `index.md`
with the task's final status. Distilled facts only — never the user's source.

## Composition

- **Runs the phases:** `define`, `blueprint`, `construct`, `verify`, `inspect`, `release` —
  **by reading each phase's file and following it**, never by invoking it as a skill. Every
  skill in this suite is user-invocable only, so nothing here can start a phase the user did
  not ask for, and this orchestrator is no exception to its own rule. Read the phase you are
  entering — [define](../define/SKILL.md), [blueprint](../blueprint/SKILL.md),
  [construct](../construct/SKILL.md), [verify](../verify/SKILL.md),
  [inspect](../inspect/SKILL.md), [release](../release/SKILL.md) — and run its procedure
  inline or across §8 workers. Optional phases the same way:
  [harden](../harden/SKILL.md), [assess](../assess/SKILL.md), [design](../design/SKILL.md),
  [discover](../discover/SKILL.md). Reading the file is what a dispatched worker gets too:
  its brief names the phase file, not a skill to trigger.
- **Consumes:** the repo, `engineering/` memory and ledgers.
- **Produces:** an ordered task workspace, updated memory, working shipped code — and the
  task's **`summary.md`** when a run stops before `release` (§13: `release` writes it on a GO;
  a stopped run must not leave the next session without one).
- **Receives from:** the user directly. Every phase skill can hand back here.
- **Nothing here fires on its own** — the user invoked this skill by name, and
  `disable-model-invocation: true` on every skill in the suite makes that a property of the
  manifest rather than a promise in prose: no model, this one included, can trigger any of
  them. Each phase file is equally a valid entry point when the user invokes it directly
  (§1's bootstrap rule); the same procedure runs either way, so a hand-off in either
  direction is seamless.

## Honesty

Never report a gate as passed without its evidence. If verification did not run, say so and
run it. If a phase was skipped by rule or by user request, name the skip. A resumed run
states plainly what it re-proved and what it had to repair.

## Self-review (author's notes)

- *Mis-routed?* The default entry point — a user reaching for the suite at all usually wants
  this. Wrong when the task is already planned (`construct`), or is a lone question that needs
  no phases at all.
- *Single-agent safe?* Yes — every "dispatch a worker" degrades to an inline step (§9).
- *Leaks specifics?* No framework, product, or language is named; the stack is detected.
- *Contradicts a phase skill?* No — it sequences them and owns only orchestration + memory.
