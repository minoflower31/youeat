# Reviewers

This file decides which reviewer runs when. Each reviewer owns its criteria, tools, model and output schema in `.claude/agents/<name>.md`, so don't add review criteria to a delegation message.

Spawn the reviewers of one review in parallel (Agent tool), by `agentType`.

## Design review

For a design proposal before code exists, run all three: `design-gap-analyzer`, `overengineering-analyzer`, `design-verifier`.

## Code review

For a diff:

| Reviewer | Runs |
|---|---|
| `bug-analyzer` | always |
| `overengineering-analyzer` | always |
| `test-analyzer` | when the diff touches test files |
| `security-auditor` | when the diff touches auth/authz config or annotations, request-bound input, file upload/download, native or dynamic SQL, or session/cookie config |

## Judging findings

`finding-verifier` judges findings before their disposition is decided: the bug and security findings of a code review, and review comments on a PR. Spawn it once per round with all of them.
