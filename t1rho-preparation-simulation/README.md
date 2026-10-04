# T1rho Preparation Simulation

Exploratory MATLAB simulations of continuous-wave (CW) T1rho preparation design using single-pool Bloch and two-pool Bloch-McConnell models.

## Purpose

This small project asks whether T1rho preparation design can alter apparent T1rho relaxation and quantitative target-reference tissue contrast.

The work progressed from single-pool preparation robustness to a generic two-mobile-pool exchange model. The final analysis deliberately distinguishes relative contrast changes (RRTD) from absolute target-reference contrast changes in milliseconds.

## Included scripts

- `src/single_pool_preparation_robustness.m` — single-pool Bloch simulation of conventional and single-refocused CW-T1rho preparation over B0/B1 variation.
- `src/two_pool_contrast_analysis.m` — two-pool Bloch-McConnell simulation with exchange, chemical-shift variation, apparent T1rho fitting, RRTD, absolute contrast, and fit-quality filtering.
- `results/simulation_summary.md` — concise record of the simulation progression and main findings.

## Main findings

Single-pool simulations showed that refocusing can substantially broaden the continuous B0/B1 robustness region. In the two-pool model, preparation-dependent differences in apparent T1rho and RRTD occurred across parts of the simulated parameter space.

However, the largest relative effects did not translate into equally large absolute tissue-separation changes. After requiring both preparations to have highly monoexponential fits (R² >= 0.999), 86.73% of simulated parameter combinations remained, but the mean absolute preparation-dependent contrast change was about 0.10 ms and the maximum was about 0.56 ms. No surviving point exceeded 1 ms.

These results suggest that normalized contrast metrics can amplify modest absolute preparation-dependent effects.

## Scope and limitations

This is an exploratory methodological simulation, not a validated tissue-specific model.

The two-pool model represents two mobile pools with transverse magnetization. The simulated parameters should not be interpreted as established values for myocardium, cardiac conduction tissue, collagen, fibrosis, or other specific biological tissues.

A realistic macromolecular tissue model may require semisolid magnetization transfer, additional pools, appropriate lineshapes, and experimental validation. The present code is therefore intended as a compact demonstration of Bloch/Bloch-McConnell modeling and quantitative MRI analysis rather than a biological mechanistic claim.

The refocused implementation uses a single-refocus phase convention for exploratory comparison. Exact replication of a published preparation should be verified against its pulse diagram before sequence-specific conclusions are drawn.

## Data

No patient data or restricted research data are included. All results are generated from synthetic simulations.
