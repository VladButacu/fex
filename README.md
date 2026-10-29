# FEX | Frontend Excellence

FEX is a plugin for Codex and Claude Code that routes frontend work to specialist skills. It inspects the project, selects guidance, and checks the result.

## Requirements

- Git
- Python 3.10+
- network access to GitHub on the first use of an uncached specialist
- the target project's frontend toolchain

FEX itself has no npm/pip dependencies.

## Installation

### One-prompt setup

Paste this into your coding agent and let it handle the rest:

```text
Install the FEX plugin from github.com/VladButacu/frontend-excellence and make sure its commands work in a new session.
```

### Claude Code

```text
/plugin marketplace add VladButacu/fex
/plugin install fex@frontend-excellence
```

### Codex

In your terminal, outside the Codex interactive prompt, run:

```bash
codex plugin marketplace add VladButacu/fex
codex plugin add fex@frontend-excellence
```

The first session after installation loads the FEX commands and prepares the pinned specialist cache automatically. No separate setup step exists.

## Usage

| Intent | Claude Code | Codex |
|---|---|---|
| Choose a mode automatically | `/fex:auto` | `$fex:auto` |
| Create or redesign a UI | `/fex:create` | `$fex:create` |
| Improve an existing UI | `/fex:improve` | `$fex:improve` |
| Review a UI without making changes | `/fex:review` | `$fex:review` |

## How FEX works

FEX inspects the project and selects one primary visual specialist:

| Task | Primary specialist |
|---|---|
| Marketing page | Taste |
| Product screen | UI/UX Pro Max |
| Isolated component | Anthropic Frontend Design |
| Standalone prototype | Anthropic Web Artifacts Builder, after visual direction is established |

FEX adds React, motion, and interface review guidance when relevant. It follows the project's existing design constraints and works on the static interface before adding decorative motion.

## Upstream skills

`plugins/fex/upstream.lock.json` pins specialist repositories to exact commits. When a specialist is first needed, FEX fetches its pinned revision into a local cache and verifies the checkout before reading the skill. Upstream files are not modified.

Manage the cache manually:

```bash
python3 plugins/fex/scripts/fex_upstreams.py doctor
python3 plugins/fex/scripts/fex_upstreams.py ensure
python3 plugins/fex/scripts/fex_upstreams.py verify
```

### Specialist projects

FEX uses these upstream projects:

| Project | Upstream repo | What FEX uses it for |
|---|---|---|
| [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | `nextlevelbuilder/ui-ux-pro-max-skill` | UI/UX, accessibility, responsive behavior, design systems, charts and stack guidance |
| [Taste Skill](https://github.com/Leonxlnx/taste-skill) | `Leonxlnx/taste-skill` | Art direction, anti-generic composition and visual inspection |
| [Anthropic Frontend Design](https://github.com/anthropics/skills/tree/main/skills/frontend-design) | `anthropics/skills` | Distinctive visual design for bounded frontend changes |
| [Anthropic Web Artifacts Builder](https://github.com/anthropics/skills/tree/main/skills/web-artifacts-builder) | `anthropics/skills` | Complex standalone interactive prototypes/artifacts |
| [Transitions.dev](https://github.com/Jakubantalik/transitions.dev) | `Jakubantalik/transitions.dev` | Semantic transitions and motion polish |
| [Vercel Agent Skills](https://github.com/vercel-labs/agent-skills) | `vercel-labs/agent-skills` | React/Next.js performance and final web-interface review |

## Development

### Local installation

From a local checkout, validate and load the plugin in Claude Code:

```bash
claude plugin validate ./plugins/fex
claude --plugin-dir ./plugins/fex
```

For Codex, add the repository root as a local marketplace with `codex plugin marketplace add ./` and install FEX from the plugin browser.

### Repository layout

```text
.agents/plugins/marketplace.json      Codex marketplace catalog
.claude-plugin/marketplace.json       Claude Code marketplace catalog
plugins/fex/
  plugin.json                         portable Agent Plugins identity
  .codex-plugin/plugin.json           Codex skills + listing overlay
  .claude-plugin/plugin.json          Claude Code plugin manifest + commands
  skills/                             Shared Claude and Codex entrypoints
  references/                         shared router/specialist/QA logic
  scripts/fex_upstreams.py            immutable upstream fetch + verification
  upstream.lock.json                  exact upstream pins
```

## Security and privacy

FEX runs within your coding agent and does not define an MCP server, collect telemetry, or require credentials. Its bootstrap script fetches public repositories at the commits listed in `upstream.lock.json`. Review the plugin and third-party licenses before using them in sensitive environments.

## License

FEX's original router, manifests, scripts, and documentation are MIT licensed. Third-party skills retain their upstream licenses and copyrights. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
