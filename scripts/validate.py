#!/usr/bin/env python3
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    for path in ROOT.rglob("*.json"):
        json.loads(path.read_text(encoding="utf-8"))
    subprocess.run([sys.executable, str(ROOT / "tests/test_bundle.py")], check=True)
    print("FEX repository validation: OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
