"""
EXPERIMENT 6: The control experiment 3/4 don't run.
Self-referential depth (symlink chain pointing back to itself) vs
NON-self-referential depth (ordinary distinct nested directories,
same depth, same filesystem, same syscall) -- same N, same machine,
same run, interleaved to cancel drift.

This is the test that actually bears on the axiom. Exp3 shows self-ref
cost grows with depth -- true, but not yet evidence FOR self-reference,
because *any* deep stat() probably grows with depth too (more path
components to resolve, more inode lookups). This script isolates that.

Two possible outcomes:
  - slopes statistically indistinguishable -> 379ns/level is just
    "traversal costs time," no support for self-reference specifically.
  - self-ref slope is measurably steeper -> first real, non-tautological
    evidence that self-reference carries a premium beyond ordinary depth.

Run: python3 exp6_selfref_vs_plain_control.py
"""
import os, time, statistics, shutil, sys

N = 1000
MAX_DEPTH = 10
BASE = "/tmp/selfref_control"

def setup():
    shutil.rmtree(BASE, ignore_errors=True)
    os.makedirs(BASE)

    # --- Self-referential chain: symlink 'meaning' -> '.' , traverse meaning/meaning/... ---
    selfref_root = os.path.join(BASE, "selfref")
    os.makedirs(selfref_root)
    os.symlink(".", os.path.join(selfref_root, "meaning"))

    # --- Non-self-referential chain: REAL distinct nested directories, same depth ---
    plain_root = os.path.join(BASE, "plain")
    cur = plain_root
    os.makedirs(cur)
    for i in range(MAX_DEPTH):
        cur = os.path.join(cur, f"level{i}")
        os.makedirs(cur)

    # --- CRITICAL third condition: symlink chain, SAME mechanism as self-ref,
    # but each symlink points to a DIFFERENT sibling dir, never back to itself.
    # This isolates "symlink resolution overhead" from "self-reference overhead" --
    # the confound the two-condition version above doesn't control for. ---
    nonloop_root = os.path.join(BASE, "nonloop_symlink")
    os.makedirs(nonloop_root)
    for i in range(MAX_DEPTH):
        d = os.path.join(nonloop_root, f"target{i}")
        os.makedirs(d)
    # chain: hop0 -> target0/hop1 -> target1/hop2 -> ... each a real symlink,
    # same syscall mechanism as the self-ref case, but no target ever equals
    # an ancestor of itself.
    prev = nonloop_root
    for i in range(MAX_DEPTH):
        target = os.path.join(nonloop_root, f"target{i}")
        link = os.path.join(prev, f"hop{i}")
        os.symlink(target, link)
        prev = target

    return selfref_root, plain_root, nonloop_root

def selfref_path(root, depth):
    return root + "/meaning" * depth if depth > 0 else root

def plain_path(root, depth):
    p = root
    for i in range(depth):
        p = os.path.join(p, f"level{i}")
    return p

def nonloop_path(root, depth):
    p = root
    for i in range(depth):
        p = os.path.join(p, f"hop{i}")
    return p

def collect(path, runs=N):
    times = []
    for _ in range(runs):
        s = time.perf_counter_ns()
        os.stat(path)
        e = time.perf_counter_ns()
        times.append(e - s)
    return statistics.median(times), statistics.stdev(times)

def linreg(xs, ys):
    n = len(xs)
    sx, sy = sum(xs), sum(ys)
    sxy = sum(x*y for x, y in zip(xs, ys))
    sx2 = sum(x*x for x in xs)
    denom = n*sx2 - sx*sx
    slope = (n*sxy - sx*sy) / denom if denom else 0
    intercept = (sy - slope*sx) / n
    ym = sy / n
    ss_res = sum((y - (slope*x+intercept))**2 for x, y in zip(xs, ys))
    ss_tot = sum((y - ym)**2 for y in ys)
    r2 = 1 - ss_res/ss_tot if ss_tot else 0
    return slope, intercept, r2

