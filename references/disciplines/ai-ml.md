# Discipline pack — AI / ML

Load when the repo shows ML frameworks (torch/tensorflow/transformers/jax/sklearn), `*.ipynb`
notebooks, `train.py`/`eval.py`, a `model/` or `data/` tree, or dataset/eval configs. Covers
both classic ML and LLM-application work. Framework and model are detected, never assumed.

## In DEFINE (spec)
- Define **success as a metric**, not a vibe: the eval set, the metric(s), and the target/
  baseline to beat. "Better" is untestable; "+X on this held-out set" is.
- Name the **data**: source, licensing, PII, train/validation/test split, and leakage risks.
- For **LLM apps**: the task contract (input → expected output shape), the failure modes that
  matter (hallucination, refusal, injection), and guardrails.

## In BUILD (construct)
- **Reproducibility first:** pin seeds, versions, and data snapshots; separate config from
  code so a run can be reproduced exactly.
- Keep a clean **train/validate/test** boundary — never let test data leak into training or
  tuning.
- For LLM apps: treat prompts as versioned artifacts; ground outputs in retrieved/authoritative
  context rather than the model's memory where correctness matters.
- Test-first still applies: write the **evaluation** before the model/prompt, so "done" is a
  number you move, not an impression.

## In VERIFY
- Run the eval set fresh and report the metric with the number — same evidence rule as any
  other verify.
- Check the failure cases explicitly (adversarial inputs, edge distributions), not just
  aggregate accuracy.

## In REVIEW (inspect) — surface-specific
- **Correctness:** data leakage, overfitting to the eval set, metric that doesn't match the
  real objective, non-reproducible runs.
- **Security/safety:** prompt injection and unsafe tool/agent use in LLM apps, PII in training
  data or logs, model/data supply-chain provenance, secrets in notebooks.
- **Performance/cost:** inference latency and token/compute cost, batch efficiency, caching.

## In SHIP (release)
- Roll out behind a flag with an offline→shadow→small-%→full path; monitor the live metric and
  drift, and keep the previous model/prompt version as an instant rollback.
