#!/usr/bin/env bash
# PreToolUse guard for Bash: enforces the CLAUDE.md Git Conventions that allow no exceptions.
# - git add -A / --all / .  -> denied; stage explicit paths instead.
# - git push --force / -f / --force-with-lease -> asks the user, once per push.
# Needs jq; without it the guard does nothing.

set -uo pipefail
command -v jq >/dev/null 2>&1 || exit 0

cmd=$(jq -r '.tool_input.command // empty' 2>/dev/null)
[ -z "$cmd" ] && exit 0

# Quoted text (commit messages, grep patterns) is replaced so it never matches.
flat="${cmd//$'\n'/ ; }"
s=$(printf '%s ' "$flat" | sed -E "s/'[^']*'/Q/g; s/\"[^\"]*\"/Q/g")

decide() {
  jq -n --arg d "$1" --arg r "$2" \
    '{hookSpecificOutput: {hookEventName: "PreToolUse", permissionDecision: $d, permissionDecisionReason: $r}}'
  exit 0
}

# Global options (-C <dir>, -c <k=v>, --no-pager ...) may come before the subcommand.
git_sub='git([[:space:]]+-[^[:space:]]+([[:space:]]+[^-[:space:]][^[:space:]]*)?)*[[:space:]]+'
args='([[:space:]]+[^;&|]*)?[[:space:]]'

# Short flags may be grouped (-Av, -uf); a +refspec and --mirror force-push too.
if printf '%s' "$s" | grep -Eq "${git_sub}add${args}(-[a-zA-Z]*A[a-zA-Z]*|--all|\.)([[:space:]]|$)"; then
  decide deny "Stage explicit paths (git add <path> ...) instead of git add -A / --all / ."
fi

if printf '%s' "$s" | grep -Eq "${git_sub}push${args}(-[a-zA-Z]*f[a-zA-Z]*|--force|--force-with-lease|--force-if-includes|--mirror|\+[^[:space:]]+)(=[^[:space:]]*)?([[:space:]]|$)"; then
  decide ask "Force-push needs the user's approval for this one push. Show git diff --stat origin/<branch>...HEAD and git log --oneline origin/<branch>..HEAD first."
fi

exit 0
