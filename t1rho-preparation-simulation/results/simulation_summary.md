# Simulation summary

## Question

Can CW-T1rho preparation design alter apparent T1rho and quantitative target-reference contrast in single- and multi-pool systems?

## 1. Single-pool validation

Explicit Bloch simulations were used to compare conventional and single-refocused CW-T1rho preparation. At the ideal condition, apparent T1rho agreed closely with the expected single-pool value. Refocusing broadened the continuous robustness region over B0/B1 variation and reduced structured preparation failures.

## 2. Two-pool Bloch-McConnell exploration

A generic two-mobile-pool model was then used to explore pool fraction, exchange rate, and chemical-shift offset. Off-resonant secondary-pool evolution produced preparation-dependent raw signals before fitting. The spectral pattern changed with spin-lock duration, consistent with coherent phase accumulation. Increasing exchange and shortening transverse relaxation damped these oscillations.

A same-resonance control showed very small preparation differences, indicating that exchange alone was not sufficient to generate the larger effects observed in the off-resonant model.

## 3. Tissue-contrast analysis

Target and reference model tissues were compared using

RRTD = 2(T_target - T_reference)/(T_target + T_reference).

Literature-inspired generic exchange ranges were explored at 3 T (pool fraction 0.05-0.20, exchange rate 500-3000 s^-1, and chemical shift 1-5 ppm). Preparation-dependent RRTD differences occurred across part of this parameter space.

Fit-quality filtering showed that relative contrast effects did not disappear completely when both preparations had highly monoexponential decays. However, RRTD is a normalized metric and can magnify small absolute differences.

## 4. Absolute contrast checkpoint

Absolute target-reference separation was therefore defined as

C = T_target - T_reference

and the preparation-dependent change as

Delta C = C_refocused - C_conventional.

Unfiltered, the maximum |Delta C| was 2.7647 ms, but this occurred with poorer refocused monoexponential fit quality (R² = 0.9583).

After fit-quality filtering:

- Both R² >= 0.990: 92.55% of points survived; mean |Delta C| = 0.1459 ms; median = 0.0778 ms; maximum = 1.6406 ms; 1.79% exceeded 1 ms.
- Both R² >= 0.995: 91.61% survived; mean = 0.1335 ms; median = 0.0772 ms; maximum = 1.2261 ms; 0.79% exceeded 1 ms.
- Both R² >= 0.999: 86.73% survived; mean = 0.0996 ms; median = 0.0716 ms; maximum = 0.5607 ms; no surviving point exceeded 1 ms.

For R² >= 0.999, |Delta C| and |Delta RRTD| were correlated (r = 0.870770), but relative effects were substantially larger numerically than the corresponding absolute contrast changes.

## Interpretation

The simulations support a preparation-dependent effect on apparent T1rho in selected multipool regimes, but the absolute target-reference contrast difference between the two tested preparations is generally modest when both signal decays are highly monoexponential.

The model is intentionally generic. It should not be interpreted as a validated model of myocardium, cardiac conduction tissue, collagen, or fibrosis. A tissue-specific extension would require better-constrained parameters and potentially semisolid magnetization-transfer modeling and experimental validation.

## Project status

The exploratory simulation is archived here as a methodological demonstration. No further model expansion is currently planned.
