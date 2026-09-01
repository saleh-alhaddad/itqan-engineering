# UI craft — universal reference (framework-neutral)

The single source of truth for UI/UX quality across the suite. Loaded by the `design` skill
and by `define` / `construct` / `inspect` on frontend or mobile tasks. Every principle here
is **stack-agnostic** — adapt it to the detected framework and design system; never hard-code
a library. **Follow the project's own design system first**; these are the defaults when it
has none. Distilled as ideas from established UI craft practice, not copied.

## DESIGN & INTAKE — shaping the UI

1. **Intent first.** Identify the real human, the verb they must accomplish, and how it
   should *feel* — in words that mean something. Check every choice against that intent.
2. **Escape the "AI aesthetic."** Name the defaults and refuse them on free axes: default
   purple/violet gradients, Inter/Roboto everywhere, over-rounded everything, stock hero +
   template metric cards, AI copy clichés ("Elevate", "Seamless"). Mine the product's real
   domain for a **signature element** that could only exist for this product.
3. **Content before container.** Resolve the actual feature/data first, then the frame.
4. **Grayscale-first.** Prove layout and hierarchy with size/weight/spacing *before* color,
   so decoration can't fake structure.
5. **Constrain the system up front.** Closed scales for spacing, size, type, and z-index —
   no arbitrary values. Fewer choices is a feature, not a limitation.
6. **Commit to one visual identity** appropriate to the product type; match type and shape
   personality to its tone. Record the choice in `design.md`.

## BUILD — implementing the UI

**Tokens & scales**
7. **Token architecture:** primitive → semantic → component; no raw hex in components; ~four
   text-emphasis levels.
8. **Spacing/layout:** a 4/8-pt grid, multiples only; density chosen deliberately in px;
   uneven rhythm — tight within a group, air between groups; consistent container widths.
9. **Type:** a ratio-stepped scale with a ~16px body floor; keep it lean (≈4 sizes, 2
   weights); optical tracking on large type; **tabular figures** for numeric data; balanced
   headings and tidy body wrapping.
10. **Color:** ~60/30/10 distribution; color is scarce and meaningful — structure in
    neutrals, **one accent per view**; semantic states carry an icon + text, never color alone.
11. **Depth:** pick **one** elevation strategy (borders-only / subtle shadow / layered /
    tonal-surface) and commit; whisper-quiet few-% lightness steps; low-opacity borders;
    concentric nested radius.

**Composition & hierarchy**
12. **Compose from accessible primitives:** native element → headless primitive → hand-roll.
    Never hand-rebuild keyboard/focus/ARIA behavior. Extract a component only on real reuse;
    prefer what the project already provides.
13. **Hierarchy is a lever:** size + weight + color together (not size alone); **de-emphasis
    is a tool** — lower a secondary element rather than only amplifying the primary; one
    focal point per view.

**Motion**
14. **Motion budget:** animate only compositor-cheap properties (transform/opacity); UI
    transitions < 300ms (interaction feedback ~200ms) with a custom ease-out; press feedback
    (~scale 0.97); spatial/origin-aware transitions; always honor `prefers-reduced-motion` and
    pointer-fine (`hover:hover`); animate only with intent.

**Performance (as principles)**
15. **Parallelize, don't waterfall:** run independent async/data work concurrently;
    code-split and lazy-load heavy or offscreen work to cut initial load.
16. **State lives at the lowest sufficient level:** local → lifted → context →
    **URL/searchParams for filters, sorting, and pagination** (shareable, survives refresh) →
    server-cache → global store. **Derive, don't sync:** compute from existing state during render instead of mirroring it
    through effects; keep callbacks/references stable to avoid churn; memoize only genuinely
    expensive work; hoist static content out of render.
17. **Virtualize large collections** with stable item identity; reserve image dimensions to
    prevent layout shift; show a skeleton for waits > ~300ms.

**Platform edges & localization**
18. Handle **safe-area insets**, dynamic viewport sizing, adequate hit targets (≥44px), and
    one fixed z-index scale; follow the platform's native navigation idioms.
19. **i18n:** route user-facing text through the translation layer; support RTL mirroring and
    locale-aware date/number/currency formatting (see the frontend/mobile packs).

**UX copy**
20. Copy is design material: active voice; name things by what the user controls; consistent
    action vocabulary through a flow; errors state **cause + fix**; empty states are
    invitations with one clear action.

## VERIFY — exercise it

21. **Complete state coverage.** Every interactive element: default / hover / focus-visible /
    active / disabled / loading. Every data view: loading / empty / error / success. Missing
    states are the fastest "unfinished" tell.
22. **Accessibility floor (testable):** WCAG AA contrast (4.5:1 text, 3:1 large/UI), visible
    keyboard focus, semantic markup before ARIA, dynamic type, reduced motion, color never
    the sole signal. Every a11y claim must be independently verifiable.
23. **Render and interact for real** across sizes and orientations; no horizontal scroll on
    the body; safe areas correct.

## REVIEW — judge it (evidence-based)

24. **A UI finding is valid only with three things:** a violated contract (the project's own
    token/design system), a demonstrated runtime impact, and a deterministic fix. This kills
    "I'd prefer…" nitpicks.
25. **Fixed axis checklist** (repeatable, not taste-driven): hierarchy/prominence,
    contrast/readability, spacing/density, consistency/polish, states/feedback, responsive
    presentation, system-coherence, motion, accessibility.
26. **Preserve product identity.** Don't flatten a distinctive design toward generic "best
    practice"; drift is a defect only when it actually reaches the reviewed surface.
27. **Craft self-audit:** squint test (hierarchy holds, nothing harsh), one focal point per
    view, single depth strategy, single accent, consistent spacing rhythm, concentric radius,
    tabular figures on data.
