# Planning skills for Claude Code and Codex

This repository packages a set of collaborative planning skills for Claude Code and Codex. They help an agent investigate and challenge a plan, bring in evidence and alternatives, and keep consequential decisions with the user unless authority has already been delegated.

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
| `to-spec` | Turn a settled plan into a spec whose stories and decisions carry IDs and sources. |
| `to-tickets` | Split a spec into vertical-slice tickets whose acceptance criteria cite the spec IDs. |
| `ask-matt` | Router: which skill or flow fits your situation. |
| `setup-matt-pocock-skills` | Configure the issue tracker, triage labels, and doc layout. Required by `to-spec`, `to-tickets`, and `wayfinder`. |

Grilling numbers its decisions (D1, D2, ...) and asks them through the harness's question picker; `to-spec` keeps those numbers and `to-tickets` checks every one is covered. Without a configured issue tracker, `setup-matt-pocock-skills/issue-tracker-local.md` defines a local Markdown tracker. `ask-matt` also routes to skills outside this bundle (`implement`, `tdd`, `code-review` and others); install those separately if you want the full flow. The `grilling/turn-reminder.sh` hook is optional; it uses `sh` and `jq`, works as a `UserPromptSubmit` hook in both Claude Code and Codex, and the skills work without it.

## Use

Install the bundle into your user-level Claude Code skills directory. From this repository, back up any same-named skills before copying:

```sh
set -eu
claude_home=${1:-"$HOME/.claude"}
skills_dir="$claude_home/skills"
backup="$claude_home/skill-backups/planning-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$skills_dir" "$claude_home/skill-backups"
mkdir "$backup"
names="grilling grill-me grill-with-docs wayfinder research prototype domain-modeling to-spec to-tickets ask-matt setup-matt-pocock-skills"
for name in $names; do
  current="$skills_dir/$name"
  if [ -e "$current" ] || [ -L "$current" ]; then
    mv "$current" "$backup/$name"
  fi
done
for name in $names; do
  cp -R "skills/$name" "$skills_dir/$name"
done
```

The command accepts an optional Claude config directory as its first argument; pass a temporary directory to try the installation in isolation. The backup folder preserves prior directories and symlinks. Keep it until the new skills work in a fresh Claude Code session. To install only some skills, include their dependencies: `grill-with-docs` and `wayfinder` need `domain-modeling`; `to-spec`, `to-tickets` and `wayfinder` need `setup-matt-pocock-skills`.

For Codex, run the same command with `claude_home` set to `$HOME/.codex` (pass it as the first argument). Codex reads `skills/<name>/agents/openai.yaml` for display names.

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

For Codex, merge the same block into `~/.codex/hooks.json` with the command `sh "$HOME/.codex/skills/grilling/turn-reminder.sh"`, then approve the new hook when Codex asks (or under `/hooks`); Codex skips hooks it has not trusted.

The hook only reminds the agent to continue the decision loop while a planning skill is the latest one used; it goes quiet once `to-spec`, `to-tickets`, `implement`, `tdd` or `code-review` runs. Restart Claude Code or Codex after installation or settings changes.

## Attribution

Several skill files adapt material from Matt Pocock's `mattpocock/skills` repository. See [the bundled upstream notice](skills/UPSTREAM-NOTICES.md). No repository-wide license is declared here.
