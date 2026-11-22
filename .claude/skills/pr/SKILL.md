---
name: pr
description: "Personal task PR workflow: fill .github/pr_template.md from task file + git diff, preview, create PR with '<type>: <TASK_ID>' title via gh CLI. Invoke via /pr."
model: sonnet
effort: medium
---

# Create Pull Request

Create a pull request for current task. Respond in Korean.

## Arguments
- `skip-approval` (optional): skips every (approval required) step, per CLAUDE.md "Skill Execution".

## Execution Rule

Checklist format:
- [ ] Step 1: Identify Current Task
- [ ] Step 2: Read PR Template
- [ ] Step 3: Analyze Changes
- [ ] Step 4: Fill PR Template
- [ ] Step 5: Preview and Confirm (approval required)
- [ ] Step 6: Create PR
- [ ] Step 7: Output

## Process

1. **Identify Current Task**
   - Get current branch name: `git rev-parse --abbrev-ref HEAD`
   - Extract `<TASK_ID>` from branch name
   - Read `docs/tasks/<TASK_ID>*.md` for context

2. **Read PR Template**
   - Read `.github/pr_template.md`

3. **Analyze Changes**
   - Get changed files: `git diff --name-only origin/<BASE_BRANCH>` (`<BASE_BRANCH>` = base branch per CLAUDE.md Git Conventions)
   - Read changed files for context
   - Understand what was implemented

4. **Fill PR Template**
   The reader is a reviewer who did not write the code. Make every section tell them what they need to know. Don't transcribe the diff.
   Tone: end every sentence (Summary and Context paragraphs, every bullet that is a sentence) in the formal polite form (~합니다 / ~했습니다), the prevailing register of Korean PR bodies. Table cells and single-phrase bullets stay terse notes. Don't use the casual polite form (~해요), or ~함 / ~됨 endings on a bullet of two or more sentences.

   4a. **Summary and Context**
   - Summary: exactly 3 one-sentence paragraphs: what changed / why / the one impact the reviewer needs to know before opening code. Separate them with blank lines, because GitHub renders consecutive lines as one paragraph.
   - Context: plain-sentence bullets on why now and why this way. Don't add a label prefix such as `왜 지금:`. Give decision tables and rejected alternatives as a link to the task file section. Don't restate them.

   4b. **Changes**
   - Describe behaviour: each bullet is "before A, now B". Don't list by module/file/class, method signatures, constructor parameters, javadoc or comment edits.
   - Group bullets under `###` sub-headings by the flow a user or operator sees (request path, file format, recovery, ...), not by module.
   - One bullet = one sentence = one behaviour change. At most one code identifier per bullet, and only when the reviewer has to open that file.
   - Give deletions, new config keys and deploy notes each their own `###` sub-heading. Config keys as a table: key / default / meaning.

   4c. **Checklist and Testing**
   - Checklist: verify each item.
   - Testing: copy the task file's verification results subsection, turning its failed and unverified label lines into `###` headings. When the task file has no results, build them in that form per `.claude/rules/task-file.md` Verification.

5. **Preview and Confirm** (approval required)
   - Show PR title: `<type>: <TASK_ID> <description>`
   - Show filled PR body
   - Print the checklist and stop until the user approves.

6. **Create PR**
   - If PR already exists: in skip-approval mode update it with `gh pr edit` without asking; otherwise ask if user wants to update with `gh pr edit`, then stop or update per user choice.
   ```bash
   gh pr create --base <BASE_BRANCH> --head <branch> \
                --title "<type>: <TASK_ID> <description>" \
                --body-file <body file written with the Write tool>
   ```

7. **Output**
   - Report PR URL in Korean
   - Show base -> head branch info
