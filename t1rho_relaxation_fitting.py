"""
Example of T1rho relaxation-time fitting using synthetic MRI data.

The script generates a mono-exponential T1rho decay, adds Gaussian noise,
estimates T1rho using nonlinear least-squares fitting, and calculates R-squared
as a simple measure of goodness of fit.

Only synthetic data are used.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def t1rho_model(tsl, s0, t1rho):
    """Mono-exponential T1rho decay model."""
    return s0 * np.exp(-tsl / t1rho)


def calculate_r_squared(observed, predicted):
    """Calculate the coefficient of determination (R-squared)."""
    residual_sum_squares = np.sum((observed - predicted) ** 2)
    total_sum_squares = np.sum((observed - np.mean(observed)) ** 2)

    return 1.0 - residual_sum_squares / total_sum_squares


# Spin-lock times (ms)
tsl = np.array([0, 10, 20, 40], dtype=float)

# Ground-truth parameters used to generate synthetic data
true_s0 = 1000.0
true_t1rho = 55.0  # ms

# Generate noise-free signal
signal_clean = t1rho_model(tsl, true_s0, true_t1rho)

# Add reproducible Gaussian noise
rng = np.random.default_rng(seed=42)
noise = rng.normal(0, 20, size=tsl.size)
signal_noisy = signal_clean + noise

# Initial parameter estimates
initial_guess = [signal_noisy.max(), 50.0]

# Fit the T1rho model
parameters, covariance = curve_fit(
    t1rho_model,
    tsl,
    signal_noisy,
    p0=initial_guess,
    bounds=(0, np.inf),
)

estimated_s0, estimated_t1rho = parameters

# Calculate fitted signal at the measured spin-lock times
signal_predicted = t1rho_model(tsl, estimated_s0, estimated_t1rho)

# Calculate goodness of fit
r_squared = calculate_r_squared(signal_noisy, signal_predicted)

# Display results
print(f"True T1rho: {true_t1rho:.1f} ms")
print(f"Estimated T1rho: {estimated_t1rho:.1f} ms")
print(f"R-squared: {r_squared:.4f}")

# Generate smooth fitted curve for visualization
tsl_fit = np.linspace(tsl.min(), tsl.max(), 200)
signal_fit = t1rho_model(tsl_fit, estimated_s0, estimated_t1rho)

# Plot synthetic measurements and fitted curve
plt.figure(figsize=(6, 4))
plt.scatter(tsl, signal_noisy, label="Synthetic data")
plt.plot(tsl_fit, signal_fit, label="T1rho fit")

plt.xlabel("Spin-lock time (ms)")
plt.ylabel("Signal intensity (a.u.)")
plt.title("Synthetic T1rho Relaxation Fitting")

plt.text(
    0.95,
    0.95,
    f"T1rho = {estimated_t1rho:.1f} ms\nR² = {r_squared:.3f}",
    transform=plt.gca().transAxes,
    horizontalalignment="right",
    verticalalignment="top",
)

plt.legend()
plt.tight_layout()
plt.show()
