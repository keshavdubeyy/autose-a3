# AutoSE Assignment 3: Agentic SDLC Workflow

Issue in, reviewed pull request out. A maintainer labels an issue in the fork. Four agents then
write the spec and the design, change the code and test it, and the pipeline opens a PR. A
separate read-only reviewer reviews the PR. A human always makes the merge decision.

| | |
| --- | --- |
| Fork | https://github.com/keshavdubeyy/tinydb |
| Pinned commit | `edff96aeb2616402e9489d46e90a592c05565621` (upstream msiemens/tinydb) |
| Default branch | `master` (protected: changes only through PRs; the bot never merges) |
| Models | Planner + Reviewer: `claude-sonnet-5-5`. Implementer + Tester + spec judge: `claude-haiku-5-5` (ADR-006) |
| Report | [`report.pdf`](report.pdf) (source: `report/report.md`) |
| Demo video | [`demo.mp4`](demo.mp4) (4:17) |
| Total spend | $1.10 over 23 workflow runs (`results/results.csv`) |

## Submission links

| Deliverable | Link |
| --- | --- |
| Report (≤ 8 pages) | [report.pdf](report.pdf) |
| Demo video (≤ 5 min) | [demo.mp4](demo.mp4) |
| Fork with the workflow | https://github.com/keshavdubeyy/tinydb (workflow: [`.github/workflows/autose.yml`](https://github.com/keshavdubeyy/tinydb/blob/master/.github/workflows/autose.yml), code: [`.autose/`](https://github.com/keshavdubeyy/tinydb/tree/master/.autose)) |
| Copy of the workflow and code | [workflow/](workflow/) |
| Actions runs | https://github.com/keshavdubeyy/tinydb/actions/workflows/autose.yml |
| Pull requests opened by the pipeline | https://github.com/keshavdubeyy/tinydb/pulls?q=is%3Apr |
| Issues (#1–#5) | https://github.com/keshavdubeyy/tinydb/issues?q=is%3Aissue |
| Architecture views | [component view](architecture/views/component-view.md), [sequence view](architecture/views/sequence-view.md), [stage map](architecture/views/stage-map.md) |
| ADRs (13) | [architecture/decisions/](architecture/decisions/README.md) |
| Issue texts and hidden tests | [experiment/issues/](experiment/issues/), [experiment/hidden_tests/](experiment/hidden_tests/) |
| Seeded PRs (reviewer check) | [experiment/seeded_prs/](experiment/seeded_prs/labels.md) |
| Decision experiments | [variants](experiment/variants.md), [results](results/experiments.md) |
| Every run, PR and review | [results/runs.md](results/runs.md), [results/results.csv](results/results.csv) |

## How to trigger the workflow

- **Start a run:** add the label `autose` to an issue in the fork, or post a comment starting with
  `/autose`. Only collaborators can start a run this way. A comment from anyone else gets a
  polite reply and the `autose-requested` label (ADR-010).
- **Clarify an issue:** a maintainer comments on it and then comments `/autose`. Maintainer comments are
  added to the agents' input. Other people's comments are not (ADR-012).
- **Cancel and restart:** comment `/autose restart`.
- **Review only (seeded PRs, experiments):** Actions → AutoSE → *Run workflow*, with `mode=review_only`,
  `pr=<number>`, `issue=<number>` and `variant=default|same_model|with_spec`.

Progress shows in a status comment on the issue. All stage artifacts (`spec.md`, `design.md`,
`diff.patch`, `test_report.md`, `pr.md`, `review.md`, logs) are uploaded to each Actions run.

## Results in one paragraph

- All 5 issues ended with a reviewer-approved PR (#7–#10, #12), and 16/16 hidden tests pass.
- The vague issue (#5) first stopped at requirements with an escalation report. It completed after
  one maintainer clarification.
- The reviewer gave the right verdict on 5/5 seeded PRs.
- Experiment A (a Haiku reviewer) and Experiment B (a reviewer that sees the spec) changed no verdicts.
  Both are negative results, and the details are in `results/experiments.md`.

## Layout

```
README.md                this file
demo.mp4                 demo video (4:17)
report.pdf               the report (5 pages)
report/                  report source (Markdown) and print stylesheet
architecture/views/      component view, sequence view, stage map
architecture/decisions/  ADR-001 … ADR-013 (ADR-001 superseded by ADR-011, kept)
workflow/                exact copy of the fork's .github/workflows/autose.yml and .autose/ (code, prompts, offline tests)
experiment/issues/       the 5 issue texts (fork issues #1–#5)
experiment/hidden_tests/ hidden acceptance tests (never placed in the fork)
experiment/seeded_prs/   the 5 reviewer-check PRs: diffs, labels and results
experiment/variants.md   what each decision-experiment variant changes
results/results.csv      one row per workflow run
results/runs.md          links to every Actions run, PR and review
results/experiments.md   Experiments A and B side by side
```

## AI use

I used Claude Code (Claude Opus 5.5) substantially:
- to explore the TinyDB codebase;
- to draft the issue texts, hidden tests and seeded PRs;
- to write the workflow, the orchestrator, the agent prompts and the offline tests;
- to run and log the experiments, and to draft the report text and diagrams.

The ADRs record my own decisions and reasoning. For each ADR, Claude asked me questions and I chose
the option and gave the reason. Claude then wrote it up in plain English, and I reviewed every ADR.
The hindsight choice and the post-experiment design decisions (keep Sonnet, keep the no-spec rule) are mine.

I reviewed all generated code and documents. All runs, PRs and reviews are real and linked in `results/runs.md`.
