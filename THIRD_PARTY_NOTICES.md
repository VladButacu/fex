# Third-party notices

Frontend Excellence (FEX) is an orchestration project. The specialist skills below are independent upstream projects; FEX does not claim authorship of them. FEX pins exact Git commits and fetches their original repositories at runtime. The cached upstream files are not rewritten by FEX.

| FEX id | Upstream project | Pinned commit | License | Use in FEX |
|---|---|---|---|---|
| `ui-ux-pro-max` | `nextlevelbuilder/ui-ux-pro-max-skill` | `28b3b8dee8c976df4fa3e94aed4e092ad43fcb03` | MIT © Next Level Builder | UI/UX, accessibility, responsive and design-system intelligence |
| `taste-skill` | `Leonxlnx/taste-skill` | `12af471f627f866411b4bd785b19646d3672784c` | MIT © Leonxlnx | Art direction and anti-generic visual design |
| `frontend-design` | `anthropics/skills` | `ca45fc496a3436251f191354091d557da31c15b5` | Apache-2.0 © Anthropic, PBC | Bounded frontend visual design doctrine |
| `web-artifacts-builder` | `anthropics/skills` | `ca45fc496a3436251f191354091d557da31c15b5` | Apache-2.0 © Anthropic, PBC | Standalone interactive artifact/prototype workflow |
| `transitions-dev` | `Jakubantalik/transitions.dev` | `6a7d68260d624eb66661cc3af17e0989476f48ae` | Transitions.dev License © Jakub Antalik | Semantic UI transition recipes |
| `transitions-polish` | `Jakubantalik/transitions.dev` | `6a7d68260d624eb66661cc3af17e0989476f48ae` | Transitions.dev License © Jakub Antalik | Motion timing/easing polish |
| `vercel-react-best-practices` | `vercel-labs/agent-skills` | `1a2c79d4e6c4a2283dc2c614b6538cbe1ed5ca62` | MIT © Vercel | React/Next.js performance and implementation guidance |
| `frontend-design-audit` | `mistyhx/frontend-design-audit` | `40c9a5f91a523dc152deb789033ef556ca8fd252` | MIT © mistyhx | Final usability/accessibility audit with severity-rated findings |

## Distribution policy

FEX intentionally does **not** republish these upstream skill directories inside this repository. Instead, `plugins/fex/scripts/fex_upstreams.py` fetches each repository from GitHub at the immutable commit listed in `plugins/fex/upstream.lock.json`, verifies the checked-out commit, and returns the original skill path.

This approach keeps attribution clear, guarantees that the specialist content is the exact pinned upstream content, and is especially important for Transitions.dev: its license permits installing and using its skills in coding agents but restricts redistribution of the transitions library itself as a competing library/motion pack.

Users remain responsible for complying with each upstream project's license. Upstream names and trademarks belong to their respective owners. FEX is not affiliated with, endorsed by, or sponsored by these upstream projects unless explicitly stated by them.
