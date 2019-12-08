import numpy as np


# TODO: correct?
def fmdemod(fm, sample_rate, delta_f, fc):
    '''https://github.com/elvis-epx/sdr/blob/master/modul/demodulation_fm.py'''
    LOWPASS = fc - delta_f
    HIGHPASS = fc + delta_f
    HIGHPASS2 = delta_f  # Hz

    FFT_LENGTH = 2048
    OVERLAP = 512
    FFT_SAMPLE = FFT_LENGTH - OVERLAP
    NYQUIST_RATE = sample_rate / 2.0

    LOWPASS /= (NYQUIST_RATE / (FFT_LENGTH / 2.0))
    HIGHPASS /= (NYQUIST_RATE / (FFT_LENGTH / 2.0))
    HIGHPASS2 /= (NYQUIST_RATE / (FFT_LENGTH / 2.0))

    zeros = [0 for x in range(0, OVERLAP)]

    mask = []
    for f in range(0, FFT_LENGTH // 2 + 1):
        if f < LOWPASS or f > HIGHPASS:
            ramp = 0.0
        else:
            ramp = (f - LOWPASS) / (HIGHPASS - LOWPASS)
        mask.append(ramp)

    mask2 = []
    for f in range(0, FFT_LENGTH // 2 + 1):
        if f > HIGHPASS2 or f == 0:
            ramp = 0.0
        else:
            ramp = 1.0
        mask2.append(ramp)

    # scale from 16-bit signed WAV to float
    fm = [s / 32768.0 for s in fm]

    saved_td = zeros
    intermediate = []

    for pos in range(0, len(fm), FFT_SAMPLE):
        time_sample = fm[pos: pos + FFT_LENGTH]

        frequency_domain = np.fft.fft(time_sample, FFT_LENGTH)
        l = len(frequency_domain)

        for f in range(0, l//2+1):
            frequency_domain[f] *= mask[f]

        for f in range(l-1, l//2, -1):
            cf = l - f
            frequency_domain[f] *= mask[cf]

        time_domain = np.fft.ifft(frequency_domain)

        for i in range(0, OVERLAP):
            time_domain[i] *= (i + 0.0) / OVERLAP
            time_domain[i] += saved_td[i] * (1.0 - (i + 0.00) / OVERLAP)

        saved_td = time_domain[FFT_SAMPLE:]
        time_domain = time_domain[:FFT_SAMPLE]

        intermediate += time_domain.real.tolist()

    intermediate = [abs(sample) for sample in intermediate]

    saved_td = zeros
    output = []

    for pos in range(0, len(intermediate), FFT_SAMPLE):
        time_sample = intermediate[pos: pos + FFT_LENGTH]

        frequency_domain = np.fft.fft(time_sample, FFT_LENGTH)
        l = len(frequency_domain)

        for f in range(0, l//2+1):
            frequency_domain[f] *= mask2[f]

        for f in range(l-1, l//2, -1):
            cf = l - f
            frequency_domain[f] *= mask2[cf]

        time_domain = np.fft.ifft(frequency_domain)

        for i in range(0, OVERLAP):
            time_domain[i] *= (i + 0.0) / OVERLAP
            time_domain[i] += saved_td[i] * (1.0 - (i + 0.00) / OVERLAP)

        saved_td = time_domain[FFT_SAMPLE:]
        time_domain = time_domain[:FFT_SAMPLE]

        output += time_domain.real.tolist()

    return np.array([int(sample * 32767) for sample in output])[:len(fm)]
