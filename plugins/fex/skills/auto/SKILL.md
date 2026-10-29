---
name: auto
description: >-
  Autonomously route a frontend request to FEX create, improve, or review. Use when the user asks to build, redesign, polish, fix, audit, or make a frontend look better, especially when they do not want to make frontend implementation decisions.
---

FEX_MODE=AUTO

Run the Frontend Excellence workflow. Locate the installed FEX plugin root, read `references/router.md` and `references/specialist-map.md`, then execute the router for this request. Use the bundled `scripts/fex_upstreams.py` to fetch only the exact pinned upstream specialists needed. Inspect the repository before asking technical questions; make routine frontend implementation decisions yourself.
