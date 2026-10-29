# FEX — Frontend Excellence

**Frontend Excellence (FEX)** is a plugin for coding agents that turns subjective frontend requests into a disciplined design-and-engineering pipeline. You can say “this looks generic,” “make this dashboard better,” or “review this UI”; FEX inspects the repository, chooses the appropriate specialist tools, makes routine frontend decisions itself, validates the result, and reports what changed.

You do **not** need to tell FEX which CSS framework, breakpoint strategy, animation library, component architecture, or rendering pattern to use. Existing repository/brand constraints remain authoritative.

## Callsigns

| Intent | Claude Code | Codex |
|---|---|---|
| Let FEX decide the mode | `/fex:auto` | `$fex-auto` |
| Build/redesign something new | `/fex:create` | `$fex-create` |
| Improve an existing UI | `/fex:improve` | `$fex-improve` |
| Audit without editing by default | `/fex:review` | `$fex-review` |

Examples:

```text
/fex:improve The homepage feels cheap and obviously AI-generated. Fix it.
```

```text
$fex-auto Improve this frontend substantially. Make the frontend decisions for me.
```

FEX routes marketing/public pages, product/app screens, isolated components, and standalone prototypes differently. It deliberately chooses **one primary visual authority** and uses other specialists only for bounded jobs, preventing five design skills from enthusiastically redesigning the same button in five different directions.

## Install from GitHub

### Claude Code

Add this repository as a marketplace, then install the `fex` plugin:

```text
/plugin marketplace add VladButacu/frontend-excellence
/plugin install fex@frontend-excellence
```

Start a new Claude Code session. The commands `/fex:auto`, `/fex:create`, `/fex:improve`, and `/fex:review` will be available.

### Codex

Add the repository as a plugin marketplace:

```bash
codex plugin marketplace add VladButacu/frontend-excellence
```

Then open Codex, run `/plugins`, select **FEX — Frontend Excellence**, and install it. Start a new chat before first use. The explicit skills are `$fex-auto`, `$fex-create`, `$fex-improve`, and `$fex-review`.

### Local development

Claude Code can validate/load the plugin directly:

```bash
claude plugin validate ./plugins/fex
claude --plugin-dir ./plugins/fex
```

For Codex, add the repository root as a local marketplace with `codex plugin marketplace add ./` and install FEX from the plugin browser.

## How FEX works

FEX first inspects the project: repository instructions, framework/runtime, styling/component system, design tokens, brand assets, neighboring screens, real content, tests/build commands, and available browser tooling. It then classifies the surface and chooses one primary design authority:

- marketing/public pages → Taste
- product/app screens → UI/UX Pro Max
- isolated visual components → Anthropic Frontend Design
- standalone prototypes → Anthropic Web Artifacts Builder for implementation, after visual direction is established

React/Next.js work additionally receives Vercel React Best Practices guidance. Interaction motion is added only after the static interface is strong, using Transitions.dev where relevant. Final review uses Vercel Web Design Guidelines plus FEX's responsive, accessibility, functional, and motion gates.

## Exact upstream content

FEX never paraphrases or silently forks its specialist skills. `plugins/fex/upstream.lock.json` pins every upstream repository to an exact 40-character Git commit. On first use, `plugins/fex/scripts/fex_upstreams.py` fetches only those immutable revisions into the plugin's persistent data/cache directory and verifies `HEAD` before FEX reads the specialist `SKILL.md`.

You can inspect the cache status manually:

```bash
python3 plugins/fex/scripts/fex_upstreams.py doctor
python3 plugins/fex/scripts/fex_upstreams.py ensure
python3 plugins/fex/scripts/fex_upstreams.py verify
```

No upstream skill file is modified by FEX. Upgrades are explicit changes to `upstream.lock.json`, reviewable in Git history.

## Upstream acknowledgements

FEX is possible because of excellent work from these projects. Please star, follow, and support them directly:

| Project | Upstream repo | What FEX uses it for |
|---|---|---|
| [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | `nextlevelbuilder/ui-ux-pro-max-skill` | UI/UX, accessibility, responsive behavior, design systems, charts and stack guidance |
| [Taste Skill](https://github.com/Leonxlnx/taste-skill) | `Leonxlnx/taste-skill` | Art direction, anti-generic composition and visual inspection |
| [Anthropic Skills — Frontend Design](https://github.com/anthropics/skills/tree/main/skills/frontend-design) | `anthropics/skills` | Distinctive visual design for bounded frontend changes |
| [Anthropic Skills — Web Artifacts Builder](https://github.com/anthropics/skills/tree/main/skills/web-artifacts-builder) | `anthropics/skills` | Complex standalone interactive prototypes/artifacts |
| [Transitions.dev](https://github.com/Jakubantalik/transitions.dev) | `Jakubantalik/transitions.dev` | Semantic transitions and motion polish |
| [Vercel Agent Skills](https://github.com/vercel-labs/agent-skills) | `vercel-labs/agent-skills` | React/Next.js performance and final web-interface review |

See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for exact pinned commits, licenses, copyright acknowledgements, and the distribution policy.

## Repository layout

```text
.agents/plugins/marketplace.json      Codex marketplace catalog
.claude-plugin/marketplace.json       Claude Code marketplace catalog
plugins/fex/
  plugin.json                         portable Agent Plugins identity
  .codex-plugin/plugin.json           Codex skills + listing overlay
  .claude-plugin/plugin.json          Claude Code plugin manifest + commands
  commands/                           /fex:* Claude Code entrypoints
  codex-skills/                       $fex-* Codex entrypoints
  references/                         shared router/specialist/QA logic
  scripts/fex_upstreams.py            immutable upstream fetch + verification
  upstream.lock.json                  exact upstream pins
```

## Design principles

FEX follows four rules: project/brand constraints outrank external taste; one specialist owns primary visual direction; static composition must work before decorative motion; and CREATE/IMPROVE work is not done merely because the build passes—material visual, responsive, accessibility, and engineering findings must be addressed first.

## Requirements

- Git
- Python 3.10+
- network access to GitHub on the first use of an uncached specialist
- whatever runtime/toolchain the target frontend already requires

FEX itself has no npm/pip dependencies.

## Security and privacy

FEX runs locally inside the coding agent and target repository. It does not define an MCP server, collect telemetry, or require credentials. Its upstream bootstrapper only invokes Git against the public repositories and immutable commits listed in `upstream.lock.json`. Review plugin code and third-party licenses before enabling it in sensitive environments, as you should with any coding-agent extension.

## License

FEX's original router, manifests, scripts, and documentation are MIT licensed. Third-party specialist skills retain their own upstream licenses and copyrights; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
