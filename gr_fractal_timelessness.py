"""
GR, fractals, and timelessness — the computations behind the 25 Jul 2026 session.

Five self-contained parts. Run the whole file, or run one function at a time.
No external data — every number here is derived from first principles in-script.
"""

import cmath
import math

import numpy as np


# ============================================================
# PART 1 — Schwarzschild: coordinate (horizon) vs curvature (r=0) singularity
# ============================================================
def part1_horizon_vs_singularity(M=1.0, G=1.0, c=1.0):
    """
    g_tt = -(1 - r_s/r)  blows up at r = r_s  -> looks singular, but it's a
    coordinate artifact (removable by switching to Kruskal coordinates).

    The Kretschmann scalar K = R_{abcd}R^{abcd} = 48 G^2 M^2 / (c^4 r^6) is the
    thing that's actually invariant under coordinate choice. It stays FINITE
    at r=r_s and only blows up at r=0.
    """
    r_s = 2 * G * M / c**2
    print("=== Part 1: Horizon (coordinate) vs r=0 (curvature) singularity ===")
    print(f"Schwarzschild radius r_s = {r_s}")
    for r in [5 * r_s, 2 * r_s, 1.01 * r_s, r_s, 0.5 * r_s, 0.01 * r_s]:
        K = 48 * G**2 * M**2 / (c**4 * r**6) if r != 0 else float("inf")
        g_tt_factor = 1 - r_s / r if r != 0 else float("-inf")
        proper_time_factor = math.sqrt(max(g_tt_factor, 0)) if g_tt_factor >= 0 else float("nan")
        print(
            f"  r = {r:8.4f}  |  dτ/dt = sqrt(1-r_s/r) = {proper_time_factor!s:>8}  "
            f"|  Kretschmann K = {K:.6g}"
        )
    print("  -> dτ/dt -> 0 at r_s (coordinate effect: infalling clock looks frozen")
    print("     to a distant observer), but K stays FINITE there: no real curvature")
    print("     catastrophe at the horizon. K only diverges at r=0 -- the true,")
    print("     frame-independent singularity.\n")


# ============================================================
# PART 2 — Julia set for c = -0.123: fixed points, multiplier, connectivity
# ============================================================
def part2_julia_fixed_points(c=-0.123):
    """
    f(z) = z^2 + c.  Fixed points solve z^2 - z + c = 0.
    Multiplier |f'(z)| = |2z| classifies each fixed point as attracting/repelling.
    If the ATTRACTING fixed point has |mu| < 1, c lies in the main cardioid of
    the Mandelbrot set, and the Julia set is connected (a quasicircle).
    """
    print(f"=== Part 2: Julia set fixed points for c = {c} ===")
    d = cmath.sqrt(1 - 4 * c)
    z1, z2 = (1 + d) / 2, (1 - d) / 2
    for z in (z1, z2):
        mult = abs(2 * z)
        kind = "ATTRACTING" if mult < 1 else "REPELLING" if mult > 1 else "NEUTRAL (parabolic)"
        print(f"  fixed point z = {z.real:+.6f}{z.imag:+.6f}i   |f'(z)| = {mult:.6f}  -> {kind}")
    mu = 2 * z2 if abs(2 * z2) < abs(2 * z1) else 2 * z1
    print(f"  attracting multiplier mu = {mu.real:+.6f}{mu.imag:+.6f}i, |mu| = {abs(mu):.6f}")
    print(f"  |mu| < 1  =>  inside main cardioid  =>  Julia set is CONNECTED\n")


def render_julia(c, path, W=700, H=700, xr=(-1.8, 1.8), yr=(-1.8, 1.8), maxit=200):
    """Escape-time render of the filled Julia set for f(z)=z^2+c. Requires Pillow."""
    from PIL import Image

    x = np.linspace(*xr, W)
    y = np.linspace(*yr, H)
    Z = (x[None, :] + 1j * y[:, None]).astype(np.complex128)
    esc = np.zeros(Z.shape, dtype=float)
    alive = np.ones(Z.shape, dtype=bool)
    for i in range(maxit):
        Z[alive] = Z[alive] ** 2 + c
        escaped_now = alive & (np.abs(Z) > 2)
        esc[escaped_now] = i + 1
        alive &= ~escaped_now
    t = esc / max(esc.max(), 1)
    img = np.zeros((H, W, 3), np.uint8)
    ext = ~alive
    img[..., 0] = (9 + 246 * t).astype(np.uint8) * ext
    img[..., 1] = (20 + 120 * t).astype(np.uint8) * ext
    img[..., 2] = (60 + 150 * np.sqrt(np.clip(t, 0, 1))).astype(np.uint8) * ext
    img[alive] = [14, 10, 30]
    Image.fromarray(img).save(path)
    print(f"  saved render -> {path}  (interior fraction = {alive.mean():.4f})")


