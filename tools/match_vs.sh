#!/bin/bash
# Play OUR bot against ANY other bot file, with the real judge.
#   ./tools/match_vs.sh path/to/their_agent.py [seed]
# The other bot must be a copy of the template (a file that starts a server on $PORT).
cd "$(dirname "$0")/.." || exit 1
source .venv/bin/activate
OTHER="$1"; SEED="${2:-1}"
[ -f "$OTHER" ] || { echo "File not found: $OTHER"; exit 1; }
OTHER_DIR="$(cd "$(dirname "$OTHER")" && pwd)"
PORT=5008 python agent.py > /tmp/ours.log 2>&1 & P1=$!
( cd "$OTHER_DIR" && PORT=5009 python "$(basename "$OTHER")" > /tmp/theirs.log 2>&1 ) & P2=$!
sleep 12
python judge_engine.py --agent1 5008 --agent2 5009 --seed "$SEED" 2>&1 | grep -E "agent1 =|agent2 =|bb/deal|Confidence|Faults|thinking|errors|RESULT|VERDICT"
kill $P1 $P2 2>/dev/null; pkill -f "PORT=5009" 2>/dev/null; lsof -ti:5008,5009 | xargs kill 2>/dev/null
echo "(logs: /tmp/ours.log and /tmp/theirs.log)"
