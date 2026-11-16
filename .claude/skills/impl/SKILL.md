---
name: impl
description: "Personal task implementation workflow: create task branch from `<BASE_BRANCH>`, write code and tests per the task file's Design section, run build/test verification. Requires design phase to be complete. Trigger on '태스크 구현해줘', 'implement task', 'task implement'."
model: opus
effort: medium
---

# Implement Task

Implement the given task following the workflow.

## Arguments
- Task ID: passed as the argument (referenced as `<TASK_ID>` below, e.g., TASK-123)
- `skip-approval` (optional): skips every (approval required) step, per CLAUDE.md "Skill Execution".

## Execution Rule

Checklist format:
- [ ] Step 1: Check Design Phase
- [ ] Step 2: Implementation
- [ ] Step 3: Verification
- [ ] Step 4: Output

## Process

1. **Check Design Phase**
   - Find task file with glob pattern `docs/tasks/<TASK_ID>*` and read it
   - If the task file has no `## Design` content, or its first line is `(승인 대기)`: invoke `/blueprint` first.
   - If `## Design` is already written, proceed to Step 2 immediately.

2. **Implementation**
   - Get current branch name: `git rev-parse --abbrev-ref HEAD`
   - If already on this task's branch (matches `<type>/<TASK_ID>-<description>`, e.g., a pre-created worktree branch): skip the rest of this branch setup (no pull, no branch creation) and go straight to code analysis below.
   - If not on `<BASE_BRANCH>` (base branch per CLAUDE.md Git Conventions), stop: "현재 <BASE_BRANCH> 브랜치가 아닙니다. 먼저 /commit으로 현재 작업을 정리해주세요."
   - Check for uncommitted changes: `git status`
   - If uncommitted changes exist:
     - If only `docs/tasks/` files are changed, proceed (task file will be carried to new branch)
     - Otherwise: stop and ask user to commit or stash first.
   - Pull latest: `git pull`
   - Create branch from `<BASE_BRANCH>`: `git checkout -b <type>/<TASK_ID>-<description>`
   - Branch type based on task nature (feat, fix, refactor, etc.)
   - For concurrency / packet-parsing / performance-critical code: enumerate edge cases explicitly, and apply `.claude/rules/java-spring/throughput.md` (hot-path judgement, forbidden patterns, ownership javadoc). That file owns the criteria; don't restate them here.
   - Build one `## Progress` step at a time, in order. Keep `## Progress` per `.claude/rules/task-file.md` Progress through Step 3.
   - Write code following CLAUDE.md conventions
   - Write unit tests using project's existing test framework
   - Testable logic needs tests. Don't skip them.

3. **Verification**
   - Scope the build to what changed. Decide from `git diff --name-only origin/<BASE_BRANCH>...HEAD`:
     - Diff touches Java / build config / migrations -> run the full build and test command.
     - Diff touches only static resources or templates (no compiled source) -> the compile+test cycle proves nothing about it. State that and skip it; those changes are verified by `workflow`'s Runtime Verification step against a running app instead.
   - Re-runs: re-run the full build only when a later revision touches compiled source. Don't re-run it for a revision confined to static resources, templates, tests already run, or docs.

4. **Output**
   - Report implementation progress in Korean
   - Print the checklist and stop. Don't proceed to commit until the user invokes `/commit`.
