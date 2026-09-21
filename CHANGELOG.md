# Changelog

All notable changes to the itqan engineering skills suite.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [SemVer](https://semver.org/).

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

[0.0.4]: https://github.com/saleh-alhaddad/itqan-engineering/compare/v0.0.3...v0.0.4
[0.0.3]: https://github.com/saleh-alhaddad/itqan-engineering/compare/v0.0.2...v0.0.3
[0.0.2]: https://github.com/saleh-alhaddad/itqan-engineering/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/saleh-alhaddad/itqan-engineering/releases/tag/v0.0.1
