'''
    FM modulation
    author: Mahmoud
'''

import numpy as np
from scipy.io import wavfile
import librosa

from demod import fmdemod


def calc_kf(beta, m, sample_rate):
    '''carson rule:
    kf = β * B * 2π / mp
    '''
    max_freq = sample_rate/2

    mp = max(abs(m))

    return beta * max_freq * 2 * np.pi / mp


def modulate_fm(audio, sample_rate, beta):
    '''modulated(t) = Ac * cos(wc * t + kf * integration(audio(t)))'''
    # time samples
    time = np.arange(0, audio.size) / sample_rate

    ac = 1

    fc = 100 * 1000  # 100 kHz
    wc = 2 * np.pi * fc

    kf = calc_kf(beta, audio, sample_rate)

    return (ac * np.cos(wc * time + kf * np.cumsum(audio))), (kf * abs(audio.max()) / 2 * np.pi)


print('read audio file')
audio, sample_rate = librosa.load('sample.wav')


for beta, name in [(5, 'wide'), (.1, 'narrow')]:
    print(f'modeulate {name} band with β = {beta}')
    modulated, delta_f = modulate_fm(audio, sample_rate, beta)

    for snr in [0, 1, 10, 20]:
        out_file_name = f'out/fm_{name}_snr_{snr}.wav'
        print(out_file_name, end='', flush=True)

        # add noise
        noise = np.random.normal(0, 1/snr if snr != 0 else 1, len(audio))
        modulated_with_noise = modulated + noise

        # demodulate
        demodulated = fmdemod(modulated_with_noise,
                              sample_rate, delta_f, 100 * 1000)

        # out
        wavfile.write(out_file_name, sample_rate, demodulated)

        print(': done')
