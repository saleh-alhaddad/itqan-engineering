# Contributing

Bug reports, fixes, and new discipline packs are all welcome. This file explains how the
suite is built so a change fits in rather than fights it.

## Report a bug

The most useful report has four things: **your OS and shell**, **which skill you invoked**,
**what you expected**, and **the literal error text**. A copied error string is worth more
than a paragraph describing one. Bugs that break a first run get priority.

## The architecture in one minute

- **`CONVENTIONS.md`** is the shared backbone — 20 numbered sections holding every rule that
  more than one skill needs. Every skill loads it whole.
- **`skills/<name>/SKILL.md`** is one skill: YAML frontmatter (`name`, `description`) plus an
  imperative body. Skills describe *actions*, never a specific runtime's tool names.
- **`references/disciplines/*.md`** are packs loaded only when the detected stack or concern
  matches — stack packs (backend, frontend, mobile, ai-ml, any-language) and concern packs
  (database, security, devops, browser-verify, ui-craft).
- **`engineering/`** is the runtime workspace the suite creates *in the user's project*, never
  in this repo.

## The rules that govern changes here

**Define once.** A rule that two skills need lives in `CONVENTIONS.md` and is cited by `§N`,
never copied into both. A rule only one skill needs lives in that skill. If you find yourself
writing the same sentence twice, it belongs in the backbone.

**Every rule must be reachable.** A rule nobody reads is worse than no rule, because it looks
like coverage. Before adding one, name the skill and the step that will act on it — and if a
skill cites `§N`, its header read-list must declare `§N` too. **CI enforces this**; a body
that cites an undeclared section fails the build.

**Every field must be read.** If you add a field to `profile.md`, `standards.md`, `plan.md`,
or `state.json`, some skill must consume it in the same change. A written-but-never-read field
is the most common defect in this repo's history.

**Rules state what to do, and pre-empt the excuse for not doing it.** The strongest rules here
carry an *iron rule* line and a short table of the specific rationalizations that precede
breaking it (see §5.1, §7, §12, §14, §20.2). A rule the model can talk itself out of is a
suggestion. When you add a load-bearing rule, add the table.

**Evidence, not assertion.** The suite's core promise is that nothing is claimed done without
fresh proof (§5.1). Any change that would let a claim through without evidence — a shortcut,
a cached result, a delegated report treated as fact — will be rejected however convenient it
looks.

**Markdown only, in skills.** Skills contain no executable code, so they run identically on
every runtime. Scripts belong in `templates/` (generated for the user to run) or
`.github/scripts/` (CI). Nothing the agent reads as instruction is executable.

**No named products as requirements.** Frameworks, vendors, and tools appear as *examples*
tied to a detected stack, never as something the suite assumes. The suite adapts by reading
the repo.

## Adding or changing a skill

1. **Check it isn't a phase that already exists.** Twelve skills cover the lifecycle; most new
   ideas are a step inside one of them, not a thirteenth skill. Adding a phase changes the
   ledger, the sweep, and the orchestrator — propose it in an issue first.
2. **Write the frontmatter for a human choosing from a list.** The `description` is browsing
   text — what it does, plus one clause distinguishing it from its nearest neighbour. Not
   trigger phrases: the suite is invoked explicitly, never auto-triggered.
3. **Keep the body imperative and under ~300 lines.** State what to do, in order.
4. **Declare your sections.** List every `§N` the body cites in the header read-list.
5. **Fill in the standard blocks** — `## Composition` (Consumes / Produces / Hands off to) and
   `## Self-review (author's notes)`, including the `*Mis-routed?*` line: when would the
   orchestrator route here and be wrong, and when would a user pick this over its neighbour?
6. **Degrade gracefully.** If a capability is missing (no subagents, no shell, no version
   control), name the degrade in one line and continue. The suite never hard-fails because a
   runtime lacks a tool.

## Adding a discipline pack

Packs are lazy — they cost nothing until the stack matches. Follow the existing shape: one
section per lifecycle phase (`In DEFINE`, `In BUILD`, `In VERIFY`, `In REVIEW`, `In SHIP`)
containing only what is *specific to that surface*. Anything true of all code belongs in
`any-language.md` or the backbone, not in a pack.

## Working on the suite while using it

Do **not** commit a `.claude/settings.json` that enables this plugin at project scope. It
looks helpful and is a trap: project scope wins over user scope, so anyone working inside this
repo silently runs whatever version that resolves to — which can be an older cached build than
the files they are editing. Enable the plugin once at user scope and let the repo stay silent
about it, so the version you run is the version you chose.

## Before you open a PR

```bash
python3 .github/scripts/validate.py
```

It checks manifest validity, frontmatter completeness, description length caps, that every
internal link resolves, that no commit or file carries AI attribution, and that every skill
declares the sections it cites. Green is required.

Then confirm by hand what CI cannot: **is the new rule reached by a runtime step, and is every
new field consumed by something?**

## Commit and PR conventions

- Small, single-purpose commits. One behavioural change per commit.
- The message describes the change and nothing else — **no AI attribution trailers**, no
  "Generated with…". CI rejects them.
- Bump the version in both `.claude-plugin/plugin.json` and `marketplace.json` together.
- Update the docs in the same change. Documentation that describes an older behaviour is
  worse than none, because it is believed.
