# Component View

How the agents, their tools and the GitHub plumbing fit together.
Status: initial design, written before any agent code (see git history).

```mermaid
flowchart TB
    subgraph GH["GitHub: keshavdubeyy/tinydb (fork)"]
        ISSUE["Issue #N<br/>(untrusted text)"]
        PR["Pull request<br/>autose/issue-N → master"]
        CI["Existing CI<br/>ci-workflow.yml"]
        ART[("Workflow artifacts<br/>spec.md · design.md · diff.patch<br/>test_report.md · pr.md · review.md<br/>state.json")]
    end

    MAINT(["Maintainer"]) -- "label 'autose' or '/autose'" --> ISSUE
    ISSUE -- "issues / issue_comment event" --> GATE

    subgraph WF["Workflow autose.yml"]
        GATE["Job 0: gate<br/>(shell, no AI)<br/>author_association check<br/>concurrency per issue"]

        subgraph BUILD["Job 1: build · token: contents+PR write"]
            ORCH["Orchestrator<br/>(deterministic Python state machine)<br/>runs checks, counts retries,<br/>decides next stage"]
            PLAN["Planner agent<br/>stages 1-2<br/>tools: Read, Grep, Glob"]
            IMPL["Implementer agent<br/>stages 3-4<br/>tools: Read, Grep, Glob, Edit, Write, Bash"]
            REL["Release step<br/>(plain code: git push, gh pr create)"]
            ORCH -- "issue (wrapped) + A1 skill" --> PLAN
            ORCH -- "spec.md + design.md<br/>(+ failure log / review findings on retry)" --> IMPL
            ORCH --> REL
        end

        subgraph REVIEW["Job 2: review · token: contents READ, PR comment"]
            RORCH["Review runner<br/>(plain code)"]
            REV["Reviewer agent<br/>stage 6 · different model<br/>tools: Read, Grep, Glob, Bash (pytest)"]
            RORCH -- "issue + PR diff +<br/>checkout at PR head" --> REV
            REV -- "review.md + verdict JSON" --> RORCH
        end

        GATE --> ORCH
        REL --> PR
        PR --> CI
        BUILD --> REVIEW
    end

    A1[["A1 skill: SKILL.md"]] -.-> PLAN
    A2[["A2 ARCHITECTURE.md"]] -.-> PLAN
    ORCH -- "upload per stage" --> ART
    RORCH -- "post review comment" --> PR
    RORCH -- "changes requested & round < 2:<br/>workflow_dispatch(start_from, round)" --> ORCH
    PR --> HUMAN(["Human: merge or close"])
```

## Who can do what

| Component | Kind | Can read | Can write | GitHub token |
| --- | --- | --- | --- | --- |
| Gate | Shell | Event payload | Nothing | read-only |
| Orchestrator | Python (no LLM) | Everything in the job | Artifacts, branch, PR | contents + PR write |
| Planner | LLM agent | Repo (read-only), issue, A1 skill, ARCHITECTURE.md | `spec.md`, `design.md` only (returned as text) | none (never sees it) |
| Implementer | LLM agent | Repo, spec, design | Working tree files | none (never sees it) |
| Release | Python (no LLM) | Branch | Push branch, open PR | contents + PR write |
| Review runner | Python (no LLM) | Issue, PR diff | One PR comment, dispatch next round | contents read, PR write |
| Reviewer | LLM agent | Issue, diff, repo at PR head | `review.md` (returned as text) | none (never sees it) |

Key rule: **no agent ever holds a GitHub token.** Every GitHub write goes through plain code
that the orchestrator controls (ADR-005, to be written).
