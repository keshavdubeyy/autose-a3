# ADR-011: Four agents. Testing moves to its own Tester (QA) agent

- **Status:** Accepted (2026-11-21, before any agent code)
- **Supersedes:** ADR-001
- **Decision area:** D1, splitting the work

## Context

ADR-001 used three agents and let the Implementer write its own tests. When I reviewed it,
I did not agree with that part.

If one agent does many jobs, it carries the bias of one job into the next. Each extra
responsibility is one more place where it can lose track and hallucinate. And if the same
agent does a task, then checks that task, then moves on, it is checking its own work. That
does not work well for people either. In a real team, the person who wrote the code is not
the person who signs off on it.

Testing has the same problem. A builder who writes their own tests will mostly write the
cases they already know work. The cases that would break the code are exactly the ones they
didn't think of, so they won't test them either. That is why real teams have QA.

ADR-001 tried to cover this with three other checks (AC-to-test mapping, hidden tests and the
reviewer). But the hidden tests are only for our experiment, so they don't exist when the
bot runs on a real issue. And the reviewer comes at the very end, after a PR is already open.
The bias needs to be caught earlier.

## Decision

Use **four agents**, each with one responsibility:

| Agent | Stage | Job in one line |
| --- | --- | --- |
| Planner | 1 Requirements, 2 Design | Understand the request and plan the change |
| Implementer | 3 Implementation | Change the code |
| Tester (QA) | 4 Testing | Write one test per acceptance criterion, run the whole suite |
| Reviewer | 6 Review | Check the finished PR independently |
| *(no agent)* | 5 Release | Push and open the PR. This is just a submit button. Deciding to merge is a human's job. |

Rules that make the Tester actually independent:

- The Tester works from **`spec.md`**, the acceptance criteria. It does **not** get
  `design.md` or the Implementer's conversation. It tests what the user asked for, not what
  the builder planned to build.
- The Tester's test files belong to the Tester. **The Implementer may not edit them.** The
  orchestrator checks this with `git diff` and rejects the attempt if they were touched.
- When tests fail, the failing output goes back to the Implementer (stage 3). The tests stay
  the same on every retry, like QA handing a bug back to the developer. The target doesn't
  move.

## Alternatives

- **One agent does everything.** Rejected: bias carries across tasks, there are more chances
  to hallucinate, and the agent validates its own work.
- **Three agents, Implementer writes its own tests (ADR-001).** Rejected after review: the
  builder only tests what it expects to work.
- **One agent per stage (six).** Rejected: release needs no agent, and splitting planning
  into two agents adds a hand-off without removing any bias. Spec and design are both
  "understanding" work.
- **Tester writes tests *before* the code exists (test-first).** Interesting, but the
  assignment fixes the order (implementation is stage 3, testing is stage 4). Our rule that
  the Tester sees only the spec gives most of the same benefit.

## Consequences

- One more agent session per run, so a bit more cost. We pick a cheaper model for the Tester
  if the budget is tight (ADR-006).
- Implementer and Tester can disagree. If tests still fail after 3 attempts, the orchestrator
  sends the work back to design (ADR-002).
- A wrong test (one that doesn't match the spec) would block a correct implementation. The
  reviewer can flag it, and we will report how often it happens.
- We can now measure test quality on its own: do the Tester's tests catch the planted bugs
  and match the hidden tests?
