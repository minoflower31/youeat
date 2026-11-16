---
name: workflow
description: "Takes one existing task file from design to merge in its own git worktree: design, implementation, verification, self-review, a PR, and cleanup after the merge. Use when the user gives a concrete task ID and asks to finish it end to end (e.g. '<TASK_ID> 처리해줘', '<TASK_ID> 끝까지', '<TASK_ID> 끝내줘')."
---

# Task End-to-End

Run one task per session. Respond in Korean.

## Invariants

- Do all code and task file work inside the worktree. Keep `<MAIN_CHECKOUT>` on `<BASE_BRANCH>`.
- Anchor every build/test/git command to an absolute path in the same invocation (`git -C <ABS>`, `./gradlew -p <ABS>`, `cd <ABS> && ...`), because a session reset drops the CWD back to `<MAIN_CHECKOUT>`.
- Give every subagent delegation (reviewers, `finding-verifier`) `<WORKTREE_ABS>` as the root its file paths resolve against, because a subagent opening a relative path from `<MAIN_CHECKOUT>` reads the base branch, not this task's code.
- Commit task file edits (a design draft, a revision, an approval) with the next code commit on the feature branch, not on their own.
- Run `fix` in a `general-purpose` subagent (Agent tool), because its code reads and build output would otherwise stay in this context through every later step. Pass its frontmatter `model` and `effort` on the Agent call, because a subagent otherwise inherits this session's model. The delegation message says:
  - follow `<MAIN_CHECKOUT>/.claude/skills/fix/SKILL.md` with the arguments the step gives, and read the `.claude/` files it names (agents, rules) from `<MAIN_CHECKOUT>`, because they can be untracked and absent from the worktree,
  - run every command from `<WORKTREE_ABS>` (`cd <WORKTREE_ABS> && ...`), because the subagent's shell starts in `<MAIN_CHECKOUT>`,
  - when the skill asks the user something or reaches an approval step, end the run with that question or approval request instead of deciding it; the user's answer resumes the run,
  - return the changed files, the exact verification command it ran with its result when the skill runs one, and any step it stopped at with the reason.
- Run `fix` inline instead, following its SKILL.md in this session, when the fix changes no design decision and edits only files this session has already read, because a subagent starts empty and re-reads the skill, rules and files at a cost larger than the edit itself.
- When that subagent ends with a question or an approval request, show it to the user and `SendMessage` the user's answer to that same subagent. Don't spawn a new one, because it starts empty.
- When that subagent returns a step it stopped at, report the reason to the user and stop.

## Arguments

| Name | Source |
|---|---|
| `<TASK_ID>` | The task ID of an existing `docs/tasks/<TASK_ID>-<description>.md`. |
| `<MAIN_CHECKOUT>` | `cd "$(git rev-parse --git-common-dir)/.." && pwd` |
| `<WORKTREE_ABS>` | `<MAIN_CHECKOUT>/.claude/worktrees/<TASK_ID>` |
| `<BASE_BRANCH>` | CLAUDE.md Git Conventions |

## Execution Rule

- Verify each sub-skill's outcome against the filesystem, git, or the API response before advancing, because a skipped step reports the same text as a completed one.
- Don't merge the branch yourself (`git merge` or squash-merge into `<BASE_BRANCH>`, `gh pr merge`). The user merges the PR.

Checklist format:

- [ ] Step 0: Create Worktree
- [ ] Step 1: Start Task
- [ ] Step 2: Design (approval required)
- [ ] Step 3: Implement
- [ ] Step 4: Runtime Verification
- [ ] Step 5: Self-Review
- [ ] Step 6: Create PR
- [ ] Step 7: Handle PR Outcome
- [ ] Step 8: Cleanup Worktree (merged path)
- [ ] Step 9: Abort Cleanup (no merge)
- [ ] Step 10: Report

### Run State

- Persist the checklist marking to a `## Run State` block at the top of the task file, above the title, because it is the only orchestration state that survives the session.
- Update `Step` at every step boundary up to PR creation, then leave the block as is. It merges into `<BASE_BRANCH>` as run history.
- Record only `Step`, because branch and PR have their own sources (`git`, `gh pr view`) and a copy goes stale.

```markdown
<!-- workflow orchestrator state; drives resume. Frozen at PR creation; after merge this is history, not live state. -->
- Step: 3 (Implement) / in_progress
```

