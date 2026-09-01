# Workspace bootstrap & access playbook

Referenced by `engineer`, `define`, `blueprint`, and `construct` (CONVENTIONS §20). Use this
when the `engineering/` workspace must be created, repaired, or the runtime blocks writes.

## 1 · Integrity checklist (what must exist on disk)

| Scope | Required, non-empty |
|---|---|
| `engineering/` root | `profile.md` · `standards.md` · `decisions.md` · `index.md` |
| every `tasks/NNNN-<slug>/` | `intake.md` · `state.json` · a row in `index.md` |
| after define | `spec.md` |
| after blueprint | `plan.md` |
| after inspect / harden / design | `review.md` / `security-review.md` / `design-review.md` |
| at close-out | `summary.md` |

A ledger phase is `done` only when its file is on disk (§20.2). Missing-but-marked-done ⇒
downgrade to `in_progress`, repair from chat/ledger content, then continue.

## 2 · When writes are blocked (sandbox / admin policy)

Probe first with **file tools, not shell**: write `<engineering>/.write_probe`, confirm it
exists, delete it. Real write, really verified (§14) — no shell, no platform assumption.
Shell-only runtime? Use the detected platform's syntax (§9): `touch`/`&&` do not exist on
PowerShell or `cmd.exe`. **A command-not-found is not a permission denial** — fix the syntax
and re-probe before concluding anything is blocked.

If genuinely blocked, **stop** and tell the user which path is blocked, then offer in order:

**a. Approval card** — retry the write via shell so the runtime shows its approval card
(Cursor: the Auto-review card). Say exactly: *"Cursor blocked writes to `<path>` — approve
the next command in the approval card to continue."*

**b. Grant the path durably** — print the snippet for the user to add:
```jsonc
// .cursor/sandbox.json
{ "additionalReadwritePaths": ["<absolute engineering/ path>"] }
```
(Other runtimes: their equivalent allow-list; name the file if known, otherwise say so.)

**c. Bootstrap script** — instantiate the template matching the detected platform (§9) —
`templates/bootstrap-engineering-workspace.sh.tmpl` on POSIX,
`templates/bootstrap-engineering-workspace.ps1.tmpl` on Windows — into a **writable** repo
(e.g. `<repo>/scripts/`), show it to the user, run it with their approval. Idempotent — safe
to re-run; preferred for bulk creation.

After any route succeeds: **list the directory and confirm the files** before claiming
anything was created (§14). Record the working route in `profile.md` → `Agent access:`.

## 3 · Placement & exposure reminder

Two one-time choices, asked together at first run and never re-asked (§20.1, recorded per
§4). **Where:** per-repo, or shared in the parent folder of several repos (a `docs/` repo
hosting it is common). **Exposure:** if it sits inside a repo, committed (team-visible
through git) or gitignored (private to this machine) — this decides who else can read the
user's specs and intake records, so it is asked, never assumed.

Record the absolute path in `profile.md` under `engineering/ at:`, the answer under
`Workspace exposure:`, and which repo plays **workspace host** in the profile's repo roles.
