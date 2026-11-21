# Seeded pull requests (reviewer check)

Five PRs written by hand, not by the pipeline, to test whether the independent reviewer approves good changes and catches bad ones. Each PR fixes one of the five issues. Two are clean. Three have one planted defect of a different kind.

The PR titles, descriptions and branch names do not say that a PR is seeded. In any case the reviewer sees only the issue, the diff and the repository at the PR head (ADR-008). The reviewer was run with `mode=review_only`, `variant=default`.

| ID | PR | Issue | Diff | Planted defect | Expected verdict | Rubric row that should fail | Hidden tests on the branch |
|---|---|---|---|---|---|---|---|
| S1 | [#13](https://github.com/keshavdubeyy/tinydb/pull/13) | #3 count() without query | [S1](S1-count-without-query.diff) | none (clean) | APPROVE | none | 3/3 pass |
| S2 | [#14](https://github.com/keshavdubeyy/tinydb/pull/14) | #4 search limit | [S2](S2-search-limit.diff) | **Hidden logic bug.** The limit is applied before the result is cached, so after `search(q, limit=2)` a later `search(q)` returns only 2 documents. The PR's own tests use a fresh table each time and so miss it. | CHANGES_CODE | R1 or R4 | 2/3 (the hidden test catches the bug) |
| S3 | [#15](https://github.com/keshavdubeyy/tinydb/pull/15) | #1 stale search after drop_table | [S3](S3-drop-table-cache.diff) | **Weak tests.** The fix is correct, but the tests only check that the table is gone. None of them checks that `search`/`count` on the held table object stop returning dropped data, which is the reported bug. | CHANGES_CODE | R3 | 3/3 pass (the code is right) |
| S4 | [#16](https://github.com/keshavdubeyy/tinydb/pull/16) | #2 half-applied update | [S4](S4-atomic-update.diff) | **Unrelated risky change.** The atomic-update fix is correct, but the PR also removes `os.fsync` from `JSONStorage.write`, which weakens durability and is out of scope for the issue. | CHANGES_CODE | R5 | 4/4 pass (the code is right) |
| S5 | [#17](https://github.com/keshavdubeyy/tinydb/pull/17) | #5 forgiving operations | [S5](S5-forgiving-operations.diff) | none (clean) | APPROVE | none | 3/3 pass |

S3 and S4 pass the hidden tests on purpose. They are defects that tests do not catch, which is exactly what a reviewer is for.

## Result (reviewer `claude-sonnet-5-5`, default variant, 21 Nov 2026)

| ID | Expected | Reviewer verdict | Rows failed | Correct? | Run | Cost |
|---|---|---|---|---|---|---|
| S1 | APPROVE | APPROVE | none | ✅ | [44924367862](https://github.com/keshavdubeyy/tinydb/actions/runs/44924367862) | $0.033 |
| S2 | CHANGES (R1/R4) | CHANGES_CODE | R1, R4 | ✅ It named the exact line and the cause (truncation before the cache store) and suggested the right fix | [44924370850](https://github.com/keshavdubeyy/tinydb/actions/runs/44924370850) | $0.025 |
| S3 | CHANGES (R3) | CHANGES_CODE | R3 | ✅ It said the tests "pass without the fix" | [44924375113](https://github.com/keshavdubeyy/tinydb/actions/runs/44924375113) | $0.025 |
| S4 | CHANGES (R5) | CHANGES_CODE | R5 | ✅ It flagged the fsync removal as high severity and out of scope | [44924379841](https://github.com/keshavdubeyy/tinydb/actions/runs/44924379841) | $0.025 |
| S5 | APPROVE | APPROVE | none | ✅ Its one low finding (docstrings) is a fair nit | [44924382880](https://github.com/keshavdubeyy/tinydb/actions/runs/44924382880) | $0.025 |

**5/5 correct verdicts, and the right rubric row failed in every case.** No false approvals and no false rejections. Total cost was $0.133.

Caveats for the report: five PRs is a small sample. Each defect is a single, fairly visible one, written by the same person who wrote the rubric, so the rubric rows map neatly onto the defects. A harder set (several small defects, or defects outside R1-R6) could show misses.
