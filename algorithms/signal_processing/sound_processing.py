import os
from enum import StrEnum

import numpy as np
import scipy.io.wavfile as wavfile
from scipy import signal

FILTER_ORDER = 6
SAMPLES_DIR = os.path.join('static', 'sound_samples')


class FilterType(StrEnum):
    LOW_PASS = 'lowpass'
    HIGH_PASS = 'highpass'
    BAND_PASS = 'bandpass'
    BAND_STOP = 'bandstop'


class SoundFrequencyFilter:

    def run_load_sample(self, sample_name: str):
        sample_path = os.path.join(SAMPLES_DIR, f"{sample_name}.wav")
        self.sample_rate, self.waveform = wavfile.read(sample_path)
        self.waveform = self._prepare_waveform_for_processing()

        return self.waveform

    def run_apply_filter(self, sample_name: str, filter_type: FilterType,
                         cutoff_frequency: float, center_frequency: float,
                         bandwidth: float):
        sample_path = os.path.join(SAMPLES_DIR, f"{sample_name}.wav")
        self.sample_rate, self.waveform = wavfile.read(sample_path)
        self.waveform = self._prepare_waveform_for_processing()

        nyquist = self.sample_rate / 2
        filtered_waveform = None

        if filter_type == FilterType.LOW_PASS:
            filtered_waveform = self._apply_lowpass(cutoff_frequency=cutoff_frequency)
        elif filter_type == FilterType.HIGH_PASS:
            filtered_waveform = self._apply_highpass(cutoff_frequency=cutoff_frequency)
        elif filter_type == FilterType.BAND_PASS:
            filtered_waveform = self._apply_bandpass(center_frequency=center_frequency, bandwidth=bandwidth)
        elif filter_type == FilterType.BAND_STOP:
            filtered_waveform = self._apply_bandstop(center_frequency=center_frequency, bandwidth=bandwidth)
        else:
            return None

        filtered_path = os.path.join(SAMPLES_DIR, f"{sample_name}_filtered.wav")

        max_val = np.max(np.abs(filtered_waveform))
        if max_val > 0:
            filtered_waveform = filtered_waveform / max_val * 0.9

        filtered_waveform_int = np.int16(filtered_waveform * 32767)
        wavfile.write(filtered_path, self.sample_rate, filtered_waveform_int)

        original_int = np.int16(self.waveform * 32767)
        original_path = os.path.join(SAMPLES_DIR, f"{sample_name}_original.wav")
        wavfile.write(original_path, self.sample_rate, original_int)

        return filtered_waveform

    def _prepare_waveform_for_processing(self):
        is_stereo_waveform = len(self.waveform.shape) > 1 and self.waveform.shape[1] > 1
        is_not_float_waveform = self.waveform.dtype != np.float32 and self.waveform.dtype != np.float64

        processed_waveform = self.waveform
        if is_stereo_waveform:
            processed_waveform = np.mean(processed_waveform, axis=1)

        if is_not_float_waveform:
            processed_waveform = processed_waveform.astype(np.float32) / (2 ** (8 * processed_waveform.itemsize - 1))

        return processed_waveform

    def _apply_lowpass(self, cutoff_frequency: float):
        nyquist = self.sample_rate / 2
        normalized_cutoff = cutoff_frequency / nyquist
        b, a = signal.butter(FILTER_ORDER, normalized_cutoff, btype='low')
        filtered_waveform = signal.filtfilt(b, a, self.waveform)
        return filtered_waveform

    def _apply_highpass(self, cutoff_frequency: float):
        nyquist = self.sample_rate / 2
        normalized_cutoff = cutoff_frequency / nyquist
        b, a = signal.butter(FILTER_ORDER, normalized_cutoff, btype='high')
        filtered_waveform = signal.filtfilt(b, a, self.waveform)
        return filtered_waveform

    def _apply_bandpass(self, center_frequency: float, bandwidth):
        nyquist = self.sample_rate / 2
        normalized_low_cutoff = max(0.001, (center_frequency - bandwidth / 2) / nyquist)
        normalized_high_cutoff = min(0.999, (center_frequency + bandwidth / 2) / nyquist)
        b, a = signal.butter(FILTER_ORDER, [normalized_low_cutoff, normalized_high_cutoff], btype='band')
        filtered_waveform = signal.filtfilt(b, a, self.waveform)
        return filtered_waveform

    def _apply_bandstop(self, center_frequency: float, bandwidth):
        nyquist = self.sample_rate / 2
        normalized_low_cutoff = max(0.001, (center_frequency - bandwidth / 2) / nyquist)
        normalized_high_cutoff = min(0.999, (center_frequency + bandwidth / 2) / nyquist)
        b, a = signal.butter(FILTER_ORDER, [normalized_low_cutoff, normalized_high_cutoff], btype='bandstop')
        filtered_waveform = signal.filtfilt(b, a, self.waveform)
        return filtered_waveform




if __name__ == '__main__':
    freq_filter = SoundFrequencyFilter()
    freq_filter.run_apply_filter(sample_name='piano', filter_type=FilterType.LOW_PASS, cutoff_frequency=1000,
                                 center_frequency=500, bandwidth=50)
