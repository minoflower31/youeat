---
name: spring-bootstrap
description: Spring Boot 프로젝트를 팀 표준으로 초기화하는 작업형 skill. API 전용/SSR용, DB 대상, Flyway, Querydsl을 먼저 결정하고 Spring Boot/Java/groupId/artifactId/packageName은 마지막에 확인한다. 프로젝트 초기화나 스캐폴딩에만 사용하며 TASK 구현 흐름이나 git 브랜치 전제를 요구하지 않는다. 현재 디렉터리에 git 저장소가 없으면 bootstrap 완료 후 초기 커밋까지 남긴다.
disable-model-invocation: true
---

# Spring Bootstrap

Spring Boot 프로젝트를 초기화한다. 이 skill은 부트스트랩 전용이다. Don't treat it as a TASK implementation flow or require git branch setup.

## Arguments
- Optional short bootstrap note supplied by the user
- `workingDirectory`: default `./`. Pass a subdirectory (e.g. `./server/`) when the repo holds more than the backend.

## Support Files

- `references/defaults.md`
  - 팀 표준 공통 기본값과 의존성 선택 규칙이 필요할 때 읽는다.
- `references/api-only.md`
  - `API 전용` 선택 시 읽는다. API 전용 기본 규칙과 산출물 예시가 들어 있다.
- `references/ssr.md`
  - `SSR용` 선택 시 읽는다. SSR 기본 규칙과 산출물 예시가 들어 있다.
- `examples/structures.md`
  - 공통 패키지 구조와 profile 파일 구조 예시가 필요할 때 읽는다.
- `examples/config-snippets.md`
  - `.env.example`, `.gitignore`, JPA, logging, Flyway, API bootstrap 예시가 필요할 때 읽는다.
- `examples/scripts.md`
  - `run.sh`(start/stop/status), Initializr 명령 형태와 metadata 조회 예시가 필요할 때 읽는다.
- `examples/verification.md`
  - 초기화 완료 후 무엇을 검증해야 하는지 체크리스트가 필요할 때 읽는다.

Read only the files needed for the current step. Do not bulk-load everything unless the task explicitly requires a full audit.

## Execution Rule

Checklist format:
- [ ] Step 1: Bootstrap 방향 결정 (approval required)
- [ ] Step 2: 데이터 접근 구성 결정 (approval required)
- [ ] Step 3: 프로젝트 메타데이터 확인 (approval required)
- [ ] Step 4: Spring Initializr 생성
- [ ] Step 5: 표준 구조 및 설정 보강
- [ ] Step 6: 검증
- [ ] Step 7: CLAUDE.md 반영
- [ ] Step 8: Git 초기화 및 첫 커밋
- [ ] Step 9: 결과 보고

## Decision Presentation Format

In every `(approval required)` step, collect all decisions via a single `AskUserQuestion` call.

- `question`: Korean, ends with `?`
- `header`: English, <=12 chars
- option `label` / `description`: Korean
- Use defaults from Spring Initializr or prior user choices when proposing values
- Don't proceed before the user answers

## Process

1. **Bootstrap 방향 결정** (approval required)
   - Ask whether the project should be `API 전용` or `SSR용`.
   - Read `references/defaults.md` before proposing defaults
   - Render the decisions using `Decision Presentation Format`
   - If `SSR용`:
     - Read `references/ssr.md`
     - Include `thymeleaf`
     - Create template/static bootstrap structure
   - If `API 전용`:
     - Read `references/api-only.md`
     - Exclude `thymeleaf` by default
     - Avoid view/template bootstrap artifacts unless the user explicitly asks otherwise
   - Print the checklist and stop until the user approves.

2. **데이터 접근 구성 결정** (approval required)
   - Ask the target DB vendor directly
     - Examples: `mysql`, `oracle`, `both`
   - Ask whether to include Flyway
   - Ask whether to include Querydsl
   - Read `references/defaults.md` before finalizing dependency choices
   - Render the decisions using `Decision Presentation Format`
   - If Flyway is enabled:
      - Add dependency and vendor-aware migration directory strategy
      - Enable `baseline-on-migrate`
   - If Querydsl is enabled:
     - Add build configuration and generated sources handling
   - Print the checklist and stop until the user approves.

3. **프로젝트 메타데이터 확인** (approval required)
   - Read `examples/scripts.md`
   - Fetch Spring Initializr metadata with `curl` from `https://start.spring.io/metadata/client`
   - From the metadata, load and propose available values and defaults for:
     - Spring Boot version
     - Java version
     - `packaging`
     - `language`
     - project type
     - default `groupId`, `artifactId`, `name`, `description`, `packageName`
   - Use fetched metadata values as the primary source of truth for selectable options
   - Present a recommended project metadata set based on:
     - the fetched defaults
     - previously selected architecture (`API 전용` or `SSR용`)
     - Flyway / Querydsl choices
   - Ask the user to confirm or override:
     - Spring Boot version
     - Java version
     - `groupId`
     - `artifactId`
     - `packageName`
     - `packaging`
     - project name / description
   - Distinguish clearly:
     - Initializr-provided options
     - bootstrap post-processing additions
   - Present a final summary of all selected options and defaults
   - Render the decisions using `Decision Presentation Format` (use a table when proposing 6+ metadata key-value pairs)
   - Print the checklist and stop until the user approves.

