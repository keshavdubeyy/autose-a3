# Pipeline runs

**Summary (first pass, 5 issues):** 4/5 reached an approved PR, and all 4 passed their hidden tests (13/13). 1/5 (the vague issue) was escalated at requirements. Total cost was $0.61, mean $0.12 per issue, max $0.19. Review send-backs: 1 (issue #2). Nothing was merged by the bot.

Hidden tests are run by hand on the bot's branch after each run. The pipeline never sees them.

| Run | Issue | Rounds | Result | Hidden tests | Cost (USD) | Tokens in/out | Wall time | PR | Notes |
|---|---|---|---|---|---|---|---|---|---|
| [44920637328](https://github.com/keshavdubeyy/tinydb/actions/runs/44920637328) | #3 count() without a query | 0 send-backs | APPROVE on first review | 3/3 pass | 0.100 | 144,961 / 6,898 | ~4 min (incl. ~2 min CI) | [#7](https://github.com/keshavdubeyy/tinydb/pull/7) | First end-to-end run. 4 ACs, 4 tests. Guard denied 4 piped Bash commands (`... \| tail`); the agents retried with plain `python -m pytest`. |
| [44921295730](https://github.com/keshavdubeyy/tinydb/actions/runs/44921295730) | #1 search() after drop_table (bug) | 0 send-backs | APPROVE on first review | 3/3 pass | 0.126 | 167,594 / 11,739 | ~5 min | [#10](https://github.com/keshavdubeyy/tinydb/pull/10) | 5 ACs, 5 tests. |
| [44921298829](https://github.com/keshavdubeyy/tinydb/actions/runs/44921298829) + [44921683626](https://github.com/keshavdubeyy/tinydb/actions/runs/44921683626) | #2 failed update() half-applied (bug) | 1 send-back | CHANGES_CODE, then APPROVE | 4/4 pass | 0.191 | 391,148 / 16,749 | ~9 min | [#9](https://github.com/keshavdubeyy/tinydb/pull/9) | Round 0: reviewer failed R4 because `update_multiple` had the same partial-update bug. Round 1 fixed it with the tests unchanged, then APPROVE. The review loop worked as designed. |
| [44921301486](https://github.com/keshavdubeyy/tinydb/actions/runs/44921301486) | #4 limit for search() (feature) | 0 send-backs | APPROVE on first review | 3/3 pass | 0.135 | 204,486 / 10,475 | ~4 min | [#8](https://github.com/keshavdubeyy/tinydb/pull/8) | 5 ACs, 5 tests. |
| [44921303956](https://github.com/keshavdubeyy/tinydb/actions/runs/44921303956) | #5 "update operations are fragile" (vague) | n/a | STOPPED at requirements, escalated | 0/3 (no code) | 0.059 | 28,941 / 6,327 | ~1 min | none | The AI judge rejected AC-4 twice ("same as today" gives no concrete expected values), so the pipeline escalated rather than guessing. The escalation report is useful but wrongly calls its own $0.03 call cap "the budget". Fix this in the report generator. |

## Per-stage cost, run 44920637328

| Stage | Model | Cost | Turns |
|---|---|---|---|
| Requirements (spec) | claude-sonnet-5-5 | 0.032 | 2 |
| AI judge | claude-haiku-5-5 | 0.000 | 1 |
| Design | claude-sonnet-5-5 | 0.030 | 3 |
| Implement | claude-haiku-5-5 | 0.003 | 7 |
| Test | claude-haiku-5-5 | 0.003 | 5 |
| Review | claude-sonnet-5-5 | 0.033 | n/a |
