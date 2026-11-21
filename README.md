# AutoSE Assignment 3: Agentic SDLC Workflow

Issue in, reviewed pull request out.

| | |
| --- | --- |
| Fork | https://github.com/keshavdubeyy/tinydb |
| Pinned commit | `edff96aeb2616402e9489d46e90a592c05565621` (upstream msiemens/tinydb) |
| Default branch | `master` (protected: PRs only) |
| Models | *to be decided in ADR-006* |
| Trigger | add label `autose` to an issue, or comment `/autose` (collaborators only) |

## Layout

```
architecture/views/      component view, sequence view, stage map
architecture/decisions/  ADRs (superseded ones kept)
workflow/                copy of the fork's .github/workflows + agent code + prompts
experiment/issues/       the 5 issue texts (posted as fork issues #1–#5)
experiment/hidden_tests/ hidden acceptance tests (never placed in the fork)
experiment/seeded_prs/   reviewer-check PRs
results/                 results.csv, runs.md
```

## Status

Design phase. The component view, stage map and ADR-001/002/003/008/011 were committed before
any agent code.

## AI use

Claude Code helped explore the codebase, draft issue texts, hidden tests and first ADR
drafts. All drafts were reviewed and edited by the author.
