# ADR-006: Cheap models for the workers, a stronger model where thinking matters, and a different model for the reviewer

- **Status:** Accepted (2026-11-21, after author review, before any agent code). The
  reviewer choice is tested in Experiment A.
- **Decision area:** D6, models

## Context

The budget is a hard **$10/month**, and about $1.29 was already spent this month. The whole
assignment (5 issues, retries, 5 seeded PRs, two experiments with several runs each) needs
roughly 25–40 runs. So a run should cost well under $0.50 on average.

My view: for now we go cheap, and we are strategic about it. Most models can do these tasks
if each one is told clearly what to do, why, and what the goal is. That clarity comes from
the prompts and the checks, not from paying for the biggest model. Where more thinking is
really needed, it is in planning: a bad spec or plan sends every later agent the wrong way.

Prices (Anthropic API, per million tokens, checked 2026-11-21):

| Model | ID | Input | Output |
| --- | --- | --- | --- |
| Claude Opus 5.5 | `claude-opus-5-5` | $4.00 | $20.00 |
| Claude Sonnet 5.5 | `claude-sonnet-5-5` | $2.00 | $10.00 |
| Claude Haiku 5.5 | `claude-haiku-5-5` | $0.10 | $0.50 |

Haiku 5.5 is 20× cheaper than Sonnet 5.5. The changes in our issues are small (a few lines in
one or two TinyDB files).

## Decision

| Agent | Model | Why |
| --- | --- | --- |
| Planner | **Sonnet 5.5** | Planning needs the most thinking, and mistakes here are the most expensive. Its inputs are small (issue, condensed skill, architecture doc), so the better model costs little. |
| Implementer | **Haiku 5.5** | Small, well-specified changes with a clear spec and plan. It does many tool calls (reading files, running tests), so a cheap model matters most here. |
| Tester | **Haiku 5.5** | Writing one test per criterion from a clear spec is a narrow task. |
| Reviewer | **Sonnet 5.5** | It must be a **different model from the Implementer** (ADR-008), and a cheap builder is best checked by a stronger checker. |
| Orchestrator, release, gate | No model | Plain code. |

Settings: reasoning effort `medium` for the Planner and Reviewer, `low` for the Implementer
and Tester. Each stage has a turn limit, and the orchestrator adds up the cost the SDK
reports after every stage and stops at the budget in ADR-009.

**Rough cost per run** (with prompt caching on repeated context): Planner ≈ $0.08,
Implementer ≈ $0.03, Tester ≈ $0.02, Reviewer ≈ $0.15. That is about **$0.30 per run**,
or roughly $9–12 for 30–40 runs. This is tight. If the real numbers are higher, the limit
goes up to $20 and the report says so.

## Alternatives

- **Opus 5.5 everywhere.** Best quality. Rejected: about 2× Sonnet and 40× Haiku per token. The
  budget would run out within a few runs.
- **Haiku everywhere.** Cheapest. Rejected: the reviewer would be the same model as the
  implementer (it must differ), and the spec quality that everything depends on would be
  weakest.
- **Sonnet for the Implementer, Haiku for the Reviewer.** Also two different models.
  Rejected: a weak checker on a strong builder is the wrong way round. Bugs from a capable
  builder are subtler, and a cheap reviewer is more likely to just approve.
- **A second provider (e.g. an OpenAI model) as reviewer.** Maximum diversity. Rejected for
  now: a second key, a second SDK and a second bill. A different Claude model tier already
  gives a different model. This can be a future change.

## Consequences

- A cheap Implementer may need more retries. We will report attempts per issue, and if retries
  cost more than a stronger model would, this ADR gets superseded.
- **Experiment A** compares the Reviewer on Sonnet 5.5 (different from the Implementer) against
  the Reviewer on Haiku 5.5 (same as the Implementer) on the seeded PRs.
- Total tokens and cost per run go in `results.csv`, as the assignment requires.

## Evidence after the runs (21 Nov 2026)

- **Experiment A:** Haiku as reviewer also got 5/5 seeded PRs right, at about 1/7 of the cost ($0.019 vs $0.133 for five reviews). It filled the rubric less precisely (once it filed a logic bug under R5) and once went deeper than Sonnet. See `results/experiments.md`.
- **Decision: keep Sonnet as reviewer.** A review costs about $0.03 per issue, and the reviewer is the last check before a human. The case we care most about was not tested with Haiku: in issue #2, Sonnet found a second, unreported copy of the bug. The saving is real but small in dollars. The argument for this ADR is now weaker than when it was written. If a harder seeded set showed no gap either, this ADR should be superseded.
- **The cheap implementer held up.** Across 6 issue runs it needed 1 retry after a review send-back (issue #2) and 1 after a CI failure (issue #5). No run ran out of budget.
