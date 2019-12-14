'''
    AM modulation with DSB-LC
    author: Evram
'''

import numpy as np
from scipy.io import wavfile
from scipy.signal import hilbert
import librosa


def modulate_dsb_lc(audio, sample_rate):
    '''modulated(t) = (Ac + audio(t)) * cos(ωc + t)'''
    # time samples
    time = np.arange(0, len(audio)) / sample_rate

    # divide min peak by the modulation index
    ac = abs(np.min(audio)) / .9

    fc = 100 * 1000  # 100 kHz
    wc = 2 * np.pi * fc

    return (ac + audio) * np.cos(wc + time)


print('read audio file')
audio, sample_rate = librosa.load('sample.wav')

print('modulate')
modulated = modulate_dsb_lc(audio, sample_rate)

print('demodulate for each snr')
for snr in [0, 1, 10, 20]:
    out_file_name = f'out/am_snr_{snr}.wav'
    print(out_file_name, end='', flush=True)

    # add noise
    noise = np.random.normal(0, 1/snr if snr != 0 else 1, len(audio))
    modulated_with_noise = modulated + noise

    # demodulate
    analytic_signal = hilbert(modulated_with_noise)
    amplitude_envelope = np.abs(analytic_signal)

    scaled = np.int16(amplitude_envelope /
                      np.max(np.abs(amplitude_envelope)) * 32767)

    # out
    wavfile.write(out_file_name, sample_rate, scaled)

    print(': done')
