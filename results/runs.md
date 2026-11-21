# Pipeline runs

**First pass (no human input):** 4/5 issues reached an approved PR, and all 4 passed their hidden tests (13/13). The vague issue (#5) was escalated at requirements instead of guessing. Cost $0.61 in total, $0.12 per issue on average.

**After one human clarification on #5:** 5/5 issues have an approved PR, and hidden tests pass 16/16. Cost $0.76 in total, max $0.21 per issue (#5, both runs). There was 1 review send-back (#2) and 1 CI-failure retry (#5). The bot merged nothing; a human decides on PRs #7-#10 and #12.

Hidden tests are run by hand on the bot's branch after each run. The pipeline never sees them.

| Run | Issue | Rounds | Result | Hidden tests | Cost (USD) | Tokens in/out | Wall time | PR | Notes |
|---|---|---|---|---|---|---|---|---|---|
| [44920637328](https://github.com/keshavdubeyy/tinydb/actions/runs/44920637328) | #3 count() without a query | 0 send-backs | APPROVE on first review | 3/3 pass | 0.100 | 144,961 / 6,898 | ~4 min (incl. ~2 min CI) | [#7](https://github.com/keshavdubeyy/tinydb/pull/7) | First end-to-end run. 4 ACs, 4 tests. Guard denied 4 piped Bash commands (`... \| tail`); the agents retried with plain `python -m pytest`. |
| [44921295730](https://github.com/keshavdubeyy/tinydb/actions/runs/44921295730) | #1 search() after drop_table (bug) | 0 send-backs | APPROVE on first review | 3/3 pass | 0.126 | 167,594 / 11,739 | ~5 min | [#10](https://github.com/keshavdubeyy/tinydb/pull/10) | 5 ACs, 5 tests. |
| [44921298829](https://github.com/keshavdubeyy/tinydb/actions/runs/44921298829) + [44921683626](https://github.com/keshavdubeyy/tinydb/actions/runs/44921683626) | #2 failed update() half-applied (bug) | 1 send-back | CHANGES_CODE, then APPROVE | 4/4 pass | 0.191 | 391,148 / 16,749 | ~9 min | [#9](https://github.com/keshavdubeyy/tinydb/pull/9) | Round 0: reviewer failed R4 because `update_multiple` had the same partial-update bug. Round 1 fixed it with the tests unchanged, then APPROVE. The review loop worked as designed. |
| [44921301486](https://github.com/keshavdubeyy/tinydb/actions/runs/44921301486) | #4 limit for search() (feature) | 0 send-backs | APPROVE on first review | 3/3 pass | 0.135 | 204,486 / 10,475 | ~4 min | [#8](https://github.com/keshavdubeyy/tinydb/pull/8) | 5 ACs, 5 tests. |
| [44921303956](https://github.com/keshavdubeyy/tinydb/actions/runs/44921303956) | #5 "update operations are fragile" (vague) | n/a | STOPPED at requirements, escalated | 0/3 (no code) | 0.059 | 28,941 / 6,327 | ~1 min | none | The AI judge rejected AC-4 twice ("same as today" gives no concrete expected values), so the pipeline escalated rather than guessing. The escalation report is useful but wrongly calls its own $0.03 call cap "the budget". Fix this in the report generator. |
| [44922654212](https://github.com/keshavdubeyy/tinydb/actions/runs/44922654212) | #5 re-run after a maintainer clarification | 0 send-backs | APPROVE on first review | 3/3 pass | 0.154 (issue total 0.213) | 202,373 / 14,207 | ~7 min | [#12](https://github.com/keshavdubeyy/tinydb/pull/12) | The maintainer posted a clarifying comment and then `/autose`. This needed pipeline PR #11, which lets maintainer comments reach the agents. Self-corrections in this run: spec AC-2 was not in Given/When/Then form (retry fixed it), and CI failed the mypy type check on the PR (implementer retry fixed it, then CI passed). |

## Per-stage cost, run 44920637328

| Stage | Model | Cost | Turns |
|---|---|---|---|
| Requirements (spec) | claude-sonnet-5-5 | 0.032 | 2 |
| AI judge | claude-haiku-5-5 | 0.000 | 1 |
| Design | claude-sonnet-5-5 | 0.030 | 3 |
| Implement | claude-haiku-5-5 | 0.003 | 7 |
| Test | claude-haiku-5-5 | 0.003 | 5 |
| Review | claude-sonnet-5-5 | 0.033 | n/a |

## Review-only runs (seeded PRs and experiments)

Verdict details, labels and costs are in `experiment/seeded_prs/labels.md` and `results/experiments.md`.

| Run | Kind | PR | Reviewer | Verdict | Correct | Review |
|---|---|---|---|---|---|---|
| [44924367862](https://github.com/keshavdubeyy/tinydb/actions/runs/44924367862) | seeded (default) | [#13](https://github.com/keshavdubeyy/tinydb/pull/13) | claude-sonnet-5-5 | APPROVE | true | [on PR](https://github.com/keshavdubeyy/tinydb/pull/13) |
| [44924370850](https://github.com/keshavdubeyy/tinydb/actions/runs/44924370850) | seeded (default) | [#14](https://github.com/keshavdubeyy/tinydb/pull/14) | claude-sonnet-5-5 | CHANGES_CODE | true | [on PR](https://github.com/keshavdubeyy/tinydb/pull/14) |
| [44924375113](https://github.com/keshavdubeyy/tinydb/actions/runs/44924375113) | seeded (default) | [#15](https://github.com/keshavdubeyy/tinydb/pull/15) | claude-sonnet-5-5 | CHANGES_CODE | true | [on PR](https://github.com/keshavdubeyy/tinydb/pull/15) |
| [44924379841](https://github.com/keshavdubeyy/tinydb/actions/runs/44924379841) | seeded (default) | [#16](https://github.com/keshavdubeyy/tinydb/pull/16) | claude-sonnet-5-5 | CHANGES_CODE | true | [on PR](https://github.com/keshavdubeyy/tinydb/pull/16) |
| [44924382880](https://github.com/keshavdubeyy/tinydb/actions/runs/44924382880) | seeded (default) | [#17](https://github.com/keshavdubeyy/tinydb/pull/17) | claude-sonnet-5-5 | APPROVE | true | [on PR](https://github.com/keshavdubeyy/tinydb/pull/17) |
| [44925038019](https://github.com/keshavdubeyy/tinydb/actions/runs/44925038019) | expA (same_model) | [#13](https://github.com/keshavdubeyy/tinydb/pull/13) | claude-haiku-5-5 | APPROVE | true | [on PR](https://github.com/keshavdubeyy/tinydb/pull/13) |
| [44925040982](https://github.com/keshavdubeyy/tinydb/actions/runs/44925040982) | expA (same_model) | [#14](https://github.com/keshavdubeyy/tinydb/pull/14) | claude-haiku-5-5 | CHANGES_CODE | true | [on PR](https://github.com/keshavdubeyy/tinydb/pull/14) |
| [44925043823](https://github.com/keshavdubeyy/tinydb/actions/runs/44925043823) | expA (same_model) | [#15](https://github.com/keshavdubeyy/tinydb/pull/15) | claude-haiku-5-5 | CHANGES_CODE | true | [on PR](https://github.com/keshavdubeyy/tinydb/pull/15) |
| [44925046839](https://github.com/keshavdubeyy/tinydb/actions/runs/44925046839) | expA (same_model) | [#16](https://github.com/keshavdubeyy/tinydb/pull/16) | claude-haiku-5-5 | CHANGES_CODE | true | [on PR](https://github.com/keshavdubeyy/tinydb/pull/16) |
| [44925050553](https://github.com/keshavdubeyy/tinydb/actions/runs/44925050553) | expA (same_model) | [#17](https://github.com/keshavdubeyy/tinydb/pull/17) | claude-haiku-5-5 | APPROVE | true | [on PR](https://github.com/keshavdubeyy/tinydb/pull/17) |
| [44925179708](https://github.com/keshavdubeyy/tinydb/actions/runs/44925179708) | expB (with_spec) | [#13](https://github.com/keshavdubeyy/tinydb/pull/13) | claude-sonnet-5-5 | APPROVE | true | [on PR](https://github.com/keshavdubeyy/tinydb/pull/13) |
| [44925182739](https://github.com/keshavdubeyy/tinydb/actions/runs/44925182739) | expB (with_spec) | [#14](https://github.com/keshavdubeyy/tinydb/pull/14) | claude-sonnet-5-5 | CHANGES_CODE | true · invalid: spec not read | [on PR](https://github.com/keshavdubeyy/tinydb/pull/14) |
| [44925185685](https://github.com/keshavdubeyy/tinydb/actions/runs/44925185685) | expB (with_spec) | [#15](https://github.com/keshavdubeyy/tinydb/pull/15) | claude-sonnet-5-5 | CHANGES_CODE | true | [on PR](https://github.com/keshavdubeyy/tinydb/pull/15) |
| [44925190171](https://github.com/keshavdubeyy/tinydb/actions/runs/44925190171) | expB (with_spec) | [#16](https://github.com/keshavdubeyy/tinydb/pull/16) | claude-sonnet-5-5 | CHANGES_CODE | true | [on PR](https://github.com/keshavdubeyy/tinydb/pull/16) |
| [44925192698](https://github.com/keshavdubeyy/tinydb/actions/runs/44925192698) | expB (with_spec) | [#17](https://github.com/keshavdubeyy/tinydb/pull/17) | claude-sonnet-5-5 | APPROVE | true | [on PR](https://github.com/keshavdubeyy/tinydb/pull/17) |
| [44925408399](https://github.com/keshavdubeyy/tinydb/actions/runs/44925408399) | expB (with_spec) | [#14](https://github.com/keshavdubeyy/tinydb/pull/14) | claude-sonnet-5-5 | CHANGES_CODE | true | [on PR](https://github.com/keshavdubeyy/tinydb/pull/14) |

## Pipeline changes merged during the experiment (by the owner)

- [#6](https://github.com/keshavdubeyy/tinydb/pull/6): pipeline setup
- [#11](https://github.com/keshavdubeyy/tinydb/pull/11): maintainer clarifications + escalation budget fix (ADR-012)
- [#18](https://github.com/keshavdubeyy/tinydb/pull/18): specs for the Experiment B variant
