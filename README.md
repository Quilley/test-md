# Planning skills for Claude Code

This repository packages a set of collaborative planning skills for Claude Code. They help an agent investigate and challenge a plan, bring in evidence and alternatives, and keep consequential decisions with the user unless authority has already been delegated.

## Skills

| Skill | Use it for |
| --- | --- |
| `grilling` | Collaborative judgment, assumption testing, and improving an idea or plan. |
| `grill-me` | Explicitly start a planning conversation using grilling. |
| `grill-with-docs` | Use grilling while updating domain language and recording decisions. |
| `wayfinder` | Carry interdependent planning decisions across sessions with a map and tickets. |
| `research` | Investigate a question and explain how its evidence affects a decision. |
| `prototype` | Explore a UI or state model to distinguish relevant possibilities. |
| `domain-modeling` | Sharpen project terms and record domain and architecture decisions. Required by `grill-with-docs` and `wayfinder`. |

`wayfinder` includes a local Markdown tracker reference. If a project already has an issue tracker, use its conventions instead. The `grilling/turn-reminder.sh` hook is optional; it uses `sh` and `jq` and requires a Claude Code `UserPromptSubmit` hook. The skills work without it.

## Use

Install the bundle into your user-level Claude Code skills directory. From this repository, back up any same-named skills before copying:

```sh
set -eu
claude_home=${1:-"$HOME/.claude"}
skills_dir="$claude_home/skills"
backup="$claude_home/skill-backups/planning-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$skills_dir" "$claude_home/skill-backups"
mkdir "$backup"
for name in grilling grill-me grill-with-docs wayfinder research prototype domain-modeling; do
  current="$skills_dir/$name"
  if [ -e "$current" ] || [ -L "$current" ]; then
    mv "$current" "$backup/$name"
  fi
done
for name in grilling grill-me grill-with-docs wayfinder research prototype domain-modeling; do
  cp -R "skills/$name" "$skills_dir/$name"
done
```

The command accepts an optional Claude config directory as its first argument; pass a temporary directory to try the installation in isolation. The backup folder preserves prior directories and symlinks. Keep it until the new skills work in a fresh Claude Code session. To install only some skills, include their dependencies: `grill-with-docs` and `wayfinder` need `domain-modeling`; `wayfinder` also needs the bundled tracker guide when using local Markdown.

To enable the optional reminder, first confirm `jq` is installed. Merge this hook into `~/.claude/settings.json`, preserving any existing hooks:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/skills/grilling/turn-reminder.sh"
          }
        ]
      }
    ]
  }
}
```

The hook only reminds Claude to continue the decision loop after a planning skill is used. Restart Claude Code after installation or settings changes.

## Attribution

Several skill files adapt material from Matt Pocock's `mattpocock/skills` repository. See [the bundled upstream notice](skills/UPSTREAM-NOTICES.md). No repository-wide license is declared here.
