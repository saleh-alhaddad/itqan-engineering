---
name: assess
description: >-
  Whole-app health report from a panel of experts — how the features connect, which are
  strong, which are weak, and what to improve, with market evidence. App-level, not diff-level.
disable-model-invocation: true
---

# assess — the expert panel over the whole app

Judge the application the way a seasoned leadership review would: several experts, one
honest report. Read [CONVENTIONS.md](../../CONVENTIONS.md) — especially the workspace and
changelog (§1, §13.1 — the app's memory tells you *why* and *when*; only the code tells you
*what exists*, §5.2), the role dial (§6), the resume sweep (§5), git isolation (§11),
gates (§7), multi-agent rules (§8), platform adapters (§9), grounding (§14), freshness
(§17), closing output (§18), and data-driven decisions (§19), and the ledger (§2), judgment (§4.1), workspace integrity (§20).

**Journal every run (§2.1).** The first write of the run, once the task folder is resolved
(§20.1), is a START entry in the task's `log.md`; then set this phase `in_progress` in
`state.json`. Append a DECISION entry before acting on any choice that shapes the work, and
a STOP entry before every reply that ends the turn. Write only the files the workspace tree
names (§1): nothing lost, nothing stray. Before asking a question or deciding, check the
user's judgment (§4.1) for a confirmed rule that covers it, and journal who decided.

**Boundary with `discover`:** `assess` judges the features that exist; when its conclusion
is "we need net-new X", hand that to `discover` (or straight to `define` if the user already
chose). Don't run both from one ambiguous ask — existing-feature health leads here. If a run
is already active, read `state.json.mode` for the multi/single answer instead of re-asking.

## Step 1 — Two questions, once

1. "Run the expert panel as **multiple parallel agents**, or **one agent playing all
   roles** in sequence?" `[multi/single]` (single-agent runtimes: always inline, §9)
2. "Do you want a **report only**, or **report + a throwaway prototype** of an improvement
   you pick from it, so you can feel it before deciding?" `[report/report+prototype]`

## Step 2 — Build the evidence base

Scan the repo, `engineering/` (profile, decisions, **feature changelog**), docs. Build the
**feature map from the code**: every feature named with where it lives (file:line, route,
table), and every "missing", "dead" or "unused" claim with the searches that found nothing,
run two ways (§5.2). The changelog explains a feature's history; it never proves the feature
is there, wired up, or working. For
usage/business numbers, **measure before asking** (§19): derive the questions, write
read-only queries from the app's own schema, run them via a connected data tool or hand them
to the user to run — and ask only for what can't be measured (§14, never invent). Map the
feature inventory and how features connect (data flows, shared models, entry points).

## Step 3 — The expert panel (five lenses)

Each lens reviews the same evidence and reports findings *with the evidence cited*:

- **Domain expert** (of the app's own field — detected from the product): does each feature
  serve the domain's real workflows? What would a practitioner miss or distrust? A claim
  about how the domain works cites a source checked in this run, or becomes a question for
  the user; never a workflow described from memory as fact (§14).
- **Software engineer**: architecture health, feature coupling, test coverage of core flows
  (from a coverage run in this run, §5.1, or said to be unmeasured), fragile or dead areas
  (structural signals only — line-level review belongs to `inspect`).
- **Product (PM)**: completeness of each feature's journey (empty/error/edge states,
  onboarding, discoverability), features that exist but don't compose into outcomes.
- **Market analyst**: how the feature set compares to the market **as of today's date —
  web-researched and cited (§17)**; table-stakes gaps; where competitors are stronger. If
  the market is unknown, ask the user or research — never fabricate competitors (§14).
- **Improvement lead**: synthesizes the others into ranked, feasible improvements
  (value vs. effort), separating quick wins from structural bets. **Value** is tied to
  measured usage (§19) or a goal the user stated; **effort** to the files and callers counted
  in this run. Either one that cannot be grounded is written `unestimated`, not guessed.

In multi-agent mode dispatch the lenses in parallel and merge; the orchestrator owns all
writes (§8). In single mode, run the lenses sequentially with fresh eyes per lens.

## Step 4 — The report (only what's good and what needs work)

Write `assessment.md` in a task folder (bootstrap per §1):

```
# App assessment — <app> · <date>
## Feature map            — features and how they link (a simple diagram helps)
## Strong                 — what's genuinely good, and why (evidence)
## Needs improvement      — ranked: what's weak/thin, why it matters, the concrete fix,
                            which expert flagged it, value vs. effort
## Market position        — cited comparison; table-stakes gaps
## Recommended next moves — the 1–3 to do first
```

No filler: every line is evidence-backed, or labelled an **unverified suggestion with how to
confirm it** (§14). "Expert judgment" is not a label that makes a claim true: the panel is
the model, and a verdict under **Strong** or **Needs improvement** always cites its evidence.
If a prototype was requested, present the report first; the user picks which improvement to
spike, and `construct` builds it on its own branch or worktree (§11), clearly disposable
(§6.2). `assess` itself never edits the source.

## Step 5 — Close the loop

Present the report. If the user wants changes: hand the chosen improvements to `define` →
`blueprint` and **stop at the plan-approval gate** as always (§7). If no changes are needed,
record the assessment date and outcome in `decisions.md` and stop.

## Composition

- **Consumes:** the repo, `engineering/` memory + changelog, web research (cited), the
  user's usage/business context.
- **Produces:** `assessment.md` and an ADR note. A prototype, if asked for, is built by
  `construct` on its own branch (§11), for the improvement the user picks.
- **Receives from:** the user directly, or `engineer` when the intent is whole-app analysis.
- **Hands off to:** `define`/`blueprint` for approved improvements. Distinct from `inspect`
  (a diff, code-level) and `discover` (net-new features/tools).

## Record the phase (§2)

`assessment.md` on disk and non-empty (§20.2) comes first; then record an `assess` entry in
the task's `state.json` (§2's optional phases) — `done` + `validated` + the artifact name.
Directly invoked, no orchestrator will do it for you.

## Guard — every verdict needs its evidence

**These thoughts mean stop — you are about to grade a feature on impression:**

| The thought | The reality |
|---|---|
| "This feature feels weak" | On what? The changelog, measured usage, or a cited market comparison — name it (§14, §19). |
| "The app looks fairly complete" | Complete against the product's stated goal, not against your sense of a finished app. |
| "I should recommend some improvements" | An honest "nothing here is worth changing yet" is a valid report (§18). Invented improvements cost the team real quarters. |
| "Competitors all have this, so it's table-stakes" | Cite the competitors you actually checked, at today's date (§17). "Everyone has it" is the shape of a guess. |
| "Usage data isn't available, I'll estimate" | Never invent a number. Say the data is missing, hand over the query that would answer it, and label the verdict provisional. |

## Self-review (author's notes)

- *Mis-routed?* `engineer` routes here for whole-app analysis; wrong when the ask is really one
  diff (`inspect`), net-new ideation (`discover`), or a UI-only audit (`design`). Pick this over
  `inspect` when the unit of review is the product, not a change.
- *Single-agent safe?* Yes — the panel runs as sequential lenses inline.
- *Leaks specifics?* No — the domain expert is instantiated from the detected product.
- *Grounded?* Market claims cited per §17; unknown numbers asked, never invented.
