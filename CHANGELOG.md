# Changelog

All notable changes to the itqan engineering skills suite.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [SemVer](https://semver.org/).

## [0.0.2] — 2026-09-01

### Added
- Google Search Console verification file, served at the site root for search indexing.

### Changed
- Docs workflow actions bumped to their Node 24 releases: `checkout` v7.0.1, `setup-python` v7.0.0, `upload-pages-artifact` v5.0.0, `deploy-pages` v5.0.0 (the last two must move together — deploy v5 requires artifacts from upload v4+). All SHAs verified against GitHub tags.

## [0.0.1] — 2026-09-01

### Added
- Initial public release: 12 skills (resumable `engineer` orchestrator, six lifecycle phases, five specialists), shared `conventions.md` (§1–§20), installer/uninstaller with 7-guard validator and 29 tests, and the documentation book published via MkDocs Material to GitHub Pages.

[0.0.2]: https://github.com/saleh-alhaddad/itqan-engineering/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/saleh-alhaddad/itqan-engineering/releases/tag/v0.0.1
