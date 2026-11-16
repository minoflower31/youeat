---
paths:
  - "**/db/migration/**"
  - "**/db/migration-external/**"
  - "**/resources/db/**/*.sql"
---

# Flyway Rule

## Why This Rule Exists

Migrations are authored in parallel git worktrees: one task per worktree, each session branching from the same base and integrating via separate PRs. Two sessions never see each other's migration files until merge time. Sequential `V<n>__` numbering therefore collides -- two worktrees both pick `V12__`, and the second PR to merge either fails checksum validation or silently shadows the first.

Every rule below exists to make independently authored migrations merge without coordination.

## Core Rules

1. **Timestamp version**: name new migrations `V<yyyyMMddHHmmss>__<description>.sql` (e.g., `V20260626143000__send_job_brand_snapshot.sql`). Don't use sequential `V12__`, `V13__` for new migrations. A timestamp is collision-free without cross-worktree coordination; a counter is not.
2. **Pre-existing sequential migrations stay as-is**. Don't renumber or rename an applied migration -- Flyway validates by checksum and a rename breaks every environment that already ran it.
3. **All vendors**: add every migration to every configured vendor directory with the same filename. Don't add to one vendor and defer the other -- the gap only surfaces on the environment that was skipped.
4. **Additive only across parallel work**: don't let a migration depend on, reorder, or modify another migration authored in a sibling worktree. Add columns and tables; do not restructure what a parallel session may be touching.
5. **Keep out-of-order execution enabled** (`spring.flyway.out-of-order=true`). Worktrees merge in an order unrelated to their timestamps, so a lower timestamp will routinely arrive after a higher one already ran. This setting is safe only while rule 4 holds.

## Authoring Checklist

Before committing a migration:

1. Filename matches `V<yyyyMMddHHmmss>__<description>.sql`.
2. The same filename exists under every vendor directory.
3. The migration is additive -- it does not reorder or depend on unmerged work.
4. No pre-existing migration file was renamed, renumbered, or edited in place.

## Project Configuration

| Item | Value |
|---|---|
| Vendor directories | <one directory per configured vendor, e.g. `db/migration/mysql/`, `db/migration/oracle/`> -- give all of them the same filename |
| Out-of-order setting location | `application.yml` (`spring.flyway.out-of-order=true`) |
| Pre-existing sequential range | <e.g. `V1`..`V11`, or none for a new project> -- exempt from rule 1, frozen by rule 2 |
