#!/bin/sh
# Keep the collaborative decision loop available while a planning skill is active.
# Works as a Claude Code UserPromptSubmit hook.
# Planning stays active until a build-phase skill runs after the latest planning skill.
input=$(cat)
transcript=$(printf '%s' "$input" | jq -r '.transcript_path // empty')
prompt=$(printf '%s' "$input" | jq -r '.prompt // empty')
skills='grilling|grill-me|grill-with-docs|wayfinder|to-spec|to-tickets|implement|implement-spec|tdd|code-review'

# Skill invocations in order, one name per line. Match actual Skill calls or typed
# commands, rather than mentions in tool output.
invoked() {
  if [ -f "$transcript" ]; then
    # A Skill tool call or a typed slash command.
    grep -oE '"name":"Skill","input":\{"skill":"[a-z-]+"|"content":"<command-message>[a-z-]+</command-message>' "$transcript" |
      sed -E 's/.*"skill":"([a-z-]+)"$/\1/; s/.*<command-message>([a-z-]+)<.*/\1/'
  fi
  # The current prompt may not be in the transcript yet.
  printf '%s\n' "$prompt" | grep -oE '^/[a-z-]+' | tr -d '/'
}

last=$(invoked | grep -xE "$skills" | tail -n 1)
echo "$last" | grep -qxE 'grilling|grill-me|grill-with-docs|wayfinder' || exit 0
jq -n '{hookSpecificOutput: {hookEventName: "UserPromptSubmit", additionalContext: "[grilling] Planning is active: follow grilling/SKILL.md for this turn (decision loop, own the gaps, decision cards for a cold reader through the question picker, IDs only as citations, AUTHORITY.md for adoption). Ignore this once planning has ended."}}'
