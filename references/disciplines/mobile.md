# Discipline pack — Mobile

Load when the repo shows `pubspec.yaml` (Flutter), `ios/`+`android/` folders, `Podfile`,
`*.xcodeproj`, `build.gradle`, a react-native dependency, or `.swift`/`.kt` sources. Adds
native/mobile concerns. Platform and framework are detected, never assumed. Read
[ui-craft.md](ui-craft.md) for the universal UI craft rules; this pack adds only the
mobile-specific concerns on top.

## In DEFINE (spec)
- Which **platforms** (iOS / Android / both) and minimum OS versions.
- **Offline behavior**: what works with no network, how data syncs, conflict handling.
- Define states across **device sizes and orientations**, not one screen size.
- **Internationalization:** check whether the app has localization or needs multiple
  languages; if so, note that user-facing text goes through the platform's localization
  system, and RTL layouts + locale formatting are in scope.

## In BUILD (construct)
- **Build to `design.md`** — the distilled UI spec (screens, states, interactions, tokens)
  is the source of truth; if it's absent on a UI task, `define` should have captured it (§6.2).
- Respect the platform's **Human Interface Guidelines** — navigation patterns, gestures,
  system controls, safe areas/notches. Don't fight the platform's conventions.
- **Localize, don't hardcode.** Route user-facing text through the platform's localization
  system (Flutter `intl`/ARB, iOS String Catalogs/`Localizable.strings`, Android
  `strings.xml`, or the RN i18n library in use) — never hardcode display strings. Support RTL
  (mirror layouts) and locale-aware date/number formatting where localization is in scope.
- Layout must adapt to screen sizes, orientation, dynamic type, and safe-area insets.
- Manage the **lifecycle**: background/foreground transitions, state restoration, permission
  prompts requested in context.
- Be frugal with battery, memory, and network — mobile resources are constrained.

## In VERIFY
- Exercise on more than one device profile / orientation; test the offline path and the
  permission-denied path. Drive the UI via the platform's **accessibility tree** (roles,
  labels, element refs), not screenshot coordinates — cheaper, more robust, and it verifies
  accessibility as a side effect.
- Verify state survives backgrounding and process death.

## In REVIEW (inspect) — surface-specific
- **Security:** secure storage for tokens/PII (keychain/keystore, not plaintext prefs),
  certificate handling, no secrets in the bundle, least-privilege permissions, safe deep-link
  handling.
- **Performance:** jank/dropped frames, main-thread work, oversized images, memory leaks from
  retained references/listeners, excessive wakeups and network chatter, slow cold start.
- **UX:** accessibility (screen reader labels, dynamic type, contrast, tap-target size).
- **i18n:** hardcoded user-facing strings, broken RTL mirroring, or wrong locale formatting
  when localization is in scope.

## In SHIP (release)
- Staged store rollout / phased release where supported; feature-flag risky changes since app
  updates can't be recalled as fast as a server deploy.
- Crash and ANR reporting in place before release.
