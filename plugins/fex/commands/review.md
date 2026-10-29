---
description: Audit a frontend with FEX and return prioritized evidence-based findings without editing by default.
argument-hint: [request]
---

FEX_MODE=REVIEW

Execute Frontend Excellence using the shared router at:
`${CLAUDE_PLUGIN_ROOT}/references/router.md`

Read that router first, then `${CLAUDE_PLUGIN_ROOT}/references/specialist-map.md`, and follow it for the user's request (`$ARGUMENTS`). Resolve and fetch only the pinned upstream specialist skills the router actually needs using `${CLAUDE_PLUGIN_ROOT}/scripts/fex_upstreams.py`. Do not ask the user frontend implementation questions that repository inspection can answer.
