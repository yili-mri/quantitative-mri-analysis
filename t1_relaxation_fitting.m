%% T1 Relaxation Fitting Example
% Example of T1 relaxation-time fitting using synthetic
% inversion-recovery MRI data.
%
% The script generates an ideal inversion-recovery signal,
% adds Gaussian noise, estimates T1 using nonlinear
% least-squares fitting, and calculates R-squared.
%
% Only synthetic data are used.

clear;
clc;
close all;

%% Inversion times (ms)

TI = [100 200 400 800 1200 1800 2500 3500 4500];

%% Ground-truth parameters

true_S0 = 1000;
true_T1 = 1200;  % ms

%% Generate synthetic inversion-recovery signal

signal_clean = true_S0 .* ...
    (1 - 2 .* exp(-TI ./ true_T1));

%% Add reproducible Gaussian noise

rng(42);
noise = 20 .* randn(size(TI));
signal_noisy = signal_clean + noise;

%% Define ideal inversion-recovery model

t1_model = @(p, ti) ...
    p(1) .* (1 - 2 .* exp(-ti ./ p(2)));

%% Initial parameter estimates

initial_guess = [max(signal_noisy), 1000];

%% Estimate S0 and T1

objective = @(p) sum( ...
    (signal_noisy - t1_model(p, TI)).^2 ...
);

estimated_parameters = fminsearch( ...
    objective, ...
    initial_guess ...
);

estimated_S0 = estimated_parameters(1);
estimated_T1 = estimated_parameters(2);

%% Calculate fitted signal

signal_predicted = t1_model( ...
    estimated_parameters, ...
    TI ...
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

fprintf('True T1: %.1f ms\n', true_T1);
fprintf('Estimated T1: %.1f ms\n', estimated_T1);
fprintf('R-squared: %.4f\n', R_squared);

%% Generate fitted curve

TI_fit = linspace(min(TI), max(TI), 500);

signal_fit = t1_model( ...
    estimated_parameters, ...
    TI_fit ...
);

%% Plot results

figure;

scatter(TI, signal_noisy, 50, 'filled');
hold on;

plot(TI_fit, signal_fit, 'LineWidth', 1.5);
yline(0);

xlabel('Inversion time (ms)');
ylabel('Signal intensity (a.u.)');
title('Synthetic T1 Inversion-Recovery Fitting');

legend('Synthetic data', 'T1 fit');

grid on;
