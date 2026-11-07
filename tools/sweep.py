import sys, os, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); sys.path.insert(0, os.path.join(ROOT, "tools"))
import pool

if __name__ == "__main__":
    CASES = json.load(open(sys.argv[1]))
    deals = int(sys.argv[2]) if len(sys.argv) > 2 else 600
    seeds = tuple(sys.argv[3].split(",")) if len(sys.argv) > 3 else ("1", "2", "3")
    for name, over in CASES:
        out, res = pool.evaluate(over, deals, seeds)
        v = list(out.values()); strong = sum(out[k] for k in ("tight", "loose", "nit", "maniac")) / 4
        print(f"{name:20s} mean {sum(v)/len(v):+.3f} strong {strong:+.3f} min {min(v):+.2f} | " +
              " ".join(f"{k[:3]}{out[k]:+.1f}" for k in out), flush=True)
