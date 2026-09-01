---
name: blueprint
description: >-
  Turns an approved spec into an ordered, dependency-sorted task plan with a shape decision
  per task. Implementation planning, not product roadmap planning.
disable-model-invocation: true
---

# blueprint — spec to ordered task plan

A plan's job is to make the build boring: a sequence of small, ordered steps, each of which
leaves the system working and can be checked on its own. You are turning the *what* (the
spec) into an executable *in-what-order*, without writing the code yet.

Read [CONVENTIONS.md](../../CONVENTIONS.md) for the workspace (§1), the resume sweep (§5), git isolation (§11), the ledger (§2), the
intake schema (§3), memory (§4), the role dial (§6), gates (§7), multi-agent rules (§8),
commit policy (§12 — Status is the resume marker), freshness (§17), and workspace
integrity (§20).

## Step 1 — Read the spec and the standards

Load `spec.md` and `standards.md`. Every task you produce must trace back to a success
criterion in the spec, and must fit the project's established conventions. If a success
criterion has no task, or a task serves no criterion, fix the mismatch before continuing.

## Step 1b — Validate the dependency reality

Before cutting tasks, check what the plan will lean on — surprises here become release/test
failures later: are the libraries the plan assumes actually in the manifest? Are their
versions current and supported (web-check with today's date when unsure, §17)? Does the plan
call any **deprecated API/method**? Is a needed capability missing entirely (a task must add
it)? Flag findings in the plan so no task builds on a dependency that isn't really there.

## Step 2 — Decompose into vertical slices

Break the work into **thin vertical slices** — each slice delivers a small piece of working,
testable behavior end-to-end, rather than a horizontal layer that can't be exercised alone.
Size each task; anything large enough to hide surprises gets broken down further. Order the
tasks by dependency: a task appears only after everything it needs is already built. Within
that ordering, schedule the **highest-risk / highest-uncertainty tasks first** — fail fast
where failure is cheapest. Split heuristics: an "and" in the title, more than 3 acceptance
bullets, or two independent subsystems means it's two tasks.

For each task capture:
```
### Task NN — <short title>
Goal:        <the behavior this delivers>
Consumes:    <what must exist first — prior tasks, interfaces, data>
Produces:    <the interface/behavior it leaves behind for later tasks>
Acceptance:  <the observable check that proves this task is done — a test can assert it>
Shape:       <which files this touches or creates · new abstraction vs reuse-and-pass-args,
              with the reason. Genuinely ambiguous (new base class vs reuse + arguments)? Put
              BOTH options and the trade-off here — the approval gate only works on a choice
              the user can see>
Size:        <XS | S | M | L>  (break down anything L)
Status:      todo   (construct updates this to in-progress → done as the slice goes green —
                     it is the resume marker now that slices aren't committed individually, §12)
```

The **Consumes/Produces** fields are what let each task be built and reviewed in isolation —
and what let worker agents run in parallel where the dependency graph allows.

## Step 3 — Write `plan.md`

Write the ordered task list to `plan.md` in the task folder. Lead with a one-line build
sequence, then the task detail. Mark which tasks are independent (parallelizable) and which
are strictly sequential — `engineer` uses this to decide fan-out.

At higher roles (Principal/VP), also note the invariants the plan must preserve and any
architectural decision worth an ADR entry in `decisions.md`.

## Step 4 — Write to disk, verify, then update the ledger

The plan is not done when it exists in chat — **write `plan.md` to disk, list the file to
verify it exists non-empty** — then run Step 4b's fresh-eyes pass against the file you
just wrote, and only after it passes set `blueprint` in `state.json` (§20.2). Close
with the artifact checklist so the user sees reality, not claims:

```
Task artifacts on disk: intake.md ✓ · spec.md ✓ · plan.md ✓ · state.json ✓
```

For multi-repo workspaces, every task in the plan names its **target repo** (`Repo:` line) —
per the profile's implement/review-only roles (§4).

## Step 4b — Fresh-eyes pass, before you present it

**Review the plan as if someone else wrote it, reading only `plan.md` and `spec.md`.** You
know what you meant by each task; the file is all the builder gets, and a step you can fill
in from memory is a step that isn't written down. In multi-agent mode dispatch a fresh reader
that never saw the decomposition (§8's five-field brief; `Output:` is the answers below).
Single-agent, re-read the two files alone — not the conversation — and check:

- Does every spec success criterion map to at least one task? Does every task serve one —
  **except setup/scaffold tasks, which serve all of them and map to none?** A greenfield plan
  legitimately opens with "create the project", and a check that flags it teaches you to
  ignore the check.
- **Could someone else build each task from its `Goal` / `Acceptance` / `Shape` alone**,
  without asking you what you meant? That is the actual bar — worker agents and your
  colleagues both get only the file.
- Does any task contain a placeholder or a hand-wave ("handle errors somehow")? Replace it.
- Are the Consumes/Produces interfaces consistent — does each task's Consumes match a prior
  task's Produces?
- Is anything ordered wrong (a task needing something built later)?

Fix what this finds **before** presenting — an approval gate only works on a plan the user
can actually evaluate.

**These thoughts mean stop — you are about to present a plan that hides its decisions:**

| The thought | The reality |
|---|---|
| "The order is obvious" | Then writing it costs nothing. If it isn't, the builder guesses. |
| "I'll figure out the shape while building" | `Shape` exists so the structural choice is visible **at the gate** — deciding it mid-build means the user approved something else. |
| "This task is big but splitting is fussy" | Anything L gets broken down. A task that hides surprises is where plans rot. |
| "The risky part can come last" | Risk-first, always: fail where failure is still cheap. |
| "The user will just approve it anyway" | That is the reason to make it evaluable, not the reason to skip it. |

## Step 5 — Approval gate

Present the plan and get explicit approval before building starts. Record it in `intake.md`
(§3) and set `blueprint.approved: true` in `state.json` (§2). **Do not begin `construct`
until the plan is approved.** A `plan.md` on disk with `approved:false` is not done — a
resumed run will re-present it, not build from it. If the user is absent, leave
`approved:false` and stop.

## Plan amendments (when build reality disagrees)

Plans meet reality in `construct`. Deviating silently and stalling are both failure modes;
the amendment loop is the correct third path — but not every surprise deserves the full loop.

**Separate a ruling from an amendment**, or the plan gates start firing on trivia and the user
learns to approve without reading:

- **A ruling** — the plan is silent or ambiguous, and the choice changes nothing the user
  approved: which helper to reuse, what to name a private function, the order of two
  independent steps. **Record the decision and its one-line reason in `intake.md`, then
  continue.** No re-approval; the ledger carries the ruling so a resumed run and a reviewer
  can both see what was chosen and why.
- **An amendment** — the *approved shape* changes: a task is infeasible, mis-ordered, or
  missing; scope moves; an interface the spec named changes. Amend `plan.md` (change only what
  must change), **bump a plan version note** (v2, with a one-line reason), get the **changed
  part re-approved** (§7 — the original approval doesn't cover a different plan), and record it
  in `intake.md`.

**When unsure which it is, it is an amendment.** And anything destructive or irreversible —
dropping a feature, deleting data, changing a public contract — is always an amendment, never
a ruling, however obvious it looks from inside the build.

## Composition

- **Consumes:** `spec.md`, `standards.md`, project memory.
- **Produces:** `plan.md`, the `blueprint` phase marked done+validated in `state.json`, and
  any new ADR entries in `decisions.md`.
- **Receives from:** `define` (approved spec), `engineer` (PLAN phase), or `construct` when
  build reality forces an amendment.
- **Hands off to:** `construct`, which builds each task TDD-first in plan order.
- Invoked directly, or by `engineer` as the PLAN phase.

## Skip rule

For a trivial one-step change, skip planning (§7) — note the skip and let `construct` handle
it directly with a single implicit task.

## Self-review (author's notes)

- *Mis-routed?* `engineer` routes here once a spec is approved; wrong for a self-contained
  one-liner, which `construct` handles directly. Pick this over `discover` when the *what* is
  settled and only the order is open.
- *Single-agent safe?* Yes — it only reads, decomposes, and writes a plan file.
- *Leaks specifics?* No framework or product is named; conventions come from `standards.md`.
- *Contradicts another skill?* No — it stops at approval and never writes production code.
