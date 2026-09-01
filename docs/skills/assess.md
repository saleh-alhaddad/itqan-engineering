# assess — whole-app health

[← Book index](../README.md) · a five-expert panel over your product

**What it is:** the app-level review — not a diff, not a screen, the *product*: how features
link, which are strong, which are thin, and where you stand against the market.

## How it works

```mermaid
flowchart TD
  E[evidence base: code · feature changelog ·<br/>measured usage · docs] --> P{{five expert lenses}}
  P --> L1[domain expert:<br/>real workflows served?]
  P --> L2[software engineer:<br/>coupling · fragile areas]
  P --> L3[PM: incomplete journeys ·<br/>features that don't compose]
  P --> L4[market analyst:<br/>cited, today's date]
  P --> L5[improvement lead:<br/>value vs effort synthesis]
  L1 & L2 & L3 & L4 & L5 --> R[assessment.md:<br/>feature map · Strong · Needs improvement ·<br/>market position · next moves]
  R --> H[your pick → define/blueprint ⛔]
```

## Best cases

- **"Which features are weak?"** — periodic product health checks.
- **Before planning a big quarter** — its ranked "next moves" feed `discover`/`define`.
- **Inherited products** — a new owner's honest map of what's actually there.

## Example

```
itqan:assess "analyze my app — feature linkage, strong vs weak, vs the market"
```

## What you get

`assessment.md`: a feature-linkage map · **Strong** (with evidence — it says what's good,
not just what's wrong) · **Needs improvement** ranked by value-vs-effort with the concrete
fix and which expert flagged it · a cited market position. Optionally a throwaway prototype
of the top recommendation so you can *feel* it before deciding.

## Hand-offs

Approved improvements → `define` → `blueprint`, stopping at the normal plan gate. Net-new
ideation leads with `discover`; code-level review with `inspect`; security depth with
`harden`. Reuses the run's multi/single-agent answer instead of re-asking.

**Pro tip:** it asks two things up front — panel as parallel agents or one, and
report-only vs report+prototype. Pick report-only the first time; add the prototype when a
finding is worth feeling.
