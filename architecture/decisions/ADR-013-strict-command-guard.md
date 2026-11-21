# ADR-013: Keep the command guard strict even though agents waste turns on it

- **Status:** Accepted (2026-11-21, after the issue runs and experiments)
- **Decision area:** D5 tools and D9 safety

## Context

ADR-005 lets the Implementer, Tester and Reviewer run exactly one shell command:
`python -m pytest [args]`. A pre-tool hook denies everything else. In the real runs, agents
kept trying commands like `python -m pytest -q 2>&1 | tail -5` or `cat issue.md diff.patch`.
The guard denied 1–3 such calls in almost every run. Each denial costs a turn. Usually the
agent then switched to the Read tool or to a plain `python -m pytest`.

In one Experiment B trial, a denied `cat … spec.md` meant the reviewer never read the spec
at all, so that trial had to be marked invalid and re-run.

## Decision

Keep the guard exactly as strict as it is. No pipes, no `cat`, no other commands.

My reason is that a wasted turn is almost free: all reviews cost $0.003–$0.04, and no run came
close to its turn or budget limit. Every extra command we allow is one more path to leak a
secret or do something outside the agent's job. Even a harmless-looking pipe opens the door to
`| curl` or `$(env)` tricks that the pattern then has to block. The agents already recover on
their own.

## Alternatives considered

- **Allow `| tail -N` and `| head -N`.** This would save most of the denied turns. Rejected: it
  makes the safety pattern more complex, and each exception is a new place where a mistake can
  let something through.
- **Tell the agents in the prompt** that only `python -m pytest` works and files must be read
  with the Read tool. Not chosen now. The guard stays the real control either way, and the
  measured cost of denials is tiny. This is the first thing to try if denials ever start
  causing failed runs.

## Consequences

- Denied tool calls are logged per agent call and shown in the status comment
  (`denied=N`), so their cost stays visible.
- An agent can occasionally miss information it tried to get with a denied command, as in the
  invalid Experiment B trial. Experiments must therefore check in the log that a treatment
  actually happened.
