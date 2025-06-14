import os
from enum import StrEnum
from pathlib import Path

import numpy as np
import pywt
from PIL import Image


class ImageCompressorMethod(StrEnum):
    FFT = "fft"
    WAVELET = "wavelet"


class ImageCompressor:
    def __init__(self, image: Image):
        self.image = image
        # PIL Image uses (width, height), but numpy uses (height, width)
        if isinstance(image, Image.Image):
            self.cols, self.rows = image.size  # Note: PIL uses (width, height)
        else:
            self.rows, self.cols = image.shape[:2]

    def run_fft_compression(self, compression_factor: float) -> np.ndarray:
        assert 0 < compression_factor < 1, "compression factor should be greater than 0 or lower than 1"

        # Convert to grayscale numpy array if needed
        if isinstance(self.image, Image.Image):
            img_array = np.array(self.image.convert('L')).astype(np.float64)
        else:
            img_array = self.image.astype(np.float64)

        # Get actual dimensions from the array
        rows, cols = img_array.shape

        f_transform = np.fft.fft2(img_array)
        f_transform_shifted = np.fft.fftshift(f_transform)

        row_center, col_center = rows // 2, cols // 2

        # Keep center frequencies (low frequencies) based on compression_factor
        row_keep = int(rows * compression_factor / 2)
        col_keep = int(cols * compression_factor / 2)

        # Create a mask to zero out high frequencies (outer regions)
        mask = np.zeros_like(f_transform_shifted, dtype=np.float64)
        mask[row_center - row_keep:row_center + row_keep,
        col_center - col_keep:col_center + col_keep] = 1

        # Apply mask to keep only low frequencies
        f_transform_shifted = f_transform_shifted * mask

        f_transform_inverse = np.fft.ifftshift(f_transform_shifted)
        img_back = np.fft.ifft2(f_transform_inverse)

        # Take the real part and ensure it's in the correct range
        img_back = np.real(img_back)
        img_back = np.clip(img_back, 0, 255)

        return img_back

    def run_wavelet_compression(self, compression_factor: float) -> np.ndarray:
        assert 0 < compression_factor < 1, "compression factor should be greater than 0 or lower than 1"

        # Convert to grayscale numpy array if needed
        if isinstance(self.image, Image.Image):
            img_array = np.array(self.image.convert('L')).astype(np.float64)
        else:
            img_array = self.image.astype(np.float64)

        coeffs = pywt.dwt2(img_array, 'db1')

        approx, details = coeffs
        horizontal, vertical, diagonal = details

        compressed_horizontal = self._apply_compression(coeffs=horizontal,
                                                        compression_factor=compression_factor)
        compressed_vertical = self._apply_compression(coeffs=vertical,
                                                      compression_factor=compression_factor)
        compressed_diagonal = self._apply_compression(coeffs=diagonal,
                                                      compression_factor=compression_factor)

        compressed_details = (compressed_horizontal, compressed_vertical, compressed_diagonal)
        compressed_coeffs = (approx, compressed_details)
        img_back = pywt.idwt2(compressed_coeffs, 'db1')

        img_back = img_back[:img_array.shape[0], :img_array.shape[1]]
        img_back = np.clip(img_back, 0, 255)

        return img_back

    @staticmethod
    def _apply_compression(coeffs: np.ndarray, compression_factor: float) -> np.ndarray:
        # Keep compression_factor proportion of coefficients
        threshold = np.percentile(np.abs(coeffs), 100 * (1 - compression_factor))
        coeffs[np.abs(coeffs) < threshold] = 0
        return coeffs