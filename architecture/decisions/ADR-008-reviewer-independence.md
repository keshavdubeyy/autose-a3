# ADR-008: An independent reviewer that must justify every verdict with a filled-in rubric

- **Status:** Accepted (2026-11-21, after author review, before any agent code). Tested in
  Experiments A and B.
- **Decision area:** D8, reviewer independence

## Context

A reviewer that says "approve" to everything is worse than no reviewer. It costs money and
gives false confidence. LLM reviewers tend to agree with confident-looking code, especially
when they share the author's context or model.

The assignment fixes some rules: the reviewer sees only the issue, the diff and the repo at
the PR head commit. It can run the code. It must **not** see the implementer's conversation
or reasoning, and it must not be able to push.

When I reviewed this, my first instinct was the opposite: a reviewer that sees the reasoning
would understand the goal better and judge more accurately. The assignment rules this out
for the real design, so we keep the rule, and we test the instinct in Experiment B (below).
We make sure the reviewer still understands the goal by giving it the original issue: that
is the user's actual goal, in the user's own words.

The second problem is how to tell whether an approval is real. An "approve" with no reasons
tells us nothing. An approval must come with evidence.

## Decision

**1. Separation.** The reviewer runs in its own Actions job, on a fresh machine, with a
read-only token. The agent itself never holds any token. Plain code posts its review after
it finishes.

**2. A different model from the implementer**, so they don't share the same blind spots
(exact pairing in ADR-006).

**3. Every verdict comes from a rubric.** The reviewer must fill in this evaluation matrix
before giving a verdict. Each row needs a result *and* evidence (a test name, command output,
or file and line):

| # | Rubric row | Result | Evidence |
| --- | --- | --- | --- |
| R1 | The change solves what the issue asks for | pass / fail | quote from issue + where in the diff |
| R2 | The full test suite passes when *I* run it | pass / fail | command + summary of output |
| R3 | The new tests actually test the issue's behaviour (not something trivial) | pass / fail | test names |
| R4 | Edge cases the issue implies are handled | pass / fail / n/a | which cases were checked |
| R5 | No unrelated or risky changes in the diff | pass / fail | files touched |
| R6 | Code is readable and follows the repo's style | pass / fail | file:line |

**4. The verdict follows from the rubric, and the code enforces it:**

- `APPROVE` is accepted only if every row is pass (or n/a) **and** every row has evidence.
  An approval with an empty or evidence-free rubric is rejected and the reviewer is asked
  once more.
- Any fail → `CHANGES_CODE` (R2–R6) or `CHANGES_APPROACH` (R1, if the whole approach misses
  the issue). The review must explain why.

**5. We check the reviewer itself** with five seeded PRs (some correct, some with planted
bugs). We report what it caught, what it missed, and its false alarms.

## Alternatives

- **The reviewer sees the implementer's reasoning.** It would understand the "why" better
  (my first instinct). Rejected for the real design: it breaks the assignment rule, and
  reasoning anchors the reviewer. If the reasoning sounds convincing, the reviewer tends to
  agree even when the code is wrong. **Experiment B tests a softer version of this
  instinct:** the reviewer gets `spec.md` (the pipeline's understanding of the goal) vs only
  the issue, and we compare catches and misses on the seeded PRs.
- **"Approve / request changes" with free-text reasons only.** Rejected: free text can be
  vague ("looks good"). A rubric forces the reviewer to check each thing and show evidence.
- **Same agent self-reviews.** Rejected: same context, same model, same blind spots.
- **Same model, separate job.** Not rejected outright: it is the control arm of
  **Experiment A** (same vs different model as reviewer).
- **The reviewer can push fixes.** Rejected: it would become a second implementer that nobody
  reviews, and it breaks the no-push rule.

## Consequences

- Every review is easy to audit: anyone can read the rubric and see what was checked.
- The reviewer doesn't know why the implementer made a choice, so it may flag deliberate
  trade-offs. We accept some false alarms and report how many there are.
- Filling a rubric costs more tokens than a one-line verdict, but it is the only way to tell
  a real approval from a rubber stamp.

## Evidence after the runs (21 Nov 2026)

- **Seeded PRs:** the default reviewer got 5/5 right, with the expected rubric row failing each time.
- **Experiment B:** a reviewer that read a spec written from the implementer's point of view gave the same verdicts in all 5 valid trials. This includes the PR whose spec listed the risky fsync removal as a requirement. The reviewer checked the spec against the issue rather than trusting it.
- **Decision: keep the rule.** Hiding the spec costs nothing, and 5 trials cannot rule out a small bias. The rule now stands as a precaution, not a measured effect.
- **False alarms:** on the five issue PRs and five seeded PRs, there were no rejections of a correct change. The one send-back on a pipeline PR (issue #2) was a real defect.
