# Communication Project

## Mahmoud Othman Adas, Sec 2, B. N 21

## Evram Youssef, Sec 1, B. N 9

# How to run:

* make sure you have python3 >3.5 and pip
* install dependencies with:

``` bash
$ python3 -m pip install --user -r requirements.txt
```

* run AM:
```bash
$ python3 am.py
```

* run FM:
```bash
$ python3 fm.py
```

* show plot:
```bash
$ python3 plot-mse.py
```

# Discussion

## Explain your code briefly.

* `fm.py` :
    - read sample.wav
    - calc max freq `B` 
    - calc Kf with `kf = β * B * 2π / mp` 
    - calc ωc
    - modulate with `modulated(t) = Ac * cos(ωc * t + kf * integration(audio(t)))` 
    - for each β (5, .1):
        - for each snr (0, 1, 10, 20):
            - add random noise relative to 1/snr
            - demodulate with fmdemod
            - write to /out

* `am.py` :
    - read sample.wav
    - calc Ac
    - calc ωc
    - modulate with `modulated(t) = (Ac + audio(t)) * cos(ωc + t)` 
    - for each snr (0, 1, 10, 20):
        - add random noise relative to 1/snr
        - demodulate with hilbert
        - write to /out

* `plot-mse.py` 
    - for each file in /out
        - calc MSE with sample.wav
    - plot in plt.png

## Discuss how you selected the sampling rate of the carrier and modulated signal.

TODO

## Discuss how you set the modulation index to 0.9 in AM.

By dividing min peak by the modulation index (.9) we got Ac.

## Discuss how you set the deviation ratio to 5 in FM (WBFM).

By setting β=5 in Carson's law:

`kf = β * B * 2π / mp` 

we get Kf.

## What do you notice on the demodulated audio as SNR increases in both cases?

* AM: Less error.
* FM: No effect.

## What do you notice on the demodulated audio for small values of β, say 0.1 (NBFM).

No difference.

## Plot a graph comparing the mean squared error (MSE), which is the average of the square of the error signal between the original audio and the demodulated audio for different values of SNR for both types of modulation. Comment on your results.

AM is effected with noise more than FM.

![](/plt.png)

