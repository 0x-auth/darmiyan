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
├── exp6_selfref_vs_plain_control.py       ← Layer 3: the controlled experiment
├── exp8_cycle_topology.py                 ←   cycle benchmark (superseded by exp9)
├── exp9_close_h9.py                       ←   closes H9: cycle length 1..4 vs chain
├── exp10_target_string.py                 ←   same topology, different target string
└── findings-h9-closed.md                  ←   write-up: the filesystem is blind to topology
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

Then the two experiments that closed it out:

```bash
python3 ./exp9_close_h9.py        # cycle length 1,2,3,4 vs 40-link chain, matched targets
python3 ./exp10_target_string.py  # topology fixed at f=id, target string varied
```

⚠️ **Run this on your own hardware.** Absolute numbers are platform-specific. Note that the exp6 *sign*, though stable across machines, turned out to be an artifact of target-string asymmetry rather than of looping — see [`./findings-h9-closed.md`](./findings-h9-closed.md).

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

**Per-hop symlink traversal cost is a pure function of the target string's resolution work — and carries no information about topology at all.** Established by `exp9_close_h9.py` + `exp10_target_string.py`; see [`./findings-h9-closed.md`](./findings-h9-closed.md).

At matched target-component counts, cycle length is irrelevant: 1-cycle (`f = id`) 306.2, 2-cycle (`f∘f = id`) 306.5, 3-cycle 307.1, 4-cycle 307.1, 40-link non-looping chain 308.4 ns/hop — a 0.7% spread, all R² ≥ 0.999. Holding topology fixed at `f = id` and varying only the target spelling reproduces the whole effect: `.` 144.0, `../n0` 203.5, absolute-4-component 309.0 ns/hop, with the gaps converting to lookup counts at the plain-dir unit of 52 ns/component.

This **replaces** the previous entry here ("self-reference costs less per level"), which was real as a measurement but misattributed: its self-ref arm used target `.` and its control used absolute targets. Same for the earlier cache explanation — working set was tested directly and does nothing (2 inodes = 40 inodes).

**It is a null, and it is the strongest result in the project.** Layer 3 as constituted cannot bear on Axiom 0 in either direction — not from noise, but because `stat()` measures VFS path parsing, and VFS path parsing is structure-blind. Every remaining question is theoretical.

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
| **H9** | **Cycle benchmark not publication-ready.** 1-cycle vs 2-cycle (+36.6%) had two untested confounds: `..` parent traversal in one arm only, and working-set size. **Both now tested (`exp9`, `exp10`).** Confound (1) accounts for the entire gap; confound (2) contributes nothing (2 inodes = 40). Cycles 1/2/3/4/∞ are flat to 0.7% at matched targets. **"Identity and involution are physically distinct" is struck.** | **closed** |
| **H10** | **Sufficiency unshown.** Does `O∈S` *guarantee* T>0? Not established either way. A system that models itself and returns to a prior state would be a counterexample. Does one exist? | open |

**Every hole above is the same failure mode:** *a framework or metric applied past the conditions that make it valid.* Gauge language on a non-invertible map. A convergence formula quoted outside where it converges. A benchmark read before its confound was controlled. A score computed from the wrong input.

**Not ten mistakes — one mistake, ten times. And the axiom itself was never what failed.**

---

## 6. Discarded, correctly

Null-geodesic analogy · diffeomorphism resolution of the join · pitch quanta · FTA-orthogonality · unitarity-forces-transfer · Poisson-as-energy-identity · cache-as-topology · symmetric co-arising · **379 ns as the cost of self-reference** · **`analyzer.py` output entirely** · **"infinite" recursion** · **small-n growth-rate precision** · **the 1-cycle/2-cycle topology premium** · **the working-set explanation of the exp6 sign** · **self-reference costing *less* per level**

*The discarded list is roughly twice the length of the surviving list. That is the reason to trust the surviving list.*

---

## 7. What would make this much stronger

1. ~~**Decompose the 379 ns on the original platform.**~~ Now a **pre-registered prediction** rather than an open question. Run `exp10_target_string.py` on the original Darwin/Apple Silicon box: the dot < rel < abs ordering should reproduce with Darwin's own per-lookup unit, and `exp9_close_h9.py` should show cycle lengths 1–4 flat at matched targets. If both hold, the Darwin decomposition is done and Layer 3 is finished. If either fails, that failure is itself the most interesting result in the repo.
2. ~~**Close the cycle benchmark** (H9).~~ **Done** — see [`./findings-h9-closed.md`](./findings-h9-closed.md).
3. **Find a genuine necessity result.** The counter shows self-reference isn't necessary for time *in general*. Is there a restricted **class** of systems where it provably is? That would upgrade Axiom 0 to a theorem — the single most valuable thing that could happen to this framework.
4. **Settle sufficiency** (H10).

---

## 8. Provenance

Theory computed with SymPy and mpmath at 30–50 decimal places. Empirics are platform-specific and labelled as such — absolute timing numbers from different machines are **not** interchangeable. The exp6 sign proved stable across hardware, but exp9/exp10 showed *why*: it tracks how many path components each arm's symlink target makes the kernel resolve, which is a property of the test construction, not of the machine or of the topology.

Scripts in this folder regenerate every number cited in §4 and §5. Nothing here should be taken on trust; that's the point.

---

*Regress open.*
