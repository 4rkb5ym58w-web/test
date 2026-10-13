"""Synthesise the ad's SFX track (assets/sfx.wav) — event times match index.html."""
import numpy as np, wave

SR = 48000
D = 24.5
out = np.zeros(int(SR * D))
rng = np.random.default_rng(7)

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

def ride(dur):
    t = np.arange(int(SR * dur)) / SR
    f = 70 + 50 * (t / dur) + 6 * np.sin(2 * np.pi * 7 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR
    saw = 2 * ((ph / (2 * np.pi)) % 1) - 1
    y = np.zeros_like(saw); prev = 0.0
    for i in range(len(saw)):
        prev += 0.08 * (saw[i] - prev); y[i] = prev
    env = np.minimum(1, t / 0.25) * np.minimum(1, (dur - t) / 0.3)
    return y / np.max(np.abs(y)) * env * 0.35

def ding():
    t = np.arange(int(SR * 1.4)) / SR
    s = sum(np.sin(2 * np.pi * f * t) * a for f, a in [(880, 0.4), (1318.5, 0.25), (1760, 0.12)])
    return s * np.exp(-t * 3.2) * (1 - np.exp(-t * 600)) * 0.6

sent = lambda: tone(1400, 900, 0.18, 26) * 0.5
recv = lambda: tone(700, 1050, 0.2, 22) * 0.5 + tone(1050, 1400, 0.2, 30) * 0.2
tick = lambda: tone(2600, 2400, 0.06, 80) * 0.25

for t in [0.9, 1.6, 5.4]: add(sent(), t)
add(recv(), 2.15, 0.5)
for t in [3.0, 3.8, 4.6]: add(recv(), t)
add(tick(), 5.85)
for t, g in [(6.1, 0.7), (6.7, 0.5), (8.6, 0.6), (10.6, 0.6), (12.75, 0.6), (14.4, 0.5), (18.9, 0.6), (20.5, 0.6)]:
    add(whoosh(), t, g)
add(recv(), 15.75); add(recv(), 15.95, 0.8)
add(ride(1.75), 16.15)
add(recv(), 17.85); add(ding(), 18.05, 0.7)
add(recv(), 19.25, 0.9)
for t in [19.95, 20.11, 20.27]: add(tick(), t, 1.6)
add(ding(), 20.6)

out = out / np.max(np.abs(out)) * 0.85
with wave.open("assets/sfx.wav", "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((out * 32767).astype(np.int16).tobytes())
