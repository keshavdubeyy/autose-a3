# Architecture Decision Records

Nygard format (Status, Context, Decision, Alternatives, Consequences), same as A2.
ADR numbers 001–010 match the assignment's decision areas D1–D10. A replacement ADR takes
the next free number, and the old one is kept and marked *Superseded*.

| ADR | Decision area | Chosen | Main option rejected | Main reason | Status |
| --- | --- | --- | --- | --- | --- |
| [001](ADR-001-splitting-the-work.md) | D1 Splitting the work | 3 agents, Implementer writes own tests | 1 agent / 6 agents | Fewer hand-offs | Superseded by 011 |
| [011](ADR-011-four-agents-with-separate-tester.md) | D1 Splitting the work | 4 agents: Planner, Implementer, Tester, Reviewer | Implementer writes its own tests | A builder only tests what it expects to work | Accepted |
| [002](ADR-002-control-flow.md) | D2 Control flow | Fixed checklist (Python state machine) + escalation report | AI manager decides next step | Shows exactly where a run failed; can't be talked out of rules | Accepted |
| [003](ADR-003-hand-offs.md) | D3 Hand-offs | Only what each agent needs; documents not chat; Goal section in spec | Pass everything forward | Extra context misleads and carries injected text | Accepted |
| [004](ADR-004-state.md) | D4 State | Artifacts + status comment; resume from last checked stage with a resume note | Restart from scratch / resume blindly | Keeps good work, doesn't trust half-done work | Accepted |
| [005](ADR-005-tools.md) | D5 Tools | Per-agent tool allowlists, hooks, git-diff check; no agent touches GitHub | GitHub MCP server for agents | No agent's task needs GitHub; a write token near untrusted text is risky | Accepted |
| [006](ADR-006-models.md) | D6 Models | Sonnet 5.5 Planner + Reviewer, Haiku 5.5 Implementer + Tester | Opus everywhere | $10 budget; cheap builder checked by stronger, different reviewer | Accepted |
| [007](ADR-007-checks.md) | D7 Checks | Code checks first, AI judge for stage 1 and review rubric, humans audit verdicts | AI judge for every gate | Exact questions get exact (free) answers | Accepted |
| [008](ADR-008-reviewer-independence.md) | D8 Reviewer independence | Separate job, read-only, different model, evidence-backed rubric | Reviewer sees implementer reasoning | Assignment rule; reasoning anchors the reviewer | Accepted |
| [009](ADR-009-safety-and-failures.md) | D9 Safety and failures | $1/issue, 15 min agent time, untrusted-input layers | Rely on the provider cap and the prompt | One bad run must not drain the month | Accepted |
| [010](ADR-010-triggers.md) | D10 Triggers | Anyone can request, collaborators approve; one run per issue, queued with a notice | Anyone's comment starts a run | Strangers could drain the budget | Accepted |
