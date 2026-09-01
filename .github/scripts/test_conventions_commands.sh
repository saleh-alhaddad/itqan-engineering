#!/usr/bin/env bash
# Executes the shell commands CONVENTIONS.md prescribes, against real fixtures.
#
# validate.py checks the repository's structure; nothing checked whether a command
# a rule tells the agent to run actually answers correctly. It cost one: §20.1 shipped
# `git check-ignore -q <engineering>` and that form reports "not ignored" for a
# directory-only pattern before the folder exists — the exact moment the rule fires.
set -u
pass=0; fail=0
ok()  { echo "  ok: $1"; pass=$((pass+1)); }
bad() { echo "  FAIL: $1"; fail=$((fail+1)); }

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

echo "TEST: §20.1's gitignore check answers correctly for every directory-only pattern"

# The command the rule prescribes, lifted from the text rather than retyped here.
form=$(grep -o 'git check-ignore -v <engineering>/[a-z.]*' "$ROOT/CONVENTIONS.md" | head -1)
if [ -z "$form" ]; then
  bad "§20.1 no longer prescribes a git check-ignore command — update this test with the rule"
else
  ok "rule prescribes: $form"
  probe=${form##*<engineering>/}          # the path under the workspace it asks about

  for pat in 'engineering/' 'engineering' '/engineering/' '**/engineering/'; do
    d="$TMP/$(echo "$pat" | tr -d '/*')"; mkdir -p "$d"
    ( cd "$d" && git init -q . && printf '%s\n' "$pat" > .gitignore
      # deliberately do NOT create engineering/ — the rule runs before it exists
      git check-ignore -q "engineering/$probe" ) \
      && ok "pattern '$pat' detected" \
      || bad "pattern '$pat' MISSED — a committed workspace would silently stage nothing"
  done

  # and the form the rule must never go back to
  d="$TMP/bare"; mkdir -p "$d"
  ( cd "$d" && git init -q . && echo 'engineering/' > .gitignore
    git check-ignore -q engineering ) \
    && bad "the bare form works here — this test's premise is stale, re-verify §20.1" \
    || ok "bare 'engineering' still misses it, as the rule warns"
fi

echo
echo "TEST: §20.1's claim about how an ignored path fails, per staging form"
d="$TMP/staging"; mkdir -p "$d"
( cd "$d" && git init -q . && echo 'engineering/' > .gitignore \
  && mkdir engineering && echo x > engineering/profile.md && echo code > main.go
  git add engineering/ >/dev/null 2>&1
  [ $? -ne 0 ] || exit 1 ) \
  && ok "explicit 'git add engineering/' exits non-zero — loud, as the rule says" \
  || bad "explicit add no longer errors; §20.1's 'exits 1' half is stale"

d="$TMP/staging2"; mkdir -p "$d"
( cd "$d" && git init -q . && echo 'engineering/' > .gitignore \
  && mkdir engineering && echo x > engineering/profile.md && echo code > main.go
  git add -A >/dev/null 2>&1 || exit 1
  git diff --cached --name-only | grep -q '^engineering/' && exit 1
  git diff --cached --name-only | grep -q '^main.go' ) \
  && ok "implicit 'git add -A' exits 0, stages code, silently skips the workspace" \
  || bad "implicit add behaviour changed; §20.1's silent-path half is stale"

echo
echo "TEST: §11's claim about worktrees on a repo with zero commits"
d="$TMP/greenfield"; mkdir -p "$d/repo"
( cd "$d/repo" && git init -q . && git worktree add ../side >/dev/null 2>&1 ) \
  && ok "worktree add succeeds with no commits on git $(git --version | awk '{print $3}') — §11 says check the version" \
  || ok "worktree add fails with no commits on this git — §11's older-git branch applies"

echo
echo "TEST: verify's bisect invocation — bounds required, 125 skips"
d="$TMP/bisect"; mkdir -p "$d"
( cd "$d" && git init -q . && git config user.email t@t && git config user.name t
  for i in 1 2 3; do echo "def f(): return $i" > m.py; git add -A; git commit -qm "c$i"; done
  echo "def f(): return 999" > m.py; git add -A; git commit -qm "c4-bug"
  for i in 5 6; do echo "def f(): return 999 # $i" > m.py; git add -A; git commit -qm "c$i"; done
  printf '#!/bin/sh\npython3 -c "import m; assert m.f() != 999" 2>/dev/null\n' > t.sh
  chmod +x t.sh
  # unbounded: must fail, and must say nothing — the silence is why the rule spells it out
  out=$(git bisect run ./t.sh 2>&1); [ $? -eq 0 ] && exit 1
  [ -n "$out" ] && exit 1
  # bounded: must name c4-bug
  git bisect start HEAD HEAD~5 >/dev/null 2>&1
  git bisect run ./t.sh 2>&1 | grep -q "c4-bug" || exit 1
  git bisect reset >/dev/null 2>&1 ) \
  && ok "unbounded bisect run is a silent no-op; bounded run finds the commit" \
  || bad "bisect behaviour changed — verify's rule needs re-checking"

echo
echo "TEST: the project install docs/02 prescribes, into a pre-existing .cursor/skills"
d="$TMP/cursor"; mkdir -p "$d/proj/.cursor/skills"    # the folder Cursor usually already made
( cd "$d/proj"
  cp -R "$ROOT/skills/." .cursor/skills/
  cp -R "$ROOT/CONVENTIONS.md" "$ROOT/references" "$ROOT/templates" .cursor/
  [ -d .cursor/skills/skills ] && exit 1              # nesting silently breaks every link
  [ -f .cursor/skills/define/SKILL.md ] || exit 1
  ( cd .cursor/skills/define && [ -f ../../CONVENTIONS.md ] ) || exit 1
  ( cd .cursor/skills/design  && [ -f ../../references/disciplines/ui-craft.md ] ) || exit 1
  [ -f .cursor/templates/bootstrap-engineering-workspace.sh.tmpl ] || exit 1 ) \
  && ok "copies contents, links resolve, templates present" \
  || bad "the documented Cursor install is broken — re-run it by hand and fix docs/02"

# and the form the doc warns against, so the warning cannot go stale unnoticed
d="$TMP/cursor-trap"; mkdir -p "$d/proj/.cursor/skills"
( cd "$d/proj" && cp -R "$ROOT/skills" .cursor/skills && [ -d .cursor/skills/skills ] ) \
  && ok "'cp -R skills' still nests into an existing folder, as the doc warns" \
  || bad "cp no longer nests — docs/02's warning about it is now misleading"

echo
echo "conventions-command tests: $pass passed, $fail failed"
[ "$fail" -eq 0 ]
