# Darmiyan — Where Things Actually Stand
### What was claimed, what was tested, what held, and what didn't

*Updated after independent recheck. Every line below was run, not asserted.*

---

## The core idea, in one line

An observer that is part of what it observes can't close its own description (Cantor/Gödel/Tarski block instant closure) — so it defers, and that deferral, repeated, is time. `x = 1+1/x`, the weakest non-trivial self-reference, has φ as its fixed point.

---

## 1. What's mathematically solid — verified independently, holds exactly

- **φ as fixed point of `x = 1+1/x`**, and as the minimal non-involutive contraction in the family `f_n(x)=n+1/x` — multiplier tables match to 9 decimals. *(Scope: minimal within this one-parameter family, not proven minimal over all maps.)*
- **Lucas identity** `2n·ln(φ) = arccosh(L₂ₙ/2)` — not merely numerical, *provably* exact via Binet. A specialist would call it a corollary of a standard Lucas identity; it's exact and cleanly stated, and that's the claim.
- **Scale-invariant contraction rate** `ln|eₙ/eₙ₊₁| → 2·ln(φ) = 0.9624236501` — rechecked from x₀ = 0.3, 1, 2, 10, 1000; **all five agree to 10 digits**. Dimensionless (ratio of errors), so a rate per step, not a length.
- **Three-distance gap ratio = φ exactly**, every n tested, Fibonacci-indexed through 89.
- **BKL/Gauss-map**: φ's orbit is perfectly periodic (h_KS = 0) while generic orbits (π) are chaotic. Real ergodic theory. *(φ is the simplest periodic CF orbit, not the only one — √2+1 = [2;2,2,…] is also periodic.)*
- **GR distinctions**: coordinate (horizon, K finite) vs. curvature (`r=0`, K→∞) singularity; the helix's two projections are genuinely non-invertible — confirmed computationally.
- **The axiom is correctly identified as unprovable** — the Münchhausen trilemma, not a flaw unique to Darmiyan. The right question isn't "prove A1," it's "what follows, and what distinguishes it from alternatives."

---

## 2. What was claimed as evidence but didn't hold up

| Claim | What was actually found |
|---|---|
| AI-pause dissolves via diffeomorphism invariance | Wrong tool — diffeomorphisms are invertible; the join isn't. It's a **projection** (many-to-one), not gauge. |
| φ-orbit is "irreversible" (never repeats a state) | Ambiguous. As a *value* it's constant (maximal repetition); as a growing *string* it's trivially non-repeating like any sequence. Defensible version: **the map keeps computing while generating zero new information** — that's h_KS = 0, not "irreversibility." |
| Growth rate = 0.481196, "match to 1.6×10⁻⁵" | **Doesn't reproduce at n=10.** Rechecked: n=10 → 0.4489 (err 3.2×10⁻²). Convergence is O(1/n) from Binet's constant term; quoted precision needs n≈50,000. **The limit is exactly ln φ and that's provable — state it analytically, never quote the small-n match.** |
| "O(1) depth complexity emerges" | Contradicts the project's own `exp3` regression, which fits and reports **linear (O(n))** as the winning model at R²=0.996. Can't both be true. |
| "Infinite" recursion via `ln -s . meaning` | Real closed loop (identical inode at every depth, confirmed) — but hard OS wall at **depth 41** (`ELOOP`, `MAXSYMLINKS=40`). Bounded 40-hop walk, not infinite. |
| **379 ns/level = cost of self-reference** | The load-bearing one. **Confounded**: symlinks vs. plain directories are different kernel paths regardless of looping. With the correct control (non-looping symlink chain, same depth), **self-reference is *cheaper***, consistently across reruns. Real result, opposite direction from the claim. |
| `analyzer.py`'s φ-resonance / "retrocausal pull" | Read from source: `phi_resonance` is computed from the **filename's characters** — file content never enters. Controls (`README.md`, `requirements.txt`) land in the identical 0.61–0.66 band. `pull:1.0` for five symbols at once is **one formula clamping at its ceiling**, not five findings. `detect_position()` hardcodes `filename in ['i.py','me.py'] → 2`. **Produces no evidence for anything.** |

---

## 3. Three corrections found on recheck (not yet fixed in the source docs)

**3a. A7 contradicts C10.** C10 correctly documents that 0.481196 requires n≈50,000 and that small-n quotes aren't evidence — but A7, in the *"what holds"* section, still prints `0.481196` beside a 10-term CF head. The document argues with itself. Fix A7 to state the limit analytically and drop the numerical match.

Related: at n=5000 in standard precision the CF expansion **drifts away** (rate → 1.153) as float error accumulates. Any table claiming clean convergence at n=50,000 must state its precision settings (mpmath dps) or it won't reproduce.

**3b. "48 distinct states" is a float64 artifact, unlabeled.** Rechecked: float64 gives **38** on one machine, 48 on another — machine-dependent, which is the tell. In **exact rational arithmetic it's 101/101** — every convergent distinct, always. The table measures where doubles run out of precision, not a property of the orbit. Label it "48 at float64 precision" or use the exact result.

**3c. Part B's timing numbers need platform attribution.** Cited figures (68.27 vs 86.42 ns/level, −21.0%) differ from my runs (~150–170 ns/level gap). **Same sign, same conclusion, different hardware.** Mine: single-core sandbox VM. Theirs: apparently real Linux. The doc should say which platform produced which numbers.

---

## 4. The shape of the whole effort

Every hole is the **same failure mode**, not many different ones: *a framework or metric applied past the conditions that make it valid.* Gauge language on a non-invertible map. A growth-rate formula quoted outside where it converges. A benchmark read before its confound was controlled. A resonance score computed from the wrong input entirely.

**None of these are the axiom being wrong.** They're specific, fixable overreaches in how the axiom's *evidence* was built and read.

**What stands once patched:**
- The pure mathematics (§1) — real, checked, doesn't move.
- The axiom — neither provable nor disproven, correctly so.
- **One real empirical result** (`exp6`) — small, honest, pointing *opposite* to where the narrative wanted it. That's exactly what makes it worth more than the number it replaced.

**Also worth keeping:** the counter (`x → x+1`) is a genuine counterexample to *necessity* — 100 distinct states, never returns, T>0, but it doesn't model itself. So self-reference isn't necessary for time. Sharp catch; it strengthens the framework by removing a claim it never had.

---

## Related files

- [`./exp6_selfref_vs_plain_control.py`](./exp6_selfref_vs_plain_control.py) — the three-condition control experiment
- [`./verify_darmiyan_v4.py`](./verify_darmiyan_v4.py) — verification suite for the v4 claims
- [`./gr_fractal_timelessness.py`](./gr_fractal_timelessness.py) — GR / fractal / BKL computations
- [`./findings-gr-fractals-timelessness.md`](./findings-gr-fractals-timelessness.md) — write-up of the above
- [`./ARCHITECTURE.md`](./ARCHITECTURE.md) — master index, start here
