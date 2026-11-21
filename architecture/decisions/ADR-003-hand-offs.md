# ADR-003: Hand off artifacts, never conversations, and give each agent the least context it needs

- **Status:** Proposed (2026-11-21, before any agent code). Will be tested in Experiment B.
- **Decision area:** D3, hand-offs

## Context

Each agent starts with an empty context. Whatever we pass in shapes what it does. More context
can help an agent, but it can also anchor it to someone else's mistakes, carry injected text
further through the pipeline, and cost money on a $10 budget.

Two inputs from earlier assignments must be used: the A1 SRS skill (stage 1) and the A2
`ARCHITECTURE.md` (stage 2). The A1 skill is large (about 3,200 lines, roughly 45k tokens).

## Decision

Agents pass **files (artifacts)**, not chat history. Each one gets exactly this:

| Agent / stage | Gets | Deliberately does NOT get | Why it's left out |
| --- | --- | --- | --- |
| Planner, stage 1 | Issue title + body inside `<untrusted_issue>` tags; a condensed A1 skill (the rules for acceptance criteria, assumptions and open questions) | Code-write tools; other issues | Requirements describe *what*, not *how*. The issue is untrusted text. |
| Planner, stage 2 | `spec.md`; A2 `ARCHITECTURE.md`; read-only repo | The raw issue | Design should follow the reviewed spec, not re-read the issue and drift. |
| Implementer, stages 3–4 | `spec.md`; `design.md`; full repo with edit and test tools. On a retry: the last test output (truncated). On a review loop: the reviewer's findings. | The raw issue; the Planner's conversation | One source of truth (the spec). The raw issue is where prompt injection would live, so the agent with write tools never reads it directly. |
| Reviewer, stage 6 | Issue; PR diff; repo checked out at the PR head commit | `spec.md`, `design.md`, `test_report.md`, any agent conversation | See ADR-008: the reviewer must judge the result against the *user's* request, not against the pipeline's own interpretation of it. |

**The A1 skill is condensed.** We extract the sections that define spec structure and
acceptance-criteria quality into `prompts/a1_skill_condensed.md`, and keep the full file in
the repo for reference. This keeps stage 1 cheap and focused.

## Alternatives

- **Pass the full conversation forward.** No information is lost. Rejected: it anchors every
  later agent to earlier reasoning, carries injected issue text all the way to the agent with
  write access, and costs grow with every stage.
- **Pass only short summaries.** Cheapest. Rejected: summaries drop details like exact
  acceptance criteria and file names, and those details are what the checks verify.
- **Give the reviewer the spec as well.** It could check every acceptance criterion directly.
  Rejected for now, because the reviewer would be judging against the Planner's
  interpretation. If the spec misread the issue, the reviewer would approve the misreading.
  **This is Experiment B**: reviewer with vs without `spec.md`, measured on the seeded PRs
  and the vague issue.
- **Feed the full A1 skill every time.** Most faithful to A1. Rejected on cost: about 45k
  extra input tokens per run, and most of it (stakeholder analysis, document templates) does
  not apply to a single GitHub issue.

## Consequences

- Every hand-off is a file a human can open in the run's artifacts, which makes runs easy to
  follow.
- If the spec is wrong, the Implementer cannot notice by re-reading the issue. Only the
  reviewer, who reads the issue fresh, can catch it. This makes ADR-008 load-bearing.
- The condensed A1 skill must be justified in the report: what was kept and why.
