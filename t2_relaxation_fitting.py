"""
Example of T2 relaxation-time fitting using synthetic MRI data.

The script generates a mono-exponential T2 decay, adds Gaussian noise,
and estimates T2 using nonlinear least-squares fitting.

Only synthetic data are used.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def t2_model(te, s0, t2):
    """Mono-exponential T2 decay model."""
    return s0 * np.exp(-te / t2)


# Echo times (ms)
te = np.array([10, 20, 30, 40, 50], dtype=float)

# Ground-truth parameters used to generate synthetic data
true_s0 = 1000.0
true_t2 = 60.0  # ms

# Generate noise-free signal
signal_clean = t2_model(te, true_s0, true_t2)

# Add reproducible Gaussian noise
rng = np.random.default_rng(seed=42)
noise = rng.normal(0, 20, size=te.size)
signal_noisy = signal_clean + noise

# Fit the T2 model
initial_guess = [signal_noisy.max(), 50.0]

parameters, covariance = curve_fit(
    t2_model,
    te,
    signal_noisy,
    p0=initial_guess,
    bounds=(0, np.inf),
)

estimated_s0, estimated_t2 = parameters

print(f"True T2: {true_t2:.1f} ms")
print(f"Estimated T2: {estimated_t2:.1f} ms")

# Generate smooth fitted curve for visualization
te_fit = np.linspace(te.min(), te.max(), 200)
signal_fit = t2_model(te_fit, estimated_s0, estimated_t2)

# Plot synthetic measurements and fitted curve
plt.figure(figsize=(6, 4))
plt.scatter(te, signal_noisy, label="Synthetic data")
plt.plot(te_fit, signal_fit, label="T2 fit")
plt.xlabel("Echo time (ms)")
plt.ylabel("Signal intensity (a.u.)")
plt.title("Synthetic T2 Relaxation Fitting")
plt.legend()
plt.tight_layout()
plt.show()
