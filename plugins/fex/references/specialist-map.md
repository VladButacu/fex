# FEX specialist map

FEX uses upstream specialist skills verbatim. `upstream.lock.json` pins the repository, exact commit, and source path. Before reading a specialist, ensure it locally with the bundled upstream manager. Never rewrite cached upstream files.

## Resolve upstream paths

Use the plugin root for the active runtime. In Claude Code, `${CLAUDE_PLUGIN_ROOT}` is substituted in loaded plugin content. In Codex/plugin environments, prefer `${PLUGIN_ROOT}` when available. If neither is available, locate this plugin's `scripts/fex_upstreams.py` from the loaded FEX skill/command source. Do not ask the user for the path.

Run only the specialist(s) you need:

```bash
python3 "<FEX_PLUGIN_ROOT>/scripts/fex_upstreams.py" ensure <skill-id> [<skill-id> ...]
python3 "<FEX_PLUGIN_ROOT>/scripts/fex_upstreams.py" path <skill-id>
```

The manager fetches the exact Git commit and verifies `HEAD` before returning a path.

| Concern | Skill id | Role |
|---|---|---|
| Marketing/public art direction; anti-generic design; screenshot critique | `taste-skill` | Primary visual authority for public pages |
| UX, accessibility, responsive layout, forms, charts, design-system intelligence | `ui-ux-pro-max` | Primary for app screens; targeted specialist elsewhere |
| Compact visual doctrine for bounded component/section changes | `frontend-design` | Primary for isolated visual changes |
| Complex self-contained interactive artifact | `web-artifacts-builder` | Prototype-only; never dictate an existing production stack |
| Semantic UI transitions | `transitions-dev` | Motion implementation specialist |
| Timing/easing/distance/blur/scale refinement | `transitions-polish` | Motion QA/polish specialist |
| React/Next.js rendering and performance | `vercel-react-best-practices` | Engineering specialist for React/Next only |
| Final interface/accessibility/UX audit | `frontend-design-audit` | Final review specialist |

## Selection matrix

**Marketing/public page:** Taste is primary. Add UI/UX Pro Max only for targeted UX/accessibility/responsive concerns. Add React best practices when the repo is React/Next. Add transitions only after static design is strong. Finish with Frontend Design Audit.

**Product/app screen:** UI/UX Pro Max is primary. Taste may be used in app-screen mode when stronger identity is genuinely needed, but it must not override established product usability conventions. Add React guidance for React/Next. Add semantic motion only when useful. Finish with Frontend Design Audit.

**Isolated component:** Frontend Design is primary when visual judgment is required. Add UI/UX Pro Max for the exact interaction/accessibility issue. Add transition guidance only if the component state change benefits from motion.

**Standalone prototype:** Web Artifacts Builder is allowed when there is no production architecture to preserve. Establish visual direction first with Taste or UI/UX Pro Max depending on page vs app semantics.

Never load all specialists as a design committee. One owns the visual direction; the rest have bounded jobs.
