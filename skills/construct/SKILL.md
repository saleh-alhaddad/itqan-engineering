---
name: construct
description: >-
  Writes the code for an already-defined task, test-first, following your codebase's own
  patterns. Also scoped fixes and performance optimizations on existing code.
disable-model-invocation: true
---

# construct — build it, test-first, no spaghetti

Your job is to turn a plan (or a clear small ask) into working code that matches how this
project is already written, proven by tests you wrote *before* the code. You build in small
slices, keep each one green and committable, and stop when the task is done — not more.

Read [CONVENTIONS.md](../../CONVENTIONS.md) for the workspace (§1), the ledger (§2), memory
(§4), role dial (§6), skip rules (§7), multi-agent rules (§8), the commit/push policy (§12),
the close-out summary (§13), and freshness (§17).

## Step 1 — Standards & patterns: scan, then detect or establish

Before writing anything, know the rules of *this* codebase and how it already solves things.

- **Scan the related code.** Read the modules this task touches and their neighbours. Find
  the **patterns to reuse** — the existing service/repository/component shape, shared
  utilities, validation/auth/error helpers, state management, naming. Extend those instead
  of inventing a parallel approach; matching what exists beats any external "best practice."
- **Follow the neighbours' *organization*, not their *defects*.** Match how the codebase lays
  things out — folders, naming, layering, error style. Do not inherit a sibling's defects just
  because they are there: where the repo states a rule (a linter's length/complexity limit,
  a documented convention) the new code meets it even when neighbouring code doesn't, and you
  note the neighbour's violation rather than copying it. This is §17's
  modern-within-convention rule applied to shape.
- **Existing code?** Detect the conventions and follow them — do not impose your own: the
  linter/formatter config, the test framework and how tests are named and laid out, folder
  structure, error-handling style. Record what you found in `standards.md` so later tasks
  and workers stay consistent.
- **Greenfield / no conventions?** Establish them: propose a minimal set (language idioms,
  test framework, structure, formatting) and get a quick approval, then write them to
  `standards.md`. From then on, follow them.

Also load the **discipline pack** for the detected stack (backend / frontend / mobile /
AI-ML / any-language) from `references/disciplines/` — it adds the concerns specific to that
surface (e.g. accessibility for frontend, platform HIG for mobile, contracts for backend).

**Choosing or upgrading a tool/library/version?** Don't pick "the latest" from memory —
establish today's date and check the web for the current version and any deprecations, then
cite it (§17). Before *adopting* a new dependency, also check that it's worth taking at all:
license compatibility with the project, maintenance health (recent releases, open-issue
trend), and supply-chain trust — not just the version number. Match what the repo already
uses unless the task is explicitly an upgrade.
Also load any **cross-cutting concern pack** the change touches: `database.md` (migrations,
queries), `security.md` (untrusted input/auth/secrets), `devops.md` (CI/containers/deploy).
Build the way this codebase already builds: `standards.md`'s `Stack:` and `Conventions:`
(§4) record what was detected — language, framework, naming, structure, error handling — and
they are the answer to "how is this normally written here", not your own habits. Read them
before the first line; a pattern they do not cover is one to take from the sibling files
(§17), and worth adding once you have.

Name things in the project's own words: `standards.md`'s `Domain terms:` (§4) is the
vocabulary the spec and plan already use, so an identifier that renames a recorded term makes
the code read as a different subject than the artifacts describing it. A term the build needs
and the glossary lacks gets added there, not invented in a file.

For a **frontend or mobile** task, also read `design.md` (§6.2) — the UI source of truth —
and `references/disciplines/ui-craft.md` for the universal UI craft rules (tokens, spacing,
type, states, motion, a11y, i18n). Build the screens, states, and interactions to match, and
scope depth to the build ambition (MVP vs full) from the spec.

## Step 2 — Build each task test-first (the core loop)

Work the plan's tasks in order (a trivial change is one implicit task). **Build into the
files the task's `Shape:` field names, and take the structural choice it records** — that
decision passed the plan gate; changing it mid-build means the plan was wrong, which is the
amendment loop, not a silent call. For each task, run
the RED → GREEN → REFACTOR loop.

**The iron law: no production code without a failing test first.** If you wrote the code
before the test, delete it and rebuild from the test — do not keep it as a reference, do not
"adapt" it while writing the test. Code you are looking at while writing its test makes the
test describe what you wrote, not what the task needs. Violating the letter of this rule is
violating its spirit.

**These thoughts mean stop — you are rationalizing:**

| The thought | The reality |
|---|---|
| "It's too simple to need a test first" | Simple code is where the cheap test lives. Write it. |
| "I'll add the test right after" | Then the test is shaped by the code, and proves nothing. |
| "The test would just mirror the implementation" | That means you don't know the behavior yet — that's the point of RED. |
| "I already know it works" | Then RED costs seconds and confirms it. If it doesn't fail, the test is wrong. |
| "Just this once, we're in a hurry" | The exceptions are throwaway prototypes and generated code — and you ask first (§7). |

