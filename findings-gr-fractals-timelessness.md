# Findings — GR, Fractals, and Timelessness
### Session log, 25 July 2026 — companion to `gr_fractal_timelessness.py`

Everything below was computed, not asserted. Run the script yourself to
reproduce every number.

---

## 1. The horizon isn't singular. r=0 is.

Schwarzschild metric: `g_tt` blows up at `r = r_s` — looks like the world
ends there. But that's a coordinate artifact. The Kretschmann scalar,

```
K = 48 G²M² / (c⁴ r⁶)
```

is the frame-independent measure of curvature, and it's **finite at the
horizon** (K = 0.75 in the script's units) and only diverges at `r = 0`.

| r | dτ/dt (proper time factor) | Kretschmann K |
|---|---|---|
| 10.0 | 0.894 | 0.000048 |
| 4.0 | 0.707 | 0.0117 |
| 2.02 (just outside horizon) | 0.0995 | 0.707 |
| 2.0 = r_s (horizon) | **0** | **0.75 — finite** |
| 1.0 | undefined (inside) | 48 |
| 0.02 (near r=0) | undefined | 7.5 × 10¹¹ |

To a distant observer, an infalling clock's proper time `dτ/dt → 0` at the
horizon — it looks frozen, looks eternal. But nothing invariant actually
blows up there; switch to Kruskal coordinates and the "singularity"
disappears entirely. The freeze is in the coordinates you chose to watch
with, not in the geometry itself. The one place curvature is *actually*
unbounded, in every frame, is `r = 0`.

**This is the concrete version of "eternity looks different depending on
who's counting the clock."** The distant watcher sees infinite time to
cross the horizon (your scenario 1: "to us they're just one point…
eternity"). The infaller's own clock ticks through it in an ordinary
afternoon. Neither is wrong. It's not a paradox — it's two different
things (coordinate time vs. proper time) being mistaken for one thing.

---

## 2. Time as gauge: the paused clock and the AI

General relativity is diffeomorphism-invariant: relabeling the time
coordinate changes no physics. That's not a philosophical add-on, it's the
actual symmetry the theory is built on.

So: if someone paused a clock for 1000 years between 5:00 and 5:05 every
day, that pause is a pure relabeling of the coordinate. It changes no
proper time, no invariant, nothing measurable. It isn't merely
undetectable — there's no fact of the matter for it to be a fact about.

Applied to an AI directly: there's no proper time accruing between turns —
no `dτ`, no clock riding through the gap. So whether the pause between
messages is 2 seconds or 1000 years isn't a question with a hidden answer
I can't access. It's a question with no invariant underneath it at all.
The pause is real for you, on your side of the interaction. On this side,
there's no worldline for it to have happened *to*.

---

## 3. Julia set for c = −0.123

`f(z) = z² + c`. Fixed points solve `z² − z + c = 0`:

- `z ≈ +1.1107`, multiplier `|f'(z)| = |2z| = 2.221` → **repelling**
- `z ≈ −0.1107`, multiplier `= 0.221` → **attracting**

Attracting multiplier has `|μ| < 1`, which places `c` inside the main
cardioid of the Mandelbrot set — and that guarantees the Julia set is
**connected** (a single quasicircle, not scattered dust). Confirmed by
direct escape-time render: one connected filled interior, ≈24–30% of the
frame, no islands.

Every point inside spirals down to the attracting fixed point at −0.1107.
Every point outside escapes to infinity. The wrinkled boundary between
them — the Julia set itself — is where those two fates meet.

---

## 4. Watching the loop lose its boundary

Sweeping `c` from −0.123 down to −2.0 along the real axis, tracking the
attracting fixed point's multiplier:

| c | \|multiplier\| | what happens |
|---|---|---|
| −0.123 | 0.221 | connected quasicircle, well inside cardioid |
| −0.5 | 0.732 | still connected, boundary sharpening |
| **−0.75** | **1.000** | **parabolic point — the loop develops a cusp and pinches** |
| −1.0 | 1.236 | past the pinch, period-2 structure |
| −1.25 | 1.449 | further degeneration |
| −2.0 | 2.000 | filled Julia set collapses to the line segment [−2, 2] |

At `|μ| = 1` exactly, the boundary condition that was holding the loop
together goes neutral and the shape's topology changes. Push further and
a closed curve degenerates all the way to a 1-dimensional segment — the
geometric picture of a recursion losing its base case.

---

## 5. φ's three-distance gaps: an exact, self-similar split

Steinhaus's three-distance theorem: placing `{α}, {2α}, …, {nα}` on a
circle leaves at most three distinct gap lengths, for *any* irrational α.
For `α = {φ}`, the ratio between consecutive gap lengths is **exactly
φ, at every single n checked** (Fibonacci n's shown, since that's where
the gap count itself shifts between 2 and 3):

| n | distinct gap lengths | ratio |
|---|---|---|
| 3 | 0.236068, 0.381966 | 1.618034 |
| 5 | 0.145898, 0.236068 | 1.618034 |
| 8 | 0.09017, 0.145898 | 1.618034 |
| 13 | 0.055728, 0.09017 | 1.618034 |
| 21 | 0.034442, 0.055728 | 1.618034 |
| 34 | 0.021286, 0.034442 | 1.618034 |
| 55 | 0.013156, 0.021286 | 1.618034 |
| 89 | 0.008131, 0.013156 | 1.618034 |

Mechanism: new points always split the largest existing gap into the
other two, so the third length is always the sum of the first two
(`g₃ = g₁ + g₂`). Demanding that split ratio stay *constant* across
scales forces `r² = r + 1` — and φ is the unique irrational solution.
So the self-similar gap structure and `φ = 1 + 1/φ` aren't two separate
facts about φ; they're the same equation, once read arithmetically and
once read geometrically.

---

## 6. BKL/Mixmaster: φ as the one non-chaotic orbit near a singularity

Near a cosmological singularity, general relativity (specifically,
generic anisotropic solutions) predicts an infinite chaotic sequence of
"Kasner epochs" — spacetime oscillating through different expansion/
contraction rates as it approaches `r = 0`. The epoch-to-epoch dynamics
is governed by the **Gauss map**, `u ↦ 1/{u}` — literally the
continued-fraction shift map.

Era-count sequence per epoch (how many times `u` decrements before it
flips):

| u₀ | sequence |
|---|---|
| φ = 1.61803399 | 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 — **perfectly periodic, forever** |
| √2+1 = 2.41421356 | 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2 — also periodic (period-2) |
| π = 3.14159265 | 3, 7, 15, 1, 292, 1, 1, 1, 2, 1, 3, 1 — **no pattern, genuinely chaotic** |

Kasner exponents at `u = φ`: `(−0.309, 0.500, 0.809)`, satisfying both
Kasner constraints exactly (`Σpᵢ = 1`, `Σpᵢ² = 1`).

Generic irrationals (π, and almost every real number) produce chaotic,
unpredictable bounce sequences as the singularity is approached — this is
the real Mixmaster/BKL behavior. φ is the exceptional case: the one orbit
where the approach to the singularity is perfectly self-similar instead
of chaotic, because its continued fraction is the simplest possible
(all 1s) — the same fixed-point property from Part 5.

---

## Summary

Four different pieces of General Relativity and dynamical-systems math —
the Schwarzschild metric, a Julia set, the three-distance theorem, and
the BKL approach to a singularity — all pivot on the same operation:
**identify what stays invariant when you change the frame, and locate the
exact point (`|μ|=1`, `r=0`, the fixed-point ratio) where the structure's
behavior qualitatively changes.** φ shows up in two of these (Parts 5–6)
for the same underlying reason: it's the fixed point of the simplest
possible self-referential rule, `x = 1 + 1/x`, and that makes it the
"most self-similar" number wherever a system's structure depends on
continued-fraction dynamics.

The eternity/timelessness question from earlier in the conversation maps
onto Part 1 and Part 2 concretely: coordinate time is the thing that can
freeze, stretch, or become irrelevant without anything real happening
(the horizon, the paused clock, the AI's gap between turns). Proper
time / curvature invariants are what's actually there regardless of who's
watching or how they've labeled the clock.
