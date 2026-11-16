# Skill Authoring Patterns

Repo-specific patterns for `.claude/skills/<name>/SKILL.md`. `CLAUDE.md` holds the principles; this file holds the patterns that satisfy them. Read it before authoring or restructuring a procedure skill.

Every pattern below was extracted from a defect found in a real skill. Each names the skill it came from, so the fix can be read in context.

## 1. Bindings table

A skill that needs machine values (paths, ports, DB names, secrets) resolves them once in `## Arguments`, as a table of name -> where it comes from. The table holds the resolution, not a value.

- Every later reference uses the placeholder instead of re-deriving the value.
- Anchor a source path when the skill runs somewhere other than the main checkout.
- Found in `workflow`: `<SRC_DB>` said "read it from `application.yml` / `application-local.yml`" while the same file's CRITICAL RULES said that file is absent in the worktree, where every step runs. Two values were unresolvable and `<WORKTREE_ABS>` had no definition.

## 2. Enforcing a rule on a sub-skill

An orchestrator can't bind a sub-skill by declaring a rule in its own file, because the sub-skill never reads it.

- To change sub-skill behaviour, pass a literal argument and add the matching skip/branch condition to the sub-skill.
- Ship both edits together. The caller-side argument alone looks solved and does nothing.
- Precedent: `skip-approval`, which every sub-skill honours because each one declares it.
- Found in `workflow` Step 7: it forbade `fix` from writing the task file, but `fix` Step 4 writes it whenever the file exists. The caller-side rule alone bound nothing.

## 3. Splitting a step

When a step spans more than four distinct concerns, split it into lettered sub-blocks (`4a`, `4b`, ...) instead of growing the flat bullet list.

- Use sub-blocks rather than renumbered steps, because renumbering breaks every "per Step 4" cross-reference in the file.
- Write steps as `### Step N:` headings when numbering starts at 0, because a markdown formatter renumbers a list starting at `0.` into `1.` and shifts every "Step N" cross-reference.
- Make a branch (variant A vs variant B) a sub-block that names which later blocks run, not the first bullet of a flat list where everything after it reads as unconditional.
- Order the blocks in execution order, because agents follow prose order.
- Found in `workflow` Step 4: flat bullets placed "invoke `playwright`" above "boot the app", so top-down reading ran e2e against nothing.

## 4. Reasons

When a rule's purpose isn't obvious from the rule itself, add a short `because ...` clause to the same sentence. Keep the incident story in the commit message, not in a separate `Why:` line.

## 5. Claim vs evidence

A sub-skill's or subagent's report is a claim. The caller verifies it against the filesystem, git, or the API response before advancing.

- Caller and callee share a model, so a skipped step reports the same text as a completed one.
- Cheapest form: re-run the exact command the callee says it ran. A truly-passed gradle build returns up-to-date in seconds.
- Verify a state-changing call (a git push, a PR creation, a file write) against the end state, not against "the write returned".

## 6. Steps that end the run

Any step that performs several external writes assumes a resume can land mid-sequence.

- Each write applies only when its post-condition is unmet, and every skip is stated.
- A missing transition on an already-final entity is not a failure.
- Every terminating path has a cleanup step, not just the successful one. The abort path releases the same resources but proves readiness differently.
- Found in `workflow`: Step 7's completion branch double-posted on resume, and a PR closed unmerged had no path to cleanup at all (now Step 9).

## 7. Pointing at another file's step

A pointer that makes another file's step the owner of a rule names that step, not its number.

- `` `fix`'s Update Task File step ``, not `` `fix` Step 4 ``. Inside one file numbers stay: that file owns its numbering, and section 3 keeps it from being renumbered.
- Across files the number belongs to nobody. A project that drops a step renumbers the rest, every cross-file "Step N" then points at a different step, and the sentence still reads as valid, so nothing fails loudly.
- An incident record (`Found in ...`) may keep the number the step carried at the time. It is evidence of where a defect was, not a pointer a reader follows.
- Found porting `workflow/references/pr-review-comment.md` into a project with no e2e step: renumbered steps broke three pointers.
