"""EXPERIMENT 9 - closing hole H9 from exp8.

H9 had two untested confounds in the 1-cycle vs 2-cycle result (+36.6%):
  (1) ARM B used "../q" / "../p" -> parent traversal that ARM A never does.
  (2) Working-set size: 2-cycle touches 2 distinct inodes, 1-cycle touches 1.

Design: all cycle arms below use ABSOLUTE symlink targets. Absolute targets
restart resolution from / -- this adds a FIXED per-hop overhead that is
IDENTICAL across arms, so comparisons among them are fair, and no arm ever
does a ".." parent lookup.

  K1_abs   1-cycle   A/loop -> ABS(A)                      1 distinct inode
  K2_abs   2-cycle   p/x -> ABS(q), q/y -> ABS(p)          2 distinct inodes
  K3_abs   3-cycle   p->q->r->p                            3 distinct inodes
  K4_abs   4-cycle   p->q->r->s->p                         4 distinct inodes
  N_abs    non-loop  hop_i -> ABS(target_i), all distinct  n distinct inodes
  K2_rel   2-cycle   original "../" version                (parent confound arm)
  C_nested plain real dirs                                 baseline
  D_flat   no depth                                        drift control

Predictions:
  - CACHE/WORKING-SET hypothesis: per-hop slope rises monotonically with
    number of distinct inodes in the walk: K1 < K2 < K3 < K4 <= N_abs,
    saturating once the working set exceeds what stays hot.
  - TOPOLOGY hypothesis (identity vs involution physically distinct):
    K1 special; K2 == K3 == K4 (all "non-identity cycles" equivalent).
  - PARENT-TRAVERSAL confound: K2_rel minus K2_abs = cost of ".." per hop.
    NOTE: K2_rel resolves ~2 components/hop ("../q") while K2_abs resolves
    a full absolute path/hop, so this difference is indicative, not clean;
    the clean comparison is WITHIN the abs family.

Usage: python3 exp9_close_h9.py [--reps 3000] [--maxdepth 12] [--rounds 5]
"""
import os, sys, time, shutil, random, argparse, statistics, json, platform

ROOT = "/tmp/exp9_h9"

def build(root):
    shutil.rmtree(root, ignore_errors=True); os.makedirs(root)
    A = os.path.join(root, "K1", "n0"); os.makedirs(A)
    os.symlink(os.path.abspath(A), os.path.join(A, "hop"))

    def make_cycle(name, k):
        base = os.path.join(root, name)
        dirs = []
        for i in range(k):
            d = os.path.join(base, "n%d" % i); os.makedirs(d); dirs.append(d)
        for i in range(k):
            nxt = dirs[(i + 1) % k]
            os.symlink(os.path.abspath(nxt), os.path.join(dirs[i], "hop"))
        return base
    make_cycle("K2", 2); make_cycle("K3", 3); make_cycle("K4", 4)

    # non-loop absolute chain, 40 distinct targets
    nb = os.path.join(root, "N"); os.makedirs(nb)
    targets = []
    for i in range(40):
        d = os.path.join(nb, "t%d" % i); os.makedirs(d); targets.append(d)
    prev = nb
    for i in range(40):
        os.symlink(os.path.abspath(targets[i]), os.path.join(prev, "hop"))
        prev = targets[i]

    # original relative 2-cycle (parent-traversal arm)
    os.makedirs(os.path.join(root, "R2", "p")); os.makedirs(os.path.join(root, "R2", "q"))
    os.symlink("../q", os.path.join(root, "R2", "p", "x"))
    os.symlink("../p", os.path.join(root, "R2", "q", "y"))

    p = os.path.join(root, "C")
    for i in range(40): p = os.path.join(p, "d%d" % i)
    os.makedirs(p); os.makedirs(os.path.join(root, "D"))

def path_K1(r, d): return os.path.join(r, "K1", "n0", *(["hop"] * d))
def path_cycle(name):
    def f(r, d): return os.path.join(r, name, "n0", *(["hop"] * d))
    return f
def path_N(r, d): return os.path.join(r, "N", *(["hop"] * d))
def path_R2(r, d): return os.path.join(r, "R2", "p", *["x" if i % 2 == 0 else "y" for i in range(d)])
def path_C(r, d): return os.path.join(r, "C", *["d%d" % i for i in range(d)])
def path_D(r, d): return os.path.join(r, "D")

