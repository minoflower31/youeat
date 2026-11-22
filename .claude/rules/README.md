---
paths:
  - "**/.claude/rules/**"
---

# Rules

Rules are auto-attached by the `paths` glob in each file's frontmatter. A rule fires
only when a matching file is touched, so an unused rule is inert -- but it is still
carried into every project that copies this set, where it becomes stale documentation
nobody owns.

## Porting to a new project

Keep the folder matching this project's stack. Delete the rest.

| File / Folder | Applies to |
|---|---|
| `comment.md` | Every stack. Take it as-is |
| `task-file.md` | Every project that keeps `docs/tasks/` task files. Take it as-is |
| `skill-authoring.md` | Every project that keeps `.claude/skills/`. Take it as-is |
| `java-spring/` | Java + Spring Boot + Gradle + Flyway |

Stack rules live only in stack folders. `comment.md`, `task-file.md` and `skill-authoring.md` are the exceptions: comment
discipline does not depend on the language, and real violations came from both Java and shell;
`task-file.md` governs task documents and `skill-authoring.md` governs skill files, not code. Before adding another exception: don't put an
invented generalization at the root; a rule goes there only when the same violation was actually
observed in different stacks. Otherwise it goes in a stack folder or a new sibling (`node/`,
`python/`, ...).

## Adding a rule

1. Put it in the stack folder it belongs to, or create a new sibling folder.
2. Set `paths` in the frontmatter so it attaches only to the files it governs.
   Too broad a glob means the rule loads on every unrelated edit.
