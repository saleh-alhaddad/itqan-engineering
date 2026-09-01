# 6 · FAQ & troubleshooting

[← Book index](README.md)

## Install & update

**`SyntaxError: Unexpected reserved word` when running `npx skills add`?**
Your Node is too old (needs ≥ 22.20; the `EBADENGINE` warnings above the error say so).
Fix: `nvm install 22 && nvm use 22`, or use the guided installer which handles it:
`curl -fsSL https://raw.githubusercontent.com/saleh-alhaddad/itqan-engineering/main/install.sh | bash`

**How do I update / remove?** See [chapter 2](02-installation.md#updating) — per-platform
commands for both. Removal never touches your projects' `engineering/` folders.

**The repo is private — can my team install?** Yes, with repo access: Claude Code via the
SSH URL, or plain git clone. The public one-liners start working the moment it's public.

## Using the suite

**Why is it asking me questions instead of just coding?**
Because wrong-thing-fast is slower than right-thing-once. Each question carries a guess —
answer in one word. Trivial changes skip the ceremony entirely (size triage).

**Why didn't it commit my changes?**
By design — it *never* commits without your approval. You get a per-file summary + risks +
a suggested message; say yes, adjust, or decline. (Loop mode has an explicit hands-off
opt-in.)

**It said "cannot verify — no execution capability." Is it broken?**
No — that's the honesty rule working. It won't claim a green it didn't see; it hands you
the exact command to run instead.

**Which skill do I call?**
Rule of thumb: know exactly what & small → `construct` · know what, not how → `engineer` ·
don't know what → `discover`/`define` · judge existing → `inspect`/`design`/`assess`/`harden`
· prove → `verify` · ship → `release`. Full map in [chapter 3](03-getting-started.md).

**Multi-repo: where does `engineering/` go? Which repo gets the code?**
The one-time setup intake asks exactly this — workspace location *and* exposure (committed
or gitignored); implement vs review-only repos; scope — and records it in `profile.md`, the
file holding how the suite operates here (§4's axis). See [Playbook 4](04-playbooks.md).

**Can it touch my production database?**
Reads only, and only safely: read-only role on a replica, statement timeout, `EXPLAIN`
first, single-statement queries, aggregates-only in any saved artifact. It never writes to
production data, ever.

**Does it work without subagents / without a shell?**
Yes — every capability has a stated degrade: phases run inline; reviews become fresh-eyes
self-passes; verification without a shell honestly reports "cannot verify" instead of faking.

**A teammate's `git pull` of this repo failed after an update.**
History was rewritten during early development (amended commits). One-time fix:
`git fetch && git reset --hard origin/main` — or remove + re-add the marketplace.

**Where do I report issues or contribute?**
Open an issue/PR on the repo — and read [CONTRIBUTING.md](https://github.com/saleh-alhaddad/itqan-engineering/blob/main/CONTRIBUTING.md) first: it
carries the architecture, the authoring rules (define once, every rule reachable, every
field consumed), and the PR checklist CI will hold you to. CI validates structure, links, description caps, the installer, no AI attribution, and
that every `§N` a skill's body cites is declared in its header read-list — on every push;
your PR gets checked automatically.

[← Book index](README.md)
