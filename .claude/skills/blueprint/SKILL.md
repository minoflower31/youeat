---
name: blueprint
description: "Personal task design workflow: read TASK file, ask the user the decisions its Requirements leave open, propose the design, run the multi-lens blueprint review (omission/complexity/feasibility), record the design in the task file for approval. Trigger on '태스크 설계해줘', 'design task', 'task design', 'blueprint'."
model: fable
effort: high
---

# Blueprint Task

Design the implementation for the given task from its Requirements. Don't write implementation code — design and analysis only. A design may show a signature or a one-line annotation where it states an interface more exactly than prose.

## Arguments
- Task ID: passed as the argument (referenced as `<TASK_ID>` below, e.g., TASK-123)

## Execution Rule

Besides approval steps, Step 2 waits only for the user's answers.

Checklist format:
- [ ] Step 1: Read Documentation
- [ ] Step 2: Analyze Requirements
- [ ] Step 3: Design Proposal
- [ ] Step 4: Blueprint Review
- [ ] Step 5: Output (approval required)

## Process

1. **Read Documentation**
   - Find task file with glob pattern `docs/tasks/<TASK_ID>*` and read it
   - Read documents listed in task file's `Depends on` section

2. **Analyze Requirements**
   - Ask the user, one question at a time, each product decision the task file does not settle: what a user sees and what is in scope. Don't ask technical choices (framework, mechanism, algorithm): Step 3 makes them and Step 5 shows them for approval.
   - Update `## Requirements` and `## Verification` with the answers per `.claude/rules/task-file.md` before Step 3, so the design and its reviewers work from them.

3. **Design Proposal**
   - Analyze existing code structure and affected components
   - Propose class/component structure, interfaces and data flow, required changes to existing code, new dependencies
   - When CLAUDE.md names files deployed separately from the build artifact and the design changes them, state why an alternative without that change is not taken
   - Verify: map every requirement item to a design element, confirm no omissions

4. **Blueprint Review**
   - Run the design review per `.claude/skills/workflow/references/reviewers.md`.
   - Give each reviewer a delegation message with the full design proposal text, the task file path, and the `## Requirements` list - a subagent starts empty.
   - Before triage, run the `probe` of each `unsettled` claim from the feasibility reviewer, and treat a claim the run contradicts as a finding. Don't run a probe that needs access outside the repo or an app boot; carry its claim to Step 5 as unconfirmed.
   - Dedupe across lenses, triage each finding valid/not-valid with a one-line justification, then apply every valid finding to the proposal. A technical limit accepted instead of fixed goes into `## Out of Scope`.
   - Don't triage reviewer `notes` or let them change the proposal. Record them per `.claude/rules/task-file.md` Out of Scope.

5. **Output** (approval required)
   - Check the final design as a document and fix every hit inline:
     - Placeholder: TBD, TODO, or a section with no content.
     - Contradiction or repetition: two places that disagree or say the same thing.
     - Ambiguity: a sentence a reader could take two ways. Pick one and state it.
     - Scope: an item that belongs in `## Out of Scope` or in another task.
   - Check the final design against every `## Requirements` and `## Verification` item, and fix the design where it contradicts one.
   - Write the design into the task file's `## Design`, and update `## Progress`, `## Requirements` and `## Verification` per `.claude/rules/task-file.md`, with `(승인 대기)` as the first line of `## Design`.
   - Present in Korean each decision line of the implementation notes, the rejected alternatives, each named with the decision it lost to, the `## Requirements` and `## Verification` items this run added, reworded or removed, each unconfirmed claim with its probe, and the task file path. Print the checklist and stop until the user approves.
   - On user approval: remove the `(승인 대기)` line. On a change request: revise the task file and present again.
   - Don't add a review-findings subsection or any per-finding record to the task file.
