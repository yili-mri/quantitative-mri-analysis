"""
Synthetic pixel-wise T2 mapping example.

This script creates a simple two-region phantom with different T2 values,
simulates multi-echo MRI data, adds Gaussian noise, and performs pixel-wise
mono-exponential fitting to estimate a quantitative T2 map.

Only synthetic data are used.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def t2_model(te, s0, t2):
    """Mono-exponential T2 decay model."""
    return s0 * np.exp(-te / t2)


# ------------------------------------------------------------
# 1. Define synthetic phantom
# ------------------------------------------------------------

image_size = 64

# Ground-truth maps
t2_true = np.zeros((image_size, image_size), dtype=float)
s0_true = np.zeros((image_size, image_size), dtype=float)

# Create coordinate grid
y, x = np.ogrid[:image_size, :image_size]

# Two non-overlapping circular tissue regions
region_1 = (x - 20) ** 2 + (y - 32) ** 2 <= 10 ** 2
region_2 = (x - 44) ** 2 + (y - 32) ** 2 <= 10 ** 2

# Assign ground-truth T2 values
t2_true[region_1] = 40.0  # ms
t2_true[region_2] = 70.0  # ms

# Assign proton-density-like signal amplitude
s0_true[region_1] = 1000.0
s0_true[region_2] = 1000.0

# Define foreground mask
mask = t2_true > 0


# ------------------------------------------------------------
# 2. Simulate multi-echo MRI data
# ------------------------------------------------------------

te = np.array([10, 20, 30, 40, 50], dtype=float)

signals = np.zeros(
    (len(te), image_size, image_size),
    dtype=float,
)

for i, echo_time in enumerate(te):
    signals[i, mask] = (
        s0_true[mask]
        * np.exp(-echo_time / t2_true[mask])
    )


# ------------------------------------------------------------
# 3. Add Gaussian noise
# ------------------------------------------------------------

rng = np.random.default_rng(seed=42)

noise_std = 20.0

noise = rng.normal(
    0,
    noise_std,
    size=signals.shape,
)

signals_noisy = signals + noise


# ------------------------------------------------------------
# 4. Perform pixel-wise T2 fitting
# ------------------------------------------------------------

t2_estimated = np.zeros(
    (image_size, image_size),
    dtype=float,
)

for row in range(image_size):
    for col in range(image_size):

        # Skip background pixels
        if not mask[row, col]:
            continue

        signal = signals_noisy[:, row, col]

        initial_guess = [
            np.max(signal),
            50.0,
        ]

        try:
            parameters, _ = curve_fit(
                t2_model,
                te,
                signal,
                p0=initial_guess,
                bounds=(0, np.inf),
                maxfev=5000,
            )

            estimated_s0, estimated_t2 = parameters

            t2_estimated[row, col] = estimated_t2

        except (RuntimeError, ValueError):
            t2_estimated[row, col] = np.nan


# ------------------------------------------------------------
# 5. Calculate regional statistics
# ------------------------------------------------------------

region_1_values = t2_estimated[region_1]
region_2_values = t2_estimated[region_2]

print("Ground-truth T2 values:")
print("Region 1: 40 ms")
print("Region 2: 70 ms")
print()

print("Estimated T2 values:")

print(
    f"Region 1: "
    f"{np.nanmean(region_1_values):.1f} ± "
    f"{np.nanstd(region_1_values, ddof=1):.1f} ms"
)

print(
    f"Region 2: "
    f"{np.nanmean(region_2_values):.1f} ± "
    f"{np.nanstd(region_2_values, ddof=1):.1f} ms"
)


# ------------------------------------------------------------
# 6. Visualize results
# ------------------------------------------------------------

display_map = np.where(
    mask,
    t2_estimated,
    np.nan,
)

plt.figure(figsize=(6, 5))

image = plt.imshow(
    display_map,
    vmin=20,
    vmax=90,
)

plt.colorbar(
    image,
    label="T2 (ms)",
)

plt.title("Estimated Synthetic T2 Map")
plt.axis("off")

plt.tight_layout()
plt.show()
