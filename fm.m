1; 
pkg load communications;
%
% FM modulation
% author: Mahmoud
% 

% carson rule:
% kf = β * B * 2π / mp
function kf = calc_kf(beta, m)
    % TODO: compute B
    % get B (max frequency)

    % spectrum = fft(m)
    % freq = fftfreq(len(spectrum))
    % threshold = 0.5 * max(abs(spectrum))
    % mask = abs(spectrum) > threshold
    % peaks = freq[mask]
    % max_freq = peaks.max()  % B
    max_freq = 5; % temporarily
    
    mp = max(abs(m));

    kf = beta * max_freq * 2 * pi / mp;
endfunction

% modulated(t) = Ac * cos(wc * t + kf * integration(audio(t)))
function modulated = modulate_fm(audio, sample_rate, beta)
    % time samples
    % TODO: cant calculate, out of memory
    t = (0:length(audio)) / sample_rate;

    ac = 1;

    fc = 100 * 1000;  % 100 kHz
    wc = 2 * pi * fc;

    kf = calc_kf(beta, audio);

    modulated = ac * cos(wc + kf * cumsum(audio));
endfunction

disp('read audio file');
[audio, sample_rate] = audioread('sample.wav');
audio = (audio(:, 1) + audio(:, 2)) / 2;

betas.wide = 5;
betas.narrow = .1;
for [beta_value, name] = betas
    disp(['modeulate ' name ' band with beta = ' num2str(beta_value)]);
    % modulated = fmmod(audio, 100 * 1000, sample_rate);
    modulated = modulate_fm(audio, sample_rate, beta_value);

    for snr = [0, 1, 10, 20]
        out_file_name = ['out/fm_' name '_snr_'  num2str(snr) '.wav'];
        disp(out_file_name);

        % add noise
        modulated_with_noise = awgn(modulated, snr);

        % demodulate
        demodulated = fmdemod(modulated_with_noise, 100 * 1000, sample_rate);

        % write out
        audiowrite(out_file_name, demodulated, sample_rate);

        disp(': done');
    endfor
endfor
