"""EXPERIMENT 10 - same topology, different target string.

Follow-up to exp9 (which closed H9: cycle length 1,2,3,4,inf all cost the
same per hop once symlink targets have equal component counts).

This script holds topology FIXED (all three arms are 1-cycles, f = id) and
varies only how the target is spelled:

  dot   hop -> "."          readlink + ~0 lookups
  rel   hop -> "../n0"      readlink + parent + 1 lookup
  abs   hop -> /a/b/c/n0    readlink + restart from / + 4 lookups

If per-hop cost tracks the target string's resolution work while topology
is constant, then the entire exp6/exp8 result family reduces to VFS path
arithmetic and says nothing about self-reference.

Result on Linux 6.18 x86_64 ext4 (2026-08-15):
  dot 144.0 ns/hop | rel 203.5 | abs 309.0
  gaps: rel-dot = 59.5 ns ~= 1.1 lookups; abs-dot = 165 ns ~= 3.2 lookups
  (per-lookup unit = 52 ns from the plain-nested-dir control in exp9)
  Cross-check vs exp8 originals: A_1cycle(".") 141.4, B_2cycle("../") 197.3
  -> exp8's +36.6%% "2-cycle premium" was dot-vs-dotdot, i.e. confound (1)
     of H9 in full. Working set contributed nothing (exp9: 2 inodes = 40).

Usage: python3 exp10_target_string.py [--reps 3000] [--maxdepth 12] [--rounds 5]
"""
import os, time, shutil, random, statistics, argparse, json, platform

ROOT = "/tmp/exp10_target"

def build(root):
    shutil.rmtree(root, ignore_errors=True)
    a = os.path.join(root, "dot", "n0"); os.makedirs(a)
    os.symlink(".", os.path.join(a, "hop"))
    b = os.path.join(root, "rel", "n0"); os.makedirs(b)
    os.symlink("../n0", os.path.join(b, "hop"))
    c = os.path.join(root, "abs", "n0"); os.makedirs(c)
    os.symlink(os.path.abspath(c), os.path.join(c, "hop"))
    return {"dot(.)": a, "rel(../n0)": b, "abs(4comp)": c}

def timed(path, reps):
    st, pc = os.stat, time.perf_counter_ns
    for _ in range(200): st(path)
    out = []
    for _ in range(reps):
        t0 = pc(); st(path); out.append(pc() - t0)
    return out

def slope(xs, ys):
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=3000)
    ap.add_argument("--maxdepth", type=int, default=12)
    ap.add_argument("--rounds", type=int, default=5)
    a = ap.parse_args()
    arms = build(ROOT)
    depths = list(range(a.maxdepth + 1))
    med = {k: {d: [] for d in depths} for k in arms}
    for _ in range(a.rounds):
        cells = [(k, d) for k in arms for d in depths]
        random.shuffle(cells)
        for k, d in cells:
            med[k][d].append(statistics.median(timed(os.path.join(arms[k], *(["hop"] * d)), a.reps)))
    slopes = {}
    for k in arms:
        ys = [statistics.median(med[k][d]) for d in depths]
        slopes[k] = slope(depths, ys)
        print("%-11s slope = %6.1f ns/hop" % (k, slopes[k]))
    print("\nAll three arms are the SAME topology (1-cycle, f=id).")
    print("If the slopes differ, cost is target-string resolution, not structure.")
    with open("exp10_results.json", "w") as f:
        json.dump({"platform": platform.platform(), "slopes": slopes}, f, indent=2)

if __name__ == "__main__":
    main()
