# ADR-004: Resume from the last checked stage, after reviewing what was done and why

- **Status:** Accepted (2026-11-21, after author review, before any agent code)
- **Decision area:** D4, state

## Context

A run can stop halfway: the network drops, GitHub cancels the job, or a timeout hits. When it
starts again, there are two simple options, and I don't think either is right:

- **Start from the beginning.** Safe, but it throws away good work and pays for it again.
- **Continue exactly where it stopped.** Fast, but the agent's memory is gone. A new agent
  session doesn't know what the old one was doing, and half-finished work (a file edited
  halfway, a test written but never run) may be broken.

What a person would do is better than both: look at what was done, why it was done, what was
supposed to happen next, and where it got cut off. Then continue from there with the same
understanding.

State is also needed between runs, because each review round is a new workflow run
(ADR-002). And whatever we store must not be visible to the reviewer (ADR-008).

## Decision

**1. Where state lives:**

| What | Where | Why there |
| --- | --- | --- |
| Stage documents (`spec.md`, `design.md`, `diff.patch`, `test_report.md`, `pr.md`, `review.md`) | Workflow artifacts on the run | Anyone can open them from the run page. They are **not** on the branch, so the reviewer's checkout doesn't contain them. |
| The code itself | The branch `autose/issue-N` | That is what the PR shows. |
| `state.json`: current stage, attempts, round, cost so far, and a log line per step (what was done, why, what the check said) | Uploaded as an artifact, and also embedded in a **status comment** on the issue that the bot edits after each stage | The status comment lets a human follow progress on the issue page, and a later run can find the state without knowing the earlier run's ID. |

**2. How a restart works (checkpoint + review):**

1. Read `state.json`: which stages passed, what each attempt did, and why.
2. **Re-check the last passed stage** with its normal check (e.g. does the branch still build,
   do the tests still pass). This is cheap and deterministic. If the check fails now, go back
   one more stage.
3. **Throw away the half-finished stage.** Reset the branch to the last good commit.
4. **Start that stage again with a resume note.** The new agent session gets a short summary
   built from the log: what was done before, why, what it was supposed to do, and where it
   stopped. It continues with the same understanding, without blindly trusting
   half-finished work.

Each stage commits to the branch only after its check passes, so "the last good commit" is
always a known checkpoint.

## Alternatives

- **Always restart from scratch.** Simplest and safest. Rejected: it wastes money (the budget
  is $10) and time, and the Planner might write a different spec the second time, which
  makes runs harder to compare.
- **Resume exactly where it stopped.** Rejected: the agent's memory is gone, and half-done
  edits can be broken.
- **Store state in files on the branch.** Simple, and everything stays in git. Rejected:
  `spec.md` and `design.md` would show up in the PR diff and in the reviewer's checkout,
  which breaks reviewer independence.
- **GitHub Actions cache.** Rejected: the cache can be evicted at any time and isn't visible
  to humans.

## Consequences

- A restart costs one re-check plus one stage, not a whole run.
- The issue's status comment doubles as a live progress view for humans.
- The status comment can be edited by maintainers. That is acceptable, because only
  collaborators can edit other people's comments, and the orchestrator validates the JSON
  before trusting it.
- Every artifact must be uploaded right after its stage, not at the end. Otherwise a crash
  would lose it.
