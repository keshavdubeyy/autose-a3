# ADR-007: Automatic checks first, an AI judge where code can't decide, and humans as the final judges

- **Status:** Accepted (2026-11-21, after author review, before any agent code)
- **Decision area:** D7, checks

## Context

Every stage has a gate that must pass before work moves on. Some gates can be checked by
code with a clear yes/no ("do the tests pass?"). Others need judgement ("is this acceptance
criterion testable?"), and there an AI judge (LLM-as-judge) can help.

AI judges can also be wrong. So I think both should exist: an AI judge to check the things
code can't (including filling and checking the rubric), and a human judge who verifies the
AI's verdicts, so we can see what problems came up, what didn't, and whether each verdict
was really a pass or a fail.

## Decision

**Order of preference for each gate: code check → AI judge → human.**

| Stage | Gate | How it's checked | Who decides |
| --- | --- | --- | --- |
| 1 Requirements | All acceptance criteria testable | Code: spec has a Goal section, each criterion has an ID and Given/When/Then form. **AI judge** (Haiku 5.5, separate call): rates each criterion testable / not, with a reason. | Orchestrator: pass only if code check passes **and** judge says every criterion is testable |
| 2 Design | Names files and functions to change | Code: parse `design.md`, check each named file and function exists in the repo (or is marked NEW) | Orchestrator |
| 3 Implementation | Code builds | Code: install the package and import it | Orchestrator |
| 4 Testing | All new and existing tests pass | Code: each criterion ID has a test; full `pytest` exit code is 0; Implementer didn't touch test files | Orchestrator |
| 5 Release | PR open and CI passes | Code: GitHub API (PR state, check runs) | Orchestrator |
| 6 Review | Approved, or 2 rounds used | **AI judge** = the Reviewer filling the rubric (ADR-008). Code checks the rubric is complete and has evidence. | Orchestrator applies the verdict rules |
| End | Merge or close | **Human** | Maintainer |

**Humans also judge the judges.** For the report, we audit every AI verdict by hand:

- For each review: was the rubric right? We compare it with the hidden tests and read the
  diff. Every disagreement is recorded as "reviewer wrong" (a missed bug or a false alarm).
- For stage 1: we read each spec and mark any criterion the judge called testable that isn't.

The final pass or fail is always made by code from clear inputs. An AI only ever supplies
one input (a rating or a rubric), never the decision itself.

## Alternatives

- **AI judge for every gate.** Flexible. Rejected: "do the tests pass?" has an exact answer,
  and asking an AI adds cost and a chance of being wrong.
- **Code checks only.** Cheapest and fully predictable. Rejected: code can't tell whether a
  criterion is meaningfully testable, or whether a change really solves the issue.
- **Human approval at every gate.** Most reliable. Rejected: the point is that the bot runs
  the stages itself. The human's job is the final merge, plus our audit for the report.

## Consequences

- Most gates are free and instant. Only stage 1 and stage 6 cost model tokens.
- The human audit gives the "where was the reviewer wrong" numbers the report needs.
- If the stage-1 judge turns out too lenient (calls vague criteria testable), we will see it
  in the audit and tighten the prompt or the code check.