## Process

### Step 0: Create Worktree

Check for this task's worktree with `git -C <MAIN_CHECKOUT> worktree list`, and look up its branch on origin:
```bash
git -C <MAIN_CHECKOUT> ls-remote --heads origin '*/<TASK_ID>-*' | grep -v -E '/<TASK_ID>-[0-9]+-' | sed 's#.*refs/heads/##'
```
When the lookup returns more than one branch, stop and ask the user which one belongs to this run. Otherwise follow the block that matches.

**0a. No worktree and no branch (new run)**
- Find the task file at `<MAIN_CHECKOUT>/docs/tasks/<TASK_ID>-*.md`. When none exists, stop and suggest `/planning`.
- Name the branch per CLAUDE.md Git Conventions: `<description>` from the task file name, `<type>` `fix` when the task's Requirements correct a defect, otherwise the type that fits (`feat` for new behavior).
- Fetch origin, then create the worktree at `<WORKTREE_ABS>` on that new branch from `origin/<BASE_BRANCH>`.
- Copy the gitignored files CLAUDE.md `## Worktree Environment` lists into the worktree with `cp -n`.

**0b. Worktree exists (resume)**
- Resume at whichever is later: the Run State `Step`, or the step the environment shows.
  - An open or merged PR (`gh pr view <branch>`) shows Step 7.
  - Commits or changes against `origin/<BASE_BRANCH>` (`git -C <WORKTREE_ABS> log` / `diff`) show Step 3 or later.

**0c. No worktree, but the branch exists**
- Check the branch's PR with `gh pr list --state all --head <branch> --json number,state`.
- If the PR is merged, go to Step 7c without recreating the worktree.
- If the PR is open or there is no PR, recreate the worktree at `<WORKTREE_ABS>` from the existing branch, copy the gitignored files as in 0a, and resume as in 0b.

### Step 1: Start Task

- Bring the task file into the worktree from the first place it exists:
  - If `<WORKTREE_ABS>/docs/tasks/<TASK_ID>-*.md` exists, use it.
  - If `<MAIN_CHECKOUT>/docs/tasks/<TASK_ID>-*.md` exists untracked, move it into `<WORKTREE_ABS>/docs/tasks/`.
  - If `<MAIN_CHECKOUT>/docs/tasks/<TASK_ID>-*.md` is tracked, the worktree already has it from `origin/<BASE_BRANCH>`.
- Verify that `<WORKTREE_ABS>/docs/tasks/<TASK_ID>-*.md` matches exactly one file.

### Step 2: Design (approval required)

- Invoke `blueprint` with `<TASK_ID>`.

### Step 3: Implement

- Invoke `impl` with `<TASK_ID> skip-approval`.
- Re-run the exact command `impl` reports having run, without `--rerun-tasks`. It has to pass.
- That command is the verification command later steps re-run. Record its results in `## Verification`.

### Step 4: Runtime Verification

- When `references/e2e.md` exists, run this step as it says.

### Step 5: Self-Review

- Build one delegation message with the diff, the changed-file list and the task file path (its Requirements and Design come from Step 2), because reviewers have no Bash and start with an empty context.
  - For a diff of about 2,000 lines or more, write it to files split into main and test code and pass their paths instead.
- Run the code review per `references/reviewers.md`.

- Check each reviewer's output before using it:
  - When it reports `input_mismatch` (the diff disagreed with the working tree), fix the input and re-run it.
  - When its verdict has an empty `read_beyond_diff`, re-run it naming the files it has to read.
- Dedupe the findings across reviewers. Spawn `finding-verifier` (Agent tool) once with the bug and security findings (id, file:line, summary and failure or attack), the diff path and the task file path.
- Decide each finding's disposition per `references/pr-review-comment.md`, with a one-line reason, and assign final severity (meanings in the same file).
  - Fix the findings to be `fixed` with `fix` and `skip-approval` in a subagent, per Invariants.
- After any fix, re-run the verification command and whatever `references/e2e.md` requires and rewrite the task file's verification results from the outcome, or state why the fix is design-time-only.

### Step 6: Create PR

