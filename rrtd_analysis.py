"""
Example calculation of relative relaxation-time difference (RRTD).

RRTD provides a normalized comparison of relaxation times between
a target tissue and a reference tissue.

Only synthetic example values are used.
"""

import numpy as np


def calculate_rrtd(target, reference):
    """
    Calculate relative relaxation-time difference (RRTD).

    RRTD = 2 * (target - reference) / (target + reference)

    Parameters
    ----------
    target : float or array-like
        Relaxation time of the target tissue.

    reference : float or array-like
        Relaxation time of the reference tissue.

    Returns
    -------
    float or numpy.ndarray
        Relative relaxation-time difference.
    """
    target = np.asarray(target, dtype=float)
    reference = np.asarray(reference, dtype=float)

    return 2.0 * (target - reference) / (target + reference)


# Synthetic example relaxation times (ms)
target_t2 = np.array([75, 78, 72, 80, 76], dtype=float)
reference_t2 = np.array([45, 48, 44, 47, 46], dtype=float)

# Calculate RRTD for each synthetic measurement
rrtd = calculate_rrtd(target_t2, reference_t2)

print("Target T2 values (ms):", target_t2)
print("Reference T2 values (ms):", reference_t2)
print("RRTD values:", np.round(rrtd, 3))

# Summary statistics
mean_rrtd = np.mean(rrtd)
std_rrtd = np.std(rrtd, ddof=1)

print(f"Mean RRTD: {mean_rrtd:.3f}")
print(f"Standard deviation: {std_rrtd:.3f}")
