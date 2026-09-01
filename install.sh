#!/usr/bin/env bash
# Installer for the itqan engineering skills suite.
# Checks the Node.js requirement of the `npx skills` CLI first, offers an
# upgrade when Node is too old, and falls back to a plain git install that
# needs no Node at all.
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/saleh-alhaddad/itqan-engineering/main/install.sh | bash
#   ./install.sh            # from a clone
set -euo pipefail

REPO="saleh-alhaddad/itqan-engineering"
REQUIRED_MAJOR=22
REQUIRED="22.20.0"
AUTO=0
for a in "$@"; do [ "$a" = "--auto" ] && AUTO=1; done

say()  { printf '%s\n' "$*"; }
ask()  { # interactive: read the terminal (works for curl|bash via /dev/tty);
         # script-from-file with piped stdin: read the pipe (scripted/CI answers);
         # fully non-interactive: fall back to the default (empty answer)
  local reply=""
  if [ "$AUTO" = 1 ]; then
    printf '%s (auto mode — using default)\n' "$1" >&2
    printf '%s' ""
    return
  fi
  if [ -t 0 ]; then
    read -r -p "$1 " reply || reply=""
  elif { : </dev/tty; } 2>/dev/null; then
    read -r -p "$1 " reply </dev/tty || reply=""
  elif [ -f "${BASH_SOURCE[0]:-}" ]; then
    # stdin is a pipe and the script came from a file, so stdin can carry answers.
    # Prompt goes to stderr — stdout is the return value captured by $(...).
    read -r reply || reply=""
    printf '%s %s\n' "$1" "$reply" >&2
  else
    printf '%s (no terminal — using default)\n' "$1" >&2
  fi
  printf '%s' "$reply"
}

node_major() { node -v 2>/dev/null | sed 's/^v//' | cut -d. -f1; }

git_fallback() {
  local target="${HOME}/.agents/skills/itqan"
  say ""
  say "Installing without Node via git clone -> ${target}"
  if [ -d "$target/.git" ]; then
    git -C "$target" pull --ff-only && say "Updated existing install."
  else
    mkdir -p "$(dirname "$target")"
    git clone --depth 1 "https://github.com/${REPO}" "$target"
    say "Installed. Point your agent's skill loader at: ${target}"
    say "(Claude Code users can instead run: /plugin marketplace add ${REPO})"
  fi
}

run_npx_install() {
  say "Node $(node -v) OK — installing via npx skills…"
  # Rescue: any npx failure (registry/network/engine edge cases) falls back to git,
  # so the installer never leaves the user with a stack trace and no install.
  if ! npx -y skills add "${REPO}"; then
    say ""
    say "npx skills failed — falling back to the plain git install."
    git_fallback
  fi
}

main() {
  if ! command -v node >/dev/null 2>&1; then
    say "Node.js is not installed. The one-command installer (npx skills) needs Node >= ${REQUIRED}."
    case "$(ask 'Install via plain git instead (no Node needed)? [Y/n]')" in
      n|N) say "Aborted. Install Node >= ${REQUIRED} (https://nodejs.org or: nvm install 22) and re-run." ;;
      *)   git_fallback ;;
    esac
    return
  fi

  local major; major="$(node_major)"
  if [ "${major:-0}" -ge "${REQUIRED_MAJOR}" ]; then
    run_npx_install "$@"
    return
  fi

  say "Your Node is $(node -v), but the npx skills CLI needs >= v${REQUIRED}."
  # Offer an in-place upgrade when nvm is available; otherwise guide + fallback.
  if [ -s "${NVM_DIR:-$HOME/.nvm}/nvm.sh" ]; then
    case "$(ask "Upgrade Node to ${REQUIRED_MAJOR} with nvm now, then install? [Y/n]")" in
      n|N) : ;;
      *)
        # shellcheck disable=SC1091
        . "${NVM_DIR:-$HOME/.nvm}/nvm.sh"
        nvm install "${REQUIRED_MAJOR}"
        nvm use "${REQUIRED_MAJOR}"
        run_npx_install "$@"
        return
        ;;
    esac
  else
    say "No nvm found. Upgrade options:"
    say "  - nvm:      curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash   (then: nvm install 22)"
    say "  - Homebrew: brew install node@22"
    say "  - Direct:   https://nodejs.org"
  fi

  case "$(ask 'Install via plain git instead right now (no Node upgrade needed)? [Y/n]')" in
    n|N) say "Aborted. Re-run this script after upgrading Node." ;;
    *)   git_fallback ;;
  esac
}

main "$@"
