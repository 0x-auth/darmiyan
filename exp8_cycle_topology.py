"""EXPERIMENT 8 - 1-cycle vs 2-cycle symlink traversal cost.

STATUS: NOT PUBLICATION-READY. See hole H9.
Two confounds remain untested:
  (1) ARM B uses "../q"/"../p" -> a parent traversal ARM A never performs.
      Re-run with sibling or absolute targets. If the gap collapses, the
      effect was parent-lookup, not cycle structure.
  (2) Working-set size. Build a 3-cycle. If cost scales with cycle length,
      it is cache footprint, not topology.
Current honest reading: the 2-cycle has a larger working set.
NOT yet "identity and involution are physically distinct."

ARMS
  A  1-cycle   A/loop -> .              f = id
  B  2-cycle   B/p/x -> ../q, q/y -> ../p    f o f = id
  C  control   real nested dirs, no symlinks
  D  flat      same dir, repeated (no depth)

METHOD  os.stat() in-process, no subprocess. Warmup discarded, median of N,
        arms interleaved and shuffled per round to cancel drift, depth swept
        so the result is a SLOPE (ns/hop) rather than a single point.

Usage: python3 exp8_cycle_topology.py [--reps 4000] [--maxdepth 12] [--rounds 7]
"""
import os, sys, time, shutil, random, argparse, statistics, json, platform

def build(root):
    shutil.rmtree(root, ignore_errors=True); os.makedirs(root)
    os.makedirs(root + "/A"); os.symlink(".", root + "/A/loop")
    os.makedirs(root + "/B/p"); os.makedirs(root + "/B/q")
    os.symlink("../q", root + "/B/p/x"); os.symlink("../p", root + "/B/q/y")
    p = root + "/C"
    for i in range(40): p = os.path.join(p, "d%d" % i)
    os.makedirs(p); os.makedirs(root + "/D")

def path_A(r, d): return os.path.join(r, "A", *(["loop"] * d))
def path_B(r, d): return os.path.join(r, "B", "p", *["x" if i % 2 == 0 else "y" for i in range(d)])
def path_C(r, d): return os.path.join(r, "C", *["d%d" % i for i in range(d)])
def path_D(r, d): return os.path.join(r, "D")

ARMS = {"A_1cycle": path_A, "B_2cycle": path_B, "C_nested": path_C, "D_flat": path_D}

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
    ap.add_argument("--reps", type=int, default=4000)
    ap.add_argument("--maxdepth", type=int, default=12)
    ap.add_argument("--rounds", type=int, default=7)
    ap.add_argument("--root", default="/tmp/exp8_cycle")
    a = ap.parse_args()

    build(a.root)
    depths = list(range(1, a.maxdepth + 1))
    acc = {arm: {d: [] for d in depths} for arm in ARMS}

    print("=" * 74)
    print("  EXPERIMENT 8 -- 1-CYCLE vs 2-CYCLE SYMLINK TRAVERSAL")
    print("  %s %s | python %s" % (platform.system(), platform.machine(), platform.python_version()))
    print("  reps=%d rounds=%d depths=1..%d" % (a.reps, a.rounds, a.maxdepth))
    print("=" * 74)

    order = [(arm, d) for arm in ARMS for d in depths]
    for r in range(a.rounds):
        random.shuffle(order)
        for arm, d in order:
            p = ARMS[arm](a.root, d)
            try: os.stat(p)
            except OSError: continue
            acc[arm][d].append(statistics.median(timed(p, a.reps)))
        print("  round %d/%d done" % (r + 1, a.rounds))

    print("\n" + "=" * 74)
    print("  %5s " % "depth" + "".join("%16s" % k for k in ARMS))
    print("=" * 74)
    res = {arm: {} for arm in ARMS}
    for d in depths:
        row = "  %5d " % d
        for arm in ARMS:
            v = acc[arm][d]
            if not v: row += "%16s" % "--"; continue
            m = statistics.median(v); res[arm][d] = m
            row += "%13.0f ns" % m
        print(row)

    print("\n" + "=" * 74)
    print("  SLOPE (ns per hop)")
    print("=" * 74)
    slopes = {}
    for arm in ARMS:
        ds = sorted(res[arm])
        if len(ds) < 3: continue
        s, icpt, r2 = lsq([float(x) for x in ds], [res[arm][x] for x in ds])
        slopes[arm] = (s, icpt, r2)
        print("  %-12s slope=%8.2f ns/hop   intercept=%8.1f ns   R2=%.4f" % (arm, s, icpt, r2))

    print("\n" + "=" * 74); print("  VERDICT"); print("=" * 74)
    if "A_1cycle" in slopes and "B_2cycle" in slopes:
        sa, sb = slopes["A_1cycle"][0], slopes["B_2cycle"][0]
        print("  1-cycle : %8.2f ns/hop" % sa)
        print("  2-cycle : %8.2f ns/hop" % sb)
        print("  delta   : %+8.2f ns/hop  (%+.1f%%)" % (sb - sa, 100 * (sb - sa) / sa))
        if abs(sb - sa) < 0.10 * sa:
            print("\n  => NO DISTINGUISHABLE DIFFERENCE (<10%).")
            print("     The kernel resolves by inode; loop topology is invisible to cost.")
        else:
            print("\n  => DIFFERENCE DETECTED. Do NOT read this as topology until the")
            print("     two confounds in the module docstring are controlled for.")
    if "D_flat" in slopes:
        print("\n  control D_flat (repetition, no depth): slope=%.2f R2=%.2f" % (slopes["D_flat"][0], slopes["D_flat"][2]))
        print("  -> should be ~0. If not, the other slopes are drift, not depth.")

    out = {"platform": platform.platform(), "python": platform.python_version(),
           "reps": a.reps, "rounds": a.rounds,
           "medians": {k: {str(d): v for d, v in res[k].items()} for k in res},
           "slopes": {k: {"ns_per_hop": v[0], "intercept": v[1], "r2": v[2]} for k, v in slopes.items()}}
    with open("exp8_results.json", "w") as f: json.dump(out, f, indent=2)
    print("\n  wrote exp8_results.json")
    shutil.rmtree(a.root, ignore_errors=True)

if __name__ == "__main__":
    main()
