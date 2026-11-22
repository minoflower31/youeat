# CLAUDE.md - Project Context for AI Agent

## Core Principles

- **Wait First**: Wait for the user's instruction before acting.
- **Simplicity First**: Use the simplest solution that works; prefer straightforward code to clever code.
- **Root Cause**: Fix the root cause, not the symptom.
- **Stop on Failure**: When an approach fails, re-plan before trying again instead of repeating it.
- **Minimal Impact**: Touch only what the task requires, and leave neighboring code as it is.
- **No Over-Engineering**: Implement only current requirements, without speculative abstractions, config flags, or hooks for hypothetical future needs.
- **Plain ASCII**: Keep code and comments free of emojis and special symbols.
- **Task File Sync**: When you change code on a task branch outside a skill, update that task's task file per `.claude/rules/task-file.md`, and record the verification results there.
- **Code Over Task Docs**: When answering from `docs/tasks/*.md`, read the newest tasks first, because a later task can change an earlier design. Verify current behavior in code before stating it.

## Skill Execution

- When a skill has a `Checklist format` block, print it before the first tool call. Each time you stop for the user and when you finish, print it again with the completed steps checked.
- At a step marked (approval required), stop until the user approves. Don't stop anywhere else unless the skill says to wait.
- When a skill lists `skip-approval` under `## Arguments` and the invocation includes a standalone argument exactly equal to `skip-approval`, skip every (approval required) step without asking. Otherwise stop at every approval step, even when the invocation includes `skip-approval`, because some gates guard outward writes such as pushing a branch or opening a PR.
- When a subagent stops at its turn limit without its result, `SendMessage` that same subagent to return it now from what it gathered, marking what it did not check as unjudged. Don't spawn a fresh one, because it starts empty and stops at the same limit.

## Skill Authoring

Before creating a new skill, read `.claude/rules/skill-authoring.md`.

## Project Overview

- **Name**: YouEat (유잇). Code name and local folder: baplog
- **Description**: 한식 접시를 반찬별로 정확하고 일관되게 재는 사진 식단 기록 앱 (`docs/PRD/`)
- **Exposure**: <who can reach the app, e.g. internal admins only, public internet>
- **Architecture**: <e.g. SSR (Thymeleaf), API only, SPA + API>
- **Tech stack**: <language, framework, build tool, database, key libraries>

## Commands

- **Build and test**: <the full build and test command>
- **One test**: <how to run a single test class or file>

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

- **Base branch**: `main`. It is the only PR base for new work, and worktrees branch from `origin/<BASE_BRANCH>`. Skills bind this value as `<BASE_BRANCH>`.
- **Branch**: `<type>/<TASK_ID>-<description>` (types: feat, fix, refactor, chore, docs, test). Planning documents outside `docs/tasks/` (PRD, specs, IA) go on `docs/plan` without a `<TASK_ID>`.
- **Commit**: `<type>: <TASK_ID> <description>`
- **PR**: Use the `/pr` skill.
- **Force-push**: Get the user's explicit approval for every force-push. Before asking, show `git diff --stat origin/<branch>...HEAD` and `git log --oneline origin/<branch>..HEAD`. One approval covers one push.
- **Staging**: Stage explicit paths (`git add <path> ...`) rather than `git add -A` / `git add .` / `git add --all`. Before committing, check the staged file list.

## DB Migration (Flyway)

Before creating or changing a migration, read `.claude/rules/java-spring/flyway.md`. Delete this section when the project has no Flyway.

## Worktree Environment

A worktree (`.claude/worktrees/<TASK_ID>`) holds only tracked files. Before the first test run or boot in a worktree, copy every gitignored path listed below from the main checkout; none listed means nothing to copy.

- `<gitignored path>`: <which test or boot fails without it>
- Per-machine config overrides (e.g. `application-local.yml`): tests use the tracked `application-test.yml` and don't need them; a live boot in the worktree does.
- Relative paths in test config resolve against the Gradle module directory (test CWD), not the repo root.
