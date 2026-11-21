# ADR-003: Each agent gets only what it needs to reach its goal, passed as documents, not chat

- **Status:** Accepted (2026-11-21, after author review, before any agent code). The
  reviewer part is tested in Experiment B.
- **Decision area:** D3, hand-offs

## Context

Every agent starts with an empty context. Whatever we hand it shapes what it does. Each agent
has one specific goal, so the question is: what does it need to reach that goal, and nothing
more?

Sending everything is tempting, but extra information is not free:

- **It can mislead.** If an agent sees material that isn't about its job, it may act on it.
  For example, it might "fix" something it read about and change code nobody asked it to.
- **It can carry an attack.** The issue text is written by anyone, so a hidden instruction
  in it travels to every agent that reads it.
- **It costs money.** We have a $10 budget, and every extra page is paid for again by every
  agent that reads it.

On the other hand, an agent with too little context doesn't know *why* it is doing the work.
For example, a builder that only sees a list of criteria might meet the letter of the spec
and miss the point.

Two inputs from earlier assignments must be used: the A1 SRS skill (stage 1) and the A2
`ARCHITECTURE.md` (stage 2). The A1 skill is long, about 3,200 lines (roughly 45k tokens).

## Decision

**Rule: give each agent as much as it needs to achieve its goal, and no more.** Agents pass
**documents**, not conversations.

**Every spec starts with a short "Goal" section**, 1–3 sentences in the Planner's words: who
wants what, and why. Every later agent knows the overall goal, but none of them has to read
the raw issue text.

| Agent | Gets | Does NOT get | Why |
| --- | --- | --- | --- |
| Planner, stage 1 | The issue inside `<untrusted_issue>` tags; the condensed A1 skill | Code-editing tools | Its job is to understand the request. It is the only agent that reads raw issue text, and it can't change code. |
| Planner, stage 2 | `spec.md`; A2 `ARCHITECTURE.md`; read-only repo | The raw issue | The plan should follow the spec. |
| Implementer, stage 3 | `spec.md` (including the Goal); `design.md`; the repo. On a retry: the failing test output. On a review loop: the reviewer's findings. | The raw issue; other agents' chats | It knows the goal and the plan, but never reads text a stranger wrote. |
| Tester, stage 4 | `spec.md` (including the Goal); the repo after implementation | `design.md`; the Implementer's chat; the raw issue | It tests what the user wants, not what the builder planned (ADR-011). |
| Reviewer, stage 6 | The issue; the PR diff; the repo at the PR head | `spec.md`, `design.md`, test report, any chat | It judges the result against the user's own words (ADR-008). |

**Who checks that each agent did its job well?** The orchestrator plays the "moderator" role.
After every stage it runs that stage's check (testable criteria, files that really exist,
build passes, tests pass) before anything moves on (ADR-002, ADR-007). The reviewer's rubric
then judges overall quality at the end. Neither of them is another LLM making decisions:
checks are code, and the only quality judgement is the reviewer, which is already
independent.

**The A1 skill is condensed.** We keep only the rules that matter for one GitHub issue: how
to write testable acceptance criteria, how to separate confirmed requirements from
assumptions, and how to list open questions. They go in `prompts/a1_skill_condensed.md`, with
a note on what was dropped and why. The full skill stays in the repo for reference.

## Alternatives

- **Pass every agent everything (full chats, all documents).** Nothing is lost. Rejected:
  extra material can mislead an agent into changes nobody asked for, carries any injected
  text to every agent, and costs more at every stage.
- **Give the builder the raw issue too.** It would hear the user directly. Rejected: the Goal
  section gives it the "why" without exposing the agent that edits code to text a stranger
  wrote. If the Goal turns out to be too thin in practice, we will revisit this.
- **Pass only short summaries.** Cheapest. Rejected: summaries drop the exact criteria and
  file names that the checks verify.
- **Full A1 skill every time.** Most faithful to A1. Rejected: about 45k extra tokens per run,
  and most of it (stakeholder analysis, long document templates) doesn't apply to one
  issue. We accept that a condensed version might miss an edge-case rule. Cost is a real
  trade-off on this budget.
- **Reviewer also gets the spec.** Tested as **Experiment B** instead of decided up front.

## Consequences

- Every hand-off is a file a human can open in the run's artifacts.
- If the Planner misreads the issue, the Implementer and Tester can't catch it, because they
  work from the spec. Only the reviewer, who reads the issue fresh, can. That makes ADR-008
  essential.
- The Goal section is now a required part of `spec.md`, and the stage-1 check rejects a spec
  without one.
- The condensed A1 skill must be explained in the report: what was kept, and why.
