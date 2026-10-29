import subprocess
import sys
from pathlib import Path

manager = Path(__file__).with_name("fex_upstreams.py")
for command in ("ensure", "verify"):
    result = subprocess.run([sys.executable, str(manager), command], capture_output=True, text=True, check=False)
    if result.returncode:
        print(f"FEX specialist setup failed during {command}: {result.stderr or result.stdout}. Retry by starting a new session.", file=sys.stderr)
        sys.exit(1)
