#!/bin/sh
# Self-check for scripts/recap against a fake HOME, project, journals remote and transcripts. Prints "ok" or fails loudly.
set -eu
R=$(cd "$(dirname "$0")" && pwd)/recap
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
export HOME="$T/home" RECAP_HOME="$T/home/journals" RECAP_REMOTE="$T/remote.git"
export GIT_AUTHOR_EMAIL=t@example.com GIT_COMMITTER_EMAIL=t@example.com
mkdir -p "$HOME" "$T/proj"
git init -q --bare -b main "$T/remote.git"
cd "$T/proj"
git init -q -b main && git commit -q --allow-empty -m init
git remote add origin https://github.com/someone/proj.git
top=$(git rev-parse --show-toplevel)
cdir="$HOME/.claude/projects/$(printf %s "$top" | sed 's/[^A-Za-z0-9]/-/g')"
mkdir -p "$cdir" "$HOME/.codex/sessions/2026/10/15"

cat > "$cdir/aaaa1111-0000.jsonl" <<'EOF'
{"type":"user","sessionId":"aaaa1111","timestamp":"2026-10-15T10:00:00Z","message":{"content":"<command-name>/model</command-name><command-args></command-args>"}}
{"type":"user","sessionId":"aaaa1111","timestamp":"2026-10-15T10:01:00Z","message":{"content":"Should we gate on the Episodes?<system-reminder>noise</system-reminder>"}}
{"type":"assistant","sessionId":"aaaa1111","timestamp":"2026-10-15T10:01:05Z","message":{"content":[{"type":"text","text":"Let me check."},{"type":"tool_use","name":"Bash","input":{}}]}}
{"type":"user","sessionId":"aaaa1111","timestamp":"2026-10-15T10:01:06Z","message":{"content":[{"type":"tool_result","content":"TOOL OUTPUT"}]}}
{"type":"assistant","sessionId":"aaaa1111","timestamp":"2026-10-15T10:02:00Z","message":{"content":[{"type":"text","text":"Report them instead. Option B costs logging."}]}}
{"type":"user","sessionId":"aaaa1111","isSidechain":true,"timestamp":"2026-10-15T10:03:00Z","message":{"content":"SUBAGENT PROMPT"}}
{"type":"user","sessionId":"aaaa1111","timestamp":"2026-10-15T10:04:00Z","message":{"content":"<command-name>/grill-me</command-name><command-args>the pricing rule</command-args>"}}
EOF
cat > "$HOME/.codex/sessions/2026/10/15/rollout-2026-10-15T11-00-00-0199aaaa-bbbb-cccc-dddd-eeee12345678.jsonl" <<EOF
{"type":"session_meta","payload":{"cwd":"$top","source":"cli"}}
{"type":"response_item","timestamp":"2026-10-15T11:00:00Z","payload":{"type":"message","role":"user","content":[{"type":"input_text","text":"Codex question"}]}}
{"type":"response_item","timestamp":"2026-10-15T11:00:10Z","payload":{"type":"message","role":"assistant","content":[{"type":"output_text","text":"Codex answer"}]}}
EOF

"$R" setup | grep -q "check: nothing recap-related"
[ "$(git config recap.folder)" = proj ]
grep -q "Covered through: none" "$RECAP_HOME/proj/recap.md"
git -C "$T/remote.git" log --oneline main | grep -q "recap: start proj"

s=$("$R" sessions)
echo "$s" | grep -q "aaaa1111 claude"
echo "$s" | grep -q "12345678 codex"
echo "$s" | grep -q "^2 sessions"

out=$("$R" read aaaa 12345678)
echo "$out" | grep -q "Souvik: Should we gate on the Episodes?$"
echo "$out" | grep -q "Reply: Report them instead. Option B costs logging."
echo "$out" | grep -q "Souvik: /grill-me the pricing rule"
echo "$out" | grep -q "Reply: Codex answer"
if echo "$out" | grep -qE "/model|noise|TOOL OUTPUT|SUBAGENT|Let me check"; then echo "noise leaked"; exit 1; fi

RECAP_PART=60 "$R" read aaaa | grep -q "\[part 1 of"

echo "# Proj" >> "$RECAP_HOME/proj/recap.md"
"$R" commit "recap: first chapter" | grep -q pushed
grep -qE "Covered through: 20[0-9-]+T[0-9:]+Z" "$RECAP_HOME/proj/recap.md"
"$R" sessions | grep -q "^0 sessions"
[ "$(git -C "$RECAP_HOME" log -1 --format=%an)" = Roy ]

mkdir -p "$RECAP_HOME/proj/docs/x" && echo old > "$RECAP_HOME/proj/journal.md" && echo old > "$RECAP_HOME/proj/docs/x/questions.md"
git config journal.folder proj
"$R" retire | grep -q "removed 2 old journal files"
[ ! -e "$RECAP_HOME/proj/docs" ]
[ -e "$RECAP_HOME/proj/recap.md" ]
[ -z "$(git config journal.folder || true)" ]
[ -z "$(git status --porcelain)" ]
echo ok