```
RED     Write ONE test for the task's acceptance criterion. Run it. Watch it FAIL —
        and confirm it fails for the RIGHT reason (the behavior is missing, not a typo
        in the test). A test that passes before you write code is usually testing
        nothing — fix it or delete it. The one honest exception is a **guard test**
        asserting that a VALID input is still accepted: it passes trivially while no
        rule exists, and starts earning its place the moment the rule lands, by
        catching a rule that is too strict. Keep those, and say which they are.
GREEN   Write the SMALLEST code that makes that test pass. No extra features, no
        speculative abstraction. Run the test — watch it pass.
REFACTOR Clean up what you just wrote while the test stays green: clear names, no
        duplication, no dead code. Update the doc-comment on any class/service/method you
        changed (intent and contract, not mechanics), matching the repo's convention.
        Leave the slice green and committable — but do NOT commit it yourself (§12).
```

### A test that cannot fail protects nothing

RED proves the test *can* fail; these three checks prove it fails for a reason worth having.
Apply them to every test you write:

1. **Name the production change that would break it.** If you cannot state a concrete edit to
   the source that turns this test red, the test asserts nothing — rewrite it or drop it.
2. **Derive the expected value independently of the implementation.** Work out what the answer
   *should* be from the spec's criterion, then compare. Reading the code and asserting what it
   currently returns writes yesterday's behavior into a test and calls it a specification.
3. **Mutate once to confirm.** On anything load-bearing, break the production line on purpose,
   watch the test go red, then restore. That is the only direct proof the test guards the
   behavior you think it guards.

**Two traps that pass RED and still protect nothing:**

| Trap | Why it fools you | What to assert instead |
|---|---|---|
| **String-presence** — asserting that output, a config, a script, or a generated file *contains* some text | Text is not behavior. The string moves, gets reworded, or appears in a comment, and the test neither breaks nor protects. | The observable effect: the command's exit code, the parsed value, the state after the run. |
| **Change-detector** — asserting a value the test itself fixed, or re-stating a constant | It fails whenever anything nearby moves and passes whenever the bug is elsewhere — noise that looks like coverage. | The rule that produced the value, exercised through a real input. |

Why test-first: watching the test fail first is the only thing that proves the test can
*detect* the bug or missing behavior. It also forces you to state "done" as an observable
check before you get attached to an implementation.

**Track slice progress in `plan.md`.** As each plan task's slice goes green, update that
task's `Status:` line (`todo → in-progress → done`). With no per-slice commits (§12), this is
the only record a resumed run has of which tasks are truly done versus half-built — keep it
current, not retrospective.

**Thin vertical slices:** each slice should leave the system working and committable — a
small end-to-end piece of behavior, not a half-built horizontal layer. Slices are the natural
commit *boundaries*, but **the run never commits on its own** (§12): when the work is done,
present the per-file change summary + risks + a suggested small commit message and let the
user approve. Never push without explicit approval, and never mention the AI in a commit
message.

**Log and document every change (§13.1).** Append a dated entry to the touched feature's
changelog (`engineering/changelog/<feature>/`) — the daily history is written by whoever
makes the change — and if the feature/file has its own doc (module README, `docs/*.md`),
update it in the same change, never as a follow-up.

**Touching logic or a response shape? The automation tests move with it.** Any change to
business logic or an API/response contract updates the impacted automation tests and spec
files **in the same change** — extended for new behavior, adjusted for changed behavior,
removed only when the behavior is gone. A passing suite that no longer describes the
behavior is worse than a failing one; and an existing test that must be *modified* to pass
is a behavior change — confirm it with the user (never silently).

**Route user-facing copy through the recorded source.** The profile's `Copy source:` (§4)
says where strings live — local i18n files or an external content tool (e.g. Ditto, a CMS).
Never hardcode display text past it; if no source is recorded yet on an app with user-facing
text, ask once and record it.

**Keep the interface docs in sync.** When a change alters a public API or contract (a route,
request/response shape, event, or public method), update the API spec alongside the code —
the OpenAPI/Swagger doc, GraphQL schema, or the project's equivalent. If none exists and the
surface is a public API, suggest adding one. The spec is part of the change, not a follow-up.

## Step 3 — Layer automation tests on top

Once the unit-level behavior is green, add the higher tests the task needs so the behavior
is guarded automatically going forward:
- **Integration** — the slice working with its real neighbors (db, service, component tree).
- **End-to-end / flow** — the user-visible path, where the task warrants it.
- **Regression** — for a bug fix, the reproduction test that now stays in the suite forever.

