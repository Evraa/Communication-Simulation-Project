%
% FM modulation
% author: Mahmoud Adas
% 

1; % script

pkg load communications;
pkg load miscellaneous;

% carson rule:
% kf = β * B * 2π / mp
function kf = calc_kf(beta, m, sample_rate)
    max_freq = sample_rate/2;

    mp = max(abs(m));

    kf = beta * max_freq * 2 * pi / mp;
endfunction

% modulated(t) = Ac * cos(wc * t + kf * integration(audio(t)))
function modulated = modulate_fm(audio, sample_rate, beta, fc)
    ac = 1;
    wc = 2 * pi * fc;
    kf = calc_kf(beta, audio, sample_rate);

    % time samples
    t = ((1:length(audio)) / sample_rate).';

    modulated = ac * cos(wc * t + kf * cumsum(audio));
endfunction

fc = 100 * 1000  % 100 kHz

disp('read audio file');
[audio, sample_rate] = audioread('sample.wav');
sample_rate

disp('stereo to mono');
audio = (audio(:, 1) + audio(:, 2)) / 2;

disp(['before resampling, audio length: ' num2str(length(audio))]);
orig_sample_rate = sample_rate;
sample_rate = fc*1.2
audio = resample(audio, sample_rate, sample_rate);
disp(['after resampling, audio length: ' num2str(length(audio))]);

betas.wide = 5;
betas.narrow = .1;
for [beta_value, name] = betas
    disp(['modeulate ' name ' band with beta = ' num2str(beta_value)]);
    modulated = modulate_fm(audio, sample_rate, beta_value, fc);

    for snr = [0, 1, 10, 20]
        out_file_name = ['out/fm_' name '_snr_'  num2str(snr) '.wav'];
        disp(out_file_name);

        % add noise
        modulated_with_noise = clip(awgn(modulated, snr), [0, 1]);

        % demodulate
        demodulated = fmdemod(modulated_with_noise, fc, sample_rate);

        % resample back
        demodulated = resample(demodulated, old_sample_rate, sample_rate);
        sample_rate = old_sample_rate;

        % write out
        audiowrite(out_file_name, demodulated, sample_rate);

        disp(': done');
    endfor
endfor
