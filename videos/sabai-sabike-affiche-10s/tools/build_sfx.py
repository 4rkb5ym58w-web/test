"""Synthesise the SFX track (assets/sfx.wav) — event times match index.html."""
import numpy as np, wave

SR = 48000
D = 10.0
out = np.zeros(int(SR * D))
rng = np.random.default_rng(11)

def add(sig, t, g=1.0):
    i = int(t * SR); n = min(len(sig), len(out) - i); out[i:i + n] += sig[:n] * g

def tone(f0, f1, dur, decay):
    t = np.arange(int(SR * dur)) / SR
    f = f1 + (f0 - f1) * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * decay) * (1 - np.exp(-t * 800))

def whoosh(dur=0.45, peak=0.6):
    n = int(SR * dur); x = rng.standard_normal(n); y = np.zeros(n); prev = 0.0
    for i in range(n):
        a = 0.02 + 0.33 * np.sin(np.pi * i / n); prev += a * (x[i] - prev); y[i] = prev
    return y * np.sin(np.pi * np.arange(n) / n) ** 2 / np.max(np.abs(y)) * peak

def boom():
    t = np.arange(int(SR * 1.2)) / SR
    f = 38 + 90 * np.exp(-t * 9)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.5) * (1 - np.exp(-t * 900))

def ding():
    t = np.arange(int(SR * 1.4)) / SR
    s = sum(np.sin(2 * np.pi * f * t) * a for f, a in [(880, 0.4), (1318.5, 0.25), (1760, 0.12)])
    return s * np.exp(-t * 3.2) * (1 - np.exp(-t * 600)) * 0.6

pop = lambda: tone(500, 1100, 0.15, 30) * 0.6

add(whoosh(0.4), 0.0, 0.6)
add(boom(), 0.3, 0.9)
add(whoosh(0.5), 0.9, 0.45)
add(whoosh(0.7), 1.95, 0.7)
for t in [2.75, 4.25, 5.55, 6.8]: add(whoosh(0.4), t, 0.65)
for t in [3.3, 4.75, 6.05]: add(tone(2400, 3200, 0.3, 14) * 0.18, t + 0.2)
for t in [7.3, 7.4, 7.5, 7.6]: add(pop(), t, 0.5)
add(ding(), 7.85, 0.8)
add(pop(), 7.7, 0.7)

out = out / np.max(np.abs(out)) * 0.85
with wave.open("assets/sfx.wav", "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((out * 32767).astype(np.int16).tobytes())
