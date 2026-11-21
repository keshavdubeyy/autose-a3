# Sequence view: one real run (issue #3, "Let count() work without a query")

Run [44920637328](https://github.com/keshavdubeyy/tinydb/actions/runs/44920637328), 21 Nov 2026. Times are UTC, taken from the run's status comment on [issue #3](https://github.com/keshavdubeyy/tinydb/issues/3). Result: [PR #7](https://github.com/keshavdubeyy/tinydb/pull/7), approved in round 0, cost $0.100, about 4 minutes.

```mermaid
sequenceDiagram
    autonumber
    actor M as Maintainer
    participant GH as GitHub (issue, PR, Actions)
    participant G as gate job<br/>(gate.py, no AI)
    participant O as build job<br/>orchestrator.py (fixed rules)
    participant P as Planner<br/>Sonnet 5.5
    participant J as AI judge<br/>Haiku 5.5
    participant I as Implementer<br/>Haiku 5.5
    participant T as Tester (QA)<br/>Haiku 5.5
    participant CI as CI workflow<br/>(17-job matrix)
    participant R as review job<br/>Reviewer, Sonnet 5.5<br/>(contents: read)

    M->>GH: adds label "autose" (15:42:49)
    GH->>G: issues.labeled event
    G->>G: label == autose? other run for #3 active? → proceed
    G->>O: outputs issue=3, start_from=requirements
    O->>GH: status comment "running" (15:43:25)
    O->>P: issue text in <untrusted_issue> + condensed A1 skill
    P-->>O: spec.md (4 Given/When/Then ACs) (15:43:42, $0.032)
    O->>O: check structure: Goal, 4 ACs in GWT form ✓
    O->>J: the 4 criteria only
    J-->>O: all testable ✓ (15:43:44)
    O->>P: spec.md + read-only repo (+ ARCHITECTURE.md)
    P-->>O: design.md: tinydb/table.py :: Table.count (15:43:56, $0.030)
    O->>O: check: file and function exist ✓
    O->>I: spec + design; may edit tinydb/ only, may run pytest only
    Note over I,O: guard denied 2 piped commands, agent retried
    I-->>O: edits table.py (15:44:10, $0.003)
    O->>O: only tinydb/ changed? builds and imports? ✓ → commit + push branch
    O->>T: spec only; may write tests/test_autose_issue_3.py only
    T-->>O: 4 tests test_ac_1..4 (15:44:24, $0.003)
    O->>O: one test per AC ✓, full suite passes ✓ → commit
    O->>GH: push autose/issue-3, open PR #7 with pr.md (15:44:32)
    O->>CI: workflow_dispatch on the branch (GITHUB_TOKEN pushes trigger nothing)
    CI-->>O: success (15:46:17)
    O->>GH: upload artifacts: spec, design, diff.patch, test_report, logs
    O->>R: needs.build.outputs.review == true
    R->>GH: checkout PR head (read-only), gh pr diff
    Note over R: sees issue + diff + repo only (no spec, no agent logs)
    R->>R: runs python -m pytest, fills rubric R1-R6 with evidence
    R->>R: code validates rubric (APPROVE needs no failed row) ✓
    R->>GH: posts review on PR #7: APPROVE (15:47:01, $0.033)
    R->>GH: status comment "approved" + "A human now decides"
    M->>GH: reads PR, review and artifacts → merge or close (human only)
```

What the diagram shows about the design:
- **The orchestrator decides every next step** (ADR-002). Agents only return documents, and plain code checks each one before the run moves on (ADR-007).
- **Each agent gets a narrower input than the previous one** (ADR-003). The Tester never sees the design or the code diff, and the Reviewer never sees the spec or any agent's log (ADR-008).
- **Only the orchestrator and the review job talk to GitHub** (ADR-005). The review job's token cannot push.
- **CI is started with `workflow_dispatch`**, because pushes made with `GITHUB_TOKEN` do not trigger workflows.
