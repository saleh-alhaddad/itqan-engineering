# Discipline pack — DevOps / delivery & operations

Load when the repo shows CI config, containerization, IaC, or deploy manifests (a
`Dockerfile`, `.github/workflows`, `k8s/`, Terraform, a Procfile, etc.), or when the task is
about pipelines, deployment, or operability. Tools are detected, never hard-coded.

## In DEFINE (spec)
- Capture the delivery constraints: target environments, deployment strategy expectations,
  and the on-call questions the feature must answer once live (what signal says "working?").

## In BUILD (construct)
- Pipelines run an **ordered shift-left gate ladder — lint → typecheck → unit → build →
  integration → e2e → dependency audit** — enforced by branch protection so red blocks
  merge; cheap gates first so failures surface in seconds, not minutes.
- **Budget ~10 minutes** for the pipeline; when exceeded, escalate in order: cache deps →
  parallelize jobs → path-filter → shard/matrix. CI holds **no production secrets** (its own
  separate secret set); a preview deployment per PR where the platform supports it.
- Keep pipelines deterministic (pinned versions, no flaky ordering).
- Build once, promote the **same artifact** across environments; don't rebuild per stage.
- Config and secrets via environment/secret store (12-factor), never baked into the image or
  repo; CI secrets from the CI store, never in logs.
- **Instrumentation is a build deliverable, not an afterthought:** write the 2–4 questions
  on-call will ask *before* adding telemetry, and make every signal answer one. Structured
  logs with correlation IDs, the RED/USE metrics, health/readiness endpoints — with
  **bounded metric labels only** (never user ID, raw URL, request ID, or error text — a
  cardinality bomb) and **percentiles (p95/p99 histograms), never averages**. Every alert
  gets a runbook link and one test-fire before launch; prove the telemetry by inducing a
  failure in staging and locating it from telemetry alone.
- Infrastructure as code where it exists — reviewed and versioned like app code.

## In VERIFY
- Run the pipeline (or its steps) for real: build the artifact, run the suite as CI runs it.
- Exercise the health/readiness endpoints and confirm the new metrics/logs actually emit.
- Deploy to a staging/preview environment where one exists and smoke-test the deployed
  artifact — "works on my machine" is not a verified deploy.

## In REVIEW (inspect)
- Pipeline correctness (does it test what ships?), missing rollback path, secrets leaking
  into CI logs or images, missing health checks, unpinned deploy dependencies, environment
  drift, cost/scale blind spots (unbounded autoscale, oversized instances).

## In SHIP (release)
- CI green **on the exact commit being shipped**; the promoted artifact is the tested one.
- Reversible rollout: flags, blue-green, or canary — with named metrics, numeric abort
  thresholds, and a bake time per stage written down *before* stage one (ties to release).
- Dashboards + symptom alerts live before launch; the rollback command rehearsed/known.
- Incident path after ship: stabilize/rollback first → root-cause (verify) → blameless
  postmortem into `decisions.md` → guard so it can't silently recur.
