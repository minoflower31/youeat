---
name: fix
description: "Analyzes a fix request on a task branch, proposes the fix design for approval, records it in the task file, then implements and verifies it. Use when the user names a concrete target with '수정해줘', '고쳐줘', '바꿔줘', '변경해줘' or 'fix' (e.g. 'X를 수정해줘', 'Y를 바꿔줘', '현재 task에서 Y 빼먹음')."
model: opus
effort: high
---

# Fix

Apply a fix with design-first approach. Respond in Korean.

## Arguments
- Fix description: passed as the argument (referenced as `<FIX_DESC>` below)
- `skip-approval` (optional): skips every (approval required) step, per CLAUDE.md "Skill Execution".

## Execution Rule

Checklist format:
- [ ] Step 1: Analyze
- [ ] Step 2: Propose Fix Design (approval required)
- [ ] Step 3: Update Task File
- [ ] Step 4: Implement Fix
- [ ] Step 5: Verify
- [ ] Step 6: Output

## Process

1. **Analyze**
   - If the current branch (`git rev-parse --abbrev-ref HEAD`) is `<BASE_BRANCH>` (per CLAUDE.md Git Conventions) or main/master, stop: "현재 <branch> 브랜치입니다. task 브랜치에서 실행해 주세요."
   - Understand the fix request from `<FIX_DESC>`
   - For an item whose location (file:line), root cause and fix direction `<FIX_DESC>` already states, read only that location and the callers the change reaches, and confirm each statement against the code. When a statement does not hold, analyze the item as the next bullet says
   - For every other item, search and read related code and identify root cause and affected areas

2. **Propose Fix Design** (approval required)
   - Propose how to fix with specific file:line references
   - Explain what changes are needed and why
   - Show the `## Requirements` and `## Verification` items Step 3 will add, reword or remove, per `.claude/rules/task-file.md` Requirements and Verification
   - Print the checklist and stop until the user approves.

3. **Update Task File**
   - Extract task ID from the current branch name
   - Update `## Requirements` and `## Verification` per `.claude/rules/task-file.md` Requirements and Verification
   - If task file exists, update its `## Design` based on approved fix design
   - If the task file has no `## Design`, add one
   - Update `## Progress` for the fix. A review-driven fix adds or rewords no step
   - Format is owned by `.claude/rules/task-file.md`
   - If no task file, skip this step

4. **Implement Fix**
   - Apply the approved fix design
   - Write or update tests if needed

5. **Verify**
   - Run the build and test command from CLAUDE.md `## Commands`
   - Update `## Progress` with the result, per `.claude/rules/task-file.md` Progress
   - When the fix changes any file other than the task file, re-run the command in the verification results and rewrite them. List a check that needs a running instance in the unverified list instead of re-running it
   - If tests fail: report and stop. Don't proceed until the user instructs.

6. **Output**
   - Report changes made in Korean, including the `## Requirements` and `## Verification` items Step 3 added, reworded or removed
   - List modified files