def main():
    print("="*75)
    print(f"  SELF-REFERENTIAL vs PLAIN DEPTH, matched, interleaved, N={N}/depth")
    print("="*75)

    selfref_root, plain_root, nonloop_root = setup()

    depths = list(range(MAX_DEPTH + 1))

    selfref_meds, plain_meds, nonloop_meds = {}, {}, {}

    for d in depths:
        sm, ss = collect(selfref_path(selfref_root, d))
        pm, ps = collect(plain_path(plain_root, d))
        nm, ns = collect(nonloop_path(nonloop_root, d))
        selfref_meds[d] = sm; plain_meds[d] = pm; nonloop_meds[d] = nm
        print(f"  depth={d:>2d}   self-ref={sm:>8,.0f}ns   plain-dir={pm:>8,.0f}ns   "
              f"nonloop-symlink={nm:>8,.0f}ns")

    sr_slope, sr_int, sr_r2 = linreg(depths, [selfref_meds[d] for d in depths])
    pl_slope, pl_int, pl_r2 = linreg(depths, [plain_meds[d] for d in depths])
    nl_slope, nl_int, nl_r2 = linreg(depths, [nonloop_meds[d] for d in depths])

    print()
    print(f"  self-ref (symlink, loops):        C(n) = {sr_int:.0f} + {sr_slope:.0f}n ns   R²={sr_r2:.4f}")
    print(f"  plain directories (no symlink):   C(n) = {pl_int:.0f} + {pl_slope:.0f}n ns   R²={pl_r2:.4f}")
    print(f"  nonloop symlink (same mechanism): C(n) = {nl_int:.0f} + {nl_slope:.0f}n ns   R²={nl_r2:.4f}")
    print()

    confound_gap = nl_slope - pl_slope   # symlink mechanism cost, nothing to do with self-reference
    real_signal = sr_slope - nl_slope    # self-reference cost, WITH mechanism controlled for

    print(f"  Step 1 -- mechanism confound (nonloop symlink minus plain dir): {confound_gap:+.1f} ns/level")
    print(f"            This is what symlink resolution alone costs, no self-reference involved.")
    print(f"  Step 2 -- self-reference premium (self-ref minus nonloop symlink): {real_signal:+.1f} ns/level")
    print(f"            Positive = self-ref costs MORE than a non-looping symlink chain.")
    print(f"            Negative = self-ref costs LESS. Sign matters, not just magnitude.")
    print()
    threshold = max(abs(sr_slope), abs(nl_slope)) * 0.15
    if abs(real_signal) < threshold:
        print("  VERDICT: once symlink-mechanism cost is controlled for, self-ref and")
        print("  non-self-ref symlink chains cost about the same. The original")
        print("  self-ref-vs-plain-directory gap was mostly/entirely the mechanism")
        print("  confound, not self-reference. This does NOT support the axiom.")
    elif real_signal > 0:
        print("  VERDICT: even after controlling for the symlink mechanism, self-")
        print("  reference still costs measurably MORE per level than a non-looping")
        print("  symlink chain of the same depth. This is the first result in this")
        print("  whole line of work that isn't tautological -- still not proof of")
        print("  the axiom, but a real, specific, falsifiable data point FOR it.")
    else:
        print("  VERDICT: self-reference costs LESS than a non-looping symlink chain")
        print("  of the same depth, once the mechanism confound is removed. That is")
        print("  the OPPOSITE of what the axiom would predict if it implied a real")
        print("  physical premium for self-reference specifically. Plausible reason:")
        print("  looping to '.' may let the kernel reuse a cached dentry/inode for the")
        print("  SAME directory every hop, while the non-loop chain forces a fresh")
        print("  lookup into a genuinely different inode each time -- i.e. self-")
        print("  reference may be numerically CHEAPER here precisely because nothing")
        print("  new is being resolved, which is arguably closer to Def 1.1's own")
        print("  claim (sigma(t+1) indistinguishable from sigma(t)) than to Section V's")
        print("  reading of the symlink benchmark. Worth sitting with, not discarding.")

    shutil.rmtree(BASE, ignore_errors=True)
    print()
    print(f"  Platform: {os.uname().machine}, {os.cpu_count()} cores, {os.uname().sysname} {os.uname().release}")
    print(f"  Python: {sys.version.split()[0]}")
    print("="*75)

if __name__ == "__main__":
    main()
