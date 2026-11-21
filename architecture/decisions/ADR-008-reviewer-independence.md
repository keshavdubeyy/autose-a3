# ADR-008: Keep the reviewer independent through separation, permissions, a different model and a fault-finding prompt

- **Status:** Proposed (2026-11-21, before any agent code). Will be tested in Experiment A.
- **Decision area:** D8, reviewer independence

## Context

A reviewer that approves everything adds cost and false confidence, and nothing else. LLM reviewers
tend to agree with confident-looking code, especially when they can see the author's
reasoning or share the author's model and blind spots. The assignment requires that the
reviewer sees only the issue, the diff and the repo at the PR head, can run code, and cannot
push.

## Decision

Independence is enforced at four layers, so that no single slip breaks it:

1. **Separate job and runner.** The reviewer runs in its own Actions job on a fresh machine.
   Nothing from the build job's workspace or agent sessions exists there. The job checks out
   the PR head commit with `persist-credentials: false`.
2. **Permissions.** The review job's token has `contents: read` and only enough PR access to
   post a comment. The reviewer *agent* never sees any token. The plain-code review runner
   posts the comment after the agent finishes. Even if the agent ran `git push`, it would
   fail.
3. **Different model from the implementer.** The two models will have different blind spots.
   The exact pairing is decided in ADR-006.
4. **A prompt that asks for faults, plus a structured verdict.**
   - The prompt says: assume the change is wrong until shown otherwise; re-read the issue and
     check the diff actually solves it; run the tests; look for edge cases the issue implies
     but no test covers.
   - Output is JSON: `{"verdict": "APPROVE" | "CHANGES_CODE" | "CHANGES_APPROACH", "findings": [...]}`,
     and every finding must cite a file and line.
   - `APPROVE` must include a list of what was checked. An approval with an empty checklist
     is treated as invalid and re-asked once.

**How we know it isn't approving everything:** we run it on five seeded PRs with known
labels (some correct, some with planted bugs) and report catches, misses and false alarms.

## Alternatives

- **Same agent self-reviews with a "be critical" prompt.** Cheapest. Rejected: same context,
  same model, same blind spots. It is the failure mode the assignment warns about.
- **Same model, separate job.** Gives most of the benefit. Not rejected outright: **this is
  the control arm of Experiment A** (same model vs different model as reviewer, measured on
  the seeded PRs).
- **Let the reviewer push fixes.** Faster. Rejected: a reviewer that fixes code becomes a
  second implementer, and nobody independent reviews its fixes. It also breaks the "no push"
  rule.
- **Human-only review.** Fully independent, but defeats the purpose of the bot. The human
  still makes the final merge decision, on top of this review.

## Consequences

- The reviewer cannot see why the implementer made a choice, so it may flag deliberate
  trade-offs as problems. We accept some false alarms in exchange for independence, and we
  report the false-alarm rate.
- A second model adds a second provider or model configuration to maintain.
- Seeded PRs give a measurable check of reviewer quality, separate from whether the
  implementer is good.
