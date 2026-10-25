# Planning and build skills for Claude Code

This repository packages a set of collaborative planning skills for Claude Code, and the build skills that carry a plan through to reviewed code. They help an agent investigate and challenge a plan, bring in evidence and alternatives, and keep consequential decisions with the user unless authority has already been delegated. A few supporting skills cover architecture, triage, teaching, HTML documents and repo setup.

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
| `implement` | Build a single ticket or small piece of work test-first, then review it. |
| `implement-spec` | Build a whole spec's tickets in parallel on one integration branch, then review it. |
| `tdd` | Red-green loop at the seams the spec agreed. |
| `code-review` | Review a diff against the repo's standards and against the spec's IDs. |
| `codebase-design` | Shared vocabulary for module depth and seams. Consulted by `tdd`. |
| `expert` | Add expert-level rigor to a specific task without changing its scope. |
| `first` | Explain the current discussion from first principles, with its assumptions and causal mechanism in plain language. |
| `recap` | Grow a project's story in Souvik's voice from everything since the last recap. Manual only. |
| `souvik` | Draft, rewrite, or critique writing in Souvik's voice, adapting to the audience and setting. |
| `setup-matt-pocock-skills` | Configure the issue tracker, triage labels, and doc layout. Required by `to-spec`, `to-tickets`, `implement-spec`, `code-review`, and `wayfinder`. |
| `triage` | Move issues and external PRs through triage roles, verify them, and write agent-ready briefs. Needs `setup-matt-pocock-skills`, `domain-modeling` and `grilling`. |
| `improve-codebase-architecture` | Find deepening opportunities in a codebase, present them as an HTML report, then grill through the one you pick. Needs `codebase-design`, `domain-modeling` and `grilling`. |
| `internal-html-design` | Apply Souvik's shared visual design to internal HTML documents when explicitly requested. Manual only. |
| `teach-bottom-up` | Teach a topic from its prerequisites, as a stepped page, a plain page, a Claude Doc, or chat. |
| `start-repo` | Set up a repo for Claude Code, Codex and other AGENTS.md tools, with plan and ship folders and the hooks that keep them current. |

Grilling numbers its decisions (D1, D2, ...) and asks them through the harness's question picker; `to-spec` keeps those numbers and `to-tickets` checks every one is covered. `implement-spec` stops a ticket rather than guessing when it hits an open item or a decision it cannot meet, records the answer in the spec, and `code-review` reports findings by ID. Without a configured issue tracker, `setup-matt-pocock-skills/issue-tracker-local.md` defines a local Markdown tracker. The `grilling/turn-reminder.sh` hook is optional; it uses `sh` and `jq`, requires a Claude Code `UserPromptSubmit` hook, and the skills work without it.

## Use

Install the bundle into your user-level Claude Code skills directory. From this repository, back up any same-named skills before copying:

```sh
set -eu
claude_home=${1:-"$HOME/.claude"}
skills_dir="$claude_home/skills"
backup="$claude_home/skill-backups/planning-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$skills_dir" "$claude_home/skill-backups"
mkdir "$backup"
names="grilling grill-me grill-with-docs wayfinder research prototype domain-modeling to-spec to-tickets implement implement-spec tdd code-review codebase-design expert recap setup-matt-pocock-skills first souvik triage improve-codebase-architecture internal-html-design teach-bottom-up start-repo"
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

The command accepts an optional Claude config directory as its first argument; pass a temporary directory to try the installation in isolation. The backup folder preserves prior directories and symlinks. Keep it until the new skills work in a fresh Claude Code session. To install only some skills, include their dependencies: `grill-with-docs` and `wayfinder` need `domain-modeling`; `to-spec`, `to-tickets`, `implement-spec`, `code-review` and `wayfinder` need `setup-matt-pocock-skills`; `implement` and `implement-spec` need `tdd` and `code-review`; `implement-spec` also needs `domain-modeling`. `triage` needs `setup-matt-pocock-skills`, `domain-modeling` and `grilling`; `improve-codebase-architecture` needs `codebase-design`, `domain-modeling` and `grilling`; `internal-html-design` draws on `souvik` for prose in Souvik's voice.

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

The hook only reminds Claude to continue the decision loop while a planning skill is the latest one used; it goes quiet once `to-spec`, `to-tickets`, `implement`, `implement-spec`, `tdd` or `code-review` runs. Restart Claude Code after installation or settings changes.

## Attribution

Several skill files adapt material from Matt Pocock's `mattpocock/skills` repository. See [the bundled upstream notice](skills/UPSTREAM-NOTICES.md). No repository-wide license is declared here.
