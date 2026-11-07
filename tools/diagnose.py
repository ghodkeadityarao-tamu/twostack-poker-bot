"""Where does our bot win/lose chips? Buckets net chips by how the hand ended."""
import sys, os, collections
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); sys.path.insert(0, os.path.join(ROOT, "tools"))
import selfplay
from game import Game, make_deal, Action, Street

def run(opp, deals=1500, seed="7"):
    A = selfplay.Bot(selfplay.get("agent")); B = selfplay.Bot(selfplay.get("tools/opponents.py:" + opp))
    buckets = collections.defaultdict(lambda: [0, 0.0])
    for swap in (False, True):
        seats = (0, 1) if not swap else (1, 0)
        A.new_half(); B.new_half()
        by = {seats[0]: A, seats[1]: B}
        for i in range(deals):
            g = Game(make_deal(seed, i), button_seat=i % 2, hand_index=i)
            while not g.is_terminal:
                s = g.to_act; g.apply(by[s].act(g.observation(s)))
            for s, b in by.items(): b.end(g.hand_result(s))
            r = g.result(); me = seats[0]; net = r.nets[me]
            last = g.history[-1]
            if not r.went_to_showdown:
                key = ("we folded " if last.seat == me else "opp folded ") + last.street.name[:3]
            else:
                key = "showdown WIN" if net > 0 else ("showdown LOSS" if net < 0 else "split")
            # classify by pot size
            sz = "big(>40)" if r.pot > 40 else "small"
            buckets[(key, sz)][0] += 1; buckets[(key, sz)][1] += net / 2
    tot = sum(v[1] for v in buckets.values()) / (deals)
    print(f"--- vs {opp}: total {tot:+.2f} bb/deal")
    for k, (n, bb) in sorted(buckets.items()):
        print(f"   {k[0]:18s} {k[1]:9s} hands={n:5d}  net={bb/deals:+.2f} bb/deal")

for o in sys.argv[1:]:
    run(o)