# ============================================================
# PART 3 — Bifurcation: the quasicircle pinching at |mu|=1
# ============================================================
def part3_bifurcation_multipliers():
    """
    As c moves from -0.123 down to -2 along the real axis, the attracting
    fixed point's multiplier |2z| rises from well under 1 to exactly 1 (at
    c=-0.75, the parabolic/period-doubling point where the boundary pinches)
    and on to 2 (at c=-2, where the filled Julia set degenerates to the
    segment [-2,2]).
    """
    print("=== Part 3: Bifurcation of the attracting multiplier ===")
    for c in [-0.123, -0.5, -0.75, -1.0, -1.25, -2.0]:
        d = cmath.sqrt(1 - 4 * c)
        z2 = (1 - d) / 2
        mu = abs(2 * z2)
        note = "  <-- PARABOLIC PINCH" if abs(c + 0.75) < 1e-9 else (
            "  <-- degenerates to a line segment" if abs(c + 2.0) < 1e-9 else ""
        )
        print(f"  c = {c:+.3f}   |attracting multiplier| = {mu:.4f}{note}")
    print()


# ============================================================
# PART 4 — Phi's three-distance gaps (self-similar split ratio)
# ============================================================
def part4_phi_three_gaps():
    """
    Steinhaus three-distance theorem: placing {k*alpha mod 1} for k=1..n always
    leaves at most 3 distinct gap lengths, for ANY irrational alpha. For
    alpha = phi (all-1s continued fraction), the ratio between consecutive
    gap lengths is exactly phi, at EVERY n -- because every gap-split uses the
    same ratio, forced by phi^2 = phi + 1.
    """
    phi = (1 + math.sqrt(5)) / 2
    alpha = phi % 1
    print(f"=== Part 4: Three-distance gaps for alpha = {{phi}} = {alpha:.10f} ===")

    def three_gaps(a, n):
        pts = sorted((k * a) % 1 for k in range(1, n + 1))
        gaps = [(pts[(i + 1) % len(pts)] - pts[i]) % 1 for i in range(len(pts))]
        return sorted(set(round(g, 10) for g in gaps))

    for n in [3, 5, 8, 13, 21, 34, 55, 89]:  # Fibonacci n's, on purpose
        u = three_gaps(alpha, n)
        ratios = [round(u[i + 1] / u[i], 6) for i in range(len(u) - 1)]
        print(f"  n={n:>3}  gaps={[round(x, 6) for x in u]}  ratios={ratios}")
    print(f"  phi = {phi:.6f}  -- every ratio above should equal this, exactly.\n")


# ============================================================
# PART 5 — BKL / Mixmaster: the Gauss map and phi as its fixed point
# ============================================================
def kasner_exponents(u):
    p1 = -u / (1 + u + u * u)
    p2 = (1 + u) / (1 + u + u * u)
    p3 = u * (1 + u) / (1 + u + u * u)
    return p1, p2, p3


def gauss_map_step(u):
    """BKL parameter map: subtract 1 while u>=1 (counts 'eras'), then flip 1/u."""
    eras = 0
    while u >= 1:
        u -= 1
        eras += 1
    if u == 0:
        return None, eras
    return 1 / u, eras


def part5_bkl_gauss_map():
    """
    Near a cosmological singularity, spacetime passes through a chaotic
    sequence of Kasner epochs (BKL/Mixmaster). The epoch-to-epoch map is the
    Gauss map u -> 1/{u}, i.e. the continued-fraction shift.

    phi is the map's period-1 fixed point (all-1s continued fraction): a
    universe whose BKL parameter equals phi bounces through IDENTICAL Kasner
    epochs forever -- perfectly self-similar. A generic irrational (e.g. pi)
    produces a chaotic, unpredictable sequence of era-counts instead.
    """
    phi = (1 + math.sqrt(5)) / 2
    print("=== Part 5: BKL/Mixmaster Gauss map -- phi as the non-chaotic fixed point ===")

    def eras_sequence(u, n):
        seq = []
        for _ in range(n):
            u, e = gauss_map_step(u)
            seq.append(e)
            if u is None:
                break
        return seq

    for label, u0 in [("phi (period-1)", phi), ("sqrt(2)+1 (period-2)", math.sqrt(2) + 1), ("pi (chaotic)", math.pi)]:
        seq = eras_sequence(u0, 12)
        print(f"  {label:22s}  u0={u0:.8f}   era-sequence = {seq}")
    p1, p2, p3 = kasner_exponents(phi)
    print(f"\n  Kasner exponents at u=phi: ({p1:.5f}, {p2:.5f}, {p3:.5f})")
    print(f"  check: sum p_i = {p1+p2+p3:.5f} (should be 1), sum p_i^2 = {p1**2+p2**2+p3**2:.5f} (should be 1)\n")


if __name__ == "__main__":
    part1_horizon_vs_singularity()
    part2_julia_fixed_points()
    try:
        render_julia(-0.123, "julia_c_-0.123.png")
    except ImportError:
        print("  (Pillow not installed -- skipping image render)\n")
    part3_bifurcation_multipliers()
    part4_phi_three_gaps()
    part5_bkl_gauss_map()
