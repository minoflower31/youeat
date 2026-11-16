# CLAUDE.md - Project Context for AI Agent

## Workflow

### Plan & Execute

- **Stop on Failure**: When an approach fails, stop and re-plan instead of pushing through.
- **Delegate Research**: Delegate research, exploration, and parallel analysis to subagents to keep the main context clean.

### Task Management

1. **Implement**: Keep `## Progress` per `.claude/rules/task-file.md`, and keep the task file in sync with design and implementation changes.
2. **Verify**: Prove it works (tests, logs, demo) and record the results in the task file.

## Core Principles

- **Wait First**: Wait for the user's instruction before acting.
- **Simplicity First**: Use the simplest solution that works; prefer straightforward code to clever code.
- **Root Cause**: Fix the root cause, not the symptom. Don't ship temporary fixes.
- **Minimal Impact**: Touch only what the task requires, and leave neighboring code as it is.
- **No Over-Engineering**: Implement only current requirements, without speculative abstractions, config flags, or hooks for hypothetical future needs.
- **Plain ASCII**: Keep code and comments free of emojis and special symbols.
- **Code Over Task Docs**: `docs/tasks/*.md` records design at the time of writing, and a later task can change it. When answering from task docs, check the newest tasks first. Code is the final source: verify current behavior in code before stating it, and state a task-doc claim as current behavior only after that check.

## Skill Execution

Every skill run follows these rules. A skill's own `## Execution Rule` holds only its checklist and the lines specific to it.

- When the skill has a `Checklist format` block, print it before starting and mark each step as you go.
- At a step marked (approval required), stop until the user confirms. Continue through every other step without stopping.
- `skip-approval`: a skill that lists it under `## Arguments`, invoked with a standalone argument exactly equal to `skip-approval`, skips every (approval required) step and asks for no confirmation. A skill that does not list it never skips an approval step, because some gates guard outward writes (e.g. `jira-push` creating tickets).
- When a subagent stops at its turn limit without its result, `SendMessage` that same subagent to return it now from what it gathered, marking what it did not check as unjudged. Don't spawn a fresh one, because it starts empty and stops at the same limit.

## Skill Authoring Principles

When writing or modifying `.claude/skills/<name>/SKILL.md`, follow these principles:

- **Consistency**: A procedure skill (a procedure the user invokes) keeps the section order Description → Body → Arguments → Execution Rule → Process. Domain-specific sections may be inserted as long as the canonical ones keep that relative order. Judgment-criteria docs and initializers are not procedure skills and are not bound by that order.
- **Simplicity**: Each rule appears once, at its decision point. Before keeping a bullet, apply the three-No test: (a) real execution decision point, (b) distinct tone/layer vs siblings, (c) removal causes drift. Three No → delete.
- **Ownership**: One rule has one owning file. A skill that depends on it points at the owner by name instead of restating it, because a restated rule is the one that drifts.
- **Plain directives**: Write directives as plain imperatives ("Do X", "Don't do Y"), and say what to do rather than only what not to do. Add emphasis (IMPORTANT, MUST, capitals) only to an instruction Claude has been seen skipping, because emphasis on many lines makes none of them stand out.
- **Placeholders**: Use the `<TASK_ID>` placeholder instead of `TASK-` or any concrete prefix literal in file paths, branches, commits, and PR/MR titles.

Repo-specific authoring patterns live in `.claude/skills/skill-polish/references/authoring.md`. Read it before authoring or restructuring a procedure skill.

## Project Overview

- **Name**: <project name>
- **Description**: <one-line description>
- **Architecture**: <e.g. SSR (Thymeleaf), API only, SPA + API>
- **Tech stack**: <language, framework, build tool, database, key libraries>

## Coding Conventions

### Package Structure

<The project's package or module tree, as a fenced code block. `spring-bootstrap` writes it here for a new Spring project.>

## 서비스 톤앤매너 (UI 가 있는 프로젝트만)

- **기본 어체**: 사용자 친밀감을 높이기 위해 해요체를 기본으로 사용한다.
- **예외 사항**: 시스템 메시지 등 명확한 정보 전달과 가독성이 필요한 경우 하오체를 사용한다.
- **메뉴/버튼명**: 간결성을 위해 명사형으로 통일한다.

## 시스템 안내 정책 (UI 가 있는 프로젝트만)

- **Alert (기본형)**: 단순 사실 확인, 경고, 입력 누락 안내 (사용자 확인 필수).
- **Modal (확장형)**: 상세 정보 노출, 복합 로직 처리, 중요 선택.

## Task ID

Work is tracked in task files (`docs/tasks/<TASK_ID>-<description>.md`), not in an issue tracker. The task file is the only record of a task.

- **PREFIX**: `TASK`
- **`<TASK_ID>`**: `<PREFIX>-\d{3}(-\d{2})?`
- **Numbering**: `planning` assigns the next number, one above the highest `<PREFIX>-NNN` in `docs/tasks/`. A follow-up split from a task takes `<parent>-NN`.
- **Examples**: `<PREFIX>-001`, `<PREFIX>-123`, `<PREFIX>-123-02`

## Git Conventions

- **Base branch**: `main` (change it when the project's PR base is another branch, e.g. `develop`). It is the only PR base for new work, and worktrees branch from `origin/<base branch>`. Skills bind this value as `<BASE_BRANCH>`.
- **Branch**: `<type>/<TASK_ID>-<description>` (types: feat, fix, refactor, chore, docs, test). Planning documents outside `docs/tasks/` (PRD, specs, IA) go on `docs/plan` without a `<TASK_ID>`.
- **Commit**: `<type>: <TASK_ID> <description>`
- **PR**: Use `/pr` skill. Template at `.github/pr_template.md`
- **Force-push**: Get the user's explicit approval for every force-push (`git push --force` / `--force-with-lease` / `-f`), including after a rebase or conflict resolution. Before asking, show `git diff --stat origin/<branch>...HEAD` and `git log --oneline origin/<branch>..HEAD` so the user confirms the files match intent. One approval covers one push.
- **Staging**: Stage explicit paths (`git add <path> ...`) rather than `git add -A` / `git add .` / `git add --all`. Local artifact paths (`.claude/` runtime outputs: `agent-memory/`, `worktrees/`, `settings.local.json`; plus `.DS_Store`, and project-specific ones such as `uploads/`) are excluded via `.gitignore`. `.claude/` skills, agents, rules, hooks and `settings.json` are tracked. Check `git diff --cached --name-only` before committing.

## DB Migration (Flyway)

When adding or changing a migration, follow `.claude/rules/java-spring/flyway.md` (auto-attached for migration paths). Delete this section when the project has no Flyway.

## Worktree Environment

A worktree (`.claude/worktrees/<TASK_ID>`) holds only tracked files. Gitignored runtime files that exist in the main checkout are absent in every worktree. Before the first test run or boot in a worktree, copy the ones this project needs from `<MAIN_CHECKOUT>` rather than discovering a missing one from a context-load failure.

- `<gitignored path>`: <which test or boot fails without it>. Copy with `cp -R <MAIN_CHECKOUT>/<path> <WORKTREE>/<path>` (list every such path here; none listed means nothing to copy).
- Per-machine config overrides (e.g. `application-local.yml`): tests use the tracked `application-test.yml` and don't need them; a live boot in the worktree does.
- Relative paths in test config resolve against the Gradle module directory (test CWD), not the repo root.
