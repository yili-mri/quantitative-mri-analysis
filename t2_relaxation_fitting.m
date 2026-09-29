%% T2 Relaxation Fitting Example
% Example of T2 relaxation-time fitting using synthetic MRI data.
%
% The script generates a mono-exponential T2 decay, adds Gaussian noise,
% and estimates T2 using nonlinear least-squares fitting.
%
% Only synthetic data are used.

clear;
clc;
close all;

%% Echo times (ms)

TE = [10 20 30 40 50];

%% Ground-truth parameters

true_S0 = 1000;
true_T2 = 60;  % ms

%% Generate synthetic T2 decay

signal_clean = true_S0 .* exp(-TE ./ true_T2);

%% Add reproducible Gaussian noise

rng(42);
noise = 20 .* randn(size(TE));
signal_noisy = signal_clean + noise;

%% Define T2 model

t2_model = @(p, te) p(1) .* exp(-te ./ p(2));

%% Initial parameter estimates

initial_guess = [max(signal_noisy), 50];

%% Estimate S0 and T2

objective = @(p) sum((signal_noisy - t2_model(p, TE)).^2);

estimated_parameters = fminsearch(objective, initial_guess);

estimated_S0 = estimated_parameters(1);
estimated_T2 = estimated_parameters(2);

%% Display results

fprintf('True T2: %.1f ms\n', true_T2);
fprintf('Estimated T2: %.1f ms\n', estimated_T2);

%% Generate fitted curve

TE_fit = linspace(min(TE), max(TE), 200);
signal_fit = t2_model(estimated_parameters, TE_fit);

%% Plot results

figure;

scatter(TE, signal_noisy, 50, 'filled');
hold on;

plot(TE_fit, signal_fit, 'LineWidth', 1.5);

xlabel('Echo time (ms)');
ylabel('Signal intensity (a.u.)');
title('Synthetic T2 Relaxation Fitting');

legend('Synthetic data', 'T2 fit');
grid on;
