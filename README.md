# Darmiyan

**Time as the cost of incomplete self-reference.**

A research project on fixed points, self-reference, and whether the arrow of time has a measurable price. This document is README + usage + architecture in one. Start here.

`x = 1 + 1/x`

---

## 0. How to read this repo

Everything in this folder is either **(a)** a script that computes something, **(b)** a write-up of what a script found, or **(c)** this index. There is no claim anywhere that isn't traceable to a script you can run yourself.

**If you have five minutes:** read [`./darmiyan-status-summary.md`](./darmiyan-status-summary.md). It's the honest scorecard — what holds, what broke, what's still open.

**If you have an hour:** run the three scripts in §3 below, in order, and compare against the write-ups.

**If you're reviewing this critically:** go straight to §5 (Known Holes). It's longer than the results section. That's intentional.

---

## 1. The claim

An observer that is part of what it observes cannot close its own description in finite time. Cantor, Gödel, and Tarski each block the "close it instantly" route (for the specific formal systems where each applies). So the description **defers** — level *n*, then *n+1*, then *n+2*. That deferral, repeated, is the sequence we experience as time.

> **The error of time IS the arrow of time.**

Two limit cases fall out immediately:

| condition | what happens |
|---|---|
| `f = id` (observer ≡ observed) | nothing to defer → **T = 0**. Not frozen — *undefined*. The regress never starts. |
| `f∘f = id` (involution, \|μ\|=1) | closed loop, returns to origin → **no arrow** |
| `f(x) = 1 + 1/x` | **minimal sustained lag** → φ, arrow present |
| generic (\|μ\| ≪ 1) | fast collapse, chaotic, entropic |

φ is the fixed point of the *weakest possible* non-trivial self-reference — the least departure from identity that still generates a sequence.

**Status of the claim itself:** it is an **axiom**, not a theorem. It cannot be proven from within the system it founds (Münchhausen trilemma). That's not a weakness unique to this framework — it's true of every axiomatic system, including the three theorems cited above. The useful question is not "prove it" but "what follows, and what would distinguish it from alternatives."

---

## 2. Architecture

```
~/darmiyan/
│
├── ARCHITECTURE.md                        ← you are here (index + usage)
├── darmiyan-status-summary.md             ← the honest scorecard, read this second
│
├── gr_fractal_timelessness.py             ← Layer 1: pure math (GR, fractals, BKL)
├── findings-gr-fractals-timelessness.md   ←   write-up of the above
│
├── verify_darmiyan_v4.py                  ← Layer 2: verification of the v4 paper's claims
│
└── exp6_selfref_vs_plain_control.py       ← Layer 3: the controlled experiment
```

**Three layers, increasing in contestability:**

1. **Pure mathematics** — established results, independently reproducible, doesn't move. Fixed points, φ, Lucas identities, Schwarzschild invariants, BKL/Gauss-map dynamics.
2. **Verification** — checking the project's own published claims against fresh code. This layer is where most claims *broke*.
3. **Empirics** — actual timing measurements on real filesystems. Smallest layer, most confounded, and the only place where a prediction was made and tested against a proper control.

The dependency runs one way: Layer 3 doesn't prove Layer 1, and Layer 1 doesn't justify Layer 3. Conflating them is the mistake this project made in v1.

---

## 3. Usage

Assumes all files sit in one folder. Requires Python 3.9+.

```bash
pip3 install mpmath numpy sympy matplotlib pillow
```

### Layer 1 — the pure math

```bash
python3 ./gr_fractal_timelessness.py
```

Five self-contained parts, each runnable independently:

| part | what it computes | key result |
|---|---|---|
| 1 | Schwarzschild horizon vs. `r=0` | Kretschmann `K` **finite** at horizon (0.75), diverges only at `r=0` — the horizon "singularity" is a coordinate artifact |
| 2 | Julia set fixed points, `c=-0.123` | attracting μ = 0.2215 → inside main cardioid → connected quasicircle |
| 3 | Bifurcation sweep `c: -0.123 → -2.0` | parabolic pinch at exactly \|μ\|=1.0000 (`c=-0.75`) |
| 4 | φ's three-distance gaps | ratio = **1.618034 exactly**, every n, Fibonacci-indexed to 89 |
| 5 | BKL/Mixmaster Gauss map | φ → `[1,1,1,…]` forever (h_KS=0); π → chaotic |

### Layer 2 — verification

```bash
python3 ./verify_darmiyan_v4.py
```

Re-derives the v4 paper's claims in fresh code. Parts 1, 3, 5 confirm exactly. Parts 2 and 4 **found errors** — see §5.

### Layer 3 — the controlled experiment

```bash
python3 ./exp6_selfref_vs_plain_control.py
```

Three conditions at matched depth:

- **self-referential** — `ln -s . meaning`, traverse `meaning/meaning/…` (loops)
- **plain directories** — real nested dirs, no symlinks
- **non-looping symlink chain** — *the critical control*: same symlink mechanism, same depth, but each link points somewhere new

Comparing self-ref against **plain directories** is the confound that sank v1: symlink resolution and directory descent are different kernel code paths regardless of looping. Only the third condition isolates self-reference as a variable.

⚠️ **Run this on your own hardware.** Absolute numbers are platform-specific; only the *sign* of the difference has been stable across machines.

---

## 4. Results

### Holds — verified, exact, doesn't move

