'''
    AM modulation with DSB-LC
    author: Evram
'''

import math
import os
import warnings

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
from scipy.signal import hilbert

import librosa

# read audio file
audio, sfr = librosa.load('sample.wav')

# time samples
time = np.arange(0, len(audio)) / sfr

# divide min peak by the modulation index
ac = abs(np.min(audio)) / .9

# shift m(t) by ac
audio += ac

# carrier frequency
fc = 100000
wc = (2*np.pi)*fc
# 200 samples from -100 to 100

coft = np.cos(math.radians(wc)*time)

# multiply element wise
modulated = audio * coft

for snr in [0, 1, 10, 20]:
    out_file_name = f'out/am_snr_{snr}.wav'
    print(out_file_name)

    # add noise
    noise = np.random.normal(0, 1/snr if snr != 0 else .1, len(audio))
    modulated += noise

    # demodulate
    analytic_signal = hilbert(modulated)
    amplitude_envelope = np.abs(analytic_signal)

    scaled = np.int16(amplitude_envelope /
                      np.max(np.abs(amplitude_envelope)) * 32767)

    # out
    wavfile.write(out_file_name, sfr, scaled)
