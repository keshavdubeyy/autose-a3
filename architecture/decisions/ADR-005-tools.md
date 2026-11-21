# ADR-005: Each agent gets only the tools for its own task, and no agent can touch GitHub

- **Status:** Accepted (2026-11-21, after author review, before any agent code)
- **Decision area:** D5, tools

## Context

Each agent has one task, and there are other agents for the other tasks. There is no reason
for an agent to be able to do someone else's job. An agent that *can* do more might do more:
for example, a Tester that can edit source code might "fix" the code to make its tests pass.
Every extra tool is also one more thing an injected instruction could misuse.

The agents run on the Claude Agent SDK. It comes with built-in tools (Read, Grep, Glob,
Edit, Write, Bash, WebFetch, WebSearch) and lets us allow or block each one per session, and
block specific actions with hooks.

## Decision

**Rule: an agent gets exactly the tools its task needs.**

| Agent | Allowed tools | Explicitly blocked | Why |
| --- | --- | --- | --- |
| Planner | Read, Grep, Glob | Edit, Write, Bash, web | It reads and writes documents. Its documents are returned as text, and the orchestrator saves them. |
| Implementer | Read, Grep, Glob, Edit, Write, Bash limited to `python -m pytest` and `python -c` | Editing the Tester's test files or `.github/`; web | It changes code. It must not change the tests that judge it, or the workflow that runs it. |
| Tester | Read, Grep, Glob, Write limited to new files under `tests/`, Bash limited to `python -m pytest` | Editing any existing file; web | It writes tests and runs them. It must not fix the code. |
| Reviewer | Read, Grep, Glob, Bash limited to `python -m pytest` | Edit, Write, web | It inspects and runs code. It never changes anything. |

**No agent ever touches GitHub.** Pushing the branch, opening the PR, posting comments and
dispatching the next round are all done by plain code (`gh` CLI) in the orchestrator. Agent
processes are started with an environment that has **no `GITHUB_TOKEN`** and no other
secrets except the model API key.

**How it's enforced (three layers):**

1. The SDK's allowed-tools list per session.
2. A pre-tool-use hook that blocks writes to protected paths (test files for the
   Implementer, everything except new test files for the Tester).
3. A check after the stage: the orchestrator runs `git diff` and rejects the stage if any
   protected file changed, even if layers 1–2 somehow missed it.

**Why the `gh` CLI and not an MCP server for GitHub:** only plain code talks to GitHub, so
there is no agent that needs a GitHub tool. The `gh` CLI is preinstalled on Actions runners,
uses the job's token, and its commands are easy to read in the logs.

## Alternatives

- **Give every agent all tools and trust the prompt.** Rejected: a prompt is a request, not a
  guarantee. An agent can ignore it, and injected text can override it.
- **Give agents the GitHub MCP server.** Lets an agent open the PR or comment itself.
  Rejected: it puts a write token next to an agent that has read untrusted text, and none of
  the agents' tasks need GitHub.
- **Unrestricted Bash.** Simplest for the agents. Rejected: Bash can do anything (network,
  edit files, `git push`), which would undo every other restriction.

## Consequences

- A confused or tricked agent can only damage its own working copy, and the orchestrator
  checks that before anything is pushed.
- Sometimes an agent will want a tool it doesn't have (e.g. the Implementer wants to install
  a package). It has to say so in its output, and the run stops for a human. We accept this.
- Every blocked attempt is logged, which is useful evidence for the report.
