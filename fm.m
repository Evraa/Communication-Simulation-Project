%
% FM modulation
% author: Mahmoud Adas
%

pkg load communications;

function modulated = fmmod2(x, fc, fs, freqdev)
    t = (0:1/fs:((size(x,1)-1)/fs))';
    t = t(:,ones(1,size(x,2)));

    int_x = cumsum(x)/fs;
    modulated = cos(2*pi*fc*t + 2*pi*freqdev*int_x);
endfunction

function demodulated = fmdemod2(y, fc, fs, freqdev)
    t = (0:1/fs:((size(y,1)-1)/fs))';
    t = t(:,ones(1,size(y,2)));

    yq = hilbert(y).*exp(-j*2*pi*fc*t);
    demodulated = (1/(2*pi*freqdev))*[zeros(1,size(yq,2)); diff(unwrap(angle(yq)))*fs];
endfunction

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

disp('read audio file');
[audio, sample_rate] = audioread('sample.wav');

disp('stereo to mono');
audio = (audio(:, 1) + audio(:, 2)) / 2;

fc = 100 * 1000  % 100 kHz

disp('resample')
orig_sample_rate = sample_rate
sample_rate = fc*4
audio = resample(audio, sample_rate, orig_sample_rate);

betas.wide = 5;
betas.narrow = .1;
for [beta_value, name] = betas
    beta_value
    freqdev = beta_value * sample_rate

    disp('modulate')
    modulated = fmmod2(audio, fc, sample_rate, freqdev);

    for snr = [20, 10, 1, 0]
        out_file_name = ['out/fm_' name '_snr_'  num2str(snr) '.wav'];
        disp(out_file_name);

        disp('  add noise')
        modulated_with_noise = awgn(modulated, snr);

        disp('  demodulate')
        demodulated = fmdemod2(modulated_with_noise, fc, sample_rate, freqdev);

        disp('  resample back')
        demodulated = resample(demodulated, orig_sample_rate, sample_rate);

        disp('  write out')
        audiowrite(out_file_name, demodulated, orig_sample_rate);

        disp('  done');
    endfor
endfor
