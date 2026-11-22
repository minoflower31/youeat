---
paths:
  - "**/docs/tasks/*.md"
---

# Task File Writing Rules

Owns the format of everything written into `docs/tasks/<TASK_ID>*.md`, by any skill or by hand, except the `## Run State` block owned by `workflow`.

## Skeleton

Create a task file with exactly these sections in this order. `(TBD)` marks a section not written yet; replace it, not append to it, when writing that section.

```markdown
# <TASK_ID>: <title>

## Depends on
- None

## Requirements
(TBD)

## Out of Scope
(TBD)

## Design
(TBD)

## Progress
(TBD)

## Verification
(TBD)
```

## Readability

Spell out a coined term in plain words; a technical term or a term the project already uses stays.

## Rewrites

When a later change (a fix, a review finding, a re-run) changes what a section says, rewrite that line in place. Don't append a record of the change.

## Sections

- **Requirements**: `planning` writes the first items and sets their bar. When a requirement is added, changed or removed, add, reword or remove only its items; leave every other item as it is. Write each item as one complete sentence ending in a verb that states what the feature does for its user in domain words; how it is exposed or built belongs in `## Design`.
- **Out of Scope**: `planning` writes the first items and sets their bar. Exclusions the user decides, technical limits found in design and reviewer `notes` are appended to `## Out of Scope`, each with its reason.
- **Design**: two subsections, in this order. Write it once, for the person who implements or reviews the task. A fact confirmed later goes where it belongs, and a sentence it proves wrong is corrected in place (see Rewrites).
  - **Implementation notes** subsection: keep a line only when, without it, that person would build a requirement differently or reopen a settled decision. That includes a constraint the code shows but does not explain: an input combination, an exception, a compatibility condition, a precondition.
    - Write each decision where it applies. Don't collect decisions or reasons in a section of their own.
    - Add a reason (`<decision>: <reason>`) only when the decision does not explain itself.
    - Leave out what the change itself will show: comment wording, sentences a document will carry, file or case counts. Keep a count that changes an alternative's cost or scope. Keep the user-facing text approved with the design (screen messages, tooltips, guide sentences), because the implementer gets it only from this file.
    - State something left unchanged only when someone would plausibly change it.
    - Write the observation a decision rests on, not how it was found.
    - Write a case table in two columns, the condition and the behavior after this task, only where a decision needs one to be understood. Don't add a before column.
    - Put how a result is checked in `## Verification` and what is excluded in `## Out of Scope`, not here.
  - **Rejected alternatives** subsection: one line each, `<alternative>: <reason>`, only for an alternative someone would plausibly propose again and whose reason the implementation notes don't already give. A review finding rejected as a design judgment goes here in the same form.
  - **Form**: at most two bullet levels. Each bullet is one fact, written as a terse Korean note that keeps its particles and ends in a nominalized verb (~함, ~됨, ~음). Don't write noun fragments or prose paragraphs. Don't use unmeasured qualifiers.
- **Claims** in `## Out of Scope` and `## Design`, rejected-alternative reasons included: end each sentence that states how the existing system or an outside party behaves with one label. Don't label what this task will build.
  - `(검증)`: a run in this task showed it (a live send, an executed command, a log). Name that run in the sentence.
  - `(추정)`: everything else, reading code included. Don't add a hedge word as well.
  - Before labeling a claim `(추정)`, run the check when a short run in the repo settles it.
  - End a decision the user made with `(사용자 결정)`.
- **Progress**: the design's implementation steps, one `- [ ]` per unit that can be built and tested on top of the steps before it, in build order. A step includes the tests it adds or changes, and stays one bullet even when it covers several changes to one component.
  - Check a step as soon as it is built and the tests it adds or changes pass; a step with no test of its own, as soon as it is built. Uncheck a step whenever its tests fail or a later check fails because of its change.
  - Put a later change into the step whose component it changes: reword it, and uncheck it if checked. Add a step only for a component no step covers, at the end or right before the first unchecked step that needs it. Drop an unchecked step no longer needed.
- **Verification**: `planning` writes the first items and sets their bar. When a requirement is added, changed or removed, add, reword or remove only the items that prove it; leave every other item as it is. Write each item as what it proves in domain words.
  - **Results** subsection, last in the section.
    - Passed items: a list with no heading, one bullet per verification item, without how it was checked.
    - Failed items (checked and found wrong) and unverified items (not checked, or needing the user's or reviewer's environment): one bullet each, `<item>: <reason>`, under a failed label line and an unverified label line. Leave out a label with no items.
    - The verification command in a `<details>` block, with the environments, cases and query steps a run used as comments.
