"""
Synthetic pixel-wise T1rho mapping example.

This script creates a simple two-region phantom with different T1rho values,
simulates spin-lock-prepared MRI data, adds Gaussian noise, and performs
pixel-wise mono-exponential fitting to estimate a quantitative T1rho map.

A pixel-wise R-squared map is calculated as a simple measure of goodness
of fit. Regional mean, standard deviation, and coefficient of variation
are also reported.

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
    total_sum_squares = np.sum(
        (observed - np.mean(observed)) ** 2
    )

    if total_sum_squares == 0:
        return np.nan

    return 1.0 - residual_sum_squares / total_sum_squares


def calculate_cov(values):
    """Calculate coefficient of variation as SD / mean."""
    mean_value = np.nanmean(values)
    std_value = np.nanstd(values, ddof=1)

    if mean_value == 0:
        return np.nan

    return std_value / mean_value


# ------------------------------------------------------------
# 1. Define synthetic phantom
# ------------------------------------------------------------

image_size = 64

# Ground-truth maps
t1rho_true = np.zeros(
    (image_size, image_size),
    dtype=float,
)

s0_true = np.zeros(
    (image_size, image_size),
    dtype=float,
)

# Create coordinate grid
y, x = np.ogrid[:image_size, :image_size]

# Two non-overlapping circular tissue regions
region_1 = (x - 20) ** 2 + (y - 32) ** 2 <= 10 ** 2
region_2 = (x - 44) ** 2 + (y - 32) ** 2 <= 10 ** 2

# Assign ground-truth T1rho values
t1rho_true[region_1] = 40.0  # ms
t1rho_true[region_2] = 70.0  # ms

# Assign proton-density-like signal amplitude
s0_true[region_1] = 1000.0
s0_true[region_2] = 1000.0

# Define foreground mask
mask = t1rho_true > 0


# ------------------------------------------------------------
# 2. Simulate spin-lock-prepared MRI data
# ------------------------------------------------------------

# Spin-lock times (ms)
tsl = np.array(
    [0, 10, 20, 40],
    dtype=float,
)

signals = np.zeros(
    (len(tsl), image_size, image_size),
    dtype=float,
)

for i, spin_lock_time in enumerate(tsl):
    signals[i, mask] = (
        s0_true[mask]
        * np.exp(
            -spin_lock_time / t1rho_true[mask]
        )
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
# 4. Perform pixel-wise T1rho fitting
# ------------------------------------------------------------

t1rho_estimated = np.full(
    (image_size, image_size),
    np.nan,
    dtype=float,
)

r_squared_map = np.full(
    (image_size, image_size),
    np.nan,
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
                t1rho_model,
                tsl,
                signal,
                p0=initial_guess,
                bounds=(0, np.inf),
                maxfev=5000,
            )

            estimated_s0, estimated_t1rho = parameters

            t1rho_estimated[row, col] = estimated_t1rho

            # Calculate predicted signal at measured TSL values
            signal_predicted = t1rho_model(
                tsl,
                estimated_s0,
                estimated_t1rho,
            )

            # Calculate pixel-wise goodness of fit
            r_squared_map[row, col] = calculate_r_squared(
                signal,
                signal_predicted,
            )

        except (RuntimeError, ValueError):
            continue


# ------------------------------------------------------------
# 5. Calculate regional statistics
# ------------------------------------------------------------

region_1_values = t1rho_estimated[region_1]
region_2_values = t1rho_estimated[region_2]

region_1_mean = np.nanmean(region_1_values)
region_2_mean = np.nanmean(region_2_values)

region_1_std = np.nanstd(
    region_1_values,
    ddof=1,
)

region_2_std = np.nanstd(
    region_2_values,
    ddof=1,
)

region_1_cov = calculate_cov(region_1_values)
region_2_cov = calculate_cov(region_2_values)

print("Ground-truth T1rho values:")
print("Region 1: 40 ms")
print("Region 2: 70 ms")
print()

print("Estimated T1rho values:")

print(
    f"Region 1: "
    f"{region_1_mean:.1f} ± "
    f"{region_1_std:.1f} ms "
    f"(CoV = {region_1_cov:.3f})"
)

print(
    f"Region 2: "
    f"{region_2_mean:.1f} ± "
    f"{region_2_std:.1f} ms "
    f"(CoV = {region_2_cov:.3f})"
)


# ------------------------------------------------------------
# 6. Visualize quantitative T1rho map
# ------------------------------------------------------------

plt.figure(figsize=(6, 5))

image = plt.imshow(
    t1rho_estimated,
    vmin=20,
    vmax=90,
)

plt.colorbar(
    image,
    label="T1rho (ms)",
)

plt.title("Estimated Synthetic T1rho Map")
plt.axis("off")

plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# 7. Visualize R-squared map
# ------------------------------------------------------------

plt.figure(figsize=(6, 5))

image = plt.imshow(
    r_squared_map,
    vmin=0.8,
    vmax=1.0,
)

plt.colorbar(
    image,
    label="R-squared",
)

plt.title("Pixel-wise T1rho Fit Quality")
plt.axis("off")

plt.tight_layout()
plt.show()
