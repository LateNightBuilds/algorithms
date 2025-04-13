from enum import StrEnum
from typing import Tuple, List

import numpy as np
from scipy.fft import fft, fftfreq


class SignalType(StrEnum):
    SINE = 'sine'
    SQUARE = 'square'
    SAWTOOTH = 'sawtooth'
    TRIANGLE = 'triangle'


def run_generate_signal(signal_type: SignalType,
                        frequency: float,
                        amplitude: float,
                        duration: float,
                        sampling_rate: float,
                        noise_level: float = 0) -> Tuple[List[float], List[float]]:
    t = np.linspace(0, duration, int(duration * sampling_rate), endpoint=False)

    if signal_type == SignalType.SINE:
        y = amplitude * np.sin(2 * np.pi * frequency * t)
    elif signal_type == SignalType.SQUARE:
        y = amplitude * np.sign(np.sin(2 * np.pi * frequency * t))
    elif signal_type == SignalType.SAWTOOTH:
        y = amplitude * 2 * (t * frequency - np.floor(0.5 + t * frequency))
    elif signal_type == SignalType.TRIANGLE:
        y = amplitude * 2 * np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5))) - 1
    else:
        y = amplitude * np.sin(2 * np.pi * frequency * t)

    if noise_level > 0:
        noise = np.random.normal(0, noise_level * amplitude, y.shape)
        y = y + noise

    return t.tolist(), y.tolist()


def run_fast_fourier_transform(signal: List[float],
                               sampling_rate: float) -> Tuple[List[float], List[float], List[float]]:
    yf = fft(signal)
    N = len(signal)
    xf = fftfreq(N, 1 / sampling_rate)

    positive_freq_idx = np.where(xf >= 0)
    xf = xf[positive_freq_idx]
    yf_abs = np.abs(yf[positive_freq_idx]) / N

    yf_phase = np.angle(yf[positive_freq_idx])

    return xf.tolist(), yf_abs.tolist(), yf_phase.tolist()
