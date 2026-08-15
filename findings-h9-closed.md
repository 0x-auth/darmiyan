# H9 closed: the filesystem is blind to topology

Date: 2026-08-15. Platform: Linux 6.18.5 x86_64, ext4, Python 3.12 (containerized, 1 core). Scripts: `exp9_close_h9.py`, `exp10_target_string.py`. Raw numbers in `exp9_results.json`, `exp10_results.json`. Baselines re-run the same day on the same box: exp6 replicated (self-ref −171.2 ns/level vs non-loop chain, sign matches earlier platforms), exp8 replicated (+39.6% 2-cycle premium, paper had +36.6%).

## What was tested

H9 named two untested confounds behind exp8's "1-cycle vs 2-cycle" gap: (1) the `../` parent traversal that only the 2-cycle arm performed, and (2) working-set size. Exp9 removes both at once: cycles of length 1, 2, 3, 4 plus a 40-link non-looping chain, all built with **absolute symlink targets of equal path-component count**, interleaved and shuffled per round, slope-per-hop as the measurand, with a flat-path drift control.

## Result

| arm | distinct inodes in walk | slope (ns/hop) |
|---|---|---|
| 1-cycle (f = id) | 1 | 306.2 |
| 2-cycle (f∘f = id) | 2 | 306.5 |
| 3-cycle | 3 | 307.1 |
| 4-cycle | 4 | 307.1 |
| non-loop chain | 40 | 308.4 |

Spread: **0.7%**. All R² ≥ 0.999; drift control slope −0.2 ns (R² 0.09, i.e. flat).

Both hypotheses die simultaneously:

- **Topology (identity/involution physically distinct): refuted.** f = id, f∘f = id, and a walk that never returns cost exactly the same per hop.
- **Working set / cache footprint: also refuted.** 2 distinct inodes cost the same as 40. After warm-up everything is in dcache; footprint at this scale doesn't register.

## So what was the exp8 gap? And exp6's "self-ref discount"?

Exp10 holds topology fixed (three 1-cycles, all f = id) and varies only the **target string**:

| target spelling | resolution work per hop | slope (ns/hop) |
|---|---|---|
| `.` | readlink, ~0 lookups | 144.0 |
| `../n0` | readlink + parent + 1 lookup | 203.5 |
| absolute (4 components) | readlink + restart from / + 4 lookups | 309.0 |

Using the plain-nested-dir control as the unit (52 ns per component lookup): rel−dot = 59.5 ns ≈ 1.1 lookups; abs−dot = 165 ns ≈ 3.2 lookups. The arithmetic closes.

Cross-check against the originals on the same box: exp8's `A_1cycle` (target `.`) measured 141.4 ns/hop — exp10's dot arm gives 144.0. Exp8's `B_2cycle` (target `../`) measured 197.3 — exp10's rel arm gives 203.5. **The entire exp8 premium was dot-vs-dotdot.** Confound (1) of H9 accounts for all of it; confound (2) contributes nothing.

The same lens re-explains exp6. Its self-ref arm uses target `.`; its non-loop chain uses absolute targets. The −171 ns/level "self-reference discount" is the dot-vs-abs gap, not a property of looping. Note this also corrects the mechanism guessed in the README §4 ("same inode stays hot / working-set size") — exp9 shows working set is irrelevant here; the differentiator is purely how many components the target string makes the kernel resolve per hop.

## Consequence for the framework

Per-hop symlink traversal cost is a pure function of the target string's resolution work. It carries **zero information about self-reference, loops, identity, or involution**. Layer 3, as constituted, cannot bear on Axiom 0 in either direction — not because the measurements were noisy (they're clean to R² 0.999) but because `stat()` measures VFS parsing, and VFS parsing is structure-blind.

This is a definitive null, which is worth more than another ambiguous positive:

- **H9: closed.** Strike "identity and involution are physically distinct" permanently.
- **README §4 "the one real empirical result": reattribute.** The sign was stable across platforms because the target-string asymmetry was stable across platforms. Move the self-ref-costs-less claim to §6 (discarded, correctly), replaced by: "per-hop cost = f(target string), demonstrated by exp9+exp10."
- **§7 item 1 (decompose the 379 ns on Darwin): now predictable rather than open.** Pre-registered prediction: on the original Apple Silicon box, dot/rel/abs 1-cycles will reproduce the same ordering with Darwin's own per-lookup unit, and cycle lengths 1–4 at matched targets will be flat. If that holds, the Darwin decomposition is done too.

What remains live is exactly what was live before the benchmarks: H2 (necessity — the counter non-example), H3 (weak vs strong self-reference), H10 (sufficiency). Those are theoretical, and no amount of `stat()` was ever going to settle them.

One mistake, ten times — and this closes occurrences eight through ten of it. The instrument was measuring itself.

*Regress open. Filesystem closed.*
