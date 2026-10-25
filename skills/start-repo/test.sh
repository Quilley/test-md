#!/bin/sh
# Tests for kit/.agents/hooks/upkeep. Usage: sh test.sh
set -u
skill=$(cd "$(dirname "$0")" && pwd -P)
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
export CLAUDE_CONFIG_DIR="$tmp/config"
fails=0

ok() { echo "ok   $1"; }
no() { echo "FAIL $1"; fails=$((fails + 1)); }
expect_empty() { [ -z "$2" ] && ok "$1" || { no "$1"; printf '%s\n' "$2" | sed 's/^/     /'; }; }
expect_has() { case $2 in *"$3"*) ok "$1" ;; *) no "$1"; printf '%s\n' "$2" | sed 's/^/     /' ;; esac; }
valid_json() { printf '%s' "$1" | python3 -I -c 'import json,sys; json.load(sys.stdin)' 2>/dev/null; }

repo="$tmp/repo"
mkdir -p "$repo" && cd "$repo" && git init -q
cp -Rn "$skill/kit/." "$repo/"
up() { sh "$repo/.agents/hooks/upkeep" "$@"; }

expect_has "fresh copy flags placeholders" "$(up check)" "AGENTS.md:1: unfilled placeholder"
sed -i.bak "s/{{purpose}}/A reading-list CLI./; s/{{date}}/$(date +%Y-%m-%d)/; s/{{model}}/claude-opus-5-5/" AGENTS.md && rm AGENTS.md.bak
expect_empty "filled kit is clean" "$(up check)"

# Each CLAUDE.md stays a shim for the AGENTS.md beside it; the skills are linked for Claude Code.
printf '\n## Agent skills\n' >>CLAUDE.md
expect_has "shim with content flagged" "$(up check)" "CLAUDE.md: has content beyond the @AGENTS.md import"
printf '<!-- Edit AGENTS.md. -->\n@AGENTS.md\n' >CLAUDE.md
expect_empty "restored shim is clean" "$(up check)"
[ -L .claude/skills/update-repo ] && [ -f .claude/skills/update-repo/SKILL.md ] && [ -f .claude/skills/audit-repo/SKILL.md ] &&
  ok "skill symlinks resolve" || no "skill symlinks resolve"
up check >/dev/null && ok "clean check exits 0" || no "clean check exits 0"

printf '\nCLI entry is `src/cli.py`; rebase on `origin/main`; specs go in `plan/work/`.\n' >>ship/AGENTS.md
out=$(up check)
expect_has "missing file path flagged" "$out" 'ship/AGENTS.md: `src/cli.py` doesn'
case $out in *origin/main* | *plan/work/*) no "branch names and folders are skipped" ;; *) ok "branch names and folders are skipped" ;; esac
up check >/dev/null && no "drift exits 1" || ok "drift exits 1"
mkdir -p ship/src && : >ship/src/cli.py
expect_empty "path relative to the file's folder resolves" "$(up check)"

# Places skills keep planning files in must be listed in plan/AGENTS.md.
mkdir -p .scratch/billing docs/adr && : >CONTEXT.md
out=$(up check)
for loc in .scratch docs/adr CONTEXT.md; do expect_has "unlisted $loc flagged" "$out" "doesn't list \`$loc\`"; done
printf '\n- `.scratch`: specs and tickets\n- `docs/adr`: decisions\n- `CONTEXT.md`: glossary\n' >>plan/AGENTS.md
expect_empty "listed places are clean" "$(up check)"

# Stop: drift reported once, as valid JSON; nothing while a stop hook is active.
echo '{}' | up start >/dev/null
rm ship/src/cli.py
out=$(echo '{"stop_hook_active":false}' | up stop)
expect_has "stop reports drift" "$out" 'src/cli.py'
valid_json "$out" && ok "stop output is valid JSON" || no "stop output is valid JSON"
expect_empty "same drift is reported once" "$(echo '{"stop_hook_active":false}' | up stop)"
echo 'Also `src/gone.py`.' >>ship/AGENTS.md
expect_empty "silent while stop_hook_active" "$(echo '{"stop_hook_active": true}' | up stop)"
expect_has "new drift is reported" "$(echo '{}' | up stop)" 'src/gone.py'
echo 'And `src/gone2.py`.' >>ship/AGENTS.md
out=$(echo '{}' | up stop codex)
expect_has "codex stop blocks with a reason" "$out" '"decision":"block"'
expect_has "codex stop names the drift" "$out" 'src/gone2.py'
valid_json "$out" && ok "codex stop output is valid JSON" || no "codex stop output is valid JSON"

# Auto memory: notes from before the first session are baseline; new feedback is reported once.
mem="$CLAUDE_CONFIG_DIR/projects/$(pwd -P | sed 's/[^A-Za-z0-9-]/-/g')/memory"
mkdir -p "$mem"
note() { printf -- '---\nname: %s\ndescription: %s\nmetadata:\n  type: %s\n---\n\nbody\n' "$2" "$3" "$4" >"$mem/$1"; }
rm -rf .git/agent-upkeep
note old.md old 'Use pnpm' feedback
echo '{}' | up start >/dev/null
case $(echo '{}' | up stop) in *'Use pnpm'*) no "baseline note not reported" ;; *) ok "baseline note not reported" ;; esac
note new.md new 'Run tests from ship/ with pytest -q' feedback
note role.md role 'User is a designer' user
out=$(echo '{}' | up stop)
expect_has "new feedback note reported" "$out" 'Run tests from ship/ with pytest -q'
case $out in *designer* | *'Use pnpm'*) no "only new feedback notes reported" ;; *) ok "only new feedback notes reported" ;; esac
valid_json "$out" && ok "memory nudge is valid JSON" || no "memory nudge is valid JSON"
expect_empty "feedback note reported once" "$(echo '{}' | up stop)"

# Start: review due on age or a new model generation, at most once a week.
expect_empty "fresh review, same generation: silent" "$(echo '{"model":"claude-sonnet-5-5"}' | up start)"
out=$(echo '{"model":"claude-opus-6"}' | up start)
expect_has "new generation: review due" "$out" "model generation changed"
valid_json "$out" && ok "start output is valid JSON" || no "start output is valid JSON"
expect_empty "review nudge once a week" "$(echo '{"model":"claude-opus-6"}' | up start)"
rm -rf .git/agent-upkeep
sed -i.bak "s/<!-- reviewed: [0-9-]* [^ ]* /<!-- reviewed: $(date +%Y-%m-%d) gpt-6.1-sol /" AGENTS.md && rm AGENTS.md.bak
expect_empty "another vendor's stamp is no generation change" "$(echo '{"model":"claude-opus-5-5"}' | up start)"
rm -rf .git/agent-upkeep
sed -i.bak 's/<!-- reviewed: [0-9-]* /<!-- reviewed: 2026-01-02 /' AGENTS.md && rm AGENTS.md.bak
expect_has "old review: review due" "$(echo '{"model":"claude-opus-5-5"}' | up start)" "days ago"

# Works from a subfolder and outside git.
expect_has "runs from a subfolder" "$(cd plan && sh ../.agents/hooks/upkeep check)" 'src/gone.py'
expect_empty "silent outside a git repo" "$(cd "$tmp" && echo '{}' | sh "$repo/.agents/hooks/upkeep" stop)"

[ "$fails" -eq 0 ] && echo "all passed" || { echo "$fails failed"; exit 1; }