ARMS = {
    "K1_abs_1cyc": path_K1,
    "K2_abs_2cyc": path_cycle("K2"),
    "K3_abs_3cyc": path_cycle("K3"),
    "K4_abs_4cyc": path_cycle("K4"),
    "N_abs_chain": path_N,
    "K2_rel_2cyc": path_R2,
    "C_nested":    path_C,
    "D_flat":      path_D,
}

def timed(path, reps):
    st, pc = os.stat, time.perf_counter_ns
    for _ in range(200): st(path)
    out = []
    for _ in range(reps):
        t0 = pc(); st(path); out.append(pc() - t0)
    return out

def lsq(xs, ys):
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n
    den = sum((x - mx) ** 2 for x in xs)
    s = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / den
    icpt = my - s * mx
    ss_res = sum((y - (s * x + icpt)) ** 2 for x, y in zip(xs, ys))
    ss_tot = sum((y - my) ** 2 for y in ys)
    return s, icpt, (1 - ss_res / ss_tot if ss_tot > 0 else float("nan"))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=3000)
    ap.add_argument("--maxdepth", type=int, default=12)
    ap.add_argument("--rounds", type=int, default=5)
    a = ap.parse_args()

    build(ROOT)
    depths = list(range(a.maxdepth + 1))
    med = {arm: {d: [] for d in depths} for arm in ARMS}

    for rnd in range(a.rounds):
        cells = [(arm, d) for arm in ARMS for d in depths]
        random.shuffle(cells)
        for arm, d in cells:
            p = ARMS[arm](ROOT, d)
            med[arm][d].append(statistics.median(timed(p, a.reps)))
        print("round %d/%d done" % (rnd + 1, a.rounds), file=sys.stderr)

    print("=" * 78)
    print("  depth |" + "".join("%14s" % k for k in ARMS))
    print("=" * 78)
    table = {}
    for d in depths:
        row = []
        for arm in ARMS:
            m = statistics.median(med[arm][d]); row.append(m)
        table[d] = row
        print("  %5d |" % d + "".join("%12dns" % v for v in row))

    print("\n  SLOPES (ns/hop):")
    slopes = {}
    for i, arm in enumerate(ARMS):
        ys = [table[d][i] for d in depths]
        s, icpt, r2 = lsq(depths, ys)
        slopes[arm] = s
        print("  %-14s slope=%8.2f  intercept=%8.1f  R2=%.4f" % (arm, s, icpt, r2))

    k = [slopes["K1_abs_1cyc"], slopes["K2_abs_2cyc"], slopes["K3_abs_3cyc"], slopes["K4_abs_4cyc"]]
    print("\n  VERDICT")
    print("  cycle-length scan (abs targets): 1:%.1f  2:%.1f  3:%.1f  4:%.1f  chain(∞):%.1f"
          % (k[0], k[1], k[2], k[3], slopes["N_abs_chain"]))
    s_cl, _, r2_cl = lsq([1, 2, 3, 4], k)
    print("  linear fit of slope vs cycle length: %.2f ns/hop per extra inode, R2=%.4f" % (s_cl, r2_cl))
    if k[0] < k[1] < k[2] < k[3]:
        print("  -> MONOTONE in cycle length: consistent with WORKING-SET/CACHE, not topology.")
    elif abs(k[1] - k[2]) < 0.15 * k[1] and abs(k[2] - k[3]) < 0.15 * k[2] and k[0] < 0.85 * k[1]:
        print("  -> K2==K3==K4 but K1 distinct: consistent with a TOPOLOGY (identity-special) effect.")
    else:
        print("  -> pattern unclear; inspect numbers.")
    print("  parent-confound arm: K2_rel %.1f vs K2_abs %.1f (mechanisms differ; indicative only)"
          % (slopes["K2_rel_2cyc"], slopes["K2_abs_2cyc"]))
    print("  drift control D_flat slope = %.2f (should be ~0)" % slopes["D_flat"])

    out = {"platform": platform.platform(), "machine": platform.machine(),
           "python": platform.python_version(), "reps": a.reps, "rounds": a.rounds,
           "slopes": slopes, "table": {str(d): table[d] for d in depths},
           "arms_order": list(ARMS)}
    with open("exp9_results.json", "w") as f: json.dump(out, f, indent=2)
    print("  wrote exp9_results.json")

if __name__ == "__main__":
    main()
