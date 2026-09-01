# 4 · Playbooks — end-to-end scenarios

[← Book index](README.md) · real situations, start to finish

## Playbook 1 — New full-stack app from scratch

```
itqan:engineer "build a task-management SaaS — Next.js, teams, boards, due dates"
```
1. Greenfield detected → establishes standards (you approve) → **initial commit** (with your OK) so branching/worktrees work.
2. `define` intake → asks UI direction; no Figma? `design` shapes it → `design.md`. Spec ⛔.
3. `blueprint` → risk-first plan (auth and data model early) ⛔.
4. Loop mode: task-by-task TDD build, commit gate between tasks (or your explicit auto-commit opt-in).
5. `harden` fires automatically (auth = security-sensitive). `release` per milestone.

**You end with:** a working app, a full `engineering/` history, and a changelog explaining every choice.

## Playbook 2 — Production bug

```
itqan:engineer "orders sometimes lose their discount — find how often and fix it"
```
1. Fix-intent on a running system → **§19 evidence first**: it writes read-only queries from your schema → *"0.4% of orders since May 12, all with stacked coupons."*
2. `verify` Part B: repro narrowed → **pinned as a failing test** → `git bisect` fingers the commit.
3. Smallest fix at the root → repro test goes green → guards forever.
4. Change summary + risks → your commit → `release` (fast path) → **Outcome:** re-run the query, rate = 0%.

## Playbook 3 — Reviewing a teammate's PR

```
itqan:verify  "check out PR #482 and confirm nothing breaks"     # evidence first
itqan:inspect "review PR #482 — logic, spaghetti, security, perf, cross-service"
itqan:design  "UI review of the changed screens"                  # only if UI changed
```
You post the ranked findings; the author fixes; `inspect` re-checks only the changed part.
Never use `construct` here — that would be taking over their PR.

## Playbook 4 — Multi-repo team (e.g. folder `a/` holding repos `b/` and `c/`)

1. First run asks the **setup intake** once: which repos are *implement* vs *review-only* ·
   scope (all / ask per task / one) · branch + commit format · where `engineering/` lives
   (shared in `a/` or per-repo) · and whether it's committed or gitignored — on a team repo
   that decides who reads your specs. Operating answers go to `profile.md`, codebase answers
   to `standards.md` (§4's axis). Never re-asked.
2. Every task then honors it: review-only repos are a hard write-boundary; each change on
   its own branch in the right repo; docs/changelog recorded in the repo they describe.
3. Teammates get context instantly: `learn "onboard me onto this repo"` reads the changelog.

## Playbook 5 — "Make it look professional" (UI)

```
itqan:design "audit the dashboard — spacing, hierarchy, states, accessibility"
```
→ `design-review.md` with evidence-based findings (violated token + impact + fix). Approve
the fixes → `construct` applies → `verify` proves states + a11y in a real browser (console
clean, a11y tree) → UI Criticals gate the ship like code Criticals.

## Playbook 6 — Pre-launch security pass

```
itqan:harden "full security review before public launch"
```
→ 5-step threat model (assets → entry points → actors → trust boundaries → STRIDE each) →
OWASP/LLM checklists → **variant analysis** (classes, not instances) →
ranked `security-review.md` → Critical/High fixed via construct→verify → re-audit →
`release` will not GO over an open Critical. Waivers require your explicit recorded acceptance.

## Playbook 7 — Quarterly product thinking

```
itqan:assess "which features are weak, vs the market?"      # health of what exists
itqan:discover "what should we build next?"                  # net-new, fed by assess's output
itqan:define …  → blueprint … → the quarter's build begins with approved specs
```

[← Book index](README.md)
