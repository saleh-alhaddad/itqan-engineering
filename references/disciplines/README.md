# Discipline packs

These are not skills — they are reference files that the phase skills (`construct`, `verify`,
`inspect`) and the orchestrator (`engineer`) load based on the stack detected in the repo.
Each pack adds the concerns specific to one surface, without hard-coding any framework.

A repo can match more than one (e.g. a full-stack web app = backend + frontend). The changed
file paths narrow which pack's concerns dominate for a given task.

`ui-craft.md` is the shared, framework-neutral UI reference that the frontend and mobile
packs (and the `design` skill) build on — it holds the universal UI/UX craft rules so they
aren't repeated in each pack.

| Pack | Load when the repo shows | File |
|------|--------------------------|------|
| Backend | server framework, routes/controllers, db/migrations, Dockerfile, API schema | [backend.md](backend.md) |
| Frontend | react/vue/svelte/angular, bundler config, `.tsx/.jsx`, `components/`, `index.html` | [frontend.md](frontend.md) |
| Mobile | `pubspec.yaml`, `ios/`+`android/`, `Podfile`, `*.xcodeproj`, `build.gradle`, react-native, `.swift`/`.kt` | [mobile.md](mobile.md) |
| AI/ML | torch/tensorflow/transformers, `*.ipynb`, `train.py`, `model/`, dataset/eval configs | [ai-ml.md](ai-ml.md) |
| Any language | none of the above match cleanly — infer from file extensions + build files | [any-language.md](any-language.md) |

**Cross-cutting concern packs** (load alongside the stack pack when the change touches them):

| Pack | Load when | File |
|------|-----------|------|
| Database | ORM/migrations/SQL/DB driver present, or data-model work | [database.md](database.md) |
| Security | untrusted input, auth, secrets, payments, PII, integrations (also backs the `harden` skill) | [security.md](security.md) |
| DevOps | CI config, containers, IaC, deploy manifests, or pipeline/ops work | [devops.md](devops.md) |
| Browser verify | verifying/reviewing a web UI with a drivable browser | [browser-verify.md](browser-verify.md) |

**Detection is stated, not silent.** `engineer` prints what it found and which pack it is
using so the user can correct it in one word (see `engineer` startup).
