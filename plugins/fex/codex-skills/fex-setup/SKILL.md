---
name: fex-setup
description: Verify the Frontend Excellence plugin installation and prepare its exact-pinned third-party specialist cache. Use after installing/upgrading FEX or when an upstream specialist cannot be loaded.
---

Locate the installed FEX plugin root. Run `python3 <FEX_PLUGIN_ROOT>/scripts/fex_upstreams.py doctor`. If Git is available, run `python3 <FEX_PLUGIN_ROOT>/scripts/fex_upstreams.py ensure` followed by `verify`. Report the exact pinned specialist versions and any failure; do not modify upstream files.
