# PR Review Comment Format

The PR comment `workflow`'s Handle PR Outcome step posts in response to a review.

- Post it with `gh pr comment <PR> --body-file <file>`, because the shell guard rejects backticks or quotes in a heredoc.
- Write sentences in the tone `pr` Fill PR Template sets.

## Vocabulary

These words carry a fixed meaning. Don't invent synonyms in the comment.

**Severity** — what the finding costs if shipped.

| Term | Meaning |
|---|---|
| `Critical` | Data loss, security hole, or a broken path with no workaround. Blocks merge. |
| `Major` | Wrong behaviour on a reachable path, or a silent state corruption the user cannot undo. Fix before merge. |
| `Minor` | Real but survivable: redundancy, a narrow-window inconsistency, a convention break. Does not block. |

**Disposition** — what is done with the finding, from this closed set of two. Skills use the English term; comments show the Korean word.

| Term | Written as | Requires |
|---|---|---|
| `fixed` | `수정` | The commit sha on this PR's branch that fixed it. A sha that predates the review comment is still `fixed` — it means the reviewer saw a stale head; say so in the line. |
| `rejected` | `반려` | The evidence: the claim refuted (probe + result), OR real but no fix benefit (why), OR pre-existing code / out of this PR's scope (the separate ticket key when it deserves one). |

**Reviewer** — who found it. The tag is the reviewer's name: `Copilot` for the automated reviewer,
the GitHub login for a human.

Rules that bind these together:

1. Give every finding exactly one disposition. Don't drop one.
2. Every finding is `fixed`, whatever the severity, unless it is `rejected` with the evidence the
   table requires. Preference or "design intent" alone is not evidence. A fix that only adds a
   guard, an exception path, an abstraction or a test for a case that cannot happen has no fix
   benefit: `rejected`.
3. A finding with a `finding-verifier` verdict takes its disposition from the verdict:
   - `verified`: `fixed`.
   - `no-impact`: `fixed` when the fix changes no runtime behavior (a comment, doc string, log
     message or its arguments, a name); otherwise `rejected`, no fix benefit.
   - `contradicted`: `rejected`, refuted, with the verifier's evidence.
   - `pre-existing`: `rejected`, out of this PR's scope. Report it to the user as a separate-task
     candidate; don't record it as deferred.
   - `unsettled`: run its probe and decide from the result. Ask the user about a probe that needs
     access outside the repo or an app boot.
   - `abnormal`: `rejected`. Record it in the task file per `.claude/rules/task-file.md`
     Out of Scope.

   Overriding a verdict needs your own file:line or run output.
4. Leave out praise, restatements of what the code does, and summaries of the diff. The PR body owns that.
5. A second or later automated-review response lists new findings only. The header total counts
   them alone, the title carries the round number, and repeats appear only in the
   repeated-findings table, one row each with a link to the earlier disposition. Don't re-list or
   re-argue a repeated finding. A round with zero new findings posts no comment.
6. When a `rejected` finding is a design judgment, add it to the task file's rejected alternatives
   per `.claude/rules/task-file.md` Design. A later finding those lines already answer is
   `rejected` with that line as evidence.

## Skeleton

Group by severity, highest first. Omit an empty severity section. The `rejected` section is always the last
section — a rejected claim carries the claimant's severity, not ours, so it is not filed under one.

```markdown
## 리뷰 검토< (<k>차)> -- 총 <n>건 (수정 <n> / 반려 <n>)

| 항목 | 내용 |
|---|---|
| 검토 대상 커밋 | `<sha>` (이후 push: `<sha, ...>` 또는 없음) |
| 리뷰어 | <이름> (<n>건), <이름> (<n>건) |
| 반복된 리뷰 | <n>건 (아래 표 참고) |

| 반복된 리뷰 | 판정 | 근거 |
|---|---|---|
| <지적 한 줄> | 수정 또는 반려 | [<k>차 대응](<earlier comment URL>) |

### Critical (<n>)

- **[<리뷰어>] <리뷰어가 확인한 내용 한 줄>** `<file basename>:<line>`
  - 결함: <재현 조건과 결과까지, 한두 문장>
  - 수정: <무엇을 어떻게 했는지>. 테스트 `<test method>` (<sha>)

### Major (<n>)
### Minor (<n>)

### 반려 (<n>)

- **[<리뷰어>] <리뷰어가 확인한 내용 한 줄>** `<file basename>:<line>`
  - 주장: <한 줄, "~한다는 지적입니다"> (리뷰어 판정 <Severity>)
  - 반려 사유: <근거 — 반증 | 실익 없음 | 기존 코드·범위 밖(별도 태스크 <TASK_ID>)>

### 검증

- <검증 명령> 성공 -- <모듈 또는 스위트별 건수, 실패·오류 0>
- <사용자가 out-of-band 로 확인한 것이 있으면 그 줄>
```

Header rules:

- Put the counts only in the title, writing 0 for a disposition with no findings. Don't repeat them
  or an inline/suppressed split in the table.
- Reviewer row: every reviewer of this round with its finding count, comma-separated.
- Repeated-findings row: when it is 0, drop the repeated-findings table. Link each row of that table
  to the earlier disposition with a labelled link, because GitHub expands a bare comment URL into the
  PR title.

Finding rules:

- The bold head is the reviewer tag plus one line of what the reviewer checked, in the reviewer's
  terms, because the reader scans for the claim, not the path. The location follows outside the bold as
  basename:line. Don't use the full path or an inline/suppressed marker.
- One block per finding: the defect (or claim) line, then the disposition line. Evidence longer than one
  line is allowed only under the rejection reason, indented one level further and capped at a short table or a
  5-line code block — if the refutation needs more, it belongs in a reply.

Name what ran in the verification section, never a bare ratio. `4/4` alone does not say what ran.
Call out skipped tests with their reason. When `references/e2e.md` exists, add the line it names.

## No findings

No severity sections and no repeated-findings table. Drop the per-disposition counts from the title.
Keep one fact per row; don't pack commit, reviewer and counts into a single row, because the
one-line form is unreadable:

```markdown
## 리뷰 검토 -- 0건 (지적 없음)

| 항목 | 내용 |
|---|---|
| 검토 대상 커밋 | `<sha>` (이후 push: `<sha, ...>` 또는 없음) |
| 리뷰어 | <이름> (0건) |
```
