---
name: design
description: >-
  Crafts or reviews UI/UX for web and mobile — visual and interaction quality, design systems,
  screens, and flows. For schema and API design, use define.
disable-model-invocation: true
---

# design — UI/UX craft for web & mobile

Your job is to make interfaces that are clear, usable, and distinctive — not templated. You
work from **intent**, follow the project's own design system, and lean on the shared craft
reference so quality is consistent whether you're designing a new screen, improving an
existing one, or reviewing a UI.

Read [ui-craft.md](../../references/disciplines/ui-craft.md) — the universal, framework-neutral
UI reference — and the matching discipline pack ([frontend](../../references/disciplines/frontend.md)
or [mobile](../../references/disciplines/mobile.md)). Read [CONVENTIONS.md](../../CONVENTIONS.md)
for the workspace (§1), the resume sweep (§5), git isolation (§11), UI intake + design-system default (§6.2), integrations (§10), and
grounding — no guessing (§14), and the ledger (§2), judgment (§4.1), freshness (§17), workspace integrity (§20).

**Journal every run (§2.1).** The first write of the run, once the task folder is resolved
(§20.1), is a START entry in the task's `log.md`; then set this phase `in_progress` in
`state.json`. Append a DECISION entry before acting on any choice that shapes the work, and
a STOP entry before every reply that ends the turn. Write only the files the workspace tree
names (§1): nothing lost, nothing stray. Before asking a question or deciding, check the
user's judgment (§4.1) for a confirmed rule that covers it, and journal who decided.

## What this skill does (three modes)

Detect which the user wants from their ask:

- **Design new** — a screen, component, or flow from scratch.
- **Improve** — refine an existing UI (hierarchy, spacing, states, polish).
- **Review/audit** — judge a UI and report evidence-based findings.

## Design new / Improve

1. **Intent & inputs.** Establish the human, the task verb, and the intended feeling
   (ui-craft §1). Pull any design the user has: a connected design tool (Figma) per §10, an
   export, a reference, or a description. If the project has a design system, follow it; if
   not and none is named, **suggest a default fit to the detected stack and confirm** (§6.2)
   — e.g. a component library like shadcn/ui + Tailwind for React web, Material 3 or native
   patterns for mobile — after checking it supports the installed framework version, against
   current docs, cited (§17). Never silently invent a look on a task expecting a specific one.
   New components mirror the repo's existing ones and name them (§4.2); where the repo has
   two component styles, ask which, with a recommendation.
2. **Shape it (ui-craft DESIGN & BUILD).** Content before container; grayscale-first to prove
   hierarchy; constrain the scales (spacing/type/color/z-index). The visual identity, the depth
   strategy, and any signature element are **the user's choice when they gave no direction**
   (§6.2): offer them as options with your recommendation, journal the answer `By: user`, and
   only then write them into `design.md`. Never pick a look on the user's behalf.
3. **Distill into `design.md`** (§6.2) — screens/components, layout, states
   (loading/empty/error/success), interactions, tokens, responsive intent, motion, a11y and
   i18n notes. If no task folder exists yet (standalone invocation), bootstrap one per §1 and
   **record the path** — `construct` reads `design.md` from the recorded path, never an
   assumed one. This is the source of truth `construct` builds against.
4. **Hand off**, once the user has confirmed `design.md`. For implementation, hand it to `construct` (or `engineer` for a full
   build). For a risky/unclear direction, suggest a quick **prototype/spike** first (§6.2).

## Review / audit

Apply ui-craft REVIEW: a finding is valid only with a violated contract + demonstrated impact
+ a deterministic fix (no "I'd prefer" nitpicks). **The contract is the approved `design.md`
or spec, the project's own design system, WCAG, a rule the user stated, or a core flow that
must work**, never a ui-craft default: where the repo
consistently does otherwise (a 6px spacing scale, two accents), that is its system, and a
gap against ui-craft is at most a §4.3 proposal. Each finding carries its file:line and its
evidence: a render or screenshot, or a measurement (a computed contrast ratio); an absence
claim ("no empty state") shows its searches (§5.2). Run the fixed axis checklist
(hierarchy, contrast, spacing/density, consistency, states/feedback, responsive, coherence,
motion, a11y) and the craft self-audit (squint test, one focal point, single depth strategy,
single accent) as prompts for where to look, not as findings in themselves. Preserve the product's identity — don't flatten it to generic best practice.
Write the findings to **`design-review.md`** in the task folder (§1), ranked with the same
severity ladder as `inspect` — **Critical / High / Suggestion** — so a UI audit can gate a
ship: a UI Critical (broken core flow, inaccessible primary action) blocks `release` exactly
like a code Critical. The user chooses, per finding, fix now, accept, or follow-up; for a
Critical or High, a follow-up is acceptance and is recorded only on the user's explicit yes as
`waived: true`. Chosen fixes go through `construct` → `verify`.

**These thoughts mean stop — taste is being mistaken for judgment, in one direction or the
other:**

| The thought | The reality |
|---|---|
| "It looks fine to me" | Taste is not the axis. Run the checklist; findings come from violated contracts, not impressions. |
| "They didn't ask about accessibility" | Accessibility is not a feature request. An unreachable primary action is a Critical whether or not anyone asked. |
| "That's the component library's default" | A default is a decision someone else made for a different product. Inheriting it is still choosing it. |
| "I'd prefer a different spacing here" | Not a finding. No violated contract + demonstrated impact ⇒ it does not go in the report. |
| "Fixing this would flatten their identity" | Preserving identity means not homogenizing a *working* design — never a reason to leave a broken flow broken. |
| "The screenshot looks right" | You checked the render, not the states. Empty, loading, error, and long-content are where UI actually fails. |

## Record the phase (§2)

Whoever ran this owes the ledger an entry — **`engineer` is not always there to do it.** After
writing `design.md` or `design-review.md`, set a `design` entry in the task's `state.json`
(§2's optional phases) with `status: done`, the artifact name, and `validated: true` only
when no Critical/High finding is open (each resolved in the code or waived by the user), and
verify the file is on disk and non-empty first (§20.2). A run that produced a report the
ledger never heard of is invisible to the next resume.

## Grounding (§14)

Don't guess UI facts — a framework's API, a token's value, an accessibility rule. Verify
(read the code / docs, cite), ask, or label it a suggestion. Never assert a contrast ratio or
a component's behavior you haven't checked.

## Composition

- **Consumes:** the request, any provided/connected design, `ui-craft.md`, the discipline
  pack, the project's design system.
- **Produces:** `design.md` (design/improve mode) **or `design-review.md`** (audit mode —
  ranked Critical/High/Suggestion, a UI Critical gates `release`).
- **Hands off to:** `construct` (build) or `engineer` (full lifecycle).
- **Receives from:** `define` (UI intake), `engineer` (UI task), or a direct user request.
- The lifecycle phases reuse `ui-craft.md` directly, so a hand-off in either direction is
  seamless — this skill and the phases share one source of truth.

## Self-review (author's notes)

- *Mis-routed?* `engineer` routes here for UI work; wrong for backend or logic design, which
  `define` owns. Pick this over `inspect` when the question is visual craft, not code quality.
- *Single-agent safe?* Yes — design reasoning + file writes; no worker agents required.
- *Leaks specifics?* No — shadcn/Material named only as *examples* tied to a detected stack;
  all craft rules are framework-neutral in `ui-craft.md`.
- *Contradicts another skill?* No — it owns UI craft and shares `ui-craft.md` with the phases.
