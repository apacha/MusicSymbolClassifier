import os
import shutil
import unittest
from glob import glob

from datasets.AudiverisOmrDatasetDownloader import AudiverisOmrDatasetDownloader
from datasets.AudiverisOmrImageGenerator import AudiverisOmrImageGenerator


class AudiverisOmrImageGeneratorTest(unittest.TestCase):

    def test_download_extract_and_crop_bitmaps(self):
        # Arrange
        dataset_downloader = AudiverisOmrDatasetDownloader("temp/audiveris_raw")

        # Act
        dataset_downloader.download_and_extract_dataset()
        image_generator = AudiverisOmrImageGenerator()
        image_generator.extract_symbols("temp/audiveris_raw", "temp/audiveris_img")
        all_image_files = [y for x in os.walk("temp/audiveris_img") for y in glob(os.path.join(x[0], '*.png'))]
        actual_number_of_files = len(all_image_files)

        # Assert
        self.assertEqual(405, actual_number_of_files)

        # Cleanup
        os.remove("AudiverisOmrDataset.zip")
        shutil.rmtree("temp")


if __name__ == '__main__':
    unittest.main()
