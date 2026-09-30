%% T1rho Relaxation Fitting Example
% Example of T1rho relaxation-time fitting using synthetic MRI data.
%
% The script generates a mono-exponential T1rho decay, adds Gaussian
% noise, estimates T1rho using nonlinear least-squares fitting, and
% calculates R-squared as a simple measure of goodness of fit.
%
% Only synthetic data are used.

clear;
clc;
close all;

%% Spin-lock times (ms)

TSL = [0 10 20 40];

%% Ground-truth parameters

true_S0 = 1000;
true_T1rho = 55;  % ms

%% Generate synthetic T1rho decay

signal_clean = true_S0 .* exp(-TSL ./ true_T1rho);

%% Add reproducible Gaussian noise

rng(42);
noise = 20 .* randn(size(TSL));
signal_noisy = signal_clean + noise;

%% Define T1rho model

t1rho_model = @(p, tsl) p(1) .* exp(-tsl ./ p(2));

%% Initial parameter estimates

initial_guess = [max(signal_noisy), 50];

%% Estimate S0 and T1rho

objective = @(p) sum( ...
    (signal_noisy - t1rho_model(p, TSL)).^2 ...
);

estimated_parameters = fminsearch( ...
    objective, ...
    initial_guess ...
);

estimated_S0 = estimated_parameters(1);
estimated_T1rho = estimated_parameters(2);

%% Calculate fitted signal at measured TSL values

signal_predicted = t1rho_model( ...
    estimated_parameters, ...
    TSL ...
);

%% Calculate R-squared

residual_sum_squares = sum( ...
    (signal_noisy - signal_predicted).^2 ...
);

total_sum_squares = sum( ...
    (signal_noisy - mean(signal_noisy)).^2 ...
);

R_squared = 1 - ...
    residual_sum_squares / total_sum_squares;

%% Display results

fprintf('True T1rho: %.1f ms\n', true_T1rho);
fprintf('Estimated T1rho: %.1f ms\n', estimated_T1rho);
fprintf('R-squared: %.4f\n', R_squared);

%% Generate fitted curve

TSL_fit = linspace(min(TSL), max(TSL), 200);

signal_fit = t1rho_model( ...
    estimated_parameters, ...
    TSL_fit ...
);

%% Plot results

figure;

scatter(TSL, signal_noisy, 50, 'filled');
hold on;

plot(TSL_fit, signal_fit, 'LineWidth', 1.5);

xlabel('Spin-lock time (ms)');
ylabel('Signal intensity (a.u.)');
title('Synthetic T1rho Relaxation Fitting');

legend('Synthetic data', 'T1rho fit');

grid on;