**Test craft:** before the first RED, discover the repo's own focused-test and full-suite
commands from its build files/CI — never assume a default runner. Prefer test doubles in
this order: **real > fake > stub > mock** (mock only what's slow or non-deterministic);
assert on resulting *state*, not on which internal methods were called; and prefer DAMP
over DRY in tests — each test should read as a self-contained specification. If a
"simplification" requires modifying an existing test to pass, you changed behavior — revert.

**Keep the pyramid shape:** most coverage at unit level, integration where components truly
meet, and e2e only for the few user-critical paths — e2e suites that re-test unit logic go
slow and flaky. Order matters: **TDD unit tests first, automation tests after** the units
are green. Match the project's test tooling; do not introduce a second framework.

## Step 4 — Scope discipline and simplicity

- **Stay in scope.** If you spot something worth fixing outside this task, *note it* (in the
  task folder or as a follow-up) — do not fix it now. Scope creep is how plans rot.
- **Per-slice circuit breaker:** after ~3 failed attempts to get one slice green, stop and
  surface the blocker instead of grinding — repeated failure usually means the plan or an
  assumption is wrong, not the code.
- **When the plan is silent or wrong**, don't deviate silently and don't stall. If the choice
  changes nothing the user approved (which helper to reuse, a private name, the order of two
  independent steps), **record the ruling and its reason in `intake.md` and continue**. If the
  approved shape changes (missing task, wrong order, infeasible dependency, scope moving),
  route back to `blueprint`'s amendment loop and get the changed part re-approved. Unsure which
  it is, or the change is irreversible? Treat it as an amendment.
- **Large refactors:** see `any-language.md` for the codemod threshold.
- **Simplify as you go** (Chesterton's Fence): before removing or rewriting something,
  understand why it exists. Prefer the clearest version, not the cleverest. No nested
  ternaries, no premature abstraction, no code the plan didn't call for.

## Re-entry — acting on review findings (a finding is a claim, not an order)

**This is not a step in the first pass — skip it while building.** It runs when the task comes
*back* here after `verify`/`inspect`/`harden`/`design`, or when a human review lands. On a
first build there are no findings yet; looking for them is wasted motion.

`construct` is where `inspect`'s, `harden`'s, and `design`'s findings come back to be fixed —
and where a human reviewer's comments land too. **Evaluate each finding before implementing
it.** A review comment is a claim about the code, exactly like a worker's report is a claim
about a test run (§8) — the burden of verifying it does not disappear because it arrived as
feedback.

For each finding, before writing anything:

1. **Restate it** in your own words. If you cannot, you do not understand it yet — ask.
2. **Verify it against the code.** Is it true *of this codebase*, at this version, on this
   platform? Reviewers work from a diff and can miss the reason something is the way it is.
3. **Check it doesn't break something else** — an existing test, a documented decision in
   `decisions.md`, or a constraint from `spec.md`.
4. **Then implement, one finding at a time, each with its own test cycle** (Step 2's loop
   applies to fixes too — the repro or the guard test comes first).

**When a finding is wrong, say so with reasoning** — cite the code, the test, or the ADR that
contradicts it, and leave the fix undone pending the user's call. Silent compliance with a
wrong finding puts a defect in the codebase and blames the reviewer for it.

**When several findings are unclear, stop and ask about all of them before implementing any**
— findings often interact, and a partial reading produces a fix that satisfies one and breaks
another.

**When a finding contradicts an approved spec or a recorded decision**, that is not yours to
resolve: surface the conflict to the user (§7) rather than quietly choosing a side.

Never answer a review with agreement-shaped noise ("good catch", "you're right") before the
verification above — enthusiasm is not evaluation, and the user cannot tell which one they
got.

## Step 5 — Hand off with evidence

Do not declare the task done here. Update `state.json` (`construct` → in_progress/done) and
hand to `verify`, which exercises the whole thing for real and demands the evidence. Record
any durable decision (a library chosen, a pattern established) in `decisions.md` with its
*why* (§4).

## Composition

- **Consumes:** `plan.md`, `standards.md`, the matching discipline pack, project memory.
- **Produces:** working code + tests in committable slices (committed only on user approval, §12); updated `standards.md` /
  `decisions.md`; `construct` marked in the ledger.
- **Hands off to:** `verify`, which exercises the change and owns the evidence.
- **Receives from:** `blueprint` (planned task), `engineer` (BUILD phase), a direct trivial
  ask, or `inspect`/`harden`/`design` returning findings to fix (see Re-entry above).
- Invoked directly, or by `engineer` as the BUILD phase. In multi-agent mode, `engineer`
  may dispatch one worker per independent plan task (§8) — each worker runs this same loop
  on its slice — **in its own worktree/branch, or returning a diff the orchestrator applies
  serially** (§8: parallel source-writers never share one tree) — and the orchestrator
  reviews each at the checkpoint and gathers the slices for the end-of-work summary +
  user-approved commit (§12).

## Self-review (author's notes)

- *Mis-routed?* `engineer` routes here once per planned task; wrong when no plan exists and the
  work is multi-step — that needs `engineer`'s earlier phases. Pick this over `engineer` when the
  task is already scoped.
- *Single-agent safe?* Yes — the loop is inline; worker fan-out is optional and degrades.
- *Leaks specifics?* No — the test framework and conventions come from detection, not hard-code.
- *Contradicts another skill?* No — it stops before claiming done; `verify` owns the evidence.
