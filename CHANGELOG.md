# Changelog

All notable changes to the itqan engineering skills suite.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [SemVer](https://semver.org/).

## [0.0.9] — 2026-09-29

### Added
- **Better ways are proposed, never imposed (CONVENTIONS §4.3).** When the run sees that code it follows or touches could be done better, it raises a proposal only if it clears four bars: a named gain (correctness, speed, robustness, structure, or a newer capability; "cleaner" alone is taste), evidence (a measurement, a failing case, or a documentation link checked against today's date), a bounded size (migrations and rewrites go through §16 or `discover`), and a place near the work.
- Each proposal comes with options (keep the current way; new code only; apply to what the task touches; record a follow-up) and the run's pick with its reasons. New-code-only is not offered where it would put two ways in one file, or add a third. At most three per task, ranked by gain; the rest go to the close-out's follow-ups.
- The answer is recorded so it is never re-asked: a chosen direction in `standards.md` and `decisions.md`, a decline in `standards.md` with its date and reason, raised again only on new evidence. Judgment never decides these.
- **Defect or proposal** is decided by one test: if following the current code would make what this task delivers return wrong results, lose data, or be exploitable, it is a defect and stops the work, with evidence and the choice of fixing it here or isolating it. Copying it is never an option, and defects are checked before any reuse. A latent risk, such as an API deprecated upstream, is a proposal.
- If the code already does what a task asks, the run says so before building: reuse, wrap, or say what differs.
- `blueprint` carries proposals in the plan's `Shape` so they are decided at the gate; `construct` raises them instead of applying them; `inspect` writes better-way suggestions as proposals. Validator guards for the bar, the limit, the record rule, and the judgment floor, each proven to fail when removed.

### Verified
- Two blind runs on a real test repository with three genuine opportunities (a query per loop iteration, a deprecated URL API, duplicated pricing logic) and two temptations (a style preference, a migration to an ORM). Both runs raised exactly the three and excluded both temptations with the right rule. Unprompted, the first also found a real defect that was not planted (money computed in floating point, and a numeric column that the driver returns as a string would concatenate instead of add), and noticed the task duplicated an existing function. Its report led to the defect-or-proposal test above; the second run applied it correctly.

## [0.0.8] — 2026-09-29

### Changed
- The guided installer is now run from a clone (`git clone …` then `./itqan-engineering/install.sh`), never fetched from a URL. README, the installation chapter, the FAQ, and the script's own usage header all say so, and no remote-script URL remains in the repository. 0.0.4 had already stopped piping the script into a shell, but downloading it and then running it is still fetching remote code to execute: the one item behind the HIGH rating from Gen Agent Trust Hub (re-audited 2026-09-25). The installer itself is unchanged, and still installs through `npx skills add` or `git clone`.

## [0.0.7] — 2026-09-29

### Added
- **Follow the code (CONVENTIONS §4.2).** An explicit order of authority for how code is written: a rule stated on purpose (lint config, documented convention, ADR, deprecation note, or the user's ruling in `standards.md`), then the code nearest the change, then recorded standards, then the user's judgment, and only then discipline packs and general practice. Discipline packs now say so themselves.
- **`Mirrors:`**, naming the existing files new code follows and anything deliberately not taken from them, in the plan's `Shape`, the journal, and the change summary. A claim to have followed the codebase without a named file is not evidence. `inspect` checks new code against its `Mirrors:` line.
- **When the codebase has two ways, it asks and recommends.** Never picks silently, blends, or adds a third. Each way is shown with where it is used, the date of its latest change, any stated signal, and whether the task's files use it, with a recommendation ranked by stated rules, then the files being edited, then the direction of travel, then prevalence, and the run's own taste last. The answer is recorded in `standards.md` so it is asked once per repo; two ways never meet in one file.
- A stated rule that disagrees with the file being edited is a scope question (migrate the file or keep its way), asked with a recommendation. All such questions go to the user in one round.
- A pattern that is itself a defect is never copied; calling or extending a defective shared helper counts as copying it.
- Validator guard: the code-shaping skills must apply §4.2 and name `Mirrors:`, and §4.2 must keep its order of authority, the two-ways rule, and the no-copied-defects rule. Proven to fail when either side is removed.

### Why
- Real runs sometimes wrote code their own way in a codebase that already had one. The rule to follow neighbouring code existed, but nothing asked for the file that was followed, nothing covered a codebase with two ways, and nothing said the repo outranks a discipline pack's advice.

### Verified
- Two blind runs against real test repos with dated git history, two competing error-handling styles, an ADR in one repo and not the other, a stale `standards.md`, and a shared SQL helper vulnerable to injection. Run 1 followed the ADR without asking, asked with real evidence where nothing settled it, and refused the SQL helper in every task; its ambiguity report exposed a contradiction between an ADR and the one-way-per-file rule, now resolved as a scope question. Run 2 handled that case correctly; its remaining gaps were closed.

## [0.0.6] — 2026-09-25

### Added
- **Judgment (CONVENTIONS §4.1): the suite learns how its user decides.** Learned only from the user's own decisions: journal entries marked `By: user` with their version-control identity, or their intake answers. A decision the run or a rule made never counts, and neither does a reply that only accepts a guess ("fine", "your call"), so the suite cannot learn from its own output. Always personal: kept in `itqan/judgment.md` in the user's home directory, never in a shared repo, so a teammate's decisions never train your rules and nothing about your rules is written into the shared workspace. Or turned off.
- Three tiers (`style`, `practice`, `architecture`) needing 3, 4 and 5 consistent decisions, each on a dial the user sets: `ask`, `suggest` (the guess in the question is the user's own past answer, cited), or `decide` (the run acts, journals `By: rule J-<n>`, and reports it with a one-word undo). Every tier starts at `suggest`; only the user raises one.
- A floor judgment can never decide or pre-fill, and never learn from: spec and plan approval, GO/NO-GO, skipping or adding a phase or routing a change as small, commits and pushes, outward-facing writes, the run-mode consent questions, security waivers, anything destructive or irreversible, scope changes, and judgment's own controls.
- The repo outranks the person: when a rule disagrees with `standards.md`, the standard is followed and the rule set aside, named in one line.
- A decision that fits two tiers takes the stricter; storage and datastores are always `architecture`. A run may reclassify a decision only toward a stricter tier.
- Harvest is tracked per person by task id, not by date, so no finished task is skipped or counted twice, including tasks closed through the small route. A judgment file that will not parse is quarantined, and the run stays off rather than starting over.
- A rule's life: candidate, confirmed only by the user's yes, contradicted (capped at `suggest`), retired (kept with its reason), and stale after 180 days unused and unconfirmed. The harvest runs at close-out and on request.
- `engineer` handles *show my judgment*, *set <tier> to decide*, *forget J-<n>*, *why did you decide that?*, *learn from my decisions*, and *stop learning*.
- Journal DECISION entries carry `By:` (user, run, or rule) and, when the user decided, `Kind: <tier> · <topic> · <scope>`.
- Validator guard: §4.1's floor must still name every excluded decision, proven to fail when one line is removed. Four routing evals, including a guard against confusing *learn from my decisions* with the `learn` skill.

### Verified
- Three blind runs by fresh agents given only the rule text and fixtures with planted traps: decisions made by the run and by rules, a floor decision repeated five times, an intake answer cited twice, contradictions, stale, declined and retired rules, and architecture cases inside, outside, and nominally inside a rule's scope.
- Run 1 applied everything correctly but by assumption in 16 places; §4.1 was rewritten so decisions group by tier *and topic*, each decision counts once, floor topics never become candidates, and every rule state is explicit.
- Run 2 got 11 of 11 harvest checks and 6 of 7 applications. The miss was the riskiest kind: it *decided* an architecture choice for a Python service from a rule learned only on Node services, because "exact match" was measured against the scope's wording. Exactness is now measured against the evidence.
- Run 3, on the revised text: 7 of 7, including that case (now `suggest`). Its three remaining ambiguities (J-numbering, candidate order, wording of a guess drawn from a candidate) were closed.
- Routing: 6 of 6, including the four new cases.
- An independent review of the whole suite then found nine defects in the first version of this release, all confirmed and fixed. The two most serious: the floor protected *approving* a spec but not *skipping* the spec phase, so a learned "treat it as small" could bypass both approval gates; and replies like "fine, your call" to the run's own guess counted as the user's decisions, letting the suite learn from itself. Two further blind runs (9 of 9, then 5 of 5) confirmed the fixes; their last findings, a leak of rule changes into the shared task log and a way to lower a decision's tier, were closed.

## [0.0.5] — 2026-09-25

### Added
- **Checkpoint journal (`log.md`, CONVENTIONS §2.1), mandatory for every skill.** Each run appends a START entry as its first write, a RESUME entry after the sweep, a DECISION entry before acting on any choice that shapes the work, and a STOP entry before every reply that ends the turn. Entries are written *before* the step they describe, so a session that dies mid-step leaves its intent on disk. Append-only; a resume reads it first and re-proves the disk against it.
- **Last write before speaking:** no turn ends until `log.md`, `state.json`, and the task's `index.md` row describe the point the run has reached.
- A phase is marked `in_progress` before its first action, not only `done` at the end.
- Validator guards: every workspace-writing skill must carry the journal rule, and every artifact §20.2 requires must have a place in §1's tree. Both were proven to fail when their rule is broken.

### Changed
- **The workspace tree is closed.** A file it does not name is a bug. Raw proof goes only in a task's `evidence/`; scratch work goes to the system temp directory and is deleted; nothing else is written into the repo.
- `verify` now produces a named `verify.md` and `release` a named `release.md`. Both skills previously described their output without naming a file, so real runs invented names and locations.

## [0.0.4] — 2026-09-21

### Changed
- No install path pipes a downloaded script into a shell any more. The guided installer is fetched to `itqan-install.sh`, read, then run: README, the installation chapter, the FAQ, and the script's own usage header all say so. Piping into a shell executes code the user never saw, which is the opposite of what this suite asks of anyone.
- The installer's Node-upgrade hint links to the nvm project instead of printing a pipe-to-shell command. The script never downloaded nvm (it only uses a locally installed one), but printing that command made automated audits read it as one.

## [0.0.3] — 2026-09-21

### Added
- Router `SKILL.md` now stops instead of improvising when the suite's own files cannot be read. A denied read, a sandbox refusal, or a managed policy on dot-directories leaves only the router inlined; it names the refused path, offers the two ways out, and treats a zero-file directory listing as a block until proven otherwise.
- Installation book: a section on managed policies that block dot-directories, with the paths to allow and a copy-out workaround.
- `release`: the rollback plan must name the data at risk and how the rollback is verified; migrations are counted for destructive statements rather than assumed additive; the decision records merge and production-deploy verdicts separately.

### Changed
- Change-size triage no longer lets a big change be treated as small: more than two code files, a new route or surface, a contract change, or a scheduled `harden` pass cancels the "small" route. A user's answer to an intake question settles scope but is not approval of a spec.
- Marketplace manifest carries a description, so plugin validation passes in strict mode.

## [0.0.2] — 2026-09-01

### Added
- Google Search Console verification file, served at the site root for search indexing.

### Changed
- Docs workflow actions bumped to their Node 24 releases: `checkout` v7.0.1, `setup-python` v7.0.0, `upload-pages-artifact` v5.0.0, `deploy-pages` v5.0.0 (the last two must move together — deploy v5 requires artifacts from upload v4+). All SHAs verified against GitHub tags.

## [0.0.1] — 2026-09-01

### Added
- Initial public release: 12 skills (resumable `engineer` orchestrator, six lifecycle phases, five specialists), shared `conventions.md` (§1–§20), installer/uninstaller with 7-guard validator and 29 tests, and the documentation book published via MkDocs Material to GitHub Pages.

[0.0.9]: https://github.com/saleh-alhaddad/itqan-engineering/compare/v0.0.8...v0.0.9
[0.0.8]: https://github.com/saleh-alhaddad/itqan-engineering/compare/v0.0.7...v0.0.8
[0.0.7]: https://github.com/saleh-alhaddad/itqan-engineering/compare/v0.0.6...v0.0.7
[0.0.6]: https://github.com/saleh-alhaddad/itqan-engineering/compare/v0.0.5...v0.0.6
[0.0.5]: https://github.com/saleh-alhaddad/itqan-engineering/compare/v0.0.4...v0.0.5
[0.0.4]: https://github.com/saleh-alhaddad/itqan-engineering/compare/v0.0.3...v0.0.4
[0.0.3]: https://github.com/saleh-alhaddad/itqan-engineering/compare/v0.0.2...v0.0.3
[0.0.2]: https://github.com/saleh-alhaddad/itqan-engineering/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/saleh-alhaddad/itqan-engineering/releases/tag/v0.0.1
