---
name: skill-polish
description: "Lists the checks for trimming a skill or one of its reference files line by line: what to cut, what to keep and what to fix. Use when the user asks to review, tidy or polish a skill (e.g. 'workflow 스킬 정리하자', 'e2e.md 다듬자', '스킬 점검해줘')."
---

# Skill Polish

Make a skill as short as it can be while a human and an agent still follow it without mistakes.

- Propose numbered cut and fix items, plus keep items for lines that look cuttable but must stay, each with the quoted line and a one-line reason. Then show the section as it would read. Edit only after the user's ok.
- Verify every fact a line states against the code, the tool list, a read-only call or a real test before keeping it. Ask before any write.
- Before a change that alters meaning, grep for the files that point at the target. List findings outside the requested section separately.
- Respond in Korean.

## Cut

- A rule another file owns, CLAUDE.md included. Point at the owner by name instead. Skip the pointer for a CLAUDE.md rule that already applies everywhere.
- A line that only explains: history, why the design exists, what a script does internally.
- A rule for behavior that follows from the skill's purpose, or a special case of a rule already present.
- An extension point nothing uses.
- Another skill's name or situation, unless this skill invokes it. State the input or output contract instead: "so the branch name matches the task file", not "because workflow looks the branch up by that name".
- Ornament. State the bare directive: "write 0 for an empty count", not "write zeros too, as proof that nothing was dropped".

## Keep

- A rule the agent was seen skipping, as the user, a memory, a commit or a task file records.
- A `because` clause whose removal lets the agent err.
- A literal block whose removal makes output vary between runs (Checklist format, output skeleton).

## Fix

- Behavior: a step that can't do what it says, such as a tool option it omits or a value its consumer reads differently.
- Description: a third-person verb sentence with the key use case first, then `Use when` with the phrases users type. No `Personal` label, no implementation detail.
- Conditions: "When/If <subject> <condition>, <action>.", naming the subject, instead of a bare `X -> Y`.
- Structure: split a step that branches on entry state or outcome into sub-blocks (`4a`, `4b`), in execution order. Number a list only when each item must run after the previous one; otherwise use bullets.
- Commands: write a well-known command as prose. Keep a code block only for a non-obvious one.
- Terms: one term per concept, in English, including the names of Korean output labels ("verification section" for `### 검증`). Korean stays only in output templates, a term-to-output mapping (`fixed` -> `수정`), and strings a script prints that the skill matches.
- Pointers: name another file's step, not its number (`references/authoring.md` section 7). After a rename, grep every reference.
- Checklist format: align it with the step headings last.
