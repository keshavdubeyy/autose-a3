# ADR-002: A fixed checklist (Python state machine) controls the flow, not an AI manager

- **Status:** Accepted (2026-11-21, after author review, before any agent code)
- **Decision area:** D2, control flow

## Context

The flow is not a straight line. It has loops:

- tests fail → back to implementation
- tests keep failing → back to design
- reviewer asks for changes → back to implementation (code problem) or design (approach
  problem), at most twice

Something has to decide when to move on, when to go back, and when to give up. There are two
basic options: an AI "manager" that decides each time, or a fixed checklist with written
rules.

When something goes wrong, the most important thing is to **see where it went wrong**. With a
fixed checklist, every step and every decision follows a rule you can read, so you can point
at the exact stage that failed. With an AI manager, the decision is hidden inside a model's
reasoning. It may decide differently on two identical runs, and it is hard to tell whether
the problem was the stage or the manager.

There is also a GitHub limit: Actions jobs cannot loop (they form a one-way chain), and the
reviewer needs fewer permissions than the builder. In Actions, permissions are set per job.

## Decision

1. **A fixed checklist decides.** A plain Python orchestrator (no AI) runs the stages in
   order, runs each stage's check itself, and picks the next step from these rules:

   | Situation | Next step |
   | --- | --- |
   | Check passed | Next stage |
   | Tests fail, fewer than 3 implementation tries | Back to stage 3 with the failing output |
   | Tests still fail after 3 tries | Back to stage 2 once, to rethink the design |
   | Still failing after the design redo, or any other stage out of budget | **Stop and escalate to a human** (below) |
   | Reviewer: code problem, round < 2 | Back to stage 3 |
   | Reviewer: approach problem, round < 2 | Back to stage 2 |
   | 2 review rounds used | Stop and hand to a human with the last review |

2. **When the bot stops, it writes an escalation report.** It doesn't just say "failed". It
   posts the report as a comment on the issue, and also saves it in the stage's artifact.
   The report has these sections:

   | Section | What it says |
   | --- | --- |
   | What went wrong | The failing check, in plain words |
   | Why | The most likely cause, with the error output as evidence |
   | Where / who is involved | Which stage and agent, which files and tests |
   | What was tried | Each attempt and what changed between attempts |
   | Options | 2–3 possible ways forward (e.g. narrow the spec, change the design, fix by hand) |
   | Trade-offs | What each option costs or risks |

3. **Three jobs in one workflow:** `gate` → `build` (stages 1–5) → `review` (stage 6, fewer
   permissions). Review rounds start a new run with `workflow_dispatch`, the one event that
   the built-in GitHub token is allowed to trigger.

## Alternatives

- **An AI manager decides the next step.** More flexible: it could skip or reorder steps.
  Rejected: you can't easily see why it chose a path, it may choose differently on identical
  runs, and text hidden in an issue could talk it out of a rule (like "skip the tests"). The
  six stages and their checks must always run, and that is easiest to guarantee with fixed
  rules.
- **One Actions job per stage.** Very visible in the UI. Rejected: jobs cannot loop back, and
  each job starts a fresh machine (about a minute of setup each time).
- **Everything in one job, including review.** Rejected: the reviewer would share the
  builder's workspace and write permissions (ADR-008).
- **Stop with a short error message.** Rejected: a human then has to dig through logs to
  understand what happened. The escalation report saves that time and makes the hand-off to
  a person clear.

## Consequences

- Every decision the bot makes can be traced to a rule and logged in `state.json`. When a run
  fails, you can see exactly which stage failed and why.
- The orchestrator is ordinary code, so we can test it without calling any model.
- Less flexible: an issue that needs an unusual path stops and goes to a human. For a bot
  working in someone else's repository, stopping and explaining is safer than improvising.
- One issue can take up to three linked runs (build plus two review rounds). `runs.md` must
  link all of them.
