---
paths:
  - "**/.claude/skills/**"
  - "**/.claude/agents/**"
  - "**/.claude/rules/**"
---

# Skill Authoring Principles

Follow these principles when writing or modifying a skill, its reference files, an agent definition or a rule:

- **Consistency**: A procedure skill (a procedure the user invokes) keeps the section order Description → Body → Arguments → Execution Rule → Process. Domain-specific sections may be inserted as long as the canonical ones keep that relative order. Judgment-criteria docs and initializers are not procedure skills and are not bound by that order.
- **Simplicity**: Each rule appears once, at its decision point.
- **Ownership**: One rule has one owning file. A skill that depends on it points at the owner by name instead of restating it, because a restated rule is the one that drifts.
- **Plain directives**: Write directives as plain imperatives ("Do X", "Don't do Y"), and say what to do rather than only what not to do. Add emphasis (IMPORTANT, MUST, capitals) only to an instruction Claude has been seen skipping, because emphasis on many lines makes none of them stand out.
- **Placeholders**: Use placeholders (`<TASK_ID>`, `<PREFIX>`, `<BASE_BRANCH>`) instead of project values such as a concrete task prefix or branch name, in file paths, branches, commits and PR titles.

Repo-specific authoring patterns live in `.claude/skills/skill-polish/references/authoring.md`. Read it before authoring or restructuring a procedure skill.
