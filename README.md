# TwoStack: Heads-Up Short Deck 5-Card PLO Bot

A Python poker bot for the Datathon Poker Bot Challenge (bot name: `EquityBot`).

## How it works
- **Preflop:** looks up hand strength in a precomputed table (`data/preflop_eq.json`).
- **Flop / turn / river:** estimates win chance with a fast Monte Carlo simulation (`data/pt_table.npy`), then compares it to the pot odds to fold, call or raise.
- **Opponent model:** learns from showdowns how strong the opponent's bets are, and steals more from opponents who fold too often.
- **Safety:** adapts its simulation size to the time bank, and always returns a legal action.

## Files
| File | Purpose |
|---|---|
| `agent.py` | The bot (web server). Don't change the server part. |
| `bot_core.py` | The strategy. |
| `data/` | Lookup tables used by the bot. |
| `requirements.txt` | Python packages. |
| `game.py`, `evaluator.py`, `judge_engine.py` | Organizers' game rules, hand scorer and local referee. |

## Run and test
```
pip install -r requirements-dev.txt
python -m pytest -q            # checks the judge can talk to the bot
./tools/check_build.sh         # Docker build + smoke test (needs Docker running)
```

Play a local match (three terminals):
```
python agent.py                              # our bot, port 5008
python baseline-bots/baseline_random.py      # opponent, port 5009
python judge_engine.py --seed 1              # referee
```

## Submit
1. Push to the public GitHub repo.
2. Run `git rev-parse HEAD` to get the full 40-character commit ID.
3. Submit team name `TwoStack`, the repo URL and the commit ID in the form.
