# Discipline pack — Any language (fallback)

Load when none of the specific packs match cleanly — a CLI tool, a library, a data pipeline, a
systems program, an unfamiliar or mixed stack. Infer everything from the repo: file
extensions, the build/dependency files, the test setup, and the existing structure. This pack
holds the concerns that are true regardless of language.

## In DEFINE (spec)
- State the objective as observable behavior and testable success criteria, whatever the
  domain. If it's a library, the **public API** is the contract — design it to be hard to
  misuse and stable across versions.

## In BUILD (construct)
- **Follow the repo's own conventions** — its formatter, its test framework, its structure,
  its idioms. Consistency with what exists beats any external "best practice."
- Keep boundaries clean: validate input at the edges, keep the core logic pure and testable.
- Test-first regardless of language; use whatever runner the project already uses.

## In VERIFY
- Run the project's real build and test commands fresh; exercise the actual entry point (the
  CLI invocation, the library call, the pipeline run) with real input.

## Size thresholds (reference)

- **Change size:** ~100 lines reviews well · ~300 is the ceiling for care · ~1000 should have
  been split — by stack, file-group, horizontal, or vertical slice.
- **Rule of 500:** a refactor touching more than ~500 lines should be a codemod/script, not
  hand edits — hands drift, scripts don't.
- **Code shape** (function/file/param/nesting limits) has no universal number — read the
  repo's own linter rule where one exists and hold the new code to it.

## In REVIEW (inspect) — surface-agnostic
- **Correctness:** edge cases, error/failure paths, resource cleanup (files, handles,
  connections), concurrency hazards.
- **Security:** untrusted input handling, injection into shells/queries/paths, secrets in
  code, unsafe deserialization, dependency/supply-chain risk.
- **Performance:** the algorithmic hot path, unbounded memory/IO, work that repeats
  needlessly — flag structural problems, leave micro-optimization to measurement.

## In SHIP (release)
- Version and changelog with the change (SemVer for a library); a way to roll back (revert,
  re-publish previous version, or flag); a signal to confirm health after release.

## When the stack is genuinely unfamiliar
Ground the work in the project's own docs and the dependency's official documentation rather
than assumptions — detect the version, read the relevant page, follow the documented pattern,
and note anything you could not verify.
