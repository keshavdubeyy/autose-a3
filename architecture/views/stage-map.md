# Stage Map

| # | Stage | Agent | Input it gets | Artifact | Check before moving on | Who decides pass/fail | On failure |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Requirements | Planner | Issue text (wrapped as untrusted), A1 skill | `spec.md` | Every acceptance criterion has an ID and a Given/When/Then shape, and the LLM judge rates each one testable | Orchestrator (script + judge verdict) | Retry once with judge feedback, then stop with reason |
| 2 | Design | Planner | `spec.md`, A2 `ARCHITECTURE.md`, read-only repo | `design.md` | Every file and function named exists in the repo (or is marked NEW) | Orchestrator (script) | Retry once, then stop |
| 3 | Implementation | Implementer | `spec.md`, `design.md`, repo | `diff.patch` | Package installs and imports | Orchestrator (script) | Retry inside the stage-3/4 loop |
| 4 | Testing | Tester (QA) | `spec.md` + repo after implementation (no `design.md`, no Implementer chat) | `test_report.md` | One test per acceptance criterion exists, the Implementer did not touch the test files, and the full suite passes | Orchestrator (pytest exit code + AC-to-test mapping + git diff on test files) | Back to 3 with failing output; tests stay fixed (max 3), then back to 2 (once), then stop |
| 5 | Release | Plain code | Branch | `pr.md` + PR link | PR is open and CI is green (CI started with `workflow_dispatch`) | Orchestrator (GitHub API) | Back to 3 with the failed CI log (counts as an implementation attempt) |
| 6 | Review | Reviewer | Issue, PR diff, repo at PR head | `review.md` | Verdict is APPROVE, or 2 review rounds are used | Review runner (verdict JSON + round counter) | `code` → stage 3, `approach` → stage 2 |

The stages and checks are fixed by the assignment. This table shows how this design assigns
them. Detailed check design is in ADR-007.

**As built (21 Nov 2026):** stage 3's check also reverts any edit outside `tinydb/`, and stage 5's
failure path was changed from "stop" to "back to 3". This change was needed on issue #5, where CI's
mypy step failed and the Implementer fixed it.
