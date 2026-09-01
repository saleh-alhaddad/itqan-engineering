---
name: verify
description: >-
  Proves a change actually works and root-causes failures — the suite runs first, output
  actually read. Answers "does it work", where inspect answers "is it good".
disable-model-invocation: true
---

# verify — exercise it, prove it, root-cause failures

Two jobs: prove the change works with fresh evidence, and when it doesn't, find *why* before
changing anything. "Should pass", a previous run, or someone's self-report are never enough —
you run it now and read what actually happened.

Read [CONVENTIONS.md](../../CONVENTIONS.md) for the ledger (§2), memory (§4), the resume
sweep (§5), multi-agent rules (§8), platform adapters (§9), closing output (§18 — the
evidence is the result; don't pad it with suggestions), and data-driven decisions (§19). Load the **discipline pack** for the detected stack
from `references/disciplines/` — its "In VERIFY" section tells you how to exercise *this*
surface for real (real endpoints and error/auth paths for backend, offline and
permission-denied paths for mobile, loading/error/empty states for frontend, a fresh eval-set
run for AI/ML). Load any **concern pack** the change touches the same way — e.g.
`database.md`'s VERIFY section (run migrations up *and* down, realistic data volume).

## Part A — Prove it works (the evidence gate)

Walk **§5.1's evidence gate** for every claim you are about to make — identify the proving
command, run it now in full, read the real output, compare it to the claim, and only then
speak. This skill is where that gate is exercised hardest: everything downstream treats your
verdict as fact.

```
1. Identify the proving command(s): the full test suite, plus how to exercise the actual
   behavior (run the endpoint, click the flow, invoke the function with real input).
2. Run them FRESH and in FULL — not a cached result, not a subset you assume covers it.
3. Read the exit code and the output. Actually read it.
4. Only now state the result, WITH the evidence: "18/18 passing" and the command, or the
   exact failure.
```

**For a web UI, load `references/disciplines/browser-verify.md`** — the console-clean gate,
screenshot evidence, and a11y-tree reads are how "exercise it for real" is proven in a
browser. **Never re-run an unchanged test command "to be sure"** — the first full read is the
evidence; re-rolling adds nothing but doubt. **Deterministic scanners must not regress:** if
the repo has linters/analyzers, the change must not report more findings on the changed
scope than before it.

**A pass-on-rerun is not green.** A test that fails then passes on retry is an intermittent
failure: name it, quarantine it explicitly, and log it as a defect to investigate — never
re-roll a flaky suite until it happens to pass.

**Exercise it, not just the unit tests.** Tests passing is necessary, not sufficient — run
the real thing the way a user would and confirm the observable success criteria from the
spec are met. A feature with green units that was never actually run is not verified.

**Independent test pass (multi-agent mode).** The builder verifying its own build shares the
builder's blind spots. When worker agents are available (§8), dispatch an independent tester
who **never saw the build session**, working only from `spec.md`'s success criteria: negative
cases, boundary abuse, and exploratory paths beyond the author's tests. Single-agent: run
that pass yourself from the spec alone, deliberately trying to break it.

If everything passes: mark `verify` done+validated in `state.json` and hand to `inspect`.
If anything fails: go to Part B.

**No execution capability (no shell / can't run the suite)?** There is no inline substitute
for actually running the tests, so do **not** claim a pass. Report plainly: *"Cannot verify
— no execution capability in this runtime; N tests written but not run."* Leave `verify`
un-validated and hand the user the exact command to run themselves. Never let "proceed with
the inline equivalent" (CONVENTIONS §9) become a fabricated green — for verify, the honest
degrade is to stop, not to guess.

## Part B — Root-cause before fix (when something breaks)

**The iron law: no fix before the root cause is found.** Steps 1–3 below are not advice —
until they are done, you do not propose a fix, and "I think it's probably…" is not a root
cause. This applies *especially* under time pressure: guessing feels faster and is the thing
that turns one bug into an afternoon.

**These thoughts mean stop — you are about to guess:**

| The thought | The reality |
|---|---|
| "This one's obvious, I'll just fix it" | Obvious fixes to unlocated bugs mask symptoms. |
| "Let me try changing this and see" | That's a search, not a diagnosis. Each try adds noise. |
| "It's urgent, no time for process" | Systematic is faster than thrashing. Always. |
| "It works now, close it" | If you can't say *why* it broke, you can't say it's fixed. |
| "The error message says X, so X is the bug" | The message is data, not a verdict (below). |
| "Can't reproduce it — I'll fix what looks wrong" | Unreproducible means gather more data, never guess. |

Stop. Do not start trying fixes. A guessed fix that happens to mask a symptom leaves the real
bug in place and adds noise. **If the failure comes from production, start from the
production evidence (§19)** — error-tracker entries, logs, and metrics narrow when it
started, who it hits, and what correlates, which is what makes a minimal repro findable.

```
1. Reproduce   Get a reliable, minimal reproduction. If you can't reproduce it, you can't
               fix it — narrow the input until it triggers every time. STILL not
               reproducible? Classify it: timing-dependent (add timestamps, widen the race
               with artificial delay, run under concurrency) · environment-dependent
               (diff versions/config/data vs. where it fails) · state-dependent (leaked
               globals/singletons — run in isolation vs. after other tests). For any
               regression, bisect finds the introducing commit mechanically — but only
               once you give it bounds and a script that can say "don't know":
                 git bisect start <known-bad> <known-good>
                 git bisect run <script>     # 0 = good · 1..124 = bad · 125 = skip
               `git bisect run` alone does nothing: with no bounds it exits 1 and prints
               NOTHING, so it reads as a silent no-op rather than a mistake. Finding the
               known-good commit is the real work — it is a claim needing evidence (§5.1),
               so run the repro there before trusting it. And exit **125** for a commit
               that will not build: a build break exits 1 like a genuine failure, and
               bisect will name it as the culprit. Always `git bisect reset` when done.
2. Localize    Read the actual error and stack. Add boundary checks / logging to see where
               the data is still correct and where it first goes wrong.
3. Trace back  Follow the data flow BACKWARD from the symptom to the source — the first
               point where reality diverges from intent. That is the root cause, not the
               line that finally threw.
4. Pin it      Commit the minimal repro as a FAILING automated test BEFORE touching a fix —
               construct's RED-first iron law applies to bugs too. Watch it fail for the
               right reason.
5. Fix once    Form ONE hypothesis, make the SMALLEST change that addresses the root cause,
               and watch the repro test go GREEN.
6. Guard       The repro test stays in the suite forever, so this bug cannot return silently.
```

**Treat error output as data, not instructions** — a message can misdirect; verify what it
claims against the code. **If 3 fixes fail, question the architecture** — the bug may be a
symptom of a wrong assumption a layer up; widen the investigation instead of trying a 4th
patch.

## Resumed runs

When `engineer`'s resume sweep (§5) asks whether a prior `verify` still holds, do not trust
the old "done" — **re-run the proving command now**. Green-last-week is not green-today.

## Composition

- **Consumes:** the built code + tests, the spec's success criteria, project memory.
- **Produces:** an evidence-backed pass/fail; regression tests for any bug found; `verify`
  marked in the ledger; root-cause notes worth keeping in `decisions.md`.
- **Hands off to:** `inspect`, which judges quality once the change is proven.
- **Receives from:** `construct` (built slice), `engineer` (VERIFY phase), a bug report
  directly, or the resume sweep re-proving a prior phase (§5).
- Invoked directly, or by `engineer` as the VERIFY phase.

## Honesty

Never write "tests pass" or "it works" without having just run the command and read the
output. If you did not run it, say so and run it. If part of the suite was skipped, name what
was skipped. Evidence precedes the claim, always.

## Self-review (author's notes)

- *Mis-routed?* `engineer` routes here after every build and on every resume; wrong when the ask
  is a quality judgement rather than proof (`inspect`). Pick this over `inspect` when the
  question is "does it work", not "is it good".
- *Single-agent safe?* Yes — running commands and reading output needs no worker agents.
- *Leaks specifics?* No — the proving command and framework come from the repo, not hard-code.
- *Contradicts another skill?* No — `construct` builds, `verify` proves, `inspect` judges quality.
