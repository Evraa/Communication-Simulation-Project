'''
    FM modulation
    author: Mahmoud
'''

import math
import os
import warnings

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
from scipy.signal import hilbert
import numpy.fft as fft

import librosa


def calc_kf(beta, m):
    '''carson rule:
    kf = β * B * 2π / mp
    '''
    # get B
    spectrum = fft.fft(m)
    freq = fft.fftfreq(len(spectrum))
    threshold = 0.5 * max(abs(spectrum))
    mask = abs(spectrum) > threshold
    peaks = freq[mask]
    max_freq = peaks.max()  # B

    mp = abs(m.max())

    return beta * max_freq * 2 * np.pi / mp


def modulate_fm(audio, sample_rate, beta):
    '''modulated(t) = Ac * cos(wc * t + kf * integration(audio(t)))'''
    # time samples
    time = np.arange(0, audio.size) / sample_rate

    # TODO: how to get Ac?
    ac = 1

    fc = 100 * 1000  # 100 kHz
    wc = 2 * np.pi * fc

    kf = calc_kf(beta, audio)

    return ac * np.cos(wc * time + kf * np.cumsum(audio))


print('read audio file')
audio, sample_rate = librosa.load('sample.wav')


for beta, name in [(5, 'wide'), (.1, 'narrow')]:
    print(f'modeulate {name} band with β = {beta}')
    modulated = modulate_fm(audio, sample_rate, beta)

    for snr in [0, 1, 10, 20]:
        out_file_name = f'out/am_{name}_snr_{snr}.wav'
        print(out_file_name, end='', flush=True)

        # add noise
        noise = np.random.normal(0, 1/snr if snr != 0 else .1, len(audio))
        modulated_with_noise = modulated + noise

        # demodulate TODO
        demodulated = audio

        # out
        wavfile.write(out_file_name, sample_rate, demodulated)

        print(': done')
