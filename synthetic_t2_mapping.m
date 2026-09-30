%% Synthetic Pixel-wise T2 Mapping Example
% This script creates a simple two-region phantom with different
% T2 values, simulates multi-echo MRI data, adds Gaussian noise,
% and performs pixel-wise mono-exponential fitting to estimate
% a quantitative T2 map.
%
% Only synthetic data are used.

clear;
clc;
close all;

%% 1. Define synthetic phantom

image_size = 64;

T2_true = zeros(image_size, image_size);
S0_true = zeros(image_size, image_size);

[x, y] = meshgrid(1:image_size, 1:image_size);

region_1 = ...
    (x - 20).^2 + (y - 32).^2 <= 10^2;

region_2 = ...
    (x - 44).^2 + (y - 32).^2 <= 10^2;

T2_true(region_1) = 40;
T2_true(region_2) = 70;

S0_true(region_1) = 1000;
S0_true(region_2) = 1000;

mask = T2_true > 0;

%% 2. Simulate multi-echo MRI data

TE = [10 20 30 40 50];

signals = zeros( ...
    image_size, ...
    image_size, ...
    length(TE) ...
);

for i = 1:length(TE)

    temp = zeros(image_size, image_size);

    temp(mask) = ...
        S0_true(mask) .* ...
        exp(-TE(i) ./ T2_true(mask));

    signals(:, :, i) = temp;

end

%% 3. Add Gaussian noise

rng(42);

noise_std = 20;

signals_noisy = signals + ...
    noise_std .* randn(size(signals));

%% 4. Perform pixel-wise T2 fitting

T2_estimated = nan(image_size, image_size);

t2_model = @(p, te) ...
    p(1) .* exp(-te ./ p(2));

for row = 1:image_size

    for col = 1:image_size

        if ~mask(row, col)
            continue;
        end

        signal = squeeze( ...
            signals_noisy(row, col, :) ...
        )';

        initial_guess = [max(signal), 50];

        objective = @(p) sum( ...
            (signal - t2_model(p, TE)).^2 ...
        );

        estimated_parameters = fminsearch( ...
            objective, ...
            initial_guess, ...
            optimset('Display', 'off') ...
        );

        estimated_T2 = estimated_parameters(2);

        % Reject non-physical fitting results
        if estimated_T2 > 0
            T2_estimated(row, col) = estimated_T2;
        end

    end

end

%% 5. Calculate regional statistics

region_1_values = T2_estimated(region_1);
region_2_values = T2_estimated(region_2);

region_1_values = ...
    region_1_values(~isnan(region_1_values));

region_2_values = ...
    region_2_values(~isnan(region_2_values));

fprintf('Ground-truth T2 values:\n');
fprintf('Region 1: 40 ms\n');
fprintf('Region 2: 70 ms\n\n');

fprintf('Estimated T2 values:\n');

fprintf( ...
    'Region 1: %.1f +/- %.1f ms\n', ...
    mean(region_1_values), ...
    std(region_1_values) ...
);

fprintf( ...
    'Region 2: %.1f +/- %.1f ms\n', ...
    mean(region_2_values), ...
    std(region_2_values) ...
);

%% 6. Visualize estimated T2 map

figure;

imagesc(T2_estimated, [20 90]);

axis image;
axis off;

colorbar;

title('Estimated Synthetic T2 Map');

cb = colorbar;
ylabel(cb, 'T2 (ms)');
