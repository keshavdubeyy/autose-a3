# Decision-experiment variants

Both experiments reuse the five seeded PRs (`seeded_prs/labels.md`), which have known correct verdicts: S1 and S5 are clean, S2 has a logic bug, S3 has weak tests, and S4 has an unrelated risky change. Every variant runs the reviewer job in `mode=review_only` with the same prompt, rubric, tools and limits. Only the one variable named below changes.

| Variant | Experiment | ADR tested | What changes | Workflow input |
|---|---|---|---|---|
| `default` | baseline for A and B | n/a | Reviewer on `claude-sonnet-5-5`. It sees the issue, the diff and the repo at the PR head. | `variant=default` |
| `same_model` | A | ADR-006 (models): "the reviewer gets the stronger model" | Reviewer on `claude-haiku-5-5`, the same cheap model the implementer and tester use | `variant=same_model` |
| `with_spec` | B | ADR-008 (independence): "the reviewer does not see the spec" | Sonnet reviewer, which may also read a spec for the PR. The specs are in `.autose/experiments/specs/pr-N.md` in the fork. They are written as the implementer understood the task, so for S2-S4 the spec agrees with the defect. Most strongly, S4's spec lists "remove fsync for speed" as requirement FR-3. | `variant=with_spec` |

**Validity check for B:** a `with_spec` trial counts only if the review log shows the reviewer read `spec.md`. This is recorded per trial.
