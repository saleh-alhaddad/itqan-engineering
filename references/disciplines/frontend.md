# Discipline pack — Frontend (web)

Load when the repo shows a web UI framework (react/vue/svelte/angular), a bundler config
(vite/next/webpack), `.tsx/.jsx`, a `components/` tree, or `index.html`. Adds client-side
concerns. Framework and design system are detected, never assumed. Read
[ui-craft.md](ui-craft.md) for the universal UI craft rules; this pack adds only the
web-specific concerns on top.

> **Authority: lowest ([CONVENTIONS §4.2](../../CONVENTIONS.md)).** This pack is general guidance, not this
> codebase's rules. Where the repo already does something its own way, follow the repo, and
> say when you use this pack's advice instead. It never overrides a decision the user made,
> and it never justifies copying a defect.

## In DEFINE (spec)
- Define the **states** every view must handle: loading, error, empty, and success — not just
  the populated happy path. Missing states are the most common UI gap.
- Capture responsive intent (breakpoints, mobile-first) and any design-system constraints.
- **Internationalization:** check whether the app already has i18n or needs multiple
  languages. If either is true, note it — user-facing text must go through the i18n layer,
  and RTL/bidi and locale formatting (dates, numbers, currency) are in scope.

## In BUILD (construct)
- **Build to `design.md`** — the distilled UI spec (screens, states, interactions, tokens)
  is the source of truth; if it's absent on a UI task, `define` should have captured it (§6.2).
- **Follow the existing design system / tokens** — colors, spacing, type. Do not invent a
  parallel styling approach. If the project has none, read `design.md` for the choice the
  user confirmed (§6.2), e.g. a component library like shadcn/ui + Tailwind for React, and
  build on that. **If no confirmed choice is recorded, stop and ask**: never assume one was
  made.
- Build **accessible by default**: semantic HTML, labels tied to inputs, keyboard operability,
  focus management, sufficient contrast (target WCAG AA).
- Prefer **composition over configuration** for components; keep state local until it must be
  shared.
- Handle all four states from the spec in the component itself.
- **i18n, not hardcoded English.** If the app has an i18n setup (i18next / react-intl /
  next-intl / vue-i18n or similar), route **every** user-facing string through it with
  translation keys — never hardcode display text. If multiple languages are required but no
  setup exists, propose adding one before scattering literals. Support RTL and locale-aware
  formatting where relevant.
- Avoid the generic "AI aesthetic" (default purple gradients, over-rounded everything, stock
  hero layouts) unless the design system calls for it — match the product's real look.

## In VERIFY
- Actually render and interact with the component — click the flow, tab through it, resize it.
  Load [browser-verify.md](browser-verify.md) for the mechanics (console-clean gate,
  screenshot evidence, network triage). Prefer the **accessibility tree** over pixels for
  element location and assertions — semantic roles/labels are cheaper and more robust than
  coordinates, and they double-check a11y for free.
- Check loading/error/empty render correctly, not only the success state.

## In REVIEW (inspect) — surface-specific
- **i18n:** hardcoded user-facing strings that bypass the translation layer; missing/duplicate
  keys; broken RTL or locale formatting when localization is in scope.
- **Accessibility:** keyboard traps, unlabeled controls, missing alt text, contrast failures,
  ARIA misuse, focus order.
- **Security:** XSS via unsanitized HTML injection, unsafe `dangerouslySetInnerHTML`/`v-html`,
  secrets shipped to the client, tokens in `localStorage` where a cookie is safer.
- **Performance (Core Web Vitals):** oversized bundles/images, layout shift, unnecessary
  re-renders, unmemoized expensive work (only after checking the installed version and
  compiler, §17: with React 19's compiler, manual memoization is not needed), blocking the
  main thread, missing lazy-loading.

## In SHIP (release)
- Progressive rollout where the surface is user-facing; watch client error rates and CWV.
