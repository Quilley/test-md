#!/bin/sh
# Keep the collaborative decision loop available after a planning skill is loaded.
transcript=$(jq -r '.transcript_path // empty')
[ -f "$transcript" ] || exit 0
# Match actual Skill calls or typed commands, rather than mentions in tool output.
grep -qE '"name":"Skill","input":\{"skill":"(grilling|grill-me|grill-with-docs|wayfinder)"|"content":"<command-message>(grilling|grill-me|grill-with-docs|wayfinder)</command-message>' "$transcript" || exit 0
echo '[grilling] While planning remains active, apply the decision loop: ground, investigate, form a judgment, choose the next move. Contribute evidence, alternatives, and warranted challenges; ask when human judgment matters. Follow grilling/AUTHORITY.md for adoption and record updates. Distinguish proposals, authorized choices, and tested claims. When planning has ended, ignore this note.'
