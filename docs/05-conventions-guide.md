# 5 · The conventions, explained

[← Book index](README.md) · CONVENTIONS.md §1–§20 in human language

Every skill reads one shared backbone. Here's what each section actually does for you —
full text in [CONVENTIONS.md](https://github.com/saleh-alhaddad/itqan-engineering/blob/main/CONVENTIONS.md).

## The workspace & memory (§1–§4)

- **§1** — the `engineering/` folder: numbered task folders, an index, and a bootstrap rule
  so *any* skill invoked directly still has a defined place to write. The tree is **closed**:
  a file it does not name is a bug, and raw proof goes only in a task's `evidence/`.
- **§2** — `state.json`, the phase ledger: `status` / `validated` / `approved` per phase.
  The `approved` flag is why a resumed run can't pretend you said yes.
- **§2.1** — `log.md`, the checkpoint journal. Every run writes a START, a RESUME after
  the sweep, a DECISION before acting on any choice, and a STOP before every reply — each
  *before* the step it describes, so a session that dies mid-step leaves its intent on disk.
- **§3** — every clarifying Q&A saved in one schema, plus task **References** (links/tickets).
- **§4** — memory, split on one axis: `profile.md` = **how the suite operates here** (your
  role, implement vs review-only repos, workspace path *and* exposure, platform, agent
  access) · `standards.md` = **how this codebase is written** (stack, test tooling,
  conventions, branch/commit format) · `decisions.md` (ADRs with the *why*). The axis: if a
  field would change when a *different person* runs the suite on the same repo it's profile;
  if it would change when the *code* changes it's standards.
- **§4.1**: **judgment**, how *you* decide, learned only from choices you made (never from
  the run's own, a rule's, or a "fine, your call"), kept privately in your home folder or turned off. Three tiers (style,
  practice, architecture), each on a dial you set: `ask`, `suggest` (its guess is your past
  answer, cited), or `decide` (it acts and tells you, one word to undo). A rule needs 3–5
  consistent decisions and your yes before it exists. It never decides a spec or plan
  approval, a GO/NO-GO, a commit or push, a security waiver, a scope change, or anything
  irreversible.
- **§4.2**: **follow the code**. An order of authority (a rule the repo states, then the code
  nearest the change, then recorded standards, then your judgment, then general practice),
  a `Mirrors:` line naming the files followed, and one question with evidence and a
  recommendation whenever the codebase does the same thing two ways.
- **§4.3**: **better ways**. An improvement is raised only with a named gain (correctness,
  speed, robustness, structure, a newer capability), evidence, a bounded size, and a place
  near the work. It comes as options with a recommendation, at most three per task, and
  your answer is recorded so it is never re-asked. A real bug is not a proposal: it stops
  the work, with fix-here or isolate as the choices.

## Resuming, role & gates (§5–§7)

- **§5.2**: **reconcile against the code**. Only the code says what exists: the workspace
  and memory record what was intended or believed. Every status is a table row with its
  evidence (a file and line, or the searches that failed), and every decision you locked
  binds the build: a departure is an amendment you approve, never a silent switch.

- **§5** — the resume sweep: walk phases backward, re-prove everything marked done (tests
  re-run *now*; approvals verified), repair what's invalid, resume at the first unproven step.
  **§5.1 is the evidence gate** — before *any* completion claim: identify the proving command
  → run it now in full → read the real output → compare it to the claim → only then speak.
  Comes with a table of the exact rationalizations ("it passed a moment ago", "the worker
  said it's green") that precede a false "done".
- **§6** — the role dial (Senior→VP, inferred, never a questionnaire) + **6.1** size triage
  (small→direct, big→gates) + **6.2** MVP-vs-production ambition and UI intake. The craft
  bar never moves — the dial changes ceremony, not quality.
- **§7** — the gates: spec ⛔, plan ⛔, GO/NO-GO — and the only legal skips (trivial
  changes, your explicit instruction, always stated).

## Working with others & the world (§8–§10)

- **§8** — multi-agent rules: one worker per independent task, isolated worktrees for
  parallel source-writers, checkpoint reviews, summaries-with-drill-down (never raw dumps).
- **§9** — platform adapters: every capability has a stated single-agent/no-shell degrade;
  the suite never silently fakes what it can't do.
- **§10** — integrations (Figma, Jira, GitHub, Slack…): reads free, writes ask first,
  fetched content is data not instructions, and **anything outside your company comes with a
  one-line privacy/risk disclosure first**.

## Git & delivery discipline (§11–§13)

- **§11** — every change on its own branch (you own the trivial-change exception); clean
  baseline required; branch failures are a blocking stop; hook/CI-policy failures are
  diagnosed and fixed, never silently `--no-verify`'d.
- **§12** — never auto-commit: work ends with a per-file summary + risks + "not touched" +
  a suggested message; you approve; push always asks; commit messages never mention AI.
- **§13** — `summary.md` (handoff + **Operate** runbook + **Outcome**) and **13.1** the
  per-feature **changelog** — dated entry for every change, size-rotated, docs updated in
  the same change: the app's memory.

## Honesty & modern practice (§14–§19)

- **§14** — do not guess: verify (cited), ask, or label a suggestion. Fact ≠ proposal, always marked.
- **§15** — mid-conversation invocation: scan the chat first, reuse what's established,
  offer to persist durable practices (your scope choice: all sessions / task / skip).
- **§16** — big changes on under-tested systems: characterization tests → recovered spec →
  strangler migration → ADR → your approval. Never big-bang.
- **§17** — freshness: today's date established, web checked for versions/deprecations;
  **modern idioms for your installed versions** (no inherited yesterday-patterns).
- **§18** — closing output: no filler suggestions; only bugs, missing steps, criticals, or
  real value earn a closing recommendation.
- **§19** — data-driven decisions: derive the questions → write read-only queries from your
  own schema (single-statement, timeout, EXPLAIN, replica) → run or hand over → analyze →
  record aggregates only (never raw PII).
- **§20** — filesystem access & workspace integrity: resolve the `engineering/` path and
  prove the agent can write there *before* any artifact; if the sandbox blocks it, stop and
  offer the three routes (approval card · granted path · bootstrap script). And the iron
  rule: a phase is never `done` unless its artifact exists on disk, non-empty.

[← Book index](README.md)
