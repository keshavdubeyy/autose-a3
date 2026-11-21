# ADR-001: Three agents (Planner, Implementer, Reviewer), with Release done in plain code

- **Status:** Superseded by ADR-011 (2026-11-21). After review I decided the Implementer should not write its own tests. Kept for the record.
- **Decision area:** D1, splitting the work

## Context

The workflow must run six fixed stages: requirements, design, implementation, testing,
release and review. The review must be done by an agent that is independent of the others.
We have a hard budget of $10/month on the model provider, and every agent session pays again
for reading the same repository.

The stages fall into three kinds of work:

1. **Understanding**: turning an issue into a spec (1) and a plan (2). This needs reading,
   not editing.
2. **Changing code**: editing code (3) and proving it works with tests (4). These two are a
   tight loop: a failing test is only useful to the agent that wrote the code.
3. **Judging**: reviewing the result (6). This must not share context with 1–3.

Release (5) is mechanical: push a branch and open a PR. It needs no judgement.

## Decision

Use **three LLM agents** and no agent at all for release:

| Agent | Stages | Why grouped |
| --- | --- | --- |
| Planner | 1 Requirements, 2 Design | Same skill (read, reason, write a document). The design should follow directly from the spec it just wrote. |
| Implementer | 3 Implementation, 4 Testing | Code and tests are one feedback loop. When tests fail, the same session sees the error and fixes it. |
| Reviewer | 6 Review | Must be separate (assignment rule, see ADR-008). |
| *(plain code)* | 5 Release | `git push` and `gh pr create` are deterministic. An LLM here only adds risk and cost. |

Planner and Implementer are **separate sessions**: the Implementer gets the Planner's
artifacts (`spec.md`, `design.md`), not its conversation (see ADR-003).

## Alternatives

- **One agent for everything.** Simplest and cheapest per run. Rejected: the agent would
  review its own work, and by stage 4 its context is full of its own earlier reasoning. That
  is exactly the self-confirmation the independent reviewer is meant to avoid. It also gives
  one agent both broad read access to the issue (untrusted) and write access to code.
- **One agent per stage (six agents).** Gives the cleanest separation. Rejected: every
  hand-off loses context and costs another full repo read. Splitting implement and test
  means a test failure must be summarised and handed back, which is slower and lossier than
  the implementer seeing it directly. Release does not need an agent at all.
- **A separate Tester agent (four agents).** The strongest alternative: tests written by a
  different agent are less likely to be shaped around the code. Rejected for now because
  the risk is already covered three other ways: (a) the orchestrator checks that every
  acceptance criterion ID from `spec.md` has a test, (b) the hidden tests are written by us
  and never seen by the bot, (c) the independent reviewer re-runs the code. If results show
  the implementer writing weak tests, this ADR will be superseded.

## Consequences

- Two hand-offs per run (Planner → Implementer, build → Reviewer) instead of five.
- The Implementer writes its own tests, so test quality depends on the AC-to-test check and
  the reviewer. We will measure this with the hidden tests.
- Each agent can get a different model and a different tool set (ADR-005, ADR-006).
- The Planner never needs write tools, so the agent that reads the raw issue text cannot
  change code. That limits the damage from prompt injection (ADR-009).
