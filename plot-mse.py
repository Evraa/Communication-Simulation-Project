import os

import matplotlib.pyplot as plt
import numpy as np
import librosa


def mse(a, b): return np.square(np.subtract(a, b)).mean()


sample, _ = librosa.load('sample.wav')

am_mse = []
fm_narrow_mse = []
fm_wide_mse = []

for filename in os.listdir('out'):
    is_am = filename.startswith('am')
    is_narrow = filename.count('narrow') > 0
    snr = int(float(filename[:-4].split('_')[-1]))

    audio, _ = librosa.load(f'out/{filename}')
    assert audio.shape == sample.shape

    if is_am:
        am_mse.append((snr, mse(audio, sample)))
    elif is_narrow:
        fm_narrow_mse.append((snr, mse(audio, sample)))
    else:
        fm_wide_mse.append((snr, mse(audio, sample)))

am_mse = sorted(am_mse, key=lambda x: x[0])
fm_narrow_mse = sorted(fm_narrow_mse, key=lambda x: x[0])
fm_wide_mse = sorted(fm_wide_mse, key=lambda x: x[0])

snrs = [x[0] for x in am_mse]
am_mse = [x[1] for x in am_mse]
fm_narrow_mse = [x[1] for x in fm_narrow_mse]
fm_wide_mse = [x[1] for x in fm_wide_mse]

print('snrs: ', snrs)
print('am_mse: ', am_mse)
print('fm_narrow_mse: ', fm_narrow_mse)
print('fm_wide_mse: ', fm_wide_mse)

plt.plot(snrs, am_mse, label='AM')
plt.plot(snrs, fm_narrow_mse)
plt.plot(snrs, fm_wide_mse, label='FM')

plt.legend(loc="upper right")
plt.xlabel('SNR')
plt.ylabel('MSE')

plt.savefig('plt.png')
plt.show()
