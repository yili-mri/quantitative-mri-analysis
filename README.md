# Quantitative MRI Analysis

This repository contains example analysis workflows for quantitative MRI and relaxation mapping.

The examples are based on generalized workflows used in my research on quantitative tissue characterization. They demonstrate relaxation-time fitting, quantitative tissue comparison, ROI-based analysis, pixel-wise relaxation mapping, and basic fit-quality assessment using synthetic data.

## Methods

Example implementations include:

- T1 inversion-recovery fitting
- T2 mono-exponential relaxation fitting
- T1ρ mono-exponential relaxation fitting
- Pixel-wise quantitative T2 mapping
- Pixel-wise quantitative T1ρ mapping
- Pixel-wise goodness-of-fit assessment
- ROI-based quantitative analysis
- Relative relaxation-time difference (RRTD) calculation
- Basic statistical analysis and visualization of quantitative MRI data

## Python

Python examples include:

- T1, T2, and T1ρ relaxation-time fitting
- Synthetic pixel-wise T2 mapping
- Synthetic pixel-wise T1ρ mapping with R² fit-quality assessment
- Relative relaxation-time difference analysis

The Python implementations use NumPy, SciPy, and Matplotlib for numerical analysis, nonlinear fitting, and visualization.

## MATLAB

MATLAB examples include:

- T1 inversion-recovery fitting
- T2 relaxation-time fitting
- T1ρ relaxation-time fitting
- Synthetic pixel-wise T2 mapping

The MATLAB examples demonstrate nonlinear relaxation fitting, quantitative mapping, and visualization using synthetic MRI data.

## Research Background

My research focuses on quantitative MRI for tissue characterization, including rotating-frame relaxation methods (RAFF and T1ρ), conventional relaxation mapping, high-resolution ex vivo MRI, histological validation, and in vivo cardiac MRI.

My work has involved the development and application of MATLAB- and Python-based analysis workflows for quantitative MRI data.

## Data

All examples in this repository use synthetic data. No patient data, identifiable information, restricted research data, or proprietary acquisition code are included.

## Author

Yi Li  
Doctoral Researcher  
Research Unit of Health Sciences and Technology  
University of Oulu, Finland


## T1rho preparation simulation

A compact exploratory MATLAB project on CW-T1rho preparation design is available in [`t1rho-preparation-simulation/`](./t1rho-preparation-simulation/). It includes single-pool Bloch robustness simulations and a generic two-pool Bloch-McConnell analysis of preparation-dependent apparent T1rho and tissue contrast. The final analysis emphasizes the distinction between normalized RRTD changes and absolute target-reference contrast changes, with explicit fit-quality filtering.
