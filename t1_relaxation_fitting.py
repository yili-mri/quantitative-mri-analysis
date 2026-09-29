"""
Example of T1 relaxation-time fitting using synthetic inversion-recovery MRI data.

The script generates an inversion-recovery signal, adds Gaussian noise,
and estimates T1 using nonlinear least-squares fitting.

Only synthetic data are used.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def t1_model(ti, s0, t1):
    """Ideal inversion-recovery signal model."""
    return s0 * (1.0 - 2.0 * np.exp(-ti / t1))


# Inversion times (ms)
ti = np.array(
    [100, 200, 400, 800, 1200, 1800, 2500, 3500, 4500],
    dtype=float,
)

# Ground-truth parameters
true_s0 = 1000.0
true_t1 = 1200.0  # ms

# Generate noise-free signal
signal_clean = t1_model(ti, true_s0, true_t1)

# Add reproducible Gaussian noise
rng = np.random.default_rng(seed=42)
noise = rng.normal(0, 20, size=ti.size)
signal_noisy = signal_clean + noise

# Initial parameter estimates
initial_guess = [signal_noisy.max(), 1000.0]

# Fit the inversion-recovery model
parameters, covariance = curve_fit(
    t1_model,
    ti,
    signal_noisy,
    p0=initial_guess,
    bounds=(0, np.inf),
)

estimated_s0, estimated_t1 = parameters

# Calculate fitted signal at measured inversion times
signal_predicted = t1_model(ti, estimated_s0, estimated_t1)

# Calculate R-squared
residual_sum_squares = np.sum((signal_noisy - signal_predicted) ** 2)
total_sum_squares = np.sum(
    (signal_noisy - np.mean(signal_noisy)) ** 2
)
r_squared = 1.0 - residual_sum_squares / total_sum_squares

# Display results
print(f"True T1: {true_t1:.1f} ms")
print(f"Estimated T1: {estimated_t1:.1f} ms")
print(f"R-squared: {r_squared:.4f}")

# Generate smooth fitted curve
ti_fit = np.linspace(ti.min(), ti.max(), 500)
signal_fit = t1_model(ti_fit, estimated_s0, estimated_t1)

# Plot results
plt.figure(figsize=(6, 4))

plt.scatter(
    ti,
    signal_noisy,
    label="Synthetic data",
)

plt.plot(
    ti_fit,
    signal_fit,
    label="T1 fit",
)

plt.axhline(
    0,
    linewidth=0.8,
)

plt.xlabel("Inversion time (ms)")
plt.ylabel("Signal intensity (a.u.)")
plt.title("Synthetic T1 Inversion-Recovery Fitting")

plt.text(
    0.95,
    0.05,
    f"T1 = {estimated_t1:.1f} ms\nR² = {r_squared:.3f}",
    transform=plt.gca().transAxes,
    horizontalalignment="right",
    verticalalignment="bottom",
)

plt.legend()
plt.tight_layout()
plt.show()
