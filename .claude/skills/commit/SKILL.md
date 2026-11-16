---
name: commit
description: "Personal task-branch commit workflow: pre-commit build/test verification, task-ID commit message (`<type>: <TASK_ID> ...`), push, optional squash-merge to `<BASE_BRANCH>`. Trigger on 'commit', '커밋해줘', 'commit and push', '커밋 푸시'."
model: sonnet
effort: low
---

# Commit and Push

Commit and push current task changes following the workflow.

## Arguments
- `skip-approval` (optional): skips every (approval required) step, per CLAUDE.md "Skill Execution".

## Execution Rule

Checklist format:
- [ ] Step 1: Identify Current Task
- [ ] Step 2: Pre-commit Verification
- [ ] Step 3: Stage Changes
- [ ] Step 4: Commit
- [ ] Step 5: Push
- [ ] Step 6: Squash Merge (approval required)

## Process

1. **Identify Current Task**
   - Get current branch name: `git rev-parse --abbrev-ref HEAD`
   - Extract `<TASK_ID>` from branch name (e.g., `feat/TASK-123-user-model` -> `TASK-123`)
   - Read `docs/tasks/<TASK_ID>*.md` for context
   - Check for uncommitted changes: `git status`
   - If no uncommitted changes, skip to Step 6

2. **Pre-commit Verification**
   - Run project's existing build and test commands
   - If tests fail: report and stop. Don't proceed until the user instructs.

3. **Stage Changes**
   - Review changed files: `git status`
   - Stage relevant files: `git add <files>`
   - Exclude unnecessary files

4. **Commit**
   - Format: `<type>: <TASK_ID> <description>`
   - Keep it a single line. Don't add a multi-line body or Co-Authored-By trailers.

5. **Push**
   - Check if remote exists: `git remote`
   - If no remote, skip to Step 6
   - Push to remote: `git push -u origin <branch>`

6. **Squash Merge**
   - `<BASE_BRANCH>` = base branch per CLAUDE.md Git Conventions.
   - Ask user: "<BASE_BRANCH>에 squash merge할까요?"
     - **Yes**:
       1. Get first commit message: `git log <BASE_BRANCH>..HEAD --reverse --format="%s" | head -1`
       2. `git checkout <BASE_BRANCH> && git pull`
       3. `git merge --squash <branch>`
       4. `git commit -m "<first commit message>"`
       5. When a remote exists, rebase onto the latest remote `<BASE_BRANCH>` right before pushing, because a parallel worktree/session may have pushed during the merge window: `git pull --rebase --autostash origin <BASE_BRANCH> && git push origin <BASE_BRANCH>`. Include `--autostash` so unrelated uncommitted files (e.g. excluded infra changes) do not block the rebase. When the rebase reports conflicts or blocked untracked files, stop and report for manual resolution. Don't force-push.
       6. `git branch -D <branch>`
       7. Report result in Korean
     - **No**: end
