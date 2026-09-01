#!/usr/bin/env bash
# Automation tests for install.sh — deterministic, no network.
# Uses PATH shims for node/git/npx so every branch is asserted without real installs.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
PASS=0; FAIL=0

check() { # check <name> <expected-substring> <actual-output>
  if printf '%s' "$3" | grep -q "$2"; then
    echo "  ok: $1"; PASS=$((PASS+1))
  else
    echo "  FAIL: $1 — expected to find: $2"; echo "  --- output was:"; printf '%s\n' "$3" | sed 's/^/  | /'; FAIL=$((FAIL+1))
  fi
}

make_shims() { # make_shims <dir> <node-version-or-none>
  local dir="$1" ver="$2"
  mkdir -p "$dir"
  if [ "$ver" != "none" ]; then
    printf '#!/bin/sh\necho %s\n' "$ver" > "$dir/node"; chmod +x "$dir/node"
  fi
  # git shim records the call instead of cloning
  printf '#!/bin/sh\necho "GIT-SHIM: $*"\nexit 0\n' > "$dir/git"; chmod +x "$dir/git"
  # npx shim records the call instead of installing
  printf '#!/bin/sh\necho "NPX-SHIM: $*"\nexit 0\n' > "$dir/npx"; chmod +x "$dir/npx"
  # keep basic tools reachable
  for t in sed cut grep mkdir dirname printf; do :; done
}

run_case() { # run_case <shimdir> <stdin> — runs installer with shims first on PATH
  local shims="$1" input="$2"
  printf '%s\n' "$input" | env PATH="$shims:/usr/bin:/bin" NVM_DIR=/nonexistent HOME="$WORK" \
    bash "$ROOT/install.sh" 2>&1 || true
}

echo "TEST 1: modern Node (v22.20.0) -> goes straight to npx install"
make_shims "$WORK/s1" v22.20.0
OUT="$(run_case "$WORK/s1" "")"
check "version accepted"        "Node v22.20.0 OK"            "$OUT"
check "npx invoked with repo"   "NPX-SHIM: -y skills add saleh-alhaddad/itqan-engineering" "$OUT"

echo "TEST 2: old Node (v12.18.4), no nvm -> warns, offers upgrade paths, git fallback on default"
make_shims "$WORK/s2" v12.18.4
OUT="$(run_case "$WORK/s2" "y")"
check "old version detected"    "needs >= v22.20.0"           "$OUT"
check "upgrade guidance shown"  "nvm install 22"              "$OUT"
check "git fallback invoked"    "GIT-SHIM: clone"             "$OUT"
check "no npx attempted"        "NPX-SHIM" "$(printf '%s' "$OUT" | grep -c NPX-SHIM | sed 's/^0$/NPX-SHIM-absent/')" || true
if printf '%s' "$OUT" | grep -q "NPX-SHIM"; then echo "  FAIL: npx must not run on old Node"; FAIL=$((FAIL+1)); else echo "  ok: npx not attempted"; PASS=$((PASS+1)); fi

echo "TEST 3: old Node, user declines fallback -> aborts cleanly"
OUT="$(run_case "$WORK/s2" "n")"
check "clean abort"             "Aborted"                     "$OUT"
if printf '%s' "$OUT" | grep -q "GIT-SHIM: clone"; then echo "  FAIL: must not clone after decline"; FAIL=$((FAIL+1)); else echo "  ok: no clone after decline"; PASS=$((PASS+1)); fi

echo "TEST 4: no Node at all -> offers git fallback"
make_shims "$WORK/s4" none
OUT="$(run_case "$WORK/s4" "y")"
check "missing node detected"   "Node.js is not installed"    "$OUT"
check "git fallback invoked"    "GIT-SHIM: clone"             "$OUT"

echo "TEST 6: npx failure -> automatic git fallback rescue"
make_shims "$WORK/s6" v22.20.0
printf '#!/bin/sh\necho "NPX-SHIM-FAILING"\nexit 1\n' > "$WORK/s6/npx"; chmod +x "$WORK/s6/npx"
OUT="$(run_case "$WORK/s6" "")"
check "npx attempted"           "NPX-SHIM-FAILING"            "$OUT"
check "rescue message"          "falling back to the plain git install" "$OUT"
check "git fallback ran"        "GIT-SHIM: clone"             "$OUT"

echo "TEST 7: --auto mode, old Node, no nvm -> silent git fallback, no prompts"
OUT="$(printf '' | env PATH="$WORK/s2:/usr/bin:/bin" NVM_DIR=/nonexistent HOME="$WORK" \
  bash "$ROOT/install.sh" --auto 2>&1 || true)"
check "auto default noted"      "auto mode — using default"   "$OUT"
check "git fallback ran"        "GIT-SHIM: clone"             "$OUT"

echo "TEST 5: bash syntax check"
if bash -n "$ROOT/install.sh"; then echo "  ok: syntax valid"; PASS=$((PASS+1)); else echo "  FAIL: syntax error"; FAIL=$((FAIL+1)); fi

echo
echo "install.sh tests: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
