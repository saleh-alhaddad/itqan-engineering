#!/usr/bin/env python3
"""Structural validation for the itqan engineering skills suite.

Guards the mechanical rules the suite depends on: valid manifests, complete
skill frontmatter, description-length caps, resolving internal links, name
consistency, and the no-AI-attribution policy. Runs with stock Python 3 only.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ERRORS: list[str] = []

DESCRIPTION_CHAR_CAP = 1024  # agentskills.io frontmatter limit
AI_ATTRIBUTION = re.compile(r"co-authored-by:.*(claude|anthropic|gpt|gemini|copilot)|generated with \[?claude", re.I)


def err(msg: str) -> None:
    ERRORS.append(msg)


def check_json_files() -> dict:
    parsed = {}
    for rel in [".claude-plugin/plugin.json", ".claude-plugin/marketplace.json", "evals/routing-evals.json"]:
        path = ROOT / rel
        if not path.is_file():
            err(f"{rel}: missing")
            continue
        try:
            parsed[rel] = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            err(f"{rel}: invalid JSON — {e}")
    return parsed


def check_name_consistency(parsed: dict) -> None:
    plugin = parsed.get(".claude-plugin/plugin.json")
    market = parsed.get(".claude-plugin/marketplace.json")
    if not (plugin and market):
        return
    names = {plugin.get("name"), market.get("name")}
    names.update(p.get("name") for p in market.get("plugins", []))
    if len(names) != 1:
        err(f"name mismatch across manifests: {sorted(n or '<missing>' for n in names)}")
    versions = {plugin.get("version")} | {p.get("version") for p in market.get("plugins", [])}
    if len(versions) != 1:
        err(f"version mismatch across manifests: {sorted(v or '<missing>' for v in versions)}")


def parse_frontmatter(text: str) -> dict | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    block = text[4:end]
    fm: dict[str, str] = {}
    key = None
    for line in block.splitlines():
        m = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if m:
            key = m.group(1)
            fm[key] = m.group(2).strip()
        elif key and (line.startswith("  ") or line.startswith("\t")):
            fm[key] = (fm[key] + "\n" + line.strip()).strip()
    return fm


def check_skills() -> None:
    skill_files = sorted(ROOT.glob("skills/*/SKILL.md"))
    if not skill_files:
        err("no skills found under skills/*/SKILL.md")
    for path in skill_files:
        rel = path.relative_to(ROOT)
        fm = parse_frontmatter(path.read_text(encoding="utf-8"))
        if fm is None:
            err(f"{rel}: missing or unterminated YAML frontmatter")
            continue
        name = fm.get("name")
        desc = fm.get("description", "")
        # strip YAML folded-block marker before measuring
        desc_body = re.sub(r"^>-?\s*", "", desc)
        if not name:
            err(f"{rel}: frontmatter missing 'name'")
        elif name != path.parent.name:
            err(f"{rel}: name '{name}' != folder '{path.parent.name}'")
        if not desc_body:
            err(f"{rel}: frontmatter missing 'description'")
        elif len(desc_body) > DESCRIPTION_CHAR_CAP:
            err(f"{rel}: description {len(desc_body)} chars exceeds cap {DESCRIPTION_CHAR_CAP}")


def check_root_skill() -> None:
    path = ROOT / "SKILL.md"
    if not path.is_file():
        err("SKILL.md: missing at repo root (needed for whole-suite installs via `npx skills`)")
        return
    fm = parse_frontmatter(path.read_text(encoding="utf-8"))
    if fm is None or not fm.get("name") or not fm.get("description"):
        err("SKILL.md (root): missing frontmatter name/description")
        return
    desc = re.sub(r"^>-?\s*", "", fm["description"])
    if len(desc) > DESCRIPTION_CHAR_CAP:
        err(f"SKILL.md (root): description {len(desc)} chars exceeds cap {DESCRIPTION_CHAR_CAP}")


def check_internal_links() -> None:
    link = re.compile(r"\[[^\]]*\]\(([^)#\s]+)\)")
    for path in list(ROOT.glob("skills/*/SKILL.md")) + [ROOT / "README.md", ROOT / "SKILL.md"] + list(
        (ROOT / "references" / "disciplines").glob("*.md")
    ) + list(ROOT.glob("docs/**/*.md")):
        if not path.is_file():
            continue
        for target in link.findall(path.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            if not (path.parent / target).resolve().exists():
                err(f"{path.relative_to(ROOT)}: broken link -> {target}")


def check_no_ai_attribution() -> None:
    """Guard THIS repo's own files against stray AI-attribution strings.

    The suite's default is no attribution, but a user's org may require a disclosure
    trailer (profile.md `Commit attribution:`, CONVENTIONS §12) — so this is a house rule
    for the suite's sources, not an assertion that attribution is universally forbidden.
    Prose that documents or quotes the convention is allowed.
    """
    documenting = ("never", "no \"", "no `", "no '", "default", "unless", "policy",
                   "attribution:", "trailer")
    for path in ROOT.rglob("*"):
        if path.is_dir() or ".git" in path.parts:
            continue
        if path.suffix not in {".md", ".json", ".yml", ".yaml"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for m in AI_ATTRIBUTION.finditer(text):
            line = text[: m.start()].count("\n") + 1
            context = text.splitlines()[line - 1].strip().lower()
            if any(k in context for k in documenting):
                continue
            err(f"{path.relative_to(ROOT)}:{line}: AI attribution string in this repo's own files")


def check_section_declarations() -> None:
    """A skill's body may only cite CONVENTIONS sections its header read-list declares.

    The header read-list is the paragraph containing the CONVENTIONS.md link near the top
    of each SKILL.md. Whole-file loading means an omission is not a functional gap today,
    but declarations that drift from usage hide real dependencies (found live: inspect
    relied on \u00a710's fetched-content rule without declaring it). Sub-refs like \u00a720.2
    count as their parent section."""
    import re as _re
    for path in sorted(ROOT.glob("skills/*/SKILL.md")):
        rel = path.relative_to(ROOT)
        body = path.read_text(encoding="utf-8").split("\n---\n", 1)[-1]
        paras = body.split("\n\n")
        hdr = next((p for p in paras if "CONVENTIONS.md](" in p), "")
        if not hdr:
            err(f"{rel}: no CONVENTIONS.md read-list paragraph found")
            continue
        declared = set(map(int, _re.findall(r"\u00a7(\d+)", hdr)))
        cited = set(map(int, _re.findall(r"\u00a7(\d+)", body.replace(hdr, "", 1))))
        missing = sorted(cited - declared)
        if missing:
            err(f"{rel}: body cites \u00a7{', \u00a7'.join(map(str, missing))} "
                f"but the header read-list omits them")


def check_markdown_tables() -> None:
    """Every table row must open AND close with a pipe.

    A row missing its trailing pipe still looks fine in a plain-text diff but renders as
    broken markdown — and the rows most likely to lose one are the long rationalization
    tables, i.e. exactly the text a reader needs when they are about to break a rule."""
    for path in sorted(list(ROOT.glob("skills/*/SKILL.md")) + [ROOT / "CONVENTIONS.md"]):
        rel = path.relative_to(ROOT)
        for num, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            s = line.strip()
            if s.startswith("|") and not s.endswith("|") and "---" not in s:
                err(f"{rel}:{num}: table row missing its closing pipe")


def check_template_keys() -> None:
    """No fenced template may define the same `Key:` twice.

    A duplicated key is invisible in review and copied faithfully by every run that fills the
    template in — one duplicate `Outcome:` produced a duplicate in every summary.md written
    against it."""
    import re as _re
    for path in [ROOT / "CONVENTIONS.md"] + sorted(ROOT.glob("skills/*/SKILL.md")):
        rel = path.relative_to(ROOT)
        for block in _re.findall(r"```[a-z]*\n(.*?)```", path.read_text(encoding="utf-8"), _re.S):
            keys = _re.findall(r"^([A-Z][A-Za-z /-]{2,20}):\s", block, _re.M)
            dupes = {k for k in keys if keys.count(k) > 1}
            for d in sorted(dupes):
                err(f"{rel}: template defines '{d}:' more than once")


def check_produced_artifacts_registered() -> None:
    """Every artifact a skill declares under `Produces:` must be enforced by §20.2.

    §7 delegates on-disk enforcement of every phase report to §20.2's required-artifacts
    table. A skill that produces a file absent from that table has a rule stated in prose
    and switched off in practice: the phase can be marked `done` with nothing on disk.
    """
    # `learn` writes into its own learning folder, not the engineering/ workspace ledger.
    exempt = {"progress.md", "roadmap.md"}
    conventions = (ROOT / "CONVENTIONS.md").read_text(encoding="utf-8")
    table = re.search(
        r"^\| Scope \| Required on disk \|$\n\|-+\|-+\|$\n((?:^\|.*$\n)+)",
        conventions, re.M)
    if not table:
        err("CONVENTIONS.md: §20.2 required-artifacts table not found")
        return
    registered = set(re.findall(r"`([a-z][a-z-]*\.(?:md|json))`", table.group(1)))

    for path in sorted(ROOT.glob("skills/*/SKILL.md")):
        skill = path.parent.name
        body = path.read_text(encoding="utf-8")
        m = re.search(r"^- \*\*Produces:\*\*(.*?)(?=^- \*\*|\Z)", body, re.M | re.S)
        if not m:
            continue
        for art in sorted(set(re.findall(r"`([a-z][a-z-]*\.(?:md|json))`", m.group(1)))):
            if art in exempt or art in registered:
                continue
            err(f"skills/{skill}/SKILL.md: produces '{art}' but §20.2's required-artifacts table never requires it on disk")


def check_ledger_vocabulary_is_reachable() -> None:
    """Every phase `status` value §2 declares must be written somewhere.

    A value listed in the schema but never set by any rule is dead vocabulary: it reads
    as modelled behaviour while nothing can ever produce it. `blocked` sat unused until a
    rejected gate needed somewhere to live — the gap looked like a design, not a hole.
    """
    conventions = (ROOT / "CONVENTIONS.md").read_text(encoding="utf-8")
    decl = re.search(r"^- `status`: (.+)$", conventions, re.M)
    if not decl:
        err("CONVENTIONS.md: §2 status vocabulary not found")
        return
    values = re.findall(r"`([a-z_]+)`", decl.group(1))
    corpus = conventions + "".join(
        p.read_text(encoding="utf-8") for p in sorted(ROOT.glob("skills/*/SKILL.md")))
    # A comparison is a read, not a write. The sweep's `if status == "blocked"` is what
    # made this value look modelled while no rule could ever produce it — strip reads
    # first, then look for something that actually sets the value.
    corpus = re.sub(r'[=!]=\s*["\x27]?[a-z_]+', "", corpus)
    corpus = corpus.replace(decl.group(0), "")
    for value in values:
        if not re.search(rf'status["\x27]?\s*[:=]\s*["\x27]?{value}\b', corpus):
            err(f"CONVENTIONS.md: §2 declares status '{value}' but no rule ever sets it")


def check_explicit_invocation_only() -> None:
    """Every skill must be user-invocable only.

    Explicit invocation is this suite's defining decision, and for a long time it lived
    only in prose while the manifest said the opposite — any model could trigger `define`,
    `verify`, or `design` on a matching turn. The frontmatter key is what actually enforces
    it; a skill missing it is auto-triggerable no matter what its body claims.
    """
    for path in sorted(ROOT.glob("skills/*/SKILL.md")):
        head = path.read_text(encoding="utf-8").split("---")[1] if "---" in path.read_text(encoding="utf-8") else ""
        if "disable-model-invocation: true" not in head:
            err(f"skills/{path.parent.name}/SKILL.md: missing 'disable-model-invocation: true' "
                f"— the suite is explicitly invoked only, and prose does not enforce that")


def check_orchestrator_does_not_invoke_skills() -> None:
    """engineer runs phases by reading their files, not by invoking them.

    With every skill user-only, a Skill-tool call from the orchestrator cannot work. The
    routing must name the phase files, and each one it claims to run must be linked.
    """
    body = (ROOT / "skills/engineer/SKILL.md").read_text(encoding="utf-8")
    for phase in ["define", "blueprint", "construct", "verify", "inspect", "release"]:
        if f"../{phase}/SKILL.md" not in body:
            err(f"skills/engineer/SKILL.md: runs '{phase}' but never links its file — "
                f"with model invocation disabled, the file is the only way in")


def check_audit_skills_are_forked() -> None:
    """A skill whose §7 job is independence must declare `context: fork`.

    §7 names the audit skills that get an isolated context. Independence asserted in a
    body is a discipline the reviewer has to remember; declared in frontmatter it is how
    the runtime starts them. If §7 promises it, the manifest has to deliver it.
    """
    conventions = (ROOT / "CONVENTIONS.md").read_text(encoding="utf-8")
    promised = re.search(r"The audit skills — (.+?) — do not rely on that discipline",
                         conventions, re.S)
    if not promised:
        err("CONVENTIONS.md: §7 no longer names the forked audit skills — update this guard")
        return
    for name in re.findall(r"`([a-z]+)`", promised.group(1)):
        path = ROOT / f"skills/{name}/SKILL.md"
        if not path.is_file():
            err(f"CONVENTIONS.md: §7 promises a fork for '{name}', which is not a skill")
        elif "context: fork" not in path.read_text(encoding="utf-8").split("---")[1]:
            err(f"skills/{name}/SKILL.md: §7 promises it runs in an isolated context "
                f"but the frontmatter never declares 'context: fork'")


def check_standards_fields_are_consumed() -> None:
    """Every field in §4's standards.md template must be read by some rule.

    A field nobody consumes is a prompt to fill in a blank that changes nothing — the
    same dead-declaration shape as a status value no rule sets. If the template asks a
    project for it, something has to use it.
    """
    conventions = (ROOT / "CONVENTIONS.md").read_text(encoding="utf-8")
    block = re.search(r"\*\*`standards\.md`\*\* — how this codebase is written:\n```\n(.*?)```",
                      conventions, re.S)
    if not block:
        err("CONVENTIONS.md: §4's standards.md template not found")
        return
    fields = re.findall(r"^([A-Z][A-Za-z ]+):", block.group(1), re.M)
    corpus = conventions.replace(block.group(0), "") + "".join(
        p.read_text(encoding="utf-8") for p in sorted(ROOT.glob("skills/*/SKILL.md")))
    for field in fields:
        if f"`{field}:`" not in corpus and f"{field}:`" not in corpus:
            err(f"CONVENTIONS.md: §4's standards.md declares '{field}:' but no rule ever reads it")


def check_enforced_promises_are_documented() -> None:
    """A frontmatter key that enforces a user-facing promise must appear in the docs.

    These keys change what the suite can do, not just how it reads. Ten versions of
    behaviour landed before the docs mentioned any of it, and README still described the
    invocation rule as a promise after it had become a guarantee. If the manifest enforces
    something a user would notice, a document a user reads has to say so.
    """
    docs = "".join(
        p.read_text(encoding="utf-8")
        for p in [ROOT / "README.md"] + sorted(ROOT.glob("docs/*.md"))
        if p.is_file())
    # Match the full `key: value` declaration. A bare key name is not a test: "context"
    # alone occurs throughout ordinary prose, so searching for it passes on any page.
    declared = set()
    for path in sorted(ROOT.glob("skills/*/SKILL.md")):
        head = path.read_text(encoding="utf-8").split("---")
        if len(head) > 1:
            declared.update(re.findall(r"^((?:disable-model-invocation|context|allowed-tools|"
                                       r"user-invocable):\s*\S+)\s*$", head[1], re.M))
    for decl in sorted(declared):
        if decl not in docs:
            err(f"skills/: '{decl}' is declared but no README or docs/ page mentions it — "
                f"an enforced promise the user cannot read about")


def main() -> int:
    parsed = check_json_files()
    check_name_consistency(parsed)
    check_skills()
    check_root_skill()
    check_internal_links()
    check_no_ai_attribution()
    check_section_declarations()
    check_markdown_tables()
    check_template_keys()
    check_produced_artifacts_registered()
    check_ledger_vocabulary_is_reachable()
    check_explicit_invocation_only()
    check_orchestrator_does_not_invoke_skills()
    check_audit_skills_are_forked()
    check_standards_fields_are_consumed()
    check_enforced_promises_are_documented()
    if ERRORS:
        print(f"FAIL — {len(ERRORS)} problem(s):")
        for e in ERRORS:
            print(f"  ✗ {e}")
        return 1
    print("OK — manifests valid, skills complete, descriptions under cap, links resolve, no AI attribution, section declarations complete, tables well-formed, produced artifacts registered, ledger vocabulary reachable, invocation explicit-only, audits forked, standards fields consumed, enforced promises documented.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
