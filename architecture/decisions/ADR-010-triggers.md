# ADR-010: Anyone can request a run, a collaborator approves it, and only one run per issue at a time

- **Status:** Accepted (2026-11-21, after author review, before any agent code)
- **Decision area:** D10, triggers

## Context

My first preference was that anyone who comments on a ticket should be able to start the
bot. It is open, friendly and easy.

But on a public repository, "anyone" includes strangers and spam bots. Every run spends
money from a $10/month budget, so one stranger posting `/autose` on 20 issues could use it
all up. And a run started by a stranger would be built from text that stranger controls,
which is the prompt-injection risk in ADR-009.

The second question is what happens when two people start the bot on the same ticket at the
same time. My view: the second person should get a clear sign that someone else is already
working on it, and be asked what they want to do, instead of two runs silently fighting over
the same branch.

## Decision

**1. Triggers**

| Event | Who | What happens |
| --- | --- | --- |
| Label `autose` added to an issue | Only people who can add labels (collaborators) | Run starts |
| Comment `/autose` on an issue or open PR | OWNER, MEMBER or COLLABORATOR (checked with `author_association`) | Run starts |
| Comment `/autose` | Anyone else | **No run.** The bot replies: "Thanks, a maintainer needs to approve this. A maintainer can add the `autose` label to start." It also adds the label `autose-requested` so maintainers can find these requests. |
| `workflow_dispatch` | The review job (next round), or a maintainer by hand | Run continues from `start_from` |

This keeps the openness I wanted (anyone can ask) while a trusted person decides whether
money gets spent.

**2. Two runs on the same ticket**

- All runs for one issue share a GitHub Actions `concurrency` group (`autose-issue-N`), with
  `cancel-in-progress: false`. A second run waits in line and never runs in parallel.
- When a second trigger arrives while a run is active, the gate job posts a comment: "A run
  for this issue is already in progress (link, started by @user). Your request is queued. To
  cancel the current run and start fresh, comment `/autose restart`. To drop your request,
  do nothing." (Only collaborators can use `/autose restart`.)
- If a queued run starts after the first one has already opened a PR that is waiting for
  review, the gate sees that in the status comment (ADR-004) and stops with a note, instead
  of building again.

## Alternatives

- **Anyone's comment starts a run.** My first choice. Rejected after thinking about cost and
  safety: strangers could drain the budget and feed the bot attack text. The request-and-
  approve flow keeps most of the openness.
- **Label only, no comments.** Simplest and safest. Rejected: `/autose` on an open PR is
  useful for re-running after a human edit, and the assignment suggests both triggers.
- **Cancel the old run when a new one starts.** Common in CI. Rejected: it can kill a run
  halfway through and waste what it already spent. Queueing plus a clear message is kinder
  and safer.
- **Run both in parallel.** Rejected: both would push to the same branch and overwrite each
  other.

## Consequences

- No stranger can spend money or start a build.
- People always know why nothing happened (a reply explains it), and who is already working
  on a ticket.
- A maintainer has to act on outside requests. For a small project that is a reasonable
  amount of work.
