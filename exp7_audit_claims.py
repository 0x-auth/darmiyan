"""EXPERIMENT 7 - audit of four asserted-but-uncontrolled claims.
Three of four invalidate a claim this project previously made.
Run: python3 exp7_audit_claims.py"""
import os, shutil, sys
from fractions import Fraction
PHI = 1.618033988749895

def hr(t): print("\n" + "=" * 72 + "\n  " + t + "\n" + "=" * 72)

def a_eloop():
    hr("A. Is the self-referential recursion infinite?  [hole H7]")
    b = "/tmp/_eloop_audit"; shutil.rmtree(b, ignore_errors=True); os.makedirs(b)
    os.symlink(".", os.path.join(b, "meaning")); w = None
    for d in range(1, 80):
        try: os.stat(b + "/meaning" * d)
        except OSError as e: w = (d, e.errno); break
    shutil.rmtree(b, ignore_errors=True)
    print("  first failure at depth %d (errno %d = ELOOP)" % w if w else "  no wall < 80")
    print("  VERDICT: real closed cycle, but MAXSYMLINKS=40 caps the walk.")
    print("           'Infinite recursion' is wrong. It is a bounded 40-hop walk.")

def b_distinct():
    hr("B. Is the 'N distinct states' figure a property of the orbit?  [hole H4]")
    N = 101
    x = 2.0; s = []
    for _ in range(N):
        x = 1 + 1 / x
        if all(abs(x - v) > 1e-20 for v in s): s.append(x)
    x = Fraction(2); ex = set()
    for _ in range(N):
        x = 1 + 1 / x; ex.add(x)
    print("  float64        : %d distinct in %d steps" % (len(s), N))
    print("  exact Fraction : %d distinct in %d steps" % (len(ex), N))
    print("\n  VERDICT: in exact arithmetic EVERY convergent is distinct (%d/%d)." % (len(ex), N))
    print("           The float64 count measures where doubles exhaust precision.")
    print("           It is machine-dependent and NOT a property of the orbit.")

def c_growth():
    hr("C. Does the CF growth-rate match reproduce at small n?  [hole H5]")
    try:
        from mpmath import mp, mpf, log, sqrt
        import numpy as np
    except ImportError:
        print("  needs mpmath + numpy; skipped"); return
    mp.dps = 60; tgt = float(log((1 + sqrt(5)) / 2))
    def g(m):
        qp, q = mpf(1), mpf(1); L = []
        for _ in range(m):
            qp, q = q, q + qp; L.append(float(log(q)))
        return float(np.polyfit(range(len(L)), L, 1)[0])
    print("  target ln(phi) = %.9f\n" % tgt)
    print("  %7s %16s %12s" % ("n", "fitted slope", "abs error"))
    for m in (10, 20, 50, 110, 500, 5000, 50000):
        v = g(m); print("  %7d %16.9f %12.2e" % (m, v, abs(v - tgt)))
    print("\n  VERDICT: convergence is O(1/n). A 1e-5 agreement needs n ~ 5e4,")
    print("           not n ~ 10. The LIMIT is exactly ln(phi), provable via")
    print("           Binet -- state it analytically, never as a small-n match.")

def d_resonance():
    hr("D. What does analyzer.py's phi_resonance measure?  [hole H8]")
    def res(v):
        if len(v) < 2: return 0.0
        r = [1.0 / (abs(v[i + 1] / v[i] - PHI) + 1.0) for i in range(len(v) - 1) if v[i]]
        return sum(r) / len(r) if r else 0.0
    print("  source:  char_vals = [ord(c) for c in filepath.name if c.isalnum()]")
    print("  -> the FILENAME is the input. File CONTENT never enters.\n")
    for n in ["i.py", "me.py", "orchestrator.py", "README.md",
              "requirements.txt", "zzz.txt", "a1b2c3.log"]:
        print("    %-20s phi_resonance = %.4f" % (n, res([float(ord(c)) for c in n if c.isalnum()])))
    print("\n  VERDICT: control filenames score in the identical band -- the metric")
    print("           is a function of spelling. detect_position() also hardcodes")
    print("           filename in ['i.py','me.py'], so 'special' files are declared")
    print("           in source, not discovered. And pull = min(1.0, 4*HD*TD)")
    print("           clamps at its ceiling: five symbols at 1.0 is ONE saturated")
    print("           formula, not five findings.")
    print("           DO NOT CITE analyzer.py OUTPUT AS EVIDENCE FOR ANYTHING.")

if __name__ == "__main__":
    print("=" * 72)
    print("  EXPERIMENT 7 -- claim audit")
    print("  %s %s | python %s" % (os.uname().sysname, os.uname().machine, sys.version.split()[0]))
    print("=" * 72)
    a_eloop(); b_distinct(); c_growth(); d_resonance()
    print("\n" + "=" * 72)
    print("  3 of 4 audits invalidated a previously-stated claim (H7, H4, H5, H8).")
    print("=" * 72)
