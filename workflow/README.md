# Workflow code

A copy of the pipeline as it runs in the fork (`keshavdubeyy/tinydb`, branch `master`).

| Path | What it is |
|---|---|
| `.github/workflows/autose.yml` | The GitHub Actions workflow: `gate` → `build` (stages 1-5) → `review` (stage 6) |
| `.autose/gate.py` | Who may start a run; queue notice; `/autose restart` (ADR-010) |
| `.autose/orchestrator.py` | Fixed state machine for stages 1-5, retry and escalation rules (ADR-002, 004) |
| `.autose/review.py` | Independent reviewer job, rubric validation, review rounds (ADR-008) |
| `.autose/agents.py` | One agent session via the Claude Agent SDK; per-agent tool policy (ADR-005, 006, 009) |
| `.autose/checks.py` | Deterministic stage checks (ADR-007) |
| `.autose/common.py` | GitHub helpers, secret handling, status-comment state |
| `.autose/prompts/` | Agent prompts; `a1_skill_condensed.md` is the A1 requirements skill (ADR-003) |
| `.autose/tests/` | Offline tests with fake agents (no model or GitHub calls) |

Run the offline tests from the fork root: `python -m pytest -o addopts= .autose/tests`
