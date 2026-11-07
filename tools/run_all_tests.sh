#!/bin/bash
# One command: runs every automatic check (about 5 minutes).
cd "$(dirname "$0")/.." || exit 1
source .venv/bin/activate
echo "=== 1/4 Unit tests ===";            python -m pytest -q 2>&1 | tail -2
echo "=== 2/4 Random-state fuzz test ==="; python tools/fuzz.py 2000
echo "=== 3/4 Slow-computer test ===";     echo '[["normal",{}],["8x slower",{"bank":1.0}]]' > /tmp/slow.json; python tools/sweep.py /tmp/slow.json 400 1,2 | cut -c1-70
echo "=== 4/4 All opponents (every number should be positive) ==="; python tools/pool.py '' 600 1,2
