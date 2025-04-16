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
        self.rows, self.cols = image.height, image.width

    def run_fft_compression(self, compression_factor: float) -> np.ndarray:
        assert 0 < compression_factor < 1, "compression factor should be greater than 0 or lower than 1"

        f_transform = np.fft.fft2(self.image)
        f_transform_shifted = np.fft.fftshift(f_transform)

        row_center, column_center = self.rows // 2, self.cols // 2

        row_discard = int(self.rows * compression_factor / 2)
        col_discard = int(self.cols * compression_factor / 2)
        from_row, to_row = row_center - row_discard, row_center + row_discard
        from_col, to_col = column_center - col_discard, column_center + col_discard

        f_transform_shifted[from_row:to_row, from_col:to_col] = 0
        f_transform_inverse = np.fft.ifftshift(f_transform_shifted)

        img_back = np.fft.ifft2(f_transform_inverse)
        return np.abs(img_back)

    def run_wavelet_compression(self, compression_factor: float) -> np.ndarray:
        assert 0 < compression_factor < 1, "compression factor should be greater than 0 or lower than 1"

        coeffs = pywt.dwt2(self.image, 'db1')
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
        return np.abs(img_back)

    @staticmethod
    def _apply_compression(coeffs: np.ndarray, compression_factor: float) -> np.ndarray:
        threshold = np.percentile(np.abs(coeffs), 100 * (1 - compression_factor))
        coeffs_compressed = np.where(np.abs(coeffs) < threshold, 0, coeffs)
        return coeffs_compressed


def main():
    current_path = Path(os.getcwd())
    image_path = current_path / 'lena.jpg'
    image = np.array(Image.open(image_path).convert("L"))

    compressor = ImageCompressor(image)

    print("Choose compression method:",
          "1. FFT Compression",
          "2. Wavelet Compression")

    method = input("Enter your choice (1/2): ")

    compression_factor = float(input("Enter compression factor (0 < factor < 1): "))

    if method == '1':
        compression_method = ImageCompressorMethod.FFT
        compressed_image = compressor.run_fft_compression(compression_factor)
    elif method == '2':
        compression_method = ImageCompressorMethod.WAVELET
        compressed_image = compressor.run_wavelet_compression(compression_factor)
    else:
        return

    output_path = current_path / f'lena_compressed_{compression_method.name}.jpg'
    Image.fromarray(compressed_image.astype(np.uint8)).save(output_path)
    print(f"Compressed image saved to {output_path}")


if __name__ == '__main__':
    main()