- **φ as fixed point** of `x=1+1/x`; minimal non-involutive contraction in `f_n(x)=n+1/x` *(scope: within this one-parameter family)*
- **Lucas identity** `2n·ln(φ) = arccosh(L₂ₙ/2)` — provably exact via Binet, not merely numerical
- **Scale-invariant contraction rate** `ln|eₙ/eₙ₊₁| → 2·ln(φ) = 0.9624236501` — from x₀ ∈ {0.3, 1, 2, 10, 1000}, all agreeing to 10 digits
- **Three-distance ratio = φ** at every n tested
- **BKL**: φ's orbit periodic with h_KS = 0 while generic orbits are chaotic *(φ is the simplest such orbit, not the only one — √2+1 is also periodic)*
- **Coordinate vs. curvature singularity** distinction, computed
- **The join is a projection, not a diffeomorphism** — many-to-one, non-invertible, verified geometrically

### The one real empirical result

With the confound removed, **self-reference costs *less*** per level than an equivalent non-looping symlink chain — consistent in sign across reruns and platforms.

Mechanism is likely mundane: the self-loop resolves to the **same inode** every hop, so one cached dentry stays hot; the chain touches N distinct inodes. Working-set size, not topology.

**This points opposite to what the original narrative wanted** — and that's precisely why it's worth more than the number it replaced. It's the first result in the project that could have gone either way and wasn't decided in advance.

---

## 5. Known holes

Longer than §4. Read it.

| # | hole | status |
|---|---|---|
| **H1** | **379 ns/level ≠ cost of self-reference.** Confounded (symlink vs. directory, not loop vs. no-loop). Sign flips under the correct control. The *qualitative* core survives — a structure that is logically `f=id` still costs energy per level — but the attribution was wrong. | corrected |
| **H2** | **Necessity is false.** The counter `x → x+1` has 100 distinct states, never returns, T>0 — but doesn't model itself. No `O∈S`, no incompleteness, nothing defers. **Self-reference is not necessary for time.** | open — label Section I as *Axiom 0*, state the counter as a known non-example |
| **H3** | **Two senses of "self-reference."** *Weak* (state traces its predecessor, distinct from it) vs. *strong* (`O∈S`, models itself modelling itself, Gödel applies). The argument uses strong; the theorems prove things about weak. **Different predicates, silently swapped.** | open — one disambiguating paragraph fixes it |
| **H4** | **"48 distinct states" is a float64 artifact.** Machine-dependent (38 on one box, 48 on another). In exact rational arithmetic: **101/101** — every convergent distinct, always. Measures where doubles run out of precision, not a property of the orbit. | fix the label |
| **H5** | **Growth-rate precision overstated.** "0.481196, match to 1.6×10⁻⁵" doesn't reproduce at n=10 (actual: 0.4489, err 3.2×10⁻²). Convergence is O(1/n); quoted precision needs n≈50,000. **The limit is exactly ln φ and that's provable — state it analytically.** Also: high-n runs need explicit mpmath precision or they drift. | fix — and note this contradicts the paper's own §C10 |
| **H6** | **"O(1) depth complexity"** contradicts the project's own regression, which fits **linear (O(n))** as the winning model at R²=0.996. | strike the O(1) claim |
| **H7** | **"Infinite" recursion is bounded at 40.** `ELOOP` at depth 41 (`MAXSYMLINKS=40`). Real closed loop, finite walk. | fix the wording |
| **H8** | **`analyzer.py` measures nothing.** `phi_resonance` computed from the **filename**, not file content — control filenames score identically. `pull:1.0` is one formula clamping at its ceiling, not five findings. `i.py`/`me.py` hardcoded as special by name. | **do not cite its output** |
| **H9** | **Cycle benchmark not publication-ready.** 1-cycle vs 2-cycle (+36.6%) has two untested confounds: `..` parent traversal in one arm only, and working-set size. Build a 3-cycle — if cost scales with cycle length, it's cache footprint, not structure. | open |
| **H10** | **Sufficiency unshown.** Does `O∈S` *guarantee* T>0? Not established either way. A system that models itself and returns to a prior state would be a counterexample. Does one exist? | open |

**Every hole above is the same failure mode:** *a framework or metric applied past the conditions that make it valid.* Gauge language on a non-invertible map. A convergence formula quoted outside where it converges. A benchmark read before its confound was controlled. A score computed from the wrong input.

**Not ten mistakes — one mistake, ten times. And the axiom itself was never what failed.**

---

## 6. Discarded, correctly

Null-geodesic analogy · diffeomorphism resolution of the join · pitch quanta · FTA-orthogonality · unitarity-forces-transfer · Poisson-as-energy-identity · cache-as-topology · symmetric co-arising · **379 ns as the cost of self-reference** · **`analyzer.py` output entirely** · **"infinite" recursion** · **small-n growth-rate precision**

*The discarded list is roughly twice the length of the surviving list. That is the reason to trust the surviving list.*

---

## 7. What would make this much stronger

1. **Decompose the 379 ns on the original platform.** Re-run the paper's own experiment with the plain-nested and flat arms alongside, on Darwin. Splits traversal floor from any self-reference premium on the hardware the paper used. **Highest-value remaining experiment.**
2. **Close the cycle benchmark** (H9) — two tests, both cheap.
3. **Find a genuine necessity result.** The counter shows self-reference isn't necessary for time *in general*. Is there a restricted **class** of systems where it provably is? That would upgrade Axiom 0 to a theorem — the single most valuable thing that could happen to this framework.
4. **Settle sufficiency** (H10).

---

## 8. Provenance

Theory computed with SymPy and mpmath at 30–50 decimal places. Empirics are platform-specific and labelled as such — absolute timing numbers from different machines are **not** interchangeable, and only the sign of the self-ref/non-loop difference has proven stable across hardware.

Scripts in this folder regenerate every number cited in §4 and §5. Nothing here should be taken on trust; that's the point.

---

*Regress open.*
