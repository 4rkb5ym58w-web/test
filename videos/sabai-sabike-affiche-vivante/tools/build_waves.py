"""Synthesise a soft ocean-wave ambience (assets/vagues.wav), stereo, 10s."""
import numpy as np, wave
from numpy.fft import rfft, irfft, rfftfreq

SR, D = 48000, 10.0
n = int(SR * D)
rng = np.random.default_rng(3)
t = np.arange(n) / SR

def coloured(seed_shift):
    x = rng.standard_normal(n)
    X = rfft(x); f = rfftfreq(n, 1 / SR)
    X *= 1 / np.maximum(f, 20) ** 0.9          # pinkish-brown
    X *= np.exp(-(f / 2500) ** 2)               # soft lowpass
    y = irfft(X, n); return y / np.max(np.abs(y))

# wave swells: rise, crash, wash out
def swell(phase):
    env = np.zeros(n)
    for c in np.arange(phase, D + 4, 4.6):
        s = t - c
        env += np.where(s < 0, np.exp(-(s / 1.3) ** 2), np.exp(-s / 1.6))
    return 0.25 + env

L = coloured(0) * swell(0.8)
R = coloured(1) * swell(1.1)
fade = np.minimum(1, t / 0.6) * np.minimum(1, (D - t) / 0.8)
st = np.stack([L, R], 1) * fade[:, None]
st = st / np.max(np.abs(st)) * 0.7
with wave.open("assets/vagues.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype(np.int16).tobytes())
