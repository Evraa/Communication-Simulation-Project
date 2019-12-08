import math
import os
from glob import glob

import matplotlib.pyplot as plt
import numpy as np
from scipy.io.wavfile import write
from scipy.signal import hilbert

import librosa as lb
import wavio


def dsb_lc():
    '''To store the final audio file'''

    # Reading the audio file
    audio_file = glob("sample.wav")
    audio, sfr = lb.load(audio_file[0])

    fm = sfr

    # Getting the time samples of the audio file
    time = np.arange(0, len(audio)) / sfr

    # vec_x = []
    # vec_y = []
    # for i in range (len(time)):
    #     vec_x.append(time[i])
    #     vec_y.append(audio[i])

    # plt.step(vec_x, vec_y)
    # plt.show()

    # Getting the minimum peek of the audio file
    min_peek = abs(np.min(audio))
    # Dividing it by the modulation index
    Ac = (1/0.9) * min_peek
    # Shiftting the m(t) by Ac
    audio += Ac

    # The Carrier frequency
    fc = 100000
    Wc = (2*np.pi)*fc
    # 200 samples from -100 to 100

    CofT = np.cos(math.radians(Wc)*time)

    # vec_x = []
    # vec_y = []
    # for i in range (len(time)):
    #     vec_x.append(time[i])
    #     vec_y.append(CofT[i])

    # plt.step(vec_x, vec_y)
    # plt.show()
    # print (CofT)

    # Multiply element wise
    modulated = audio * CofT

    # Add some noise
    # As SNR gets larger, the noise effect gets lower
    SNR = 1
    noise = np.random.normal(0, 1/SNR, len(audio_file))
    #print (modulated)
    modulated += noise
    #print (modulated)

    # Finally demodulate the signal
    analytic_signal = hilbert(modulated)
    amplitude_envelope = np.abs(analytic_signal)

    scaled = np.int16(amplitude_envelope /
                      np.max(np.abs(amplitude_envelope)) * 32767)
    write('snr 1.wav', fm, scaled)

    print("Finished")


dsb_lc()
