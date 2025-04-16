import os
from pathlib import Path
import numpy as np
import librosa
import matplotlib.pyplot as plt
import pandas as pd

from enum import StrEnum


class KalmanFilterDataType(StrEnum):
    AUDIO = 'audio'
    STOCK = 'stock'


def kalman_filter(A, H, Q, R, x0, P0, z_seq):
    # Kalman Filter implementation based on the guide: https://bilgin.esme.org/BitsAndBytes/KalmanFilterforDummies

    x_hat_k_prior = x0
    P_k = P0
    x_hat_hist = []

    for k in range(len(z_seq)):
        z_k = np.array([[z_seq[k]]])

        # prediction
        x_hat_k_pred = A @ x_hat_k_prior
        P_k_prior = A @ P_k @ A.T + Q

        # correction
        K_k = P_k_prior @ H.T @ np.linalg.inv(H @ P_k_prior @ H.T + R)
        x_hat_k_prior = x_hat_k_pred + K_k @ (z_k - H @ x_hat_k_pred)
        P_k = (np.eye(len(P_k)) - K_k @ H) @ P_k_prior

        x_hat_hist.append(x_hat_k_prior.copy())

    return x_hat_hist


class SoundKalmanFilter:
    def __init__(self, base_sample_name: str, frame_length: int = 4096):
        current_path = Path(os.getcwd()).parent.parent.parent / 'static' / 'sound_samples'
        base_sample_path = current_path / f'{base_sample_name}.wav'
        self.base_sound, self.base_sr = librosa.load(base_sample_path)

        self.frame_length = frame_length

    def run_kalman_filter(self):
        base_frequency = self._get_base_frequency()

        dt = 1 / (self.base_sr / self.frame_length)
        A = np.array([[1, dt],
                      [0, 1]])
        H = np.array([[1, 0]])
        Q = np.array([[1, 0],
                      [0, 3]])
        R = np.array([[10]])
        x0 = np.array([[base_frequency[0]],
                       [0]])
        P0 = np.eye(2)

        fixed_base_frequency = kalman_filter(A, H, Q, R, x0, P0, base_frequency)
        fixed_base_frequency_np = np.hstack(fixed_base_frequency)
        fixed_base_frequency_first_dimension = fixed_base_frequency_np[0, :]

        return base_frequency, fixed_base_frequency_first_dimension

    def _get_base_frequency(self):
        base_frequency, _, _ = librosa.pyin(y=self.base_sound,
                                            fmin=float(librosa.note_to_hz('C2')),
                                            fmax=float(librosa.note_to_hz('C6')),
                                            frame_length=self.frame_length)
        clean_base_frequency = np.copy(base_frequency)
        nans = np.isnan(clean_base_frequency)
        clean_base_frequency[nans] = np.interp(np.flatnonzero(nans), np.flatnonzero(~nans), clean_base_frequency[~nans])
        return clean_base_frequency


class StockPriceKalmanFilter:
    def __init__(self, frame_length: int = 32):
        current_path = Path(os.getcwd()).parent.parent.parent / 'static' / 'stock_price_samples'
        stock_prices_path = current_path / f'mock_stock_prices.csv'
        self.stock_df = pd.read_csv(stock_prices_path)

        self.frame_length = frame_length

    def run_kalman_filter(self):
        base_frequency = self.stock_df['Low']

        A = np.array([[1, 0],
                      [0, 1]])
        H = np.array([[1, 0]])
        Q = np.array([[1, 0],
                      [0, 3]])
        R = np.array([[10]])
        x0 = np.array([[base_frequency[0]],
                       [0]])
        P0 = np.eye(2)

        fixed_base_frequency = kalman_filter(A, H, Q, R, x0, P0, base_frequency)
        fixed_base_frequency_np = np.hstack(fixed_base_frequency)
        fixed_base_frequency_first_dimension = fixed_base_frequency_np[0, :]

        return base_frequency, fixed_base_frequency_first_dimension


def main():
    obj = SoundKalmanFilter(base_sample_name='piano_scale')
    real, filtered = obj.run_kalman_filter()
    plt.plot(real, label='Original', alpha=0.5)
    plt.plot(filtered, label='Kalman Filtered f0')
    plt.xlabel('Time [s]')
    plt.ylabel('Frequency [Hz]')
    plt.legend()
    plt.title('Kalman Filter on Pitch Estimation')
    plt.grid(True)
    plt.show()

    obj = StockPriceKalmanFilter()
    real, filtered = obj.run_kalman_filter()
    plt.plot(real, label='Original', alpha=0.5)
    plt.plot(filtered, label='Kalman Filtered f0')
    plt.xlabel('Time [s]')
    plt.ylabel('Frequency [Hz]')
    plt.legend()
    plt.title('Kalman Filter on Pitch Estimation')
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
