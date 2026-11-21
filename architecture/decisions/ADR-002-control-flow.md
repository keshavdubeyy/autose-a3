# ADR-002: A deterministic Python state machine controls the flow, with review in a separate job

- **Status:** Proposed (2026-11-21, before any agent code)
- **Decision area:** D2, control flow

## Context

The flow is not a straight line. It has three loops:

- tests fail → back to implementation (with a retry budget)
- tests keep failing → back to design
- reviewer requests changes → back to implementation (code problem) or design (approach
  problem), at most twice

Someone has to decide when to move on, when to go back, and when to give up. GitHub Actions
jobs form a DAG (`needs:`), which means **jobs cannot loop**. The reviewer must also run with
fewer permissions than the builder (ADR-008), and in Actions permissions are set per job.

## Decision

1. **One workflow (`autose.yml`) with three jobs:** `gate` → `build` → `review`.
2. **Inside `build`, a plain Python orchestrator runs stages 1–5 as a state machine.** It
   calls an agent for a stage, runs that stage's check itself, and picks the next state from
   fixed rules:

   | Situation | Next state |
   | --- | --- |
   | Check passed | Next stage |
   | Tests fail, implementation tries < 3 | Stage 3 again, with the failure output |
   | Tests fail, 3 tries used, design redo not used | Stage 2 again, with the failure summary |
   | Anything else fails past its budget | STOP: write the reason into the stage artifact |

3. **The reviewer's verdict decides where a review loop goes back to**, but the
   orchestrator enforces it: `code` → stage 3, `approach` → stage 2, round ≥ 2 → stop and
   hand to a human.
4. **Review loops are new workflow runs.** The review job starts the next round with
   `workflow_dispatch` (inputs: issue, `start_from`, `round`). This is the one event that
   GitHub lets the built-in token trigger.

**No LLM decides the control flow.** Agents produce artifacts, and code decides what happens
next.

## Alternatives

- **An LLM orchestrator ("planner agent picks the next step").** More flexible: it could skip
  stages or invent new paths. Rejected: we must guarantee the six stages and checks always
  run, budgets are always respected, and a human always merges. An LLM controller can be
  talked out of a rule by injected issue text, and its decisions are hard to audit. A state
  machine is easy to draw in the sequence view and easy to test.
- **One Actions job per stage, chained with `needs:`.** Very visible in the Actions UI.
  Rejected: jobs cannot loop back, so retries would need extra dispatch runs for every
  failure. Each job also starts a fresh runner, which means installing Python, the SDK and
  the repo again, about a minute each.
- **Everything, including review, in one job.** Simplest. Rejected: the reviewer would run
  in the same workspace and with the same write token as the implementer, which breaks
  independence (ADR-008).
- **Jobs triggering each other through labels or comments.** Rejected: events created by the
  built-in `GITHUB_TOKEN` do not start new workflow runs (except `workflow_dispatch`), so
  this would need a personal access token, which adds a secret and widens permissions.

## Consequences

- All retry budgets are visible in one place (the orchestrator) and logged in `state.json`.
- One workflow run covers one build attempt plus one review. A full issue with two review
  rounds is up to three linked runs, and `runs.md` must link all of them.
- The orchestrator is ordinary code, so it can be unit-tested without calling a model.
- Less flexible: if an issue needs a path that isn't in the table, the run stops and a human
  decides. We accept this. For a bot in someone else's repository, stopping is safer than
  improvising.