- Make the last commit before the PR carry the final Run State `Step: 6 / done`.
- Commit and push the self-review fixes, then invoke `pr` with `skip-approval` (base `<BASE_BRANCH>`, head `<type>/<TASK_ID>-<description>`).
- Don't post the self-review as a PR comment.
- Don't request the automated review yourself, because GitHub already requests it on every push and a second request starts another fix round.
- Report in one message, in this order, even when every test passed:
  - the PR URL,
  - a short summary of the self-review: what was `fixed` and what was `rejected`, one line each,
  - anything the user is expected to verify out-of-band, stated as such,
  - decisions the implementation or self-review made beyond the approved design,
  - anything the user must decide before merging.
- Start one background watch for the automated review and the merge without asking, and tell the user neither needs relaying.
  - Use the `Monitor` tool with `persistent: true` (load it via ToolSearch), not a Bash `run_in_background` loop, which gets reaped mid-watch.
  - Poll and act on whichever signal lands first:
    - When `copilot-pull-request-reviewer[bot]` posts a new review (the `gh api repos/<owner>/<repo>/pulls/<PR>/reviews` count grew), go to Step 7a.
    - When `gh pr view <PR> --json state,mergedAt` shows the PR merged, run Step 7c and Step 8 without asking, then notify.
    - When the PR is closed unmerged, ask the user whether the task is abandoned. If it is, run Step 9. Either way, stop.
- When the PR conflicts with `<BASE_BRANCH>`, merge `origin/<BASE_BRANCH>` into the feature branch in the worktree, rebuild (`./gradlew -p <WORKTREE_ABS> build`), and push normally.

### Step 7: Handle PR Outcome

Check the PR state, then follow the block that matches:
```bash
gh pr view <PR> --json state,reviewDecision,mergedAt,mergeCommit
```
An automated review lands as `COMMENTED` with its findings in inline comments, so judge whether it left comments from the inline comments, not from `reviewDecision` or the review body.

**7a. Review comments present** (`reviewDecision` is `CHANGES_REQUESTED`, the user relays comments, or an automated reviewer left comments)
1. Fetch the reviews and inline comments. An automated review's body also holds findings in a collapsed "Suppressed comments" list.
   ```bash
   gh pr view <PR> --json reviews,comments
   gh api repos/<owner>/<repo>/pulls/<PR>/comments
   ```
2. For an automated review, drop each finding that an earlier response comment on this PR already dispositioned, matching by file and claim substance.
3. Spawn `finding-verifier` (Agent tool) once with the remaining findings (id, file:line, claim), the PR diff path and the task file path. Decide each disposition from its verdict per `references/pr-review-comment.md`, with a one-line reason. If a comment is ambiguous or you disagree with a human reviewer, ask the user first.
4. Run `fix` with `skip-approval` in a subagent, per Invariants, passing the comments to fix as `<FIX_DESC>`.
5. Apply `references/e2e.md`'s rule for review fixes, when that file exists.
6. Commit and push to the same branch with `git -C <WORKTREE_ABS> push`.
7. Report the triage to the user and as a PR comment, following `references/pr-review-comment.md`.

**7b. Not merged, no changes requested**
- Report that the PR awaits review or merge, and stop.

**7c. Merged**
- Check that the merged base builds in the main checkout:
  ```bash
  git -C <MAIN_CHECKOUT> pull --ff-only origin <BASE_BRANCH>
  ./gradlew -p <MAIN_CHECKOUT> build -x test
  ```
  - If `<MAIN_CHECKOUT>` is not on `<BASE_BRANCH>` or the pull refuses, report and stop without touching it.
  - If the build fails, report and stop.

### Step 8: Cleanup Worktree (merged path)

- When `references/e2e.md` exists, tear down the live instance as it says.
- Check that the task file is in `origin/<BASE_BRANCH>`. If it is not, commit and push the late edits and open a follow-up PR before removing anything.
- Remove the worktree. If it is already gone (0c), there is nothing to remove.

### Step 9: Abort Cleanup (no merge)

- Enter this step when the user abandons the task.
- When `references/e2e.md` exists, tear down the live instance as in Step 8.
- Check that the worktree has no uncommitted changes and no commits missing from its upstream. If it has either, commit and push to the branch first. If the branch has no upstream, it was never pushed; stop and ask the user.
- Remove the worktree.
- Leave the remote branch in place. Don't delete it unprompted, because it is outward-facing.

### Step 10: Report

Report the run's outcome:

- the PR URL and whether it merged,
- when merged, the post-merge build result,
- on the Step 9 path, what was torn down and that the remote branch was left to the user.