4. **Spring Initializr 생성**
   - Read `examples/scripts.md` and use the Initializr command shape as the base template
   - Create the project in `workingDirectory`, and run every later build and verification step there. Step 7 still edits the repository-root `CLAUDE.md`.
   - Download the base project from Spring Initializr using the approved metadata
   - Use `Gradle - Groovy`, `Java`, and `configurationFileFormat=yaml` unless the user explicitly requests otherwise
   - Rename `src/main/resources/application.yaml` to `application.yml` if generated
   - Delete generated helper files such as `HELP.md` if present
   - Include only the approved dependencies
   - Don't infer extra dependencies from habit or convenience

5. **표준 구조 및 설정 보강**
   - Read `examples/structures.md` and `examples/config-snippets.md`
   - Read `references/api-only.md` or `references/ssr.md` again if architecture-specific files/classes are being created
   - Add team-standard package structure under the base package
   - Don't create `.gitkeep`. Package structure lives in `CLAUDE.md`.
   - Add standard environment files and scripts as needed
     - `.env.example`
     - `.gitignore`
     - `run.sh` (subcommands: `start` / `stop` / `status`)
   - Add profile structure under `src/main/resources`
     - `application.yml`
     - `application-local.yml`
     - `application-stg.yml`
     - `application-prod.yml`
   - Add test profile structure under `src/test/resources`
     - `application-test.yml`
   - Add logging, datasource, JPA, and profile defaults according to approved options
   - Add test defaults
     - `@ActiveProfiles("test")`
     - H2 test runtime
   - Add JPA auditing bootstrap by default
   - If `bootJar` is used, set `jar { enabled = false }`
   - If DB vendor is `both`:
     - Design configuration keys so vendor switching is profile/environment driven
   - If `SSR용`:
     - Create `templates/{layout,fragments,error}` and `static/{css,js,images}`
     - Add view/error-page bootstrap structure
   - If `API 전용`:
     - Add `ApiResponse`, `ErrorCode`, `BusinessException`, and API exception handler skeleton
     - Don't add unused template artifacts
   - If Flyway is enabled:
     - Create migration directories consistent with the selected DB strategy
   - If Querydsl is enabled:
     - Configure generated source directories and related build hooks
   - Add only foundation-level code and files
   - Don't implement domain features beyond bootstrap scope

6. **검증**
   - Read `examples/verification.md`
   - Run the project build and tests using the existing project toolchain
   - Use the verification checklist as the minimum acceptance baseline
   - If verification fails:
     - Identify the concrete mismatch or broken step
     - Fix the bootstrap issue before reporting completion

7. **CLAUDE.md 반영**
   - Update `CLAUDE.md` after bootstrap completes
   - In `## Project Overview`, record:
     - project name / description
     - selected architecture (`API 전용` or `SSR용`)
     - tech stack
   - In `## Coding Conventions`, record only:
     - package structure: copy the tree in `examples/structures.md` verbatim as a fenced code block, substituting only the root package and application class name. Don't compress it (bullets, brace shorthand, prose).
   - Don't record facts derivable from project files (profile list, yml values, log paths, error page locations, etc.). Let future sessions read those from source.

8. **Git 초기화 및 첫 커밋**
   - When `workingDirectory` is not `./`, skip this step: the repo root already owns git init and its first commit.
   - If the current working directory is not already inside a git repository, initialize one with `git init`
   - If a git repository already exists, don't re-initialize it
   - After bootstrap files are created and CLAUDE.md is updated, stage the paths this skill created explicitly (`git add <path> ...`; the staging rule is owned by CLAUDE.md `Git Conventions`)
   - Create the first commit for the bootstrap result with `git commit -m "chore: initialize project"`

9. **결과 보고**
   - Report the bootstrap result in Korean
   - Summarize:
     - selected architecture (`API 전용` or `SSR용`)
     - selected DB vendor
     - Flyway / Querydsl inclusion
     - final Spring Boot / Java / package metadata
     - whether git was newly initialized or an existing repository was reused
   - List created or adjusted major files/directories
   - Mention any intentionally deferred items for later TASK work

## Notes

- This skill is independent from TASK design / implementation flow
- Don't require `git rev-parse`, `git pull`, `git checkout -b`, or main-branch checks
- Respond in Korean
