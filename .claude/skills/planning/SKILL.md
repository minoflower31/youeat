---
name: planning
description: "Interviews the user to pin down what to build, splits it into tasks, and writes their docs/tasks/<TASK_ID>-<description>.md files with Requirements, Out of Scope and Verification. Use when the user asks to organize requirements or split work into tasks (e.g. '요구사항 정리해줘', '태스크 나눠줘', '태스크 쪼개줘')."
model: opus
effort: medium
---

# Planning

Pin down requirements through an interview and turn them into task files. Don't write code or settle how a task is built. Respond and write in Korean.

## Arguments
- One optional argument, passed as the argument: a plan document path.

## Execution Rule

Besides approval steps, Step 2 waits only for interview answers.

Checklist format:
- [ ] Step 1: Read Inputs
- [ ] Step 2: Interview
- [ ] Step 3: Propose Tasks (approval required)
- [ ] Step 4: Write Files
- [ ] Step 5: Output

## Process

1. **Read Inputs**
   - A plan document path: read it.
   - List `docs/tasks/<PREFIX>-*.md` to find the numbers already taken.

2. **Interview**
   - Ask one question at a time. Skip what the plan document or the conversation already answers.
   - Ask requirement-side questions only: goal, edge cases (e.g. the allowed length and format of each input), exclusions, the task split, a contract several tasks share, and how to prove it works. Don't ask how one task is built; with a plan document, record that question under its task as an item to settle in design.
   - Continue until every requirement is a verifiable statement and each task's exclusions and proof of completion are settled.

3. **Propose Tasks** (approval required)
   - Split into tasks, each one verifiable increment that fits a single `blueprint` -> `impl` cycle. One task is a valid result.
   - Present a table: proposed `<TASK_ID>` (next number per CLAUDE.md Task ID), title, Depends on, the requirements it covers.
   - Write each title as a terse noun phrase, because it becomes the task file heading.
   - Print the checklist and stop until the user approves.

4. **Write Files**
   - A plan document argument or two or more tasks: record the decisions and the task list in the plan document (default `docs/plan.md`).
   - Write `docs/tasks/<TASK_ID>-<description>.md` per `.claude/rules/task-file.md`: title, `## Depends on` with the predecessors' `<TASK_ID>`s, `## Requirements` derived from the plan items it covers, `## Out of Scope` and `## Verification` from the interview answers. `<description>` is a short kebab-case ASCII slug of the title.
   - Before writing, check that no `docs/tasks/<TASK_ID>*` file exists for an approved ID. If one does, stop and report it.
   - A section the user's answers do not settle stays as the Skeleton has it.

5. **Output**
   - Report the written files. Suggest next step: `/workflow <TASK_ID>` for each task with no unmet Depends on.
