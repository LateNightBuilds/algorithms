from dataclasses import dataclass
from typing import List, Tuple, Dict

import numpy as np
from scipy.optimize import least_squares
from scipy.signal import correlate, chirp

SPEED_OF_SOUND = 343  # meters per second


@dataclass
class Position:
    x: float
    y: float

    def euclidean_distance(self, other_position: 'Position') -> float:
        return np.sqrt((self.x - other_position.x) ** 2 + (self.y - other_position.y) ** 2)


@dataclass
class Mic:
    id: int
    signal: np.array
    position: Position


class SoundRadar:
    def __init__(self,
                 noise_signal: np.array,
                 noise_resolution: float,
                 microphone_positions: List[Position]):
        self.noise_signal = noise_signal
        self.noise_resolution = noise_resolution
        self.microphone_positions = microphone_positions

    def run_sound_radar(self, noise_position: Position) -> Position:
        mics: List[Mic] = self._get_radar_mics(noise_position=noise_position)
        reference_mic = mics[0]
        time_delay_by_mic_pair_ids = self._get_time_delay_by_mic_pair_ids(reference_mic=reference_mic, mics=mics)
        source_position = self._compute_source_position(reference_mic=reference_mic, mics=mics,
                                                        time_delay_by_mic_pair_ids=time_delay_by_mic_pair_ids)
        return source_position

    def _get_radar_mics(self, noise_position: Position) -> List[Mic]:
        mics = []
        for i, mic_pos in enumerate(self.microphone_positions):
            noise_mic_distance = mic_pos.euclidean_distance(noise_position)
            time_delay = noise_mic_distance / SPEED_OF_SOUND
            sample_delay = int(round(time_delay * self.noise_resolution))
            delayed_signal = np.zeros(len(self.noise_signal) + sample_delay)
            delayed_signal[sample_delay:sample_delay + len(self.noise_signal)] = self.noise_signal
            mics.append(Mic(id=i, signal=delayed_signal, position=mic_pos))
        return mics

    def _get_time_delay_by_mic_pair_ids(self, reference_mic: Mic, mics: List[Mic]):
        time_delay_by_mic_pair_ids: Dict[Tuple[int, int], float] = {}
        for mic in mics[1:]:
            cross_correlation = correlate(mic.signal, reference_mic.signal, mode='full')
            lag = np.argmax(np.abs(cross_correlation)) - (len(reference_mic.signal) - 1)
            time_delay = lag / self.noise_resolution
            time_delay_by_mic_pair_ids[(reference_mic.id, mic.id)] = time_delay
        return time_delay_by_mic_pair_ids

    def _compute_source_position(self, reference_mic: Mic, mics: List[Mic],
                                 time_delay_by_mic_pair_ids: Dict[Tuple[int, int], float]) -> Position:
        x_init = sum(mic.position.x for mic in mics) / len(mics)
        y_init = sum(mic.position.y for mic in mics) / len(mics)
        deltas = list(time_delay_by_mic_pair_ids.values())
        result = least_squares(self.cost_function, (x_init, y_init), args=(mics, reference_mic, deltas))
        return Position(*result.x)

    @staticmethod
    def cost_function(x0: Tuple[float, float], mics: List[Mic], reference_mic: Mic, deltas: List[float]) -> List[float]:
        pos = Position(*x0)
        equations = []
        for i, mic in enumerate(mics):
            if i == 0:
                continue
            expected_delta = deltas[i - 1] * SPEED_OF_SOUND
            distance_difference = pos.euclidean_distance(mic.position) - pos.euclidean_distance(reference_mic.position)
            equations.append(distance_difference - expected_delta)
        return equations


def main():
    noise_resolution = 44100
    duration = 0.03  # 30 ms chirp
    t = np.linspace(0, duration, int(noise_resolution * duration), endpoint=False)
    noise_signal = chirp(t, f0=500, f1=5000, t1=duration, method='linear')

    microphone_positions = [
        Position(x=0.0, y=0.0),
        Position(x=1.0, y=0.0),
        Position(x=0.0, y=1.0),
        Position(x=1.0, y=1.0),
    ]

    noise_position = Position(x=0.6, y=0.7)

    radar = SoundRadar(
        noise_signal=noise_signal,
        noise_resolution=noise_resolution,
        microphone_positions=microphone_positions
    )

    estimated = radar.run_sound_radar(noise_position=noise_position)

    print(f"Estimated:{estimated}")
    print(f"Actual:{noise_position}")


if __name__ == '__main__':
    main()
